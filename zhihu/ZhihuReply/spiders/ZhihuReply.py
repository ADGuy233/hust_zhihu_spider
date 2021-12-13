import scrapy, re, json
from ZhihuReply import items

class ZhihureplySpider(scrapy.Spider):
    name = 'ZhihuReply'

    def start_requests(self):
        question_list = [496963656]
        yield scrapy.Request(
                url='https://www.zhihu.com/api/v4/questions/{}/answers?'
                    'include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cvip_info%2Cbadge%5B*%5D.topics%3Bdata%5B*%5D.settings.table_of_content.enabled'
                    '&offset=0&limit=20&sort_by=updated'.format(question_list[0]),
                callback=self.answer_parse)

    def question_parse(self,response):
        is_end = json.loads(response.body.decode("utf-8"))["paging"]['is_end']
        questions = json.loads(response.body.decode("utf-8"))["data"]
        for question in questions:
            qid = question['question']['id']
            yield items.Reply()
        if is_end:
            pass
        else:
            yield scrapy.Request(url=json.loads(response.body.decode("utf-8"))["paging"]['next'],
                                 callback=self.answer_parse)


    def answer_parse(self, response):
        is_end = json.loads(response.body.decode("utf-8"))["paging"]['is_end']
        answers = json.loads(response.body.decode("utf-8"))["data"]
        for answer in answers:
            aid = answer['id']
            print("aid:{}".format(aid))
            qid = answer['question']['id']
            author = answer['author']['name']
            updated_time = answer['updated_time']
            comment_count = answer['comment_count']
            voteup_count = answer['voteup_count']
            content = answer['content']
            '''yield items.Reply(aid=aid, qid=qid, updated_time=updated_time, author=author,
                              comment_count=comment_count, voteup_count=voteup_count, content=content)'''
            if comment_count != 0:
                yield scrapy.Request(
                    url='https://www.zhihu.com/api/v4/answers/{}/root_comments?order=normal&limit=20&offset=0&status=open'.format(aid),
                    callback=self.comment_parse)
        if is_end:
            pass
        else:
            yield scrapy.Request(url=json.loads(response.body.decode("utf-8"))["paging"]['next'],
                                 callback=self.answer_parse)

    def comment_parse(self,response):
        is_end = json.loads(response.body.decode("utf-8"))["paging"]['is_end']
        comments = json.loads(response.body.decode("utf-8"))["data"]
        aid = response.url.split('/')[6]
        for comment in comments:
            cid = comment['id']
            print('cid:', cid)
            author = comment['author']['member']['name']
            updated_time = comment['created_time']
            child_comment_count = comment['child_comment_count']
            vote_count = comment['vote_count']
            content = comment['content'].get('message')
            '''yield items.Reply(aid=aid, cid=cid, updated_time=updated_time, author=author,
                              comment_count=child_comment_count, voteup_count=vote_count, content=content)'''
            if child_comment_count <= 2:
                print(comment['child_comments']['id'])
                #yield items.Reply()
            else:
                yield scrapy.Request(url='https://www.zhihu.com/api/v4/comments/{}/child_comments'.format(cid),
                                     callback=self.child_comment_parse)
        if is_end:
            pass
        else:
            yield scrapy.Request(url=json.loads(response.body.decode("utf-8"))["paging"]['next'],
                                 callback=self.comment_parse)

    def child_comment_parse(self,response):
        is_end = json.loads(response.body.decode("utf-8"))["paging"]['is_end']
        comments = json.loads(response.body.decode("utf-8"))["data"]
        cid = response.url.split('/')[6]
        for comment in comments:
            ccid = comment['id']
            print('ccid',ccid)
            author = comment['author']['member']['name']
            reply_to_author = comment['reply_to_author']['member']['name']
            updated_time = comment['created_time']
            child_comment_count = comment['child_comment_count']
            vote_count = comment['vote_count']
            content = comment['content'].get('message')
            '''yield items.Reply(cid=cid, ccid=ccid, reply_to_author=reply_to_author, updated_time=updated_time, author=author,
                              comment_count=child_comment_count, voteup_count=vote_count, content=content)'''
        if is_end:
            pass
        else:
            yield scrapy.Request(url=json.loads(response.body.decode("utf-8"))["paging"]['next'],
                                 callback=self.child_comment_parse)




