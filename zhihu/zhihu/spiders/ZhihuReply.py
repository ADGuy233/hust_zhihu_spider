import scrapy,re,json


class ZhihureplySpider(scrapy.Spider):
    name = 'ZhihuReply'

    def start_requests(self):
        answer_list = []
        yield scrapy.Request(
                url='https://api.bilibili.com/x/v2/reply?oid={}&type=1&sort=0&ps={}&pn=1&jsonp=jsonp'.format(aid_list[0], PS_1), #[0]
                callback=self.parse)

    def parse(self, response):
        max_pn = json.loads(response.body.decode("utf-8"))["paging"]['totals']
        offset = 0
        while offset <= max_pn:
            datas = json.loads(response.body.decode("utf-8"))["data"]
            for answer in datas:
                aid = answer['id']
                print("aid:{}".format(aid))
                qid = answer['question']['id']
                author = answer['author']['name']
                updated_time = answer['updated_time']
                comment_count = answer['comment_count']
                voteup_count = answer['voteup_count']
                content = answer['content'].get('message')
                print(content)
                yield items.Reply(aid=aid, qid=qid, updated_time=updated_time, author=author,
                                  comment_count=comment_count, voteup_count=voteup_count, content=content)
                print("{} replies in aid {} root{} page {}".format(len(replies), aid, root, NUM))
            offset += 20




