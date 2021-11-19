# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Reply(scrapy.Item):         # 使用视频列表aid生成请求
    rpid = scrapy.Field()         # 评论ID  （PK）
    aid = scrapy.Field()          # 视频AV号
    mid = scrapy.Field()          # 评论用户
    root = scrapy.Field()         # 根评论/上级评论（非0时为跟帖）
    reply_ctime = scrapy.Field()  # 评论时间
    reply_count = scrapy.Field()  # 回复总数
    reply_like = scrapy.Field()   # 赞数
    content = scrapy.Field()       # 评论内容

