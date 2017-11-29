# -*- coding: utf-8 -*-
import scrapy
import re

import json
from scrapy.http import Request
from ..items import ZhihuItem, RelationItem, AnswerItem, QuestionItem, ArticleItem
from ..scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from ..items import ZhihuItem, RelationItem, AnswerItem, QuestionItem, ArticleItem, QATopicItem
from ..scrapy_redis.spiders import RedisSpider


class QAZhihuSpider(RedisSpider):
    name = 'zhihuspider'
    redis_key = "zhihuspider:start_urls"
    allowed_domains = ['zhihu.com']
    start_topics_id = ['19583842']
    start_urls = ['http://zhihu.com/']

    # handle_httpstatus_list=[200,302]

    def parse(self, response):
        body = str(response.body, encoding="utf8")

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
            yield Request(response.url + next_url, callback=self.parse_topic_top_questions)

    def parse_question(self, response):
        """
        解析问题页面
        :param response:
        :return:
        """
        question_title=response.xpath(r"//h1[@class='QuestionHeader-title']/text()")[0].extract().strip()
        # 这个大坑啊我靠,我眼花了都
        question_content=re.search(r"(?:editableDetail)(.*)(?:visitCount)",response.xpath(r"//div[@id='data']/@data-state")[0].extract()).group(0)


        pass
