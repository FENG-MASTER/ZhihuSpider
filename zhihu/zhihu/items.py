# -*- coding: utf-8 -*-

# ------------------------------------------
#   版本：1.0
#   日期：2017-8-06
#   作者：AlexTan
#   <CSDN:   http://blog.csdn.net/alextan_>  
#   <e-mail: alextanbz@gmail.com>
# ------------------------------------------

import scrapy


class ZhihuItem(scrapy.Item):
    user_id = scrapy.Field()
    user_image_url = scrapy.Field()
    name = scrapy.Field()
    locations = scrapy.Field()
    business = scrapy.Field()  # 所在行业
    employments = scrapy.Field()  # 职业经历
    gender = scrapy.Field()
    education = scrapy.Field()
    followees_num = scrapy.Field()  # 我关注的人数
    followers_num = scrapy.Field()  # 关注我的人数


class RelationItem(scrapy.Item):
    user_id = scrapy.Field()
    relation_type = scrapy.Field()  # 关系类型
    relations_id = scrapy.Field()


# 答案模型
class AnswerItem(scrapy.Item):
    # 回答用户ID
    answer_user_id = scrapy.Field()
    # 答案ID
    answer_id = scrapy.Field()
    # 问题ID
    question_id = scrapy.Field()
    # 答案创建时间
    cretated_time = scrapy.Field()
    # 答案更新时间
    updated_time = scrapy.Field()
    # 答案点赞数
    voteup_count = scrapy.Field()
    # 评论数
    comment_count = scrapy.Field()
    # 回答内容
    content = scrapy.Field()


# 问题模型
class QuestionItem(scrapy.Item):
    # 提问题用户ID
    ask_user_id = scrapy.Field()
    # 问题ID
    question_id = scrapy.Field()
    # 提问时间
    ask_time = scrapy.Field()
    # 答案数目
    answer_count = scrapy.Field()
    # 关注者数量
    followees_count = scrapy.Field()
    # 问题标题
    title = scrapy.Field()
    # 问题详细说明
    content = scrapy.Field()
    # 问题被浏览次数
    view_count = scrapy.Field()
    # 问题所属话题ID列表
    topics = scrapy.Field()


class ArticleItem(scrapy.Item):
    author_id = scrapy.Field()
    title = scrapy.Field()
    article_id = scrapy.Field()
    content = scrapy.Field()
    cretated_time = scrapy.Field()
    updated_time = scrapy.Field()
    voteup_count = scrapy.Field()
    comment_count = scrapy.Field()


# 问题模型
class QAQuestionItem(scrapy.Item):
    # 提问题用户ID
    ask_user_id = scrapy.Field()
    # 问题ID
    question_id = scrapy.Field()
    # 提问时间
    create_time = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()
    # 答案数目
    answer_count = scrapy.Field()
    # 关注者数量
    followees_count = scrapy.Field()
    # 问题标题
    title = scrapy.Field()
    # 问题详细说明
    content = scrapy.Field()
    # 问题被浏览次数
    view_count = scrapy.Field()
    # 问题所属话题ID列表
    topics = scrapy.Field()
    # 问题评论数目
    comment_count = scrapy.Field()


# 答案模型
class QAAnswerItem(scrapy.Item):
    # 回答用户ID
    answer_user_id = scrapy.Field()
    # 答案ID
    answer_id = scrapy.Field()
    # 问题ID
    question_id = scrapy.Field()
    # 答案创建时间
    create_time = scrapy.Field()
    # 答案更新时间
    update_time = scrapy.Field()
    # 答案点赞数
    voteup_count = scrapy.Field()
    # 评论数
    comment_count = scrapy.Field()
    # 回答内容
    content = scrapy.Field()
    # 简介
    excerpt=scrapy.Field()


# 话题模型
class QATopicItem(scrapy.Item):
    # 话题名称
    name = scrapy.Field()
    # 话题描述
    desc = scrapy.Field()
    # 话题ID
    id = scrapy.Field()
    # 子话题ID列表
    children = scrapy.Field()
    # 父话题ID
    father = scrapy.Field()
