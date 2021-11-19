import re
import scrapy
import sqlite3
import json
import math

from BiliReply import items

DB_FILE = r'C:/Users/ti/Desktop/av412935552.db'
PS_1 = 49
PS_2 = 10

# 完整爬取时间在11min左右

class BiliSpiderReply(scrapy.Spider):
    name = 'BiliReply'

    def start_requests(self):
        aid_list=['412935552']
        yield scrapy.Request(
                url='https://api.bilibili.com/x/v2/reply?oid={}&type=1&sort=0&ps={}&pn=1&jsonp=jsonp'.format(aid_list[0], PS_1), #[0]
                callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body.decode("utf-8"))["data"]
        replies = data["replies"]
        MAX_PN = math.ceil(data["page"].get("count")/PS_1)
        NUM = re.search('pn=\d*', response.request.url)
        NUM = int(NUM.group()[len('pn='):])
        AID = re.search('oid=\d*', response.request.url)
        AID = int(AID.group()[len('oid='):])
        ROOT = re.search('root=\d*', response.request.url)
        if (ROOT is None) and (NUM == 1):    # 此时url为一级评论初始url
            if replies is None:
                print("aid {} 无评论")
                yield items.Reply(rpid=0)
            for reply in replies:
                rpid = reply['rpid']
                print("rpid:{}".format(rpid))
                aid = reply['oid']
                #print("aid:{}".format(aid))
                mid = reply['mid']
                root = reply['root']
                #print("root:{}".format(root))
                reply_ctime = reply['ctime']
                reply_count = reply['rcount']
                #print("reply_count:{}".format(reply_count))
                reply_like = reply['like']
                content = reply['content'].get('message')
                print(content)
                yield items.Reply(rpid=rpid, aid=aid, mid=mid, root=root, reply_ctime=reply_ctime,
                         reply_count=reply_count, reply_like=reply_like, content=content)
                print("{} replies in aid {} root{} page {}".format(len(replies), aid, root, NUM))
                if reply_count > 0:     # rpid为root的所有二级评论的请求
                    for C2_PN in range(1, math.ceil(reply_count/PS_2) + 1):
                        # print('root：{} pn：{} https://api.bilibili.com/x/v2/reply/reply?oid={}&root={}&type=1&ps={}&pn={}&jsonp=jsonp'.format(
                          #  rpid, C2_PN, aid, rpid, PS_2, C2_PN)),
                        yield scrapy.Request(
                            url='https://api.bilibili.com/x/v2/reply/reply?oid={}&root={}&type=1&ps={}&pn={}&jsonp=jsonp'.format(aid, rpid, PS_2, C2_PN),
                            callback=self.parse)
            for C1_PN in range(2, MAX_PN + 1):  # 同aid下的所有一级评论请求
              #  print('aid:{} pn:{} https://api.bilibili.com/x/v2/reply?oid={}&type=1&sort=0&ps={}&pn={}&jsonp=jsonp'.format(AID, C1_PN, AID, PS_1, C1_PN))
                yield scrapy.Request(
                      url='https://api.bilibili.com/x/v2/reply?oid={}&type=1&sort=0&ps={}&pn={}&jsonp=jsonp'.format(AID, PS_1, C1_PN),
                      callback=self.parse)

        elif (ROOT is None) and NUM > 0:     # 判断url为任意非初始一级url
            for reply in replies:
                rpid = reply['rpid']
                print("rpid:{}".format(rpid))
                aid = reply['oid']
               # print("aid:{}".format(aid))
                mid = reply['mid']
                root = reply['root']
               # print("root:{}".format(root))
                reply_ctime = reply['ctime']
                reply_count = reply['rcount']
               # print("reply_count:{}".format(reply_count))
                reply_like = reply['like']
                content = reply['content'].get('message')
                print(content)
                if reply_count > 0:     # rpid为root的所有二级评论的请求
                    for C2_PN in range(1, math.ceil(reply_count/PS_2) + 1):
                      #  print('root：{} pn:{} https://api.bilibili.com/x/v2/reply/reply?oid={}&root={}&type=1&ps={}&pn={}&jsonp=jsonp'.format(rpid, C2_PN, aid, rpid, PS_2, C2_PN))
                        yield scrapy.Request(
                            url='https://api.bilibili.com/x/v2/reply/reply?oid={}&root={}&type=1&ps={}&pn={}&jsonp=jsonp'.format(aid, rpid, PS_2, C2_PN),
                            callback=self.parse)
                yield items.Reply(rpid=rpid, aid=aid, mid=mid, root=root, reply_ctime=reply_ctime,
                                  reply_count=reply_count, reply_like=reply_like, content=content)
                print("{} replies in aid {} root{} page {}".format(len(replies), aid, root, NUM))

        elif int(ROOT.group()[len('root='):]) > 0:      # 判断url为任意二级评论url
            for reply in replies:
                rpid = reply['rpid']
                print("rpid:{}".format(rpid))
                aid = reply['oid']
              # print("aid:{}".format(aid))
                mid = reply['mid']
                root = reply['root']
              # print("root:{}".format(root))
                reply_ctime = reply['ctime']
                reply_count = reply['rcount']
              # print("reply_count:{}".format(reply_count))
                reply_like = reply['like']
                content = reply['content'].get('message')
                print(content)
                yield items.Reply(rpid=rpid, aid=aid, mid=mid, root=root, reply_ctime=reply_ctime,
                         reply_count=reply_count, reply_like=reply_like, content=content)
                print("{} replies in aid {} root{} page {}".format(len(replies), aid, root, NUM))
