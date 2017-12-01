# 知乎爬虫  

*原作者*: AlexTan  

*原作者原文博客：[ZhihuSpider](http://blog.csdn.net/AlexTan_/article/details/77057068)*

*原github地址 : https://github.com/AlexTan-b-z/ZhihuSpider*


## 功能

主要是原作者实现的功能和我需要的有一点不相符,所以修改了一下.


## 爬取内容

从知乎的[根话题]开始,深度遍历的方式,从最底层的话题的精华问题和未回答问题开始爬取

PS: 因为我要爬取的信息比较全面,特别是问题,知乎API里并没有直接获取问题所有信息的接口,我用的网页爬取,所以会慢一些,以后如果需要我会优化

### 问题

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

### 回答
	
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
	    excerpt = scrapy.Field()

### 话题

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