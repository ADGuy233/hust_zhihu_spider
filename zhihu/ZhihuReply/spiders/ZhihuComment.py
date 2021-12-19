import scrapy
import json
import re
from bs4 import BeautifulSoup as bs
import pandas as pd

from ZhihuReply import items

class ZhihuReplySpider(scrapy.Spider):
    name = 'ZhihuComment'

    def start_requests(self):
        file_path = r"C:\Users\ti\OneDrive\论文硕士\知乎豆瓣\Spiders\Data\QuestionList\questionlist.csv"
        Data = pd.read_csv(file_path)
        # 以排序方式为essence的问题列表中的qid为种子
        # question_list_essence = Data[Data['sortby']=="essence"]['qid'].to_list()
        # question_list = list(set(question_list_essence))
        question_list = ['487684056']

        for qid in question_list:
            # 生成回答页面的初始url
            yield scrapy.Request(
                    url='https://www.zhihu.com/api/v4/questions/{}/answers?'
                        'include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cvip_info%2Cbadge%5B*%5D.topics%3Bdata%5B*%5D.settings.table_of_content.enabled'
                        '&offset=0&limit=20&sort_by=updated'.format(qid),
                    callback=self.answer_parse)

    def answer_parse(self, response):
        # 获取“is_end”标签与当前页数
        is_end = json.loads(response.body.decode("utf-8"))["paging"]['is_end']
        offset = re.search('offset=\d*', response.request.url)
        offset = int(offset.group()[len('offset='):])
        # 在初始回答页，获取api未能覆盖的回答信息
        if offset==0:
            question = json.loads(response.body.decode("utf-8"))["data"][0]['question']
            # 用meta传递不方便从html获取的信息
            meta = {}
            meta['qid'] = question['id']
            meta['title'] = question['title']
            meta['created'] = question['created']
            yield scrapy.Request(
                    url='https://www.zhihu.com/question/{}/answers/updated'.format(meta['qid']),
                    callback=self.question_parse,meta=meta)
        # 对回答列表的数据进行批量解析
        answers = json.loads(response.body.decode("utf-8"))["data"]
        for answer in answers:
            aid = answer['id']
            qid = answer['question']['id']
            author = answer['author']['url_token']
            name = answer['author']['name']
            updated_time = answer['updated_time']
            comment_count = answer['comment_count']
            voteup_count = answer['voteup_count']
            content = answer['content']
            yield items.Answer(aid=aid, qid=qid, updated_time=updated_time, author=author,name=name,
                              comment_count=comment_count, voteup_count=voteup_count, content=content)
            meta = {}
            meta['aid'] = aid
            meta['qid'] = qid
            # 生成挂靠answer的一级评论url qid 不变 aid 不变
            if comment_count != 0:
                yield scrapy.Request(
                    url='https://www.zhihu.com/api/v4/answers/{}/root_comments?order=normal&limit=20&offset=0&status=open'.format(aid),
                    callback=self.comment_parse,meta=meta)
        if is_end:
            pass
        else:
            yield scrapy.Request(url=json.loads(response.body.decode("utf-8"))["paging"]['next'],
                                 callback=self.answer_parse)

    def question_parse(self,response):
        meta = response.meta  # 传入answer中的qid、title与created
        qid = meta['qid']
        title = meta['title']
        created = meta['created']
        soup = bs(response.body.decode("utf-8"),"html.parser")
        # 解析问题的作者url_token
        authorinfo = soup.find(class_="AuthorInfo")
        author = authorinfo.find(itemprop="url")['content']
        author = author.split('/')[-1]
        name = authorinfo.find(itemprop="name")['content']
        # 解析问题的话题标签
        topics = soup.find('div', attrs={'data-zop-question':True})['data-zop-question']
        topics = json.loads(topics)['topics']
        # 无加密的话题信息仅能获得token、name
        for topic in topics:
            tid = topic['id']
            yield scrapy.Request(
                    url='https://www.zhihu.com/api/v4/topics/{}?include=introduction%2Cquestions_count%2Cfollowers_count%2Cis_following'.format(tid),
                    callback=self.topic_parse)
        topic_list = json.dumps(topics)
        # 解析问题的关注数与浏览数
        numboard = soup.find(class_="NumberBoard QuestionFollowStatus-counts NumberBoard--divider")
        numboard = numboard.find_all(class_="NumberBoard-itemValue")
        follow = numboard[0]["title"]
        view = numboard[1]["title"]
        def clean(string):
            string = string.replace(' ', '')
            string = string.replace("\u200B", '')  # 注意解析结果有异常制表符
            string = string.replace("好问题", '')
            string = string.replace("添加评论", '0')
            string = string.replace("条评论", '')
            if string == "":
                return 0
            else:
                return eval(string)
        good_question = clean(soup.find(class_='GoodQuestionAction').get_text())
        comment = clean(soup.find(class_='QuestionHeader-Comment').get_text())
        yield items.Question(qid=qid, title=title, created=created, author=author, name=name, topic_list=topic_list,
                             follow=follow, view=view, good_question=good_question, comment=comment)

        if comment > 0: # 传给挂靠Question的一级评论  qid 不变 aid = 0 root_comment = 0
            meta = {}
            meta['qid'] = qid
            meta['aid'] = 0
            meta['root_comment'] = 0
            yield scrapy.Request(
                    url='https://www.zhihu.com/api/v4/questions/{}/root_comments?order=normal&limit=20&offset=0&status=open'.format(meta['qid']),
                    callback=self.root_comment_parse,meta=meta)

    # 负责解析挂靠于answer的一级评论  qid 不变 aid不变 root_comment = 0
    def comment_parse(self,response):
        is_end = json.loads(response.body.decode("utf-8"))["paging"]['is_end']
        comments = json.loads(response.body.decode("utf-8"))["data"]
        meta = response.meta
        for comment in comments:
            cid = comment['id']
            aid = meta['aid']
            qid = meta['qid']
            root_comment = 0
            created_time = comment['created_time']
            author = comment['author']['member']["url_token"]
            name = comment['author']['member']["name"]
            child_comment_count = comment['child_comment_count']
            vote_count = comment['vote_count']
            content = comment['content']
            if comment['featured'] is True:
                featured = 1
            else:
                featured = 0
            yield items.Comment(cid=cid, aid=aid, qid=qid, root_comment=root_comment, created_time=created_time, author=author,
                              name=name, comment_count=child_comment_count, voteup_count=vote_count, content=content,featured=featured)
            # 当子评论在两条以内时,相关内容会在上级评论中连带给出
            if child_comment_count <= 2:
                child_comments = comment["child_comments"]
                for child_comment in child_comments:
                    root_comment = cid
                    cid = child_comment['id']
                    created_time = child_comment['created_time']
                    try:
                        author = child_comment['author']['member']["url_token"]
                    except KeyError as e:
                        print(e)
                        author = ""
                    name = child_comment['author']['member']["name"]
                    child_comment_count = 0
                    vote_count = child_comment['vote_count']
                    content = child_comment['content']
                    reply_to_author = child_comment['reply_to_author']['member']["name"]
                    yield items.ChildComment(cid=cid, aid=aid, qid=qid, root_comment=root_comment ,created_time=created_time, author=author,
                                        name=name, comment_count=child_comment_count, voteup_count=vote_count, content=content, reply_to_author=reply_to_author)
            else:
                meta['root_comment'] = cid
                yield scrapy.Request(url='https://www.zhihu.com/api/v4/comments/{}/child_comments'.format(cid),
                                     meta=meta, callback=self.child_comment_parse)
        if is_end:
            pass
        else:
            yield scrapy.Request(url=json.loads(response.body.decode("utf-8"))["paging"]['next'],
                                 meta=meta, callback=self.comment_parse)

    # 负责解析挂靠于question的一级评论
    def root_comment_parse(self,response):
        is_end = json.loads(response.body.decode("utf-8"))["paging"]['is_end']
        comments = json.loads(response.body.decode("utf-8"))["data"]
        meta = response.meta
        for comment in comments:
            cid = comment['id']
            aid = meta['aid']
            qid = meta['qid']
            root_comment = meta['root_comment']
            created_time = comment['created_time']
            author = comment['author']['member']["url_token"]
            name = comment['author']['member']["name"]
            child_comment_count = comment['child_comment_count']
            vote_count = comment['vote_count']
            content = comment['content']
            if comment['featured'] is True:
                featured = 1
            else:
                featured = 0
            yield items.Comment(cid=cid, aid=aid, qid=qid, root_comment=root_comment, created_time=created_time, author=author,
                              name=name, comment_count=child_comment_count, voteup_count=vote_count, content=content,featured=featured)
            # 当子评论在两条以内时,相关内容会在上级评论中连带给出
            if child_comment_count <= 2:
                child_comments = comment["child_comments"]
                for child_comment in child_comments:
                    root_comment = cid
                    cid = child_comment['id']
                    created_time = child_comment['created_time']
                    try:
                        author = child_comment['author']['member']["url_token"]
                    except KeyError as e:
                        print(e)
                        author = ""
                    name = child_comment['author']['member']['name']
                    child_comment_count = 0
                    vote_count = child_comment['vote_count']
                    content = child_comment['content']
                    reply_to_author = child_comment['reply_to_author']['member']["name"]
                    yield items.ChildComment(cid=cid, aid=aid, qid=qid, root_comment=root_comment,created_time=created_time, author=author,
                                        name=name, comment_count=child_comment_count, voteup_count=vote_count, content=content,reply_to_author=reply_to_author)
            else:
                meta['root_comment'] = cid
                yield scrapy.Request(url='https://www.zhihu.com/api/v4/comments/{}/child_comments'.format(cid),
                                     meta=meta, callback=self.child_comment_parse)
        if is_end:
            pass
        else:
            meta['root_comment'] = 0
            yield scrapy.Request(url=json.loads(response.body.decode("utf-8"))["paging"]['next'],
                                 meta=meta, callback=self.comment_parse)


    # 负责解析挂靠于评论的二级评论
    def child_comment_parse(self,response):
        is_end = json.loads(response.body.decode("utf-8"))["paging"]['is_end']
        child_comments = json.loads(response.body.decode("utf-8"))["data"]
        meta = response.meta
        for child_comment in child_comments:
            cid = child_comment['id']
            aid = meta['aid']
            qid = meta['qid']
            root_comment = meta['root_comment']
            try:
                author = child_comment['author']['member']["url_token"]
            except KeyError as e:
                print(e)
                author = ""
            name = child_comment['author']['member']["name"]
            created_time = child_comment['created_time']
            child_comment_count = 0
            vote_count = child_comment['vote_count']
            content = child_comment['content']
            reply_to_author = child_comment['reply_to_author']['member']["name"]
            yield items.ChildComment(cid=cid, aid=aid, qid=qid, root_comment=root_comment, created_time=created_time, author=author,
                              name=name, comment_count=child_comment_count, voteup_count=vote_count, content=content, reply_to_author=reply_to_author)
        if is_end:
            pass
        else:
            yield scrapy.Request(url=json.loads(response.body.decode("utf-8"))["paging"]['next'],meta=meta,
                                 callback=self.child_comment_parse)

    def topic_parse(self,response):
        topic = json.loads(response.body.decode("utf-8"))
        tid = topic['id']
        name = topic['name']
        questions_count = topic['questions_count']
        introduction = topic['introduction']
        followers_count = topic['followers_count']
        try:
           best_answers_count = topic['best_answers_count']
        except KeyError:
            best_answers_count = topic['best_answerers_count']
        yield items.Topic(tid=tid,name=name,questions_count=questions_count,introduction=introduction,
                          followers_count=followers_count,best_answers_count=best_answers_count)





