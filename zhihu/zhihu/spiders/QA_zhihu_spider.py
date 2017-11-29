# -*- coding: utf-8 -*-
import scrapy
import re
import pdb
import json
from scrapy.http import Request
from ..items import ZhihuItem, RelationItem, AnswerItem, QuestionItem, ArticleItem
from ..scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from ..items import ZhihuItem, RelationItem, AnswerItem, QuestionItem, ArticleItem, QATopicItem
from ..scrapy_redis.spiders import RedisSpider


class QAZhihuSpider(RedisSpider):
    name = 'zhihuqaspider'
    redis_key = "zhihuqaspider:start_urls"
    allowed_domains = ['zhihu.com']
    start_topics_id = ['19776749']
    start_urls = ['http://zhihu.com/']

    def parse(self, response):
        body = str(response.body, encoding="utf8")

    def start_requests(self):
        for topic in self.start_topics_id:
            yield Request(
                'https://www.zhihu.com/topic/' + topic + '/organize/entire', callback=self.parse_topic,dont_filter=True)

    def parse_topic(self, response):
        """
        解析主题页面
        :param response:解析页面
        :return:
        """
        # 当前话题ID
        now_topic_id = re.match(r"(?:https://www.zhihu.com/topic/)(\d+)(?:/organize/entire)", response.url).group(1)
        now_topic_name = response.xpath("//h1[@class='zm-editable-content']/text()")[0].extract().strip()
        now_topic_desc = response.xpath("//div[@id='zh-topic-desc']/div[@class='zm-editable-content']")[
            0].extract().strip()

        item = QATopicItem()

        item['id'] = now_topic_id
        item['name'] = now_topic_name
        item['desc'] = now_topic_desc

        # 保存当前话题
        yield item

        children = response.xpath("//a[@class='zm-item-tag']/@data-token")
        for c in children:
            tid = c.extract().strip()
            yield Request('https://www.zhihu.com/topic/' + tid + '/organize/entire', callback=self.parse_topic)

        # 深度优先,先遍历所有话题,从最底层的子话题开始搜索问题



        print("??")
        pass
