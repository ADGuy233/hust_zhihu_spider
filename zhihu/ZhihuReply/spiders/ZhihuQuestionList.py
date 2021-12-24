import json
import time
from bs4 import BeautifulSoup as bs

import scrapy
from ZhihuReply import items

class ZhihuQuestionList(scrapy.Spider):
    name = "ZhihuQuestionList"

    def start_requests(self):
        BeginPage = 0
        EndPage = 130
        type = 'top_activity'  # 'essence'\\'top_activity'\\'timeline_activity' 近期精华、 最高热度、 最新讨论
        topicids = ['19566933']
        include = "data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp&data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics"
        for topicid in topicids:
            for offset in range(BeginPage * 10, EndPage * 10 + 1, 10):
                url_part = "/api/v5.1/topics/{}/feeds/{}?offset={}&limit=10&include={}".format(topicid, type, offset, include)
                # headers = self.gen_header(url_part=url_part)
                url = 'https://www.zhihu.com{}'.format(url_part)
                meta = {}
                meta['access_time'] = time.strftime("%Y/%m/%d %H:00", time.localtime(time.time()))
                meta['topicid'] = topicid
                meta['type'] = type
                meta['encrypt'] = url_part
                yield scrapy.Request(url=url,meta=meta,dont_filter=True,callback=self.question_list_parse)

    def question_list_parse(self,response):
        question_list = json.loads(response.body.decode("utf-8"))["data"]
        meta = response.meta
        for question in question_list:
            try:
                qid = question['target']['question']['id']
                print("get question {}".format(qid))
                title = question['target']['question']['title']
                created = question['target']['question']['created']
                topicid = meta['topicid']
                access_time = meta['access_time']
                type = meta['type']  # 列表类型
                yield items.QuestionList(qid=qid,title=title,created=created,topicid=topicid,access_time=access_time,type=type)
                meta = {}
                meta['qid'] = qid
                meta['title'] = title
                meta['created'] = created
                yield scrapy.Request(url='https://www.zhihu.com/question/{}'.format(qid),
                                     meta=meta, callback=self.question_parse, dont_filter=True)
            except KeyError:
                print("not a question!")

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
        topic_list = []
        for topic in topics:
            tid = topic['id']
            name = topic['name']
            topic_list.append(name)
            url_part = "/api/v4/topics/{}?include=introduction%2Cquestions_count%2Cfollowers_count%2Cis_following".format(tid)
            meta = {}
            meta['encrypt'] = url_part
            yield scrapy.Request(url='https://www.zhihu.com{}'.format(url_part), callback=self.topic_parse,dont_filter=True)
        topic_list = " ".join(topic_list)
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


