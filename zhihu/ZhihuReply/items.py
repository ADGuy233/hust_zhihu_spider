# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Question(scrapy.Item):
    pass

class Answer(scrapy.Item):
    aid = scrapy.Field()  #答案id
    qid = scrapy.Field()
    updated_time = scrapy.Field()  #
    author = scrapy.Field()
    content = scrapy.Field()  #
    voteup_count = scrapy.Field()
    comment_count = scrapy.Field()
