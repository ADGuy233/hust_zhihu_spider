# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class QuestionList(scrapy.Item):
    qid = scrapy.Field()
    title = scrapy.Field()
    created = scrapy.Field()
    topicid = scrapy.Field()
    access_time = scrapy.Field()
    type = scrapy.Field()

class Question(scrapy.Item):
    qid = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()   # 用户id
    name = scrapy.Field()
    created = scrapy.Field()
    topic_list = scrapy.Field()
    follow = scrapy.Field()
    view = scrapy.Field()
    good_question = scrapy.Field()
    comment = scrapy.Field()

class Answer(scrapy.Item):
    aid = scrapy.Field()  #回答的标识id
    qid = scrapy.Field()  #挂靠问题的标识id (即root)
    updated_time = scrapy.Field()
    author = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()
    voteup_count = scrapy.Field()
    comment_count = scrapy.Field()

class Comment(scrapy.Item):
    cid = scrapy.Field()  # 评论的标识id
    aid = scrapy.Field()  # 挂靠回答的id(如果为问题评论则为0)
    qid = scrapy.Field()  # 回答挂靠问题的id
    root_comment = scrapy.Field() # 挂靠评论的id(如果为1级评论则为0)
    created_time = scrapy.Field()
    author = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()
    voteup_count = scrapy.Field()
    comment_count = scrapy.Field()
    featured = scrapy.Field()  # 是否为精选

class ChildComment(scrapy.Item):
    cid = scrapy.Field()  # 评论的标识id
    aid = scrapy.Field()  # 挂靠回答的id(如果为问题评论则为0)
    qid = scrapy.Field()  # 回答挂靠问题的id
    root_comment = scrapy.Field() # 挂靠评论的id(如果为1级评论则为0)
    created_time = scrapy.Field()
    author = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()
    voteup_count = scrapy.Field()
    comment_count = scrapy.Field()
    reply_to_author = scrapy.Field()

class Topic(scrapy.Item):
    tid = scrapy.Field() # 话题的标识id
    name = scrapy.Field()
    questions_count = scrapy.Field()
    introduction = scrapy.Field()
    followers_count = scrapy.Field()
    best_answers_count = scrapy.Field()

class Author(scrapy.Item):
    author = scrapy.Field()  # 用户id作为主键
    name = scrapy.Field()
    answer_count = scrapy.Field()
    badge = scrapy.Field()

class FollowingTopic(scrapy.Item):
    author = scrapy.Field()
    following_topic = scrapy.Field()




