# -*- coding: utf-8 -*-
import scrapy
import re

import json
from scrapy.http import Request

from ..scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from ..items import QATopicItem, QAQuestionItem, QAAnswerItem
from ..scrapy_redis.spiders import RedisSpider


class QAZhihuSpider(RedisSpider):
    name = 'zhihuspider'
    redis_key = "zhihuspider:start_urls"
    allowed_domains = ['zhihu.com']
    start_topics_id = ['19776749']
    start_urls = ['http://zhihu.com/']

    # handle_httpstatus_list=[200,302]

    # 更多答案url
    more_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data[*]" \
                      ".is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action," \
                      "annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count," \
                      "can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission" \
                      ",created_time,updated_time,review_info,question,excerpt,relationship.is_authorized," \
                      "is_author,voting,is_thanked,is_nothelp,upvoted_followees;" \
                      "data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics&" \
                      "limit={1}&offset={2}"

    def start_requests(self):
        for topic in self.start_topics_id:
            yield Request(
                'https://www.zhihu.com/topic/' + topic + '/organize/entire', callback=self.parse_topic,
                dont_filter=True)

    def parse_topic(self, response):
        """
        解析主题页面
        :param response:解析页面
        :return:
        """
        # 当前话题ID
        now_topic_id = re.match(r"(?:https://www.zhihu.com/topic/)(\d+)(?:/organize/entire)", response.url).group(1)
        # 当前话题名称
        now_topic_name = response.xpath("//h1[@class='zm-editable-content']/text()")[0].extract().strip()
        # 当前话题描述
        now_topic_desc = response.xpath("//div[@id='zh-topic-desc']/div[@class='zm-editable-content']")[
            0].extract().strip()
        # 当前话题的所有子话题
        now_topic_children = []
        # 当前话题的所有父话题
        now_topic_father = []

        father = response.xpath(
            r"//div[@class='zm-side-section-inner parent-topic']/descendant::a[@class='zm-item-tag']/@data-token")

        if len(father) != 0:
            #     有父话题
            for f in father:
                tid = f.extract().strip()
                now_topic_father.append(tid)
        else:
            now_topic_father = 0

        children_list = response.xpath(
            r"//div[@class='zm-side-section-inner child-topic']/descendant::a[@class='zm-item-tag']/@data-token")

        if len(children_list) != 0:
            #     有子话题
            for c in children_list:
                tid = c.extract().strip()
                now_topic_children.append(tid)

        item = QATopicItem()

        item['id'] = now_topic_id
        item['name'] = now_topic_name
        item['desc'] = now_topic_desc
        item['children'] = now_topic_children
        item['father'] = now_topic_father

        # 保存当前话题
        yield item

        if len(children_list) != 0:
            # 有子话题
            for c in children_list:
                tid = c.extract().strip()
                yield Request('https://www.zhihu.com/topic/' + tid + '/organize/entire', callback=self.parse_topic)

        # 深度优先,先遍历所有话题,从最底层的子话题开始搜索问题

        if len(children_list) != 0:
            for c in children_list:
                tid = c.extract().strip()
                yield Request('https://www.zhihu.com/topic/' + tid + '/top-answers',
                              callback=self.parse_topic_top_questions)
                yield Request('https://www.zhihu.com/topic/' + tid + '/unanswered',
                              callback=self.parse_topic_top_questions)
        # 还要搜索本身话题的问题(当然,可能重复)
        yield Request('https://www.zhihu.com/topic/' + now_topic_id + '/top-answers',
                      callback=self.parse_topic_top_questions)
        yield Request('https://www.zhihu.com/topic/' + now_topic_id + '/unanswered',
                      callback=self.parse_topic_top_questions)

    def parse_topic_top_questions(self, response):
        """
        解析话题精华问题
        :param response:
        :return:
        """
        questions_url = response.xpath(r"//h2/a[@class='question_link']/@href")

        # 处理当前页的所有问题
        for url in questions_url:
            yield Request('https://www.zhihu.com' + url.extract().strip(), callback=self.parse_question)

        # 下一页
        next = response.xpath(r"//div[@class='zm-invite-pager']/span[last()]/a/@href")
        if len(next) != 0:
            next_url = next[0].extract().strip()
            yield Request(response.url.split('?')[0] + next_url, callback=self.parse_topic_top_questions)

    def parse_topic_unanswers(self, response):
        """
        解析未完成话题
        :param response:
        :return:
        """
        self.parse_topic_top_questions(response)

    def parse_question(self, response):
        """
        解析问题页面
        :param response:
        :return:
        """
        # 问题标题
        question_title = response.xpath(r"//h1[@class='QuestionHeader-title']/text()")[0].extract().strip()
        # 问题详细内容,这个大坑啊我靠,我眼花了都
        question_content = re.search(r"(?:editableDetail\":)(.*)(?:\"visitCount)",
                                     response.xpath(r"//div[@id='data']/@data-state")[0].extract()).group(1)
        # id 直接从URL拿就好了
        question_id = response.url.split('/')[-1]
        # 问题创建时间
        question_create_time = \
            response.xpath(r"//div[@class='QuestionPage']/meta[@itemprop='dateCreated']/@content").extract()[0]
        # 问题更新时间
        question_update_time = \
            response.xpath(r"//div[@class='QuestionPage']/meta[@itemprop='dateModified']/@content").extract()[0]
        # 问题被浏览次数
        question_view_count = response.xpath(
            r"//div[@class='NumberBoard QuestionFollowStatus-counts']/div[@class='NumberBoard-item']/div[@class='NumberBoard-value']/text()").extract()[
            0]
        # 问题关注者数量
        question_follower_count = \
            response.xpath(r"//div[@class='QuestionPage']/meta[@itemprop='zhihu:followerCount']/@content").extract()[0]
        # 问题回答数目
        question_answer_count = int(
            response.xpath(r"//div[@class='QuestionPage']/meta[@itemprop='answerCount']/@content").extract()[0])
        # 问题评论数目
        question_comment_count = \
            response.xpath(r"//div[@class='QuestionPage']/meta[@itemprop='commentCount']/@content").extract()[0]

        # 问题所属话题ID列表
        topic_list = response.xpath(r"//a[@class='TopicLink']")

        question_topics = []
        for node in topic_list:
            tid = node.xpath(r"./@href").extract()[0].split('/')[-1]
            question_topics.append(tid)

        item = QAQuestionItem()

        item['question_id'] = question_id
        item['create_time'] = question_create_time
        item['update_time'] = question_update_time
        item['answer_count'] = question_answer_count
        item['followees_count'] = question_follower_count
        item['title'] = question_title
        item['content'] = question_content
        item['view_count'] = question_view_count
        item['topics'] = question_topics
        item['comment_count'] = question_comment_count

        yield item

        # 处理问题下的答案
        n = 0
        while n + 10 <= question_answer_count:
            yield Request(self.more_answer_url.format(question_id, n + 10, n),
                          callback=self.parse_answer)
            n += 10

    def parse_answer(self, response):
        """
        解析答案 json格式
        :param response:
        :return:
        """
        answers = json.loads(response.text)

        for ans in answers['data']:
            item = QAAnswerItem()
            item['answer_user_id'] = ans['author']['name']
            item['question_id'] = ans['question']['id']
            item['answer_id'] = ans['id']
            item['create_time'] = ans['created_time']
            item['update_time'] = ans['updated_time']
            item['voteup_count'] = ans['voteup_count']
            item['comment_count'] = ans['comment_count']
            item['excerpt'] = ans['excerpt']
            item['content'] = ans['content']
            yield item
