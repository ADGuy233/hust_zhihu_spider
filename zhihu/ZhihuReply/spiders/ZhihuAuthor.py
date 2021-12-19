import scrapy
import json
import re
import requests
from bs4 import BeautifulSoup as bs
import urllib.request
import pandas as pd

from ZhihuReply import items

def GetTopic(token,offset):
    url = 'https://www.zhihu.com/api/v4/members/{}/' \
          'following-topic-contributions?include=data%5B*%5D.topic.introduction&offset={}&limit=20'.format(token , offset)
    headers_zhihu={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'cookie':'__snaker__id=qxvYG030DxDOhb61; SESSIONID=3U1KhGFNnUdFBPvI4z3I7dGWUIjwYsx5DPE8JusXCnE; '
                 'osd=UF8SCknmtyL2vN6tVO0y_anIpVNAwJQP3p_4jnnFkQHblP2LdxkbuJy526NRfE3Qg9K_OHKmP0KyWR_j8qhaZgw=; '
                 'JOID=V1kWAErhsSb8v9mrUOcx-q_Mr1BHxpAF3Zj-inPGlgffnv6McR0Ru5u_36lSe0vUidG4PnasPEW0XRXg9a5ebA8=; _zap=b8487359-95b8-471c-8f0d-15a769d1032e; d_c0="ANBbFp3l5xGPTmp0unQOjQTYLzMMOM8yxts=|1600400115"; _ga=GA1.2.809078608.1600400120; _xsrf=TWyhmiyMmvpC4G1iya2UEdD3dI8mWdsn; _9755xjdesxxd_=32; YD00517437729195:WM_TID=ipzKuKwpK+BFFEAFBAJ+07kzCgHvBevm; __snaker__id=TCvgXmAmnGFpMNxw; captcha_session_v2="2|1:0|10:1637481450|18:captcha_session_v2|88:eFNxOU5tZHN6a0RIM1pSeVM1aTlRM2lhVjlIN3RpZjJOVkNTTTVvTGw1a3h4VmRGcU1hNzBKaHdVYyt5RmtRNg==|5d50d212eddd8ed992af37a6eade88cf8956ff14dd248a096abc029c273aeeaa"; gdxidpyhxdE=WXS/mqX2dZp4urzya4jKnljDun30Ha0\QEMEIjCN1T71EGRNuQCQG+TQu4Dz9cdL/qHuC3ysU018z+w5HK2iuC9rdqsrEDzLBTRHQjSeRKD+61OoycyO+Y7nGlKa+wX1IIgU7EXGpCzq9wnCvUjqMvmw+rY4NHfrgJKP/qcdo2D+EkiX:1637482351714; YD00517437729195:WM_NI=0oKvnSeXO9MUR80BaFvck+/PFSqFvnuIMD7fgmrsWlaBAw4C0IxzSv/V5ZyGfaoCQxMqKm87199P8Z7cWSkCHJfAkGL+Smvz+37wVioyud2lg+9XunjpvTyVitqtHud+QlE=; YD00517437729195:WM_NIKE=9ca17ae2e6ffcda170e2e6ee8dc77f8397ff96cb47f48a8fa3d15e838b9b85b633f19b8d88d84a958887b2d42af0fea7c3b92af4b18597ed59a78881dad05f92e800a3e44eb6bda5ccae5c868dbfa7f566b79783a5b66ea5b3be94d668a39e8f98b749f497b89bd27eed8afbbbfc4da6bfa1a4d4748faf858ebb3df3e7f7b1bb52f5bd99b4ea498c96aaa2ea4d90f59d8ef572e9edf998d563ada7bb85b168a5f5f7b9f866aab0bab5fc5eabacbf95cb7fa8f59f8dc837e2a3; captcha_ticket_v2="2|1:0|10:1637481459|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfNzlrcUVydEZQMTZYaXU0d05kLnJSdklYaFE0OVA5NXA2VjRVODR1MU1rR0xZb2hUVHVhNF9tTklCVGVTbmxjVjdaRXNEazlvTUpUdGo5QVZFY3NvRUlwQ2U0Vkh2cTVLeHZHdElMWnk5OWRDVzg4T2lIMVV2MEl2S1Z5dmRHMHlJU3VxbmFLcVFXaW1EdjRpMUNNYkp2MHpiUnhlbzdLeDlNanJZX2VSV1A0SHlUelBENjRfWmIwLTkuLUptLkU2VG44LUM1WHZCNDY5dWFGRnhGYWR3b3p5dVQ4UDhpcXd5NlJsS1hPeF9FR09xLU9pVlY5Sm1feXYwcGFKX1VrTlprdmM2d2JPcy4xVkJqdjlEWlFjb29MQzRkV1NDd2NXQ01FaXEtZmNZNXNuamJBTS5ZLmtXTUF3NllVbFlFaURDN2t3Q00tLVlMbzZXRUg4UnlyLWdFdTZTQy5oTTZiUWdEcjlDS0d2THZZT081Y3Nac0F1QmpzV3JudWNycVJjdWg5dzFMYWhqZzZHMU5SYTJhNEpnUVh5TDRyem43ODVDMHNkWEE5eHpEdXRIb3NZTHJ6QlVjNjZudHZMa1JYRXUtaVN3OEM2bnNpTUlpVy56czcucjlOdWMxS3A1bVNCTnFGX0U1RG02LmR4MDFXZU5vRmQwekFYcEFaMyJ9|59d15d3e12b1e38b09c7f27c48bf6aa88cdcded5e269e1887ab1fbcdd5d9ab39"; z_c0="2|1:0|10:1637481475|4:z_c0|92:Mi4xY0lHZEh3QUFBQUFBMEZzV25lWG5FU1lBQUFCZ0FsVk5BMHFIWWdDV3REUUNJblRTcHUzM3FQU1dRcVVNVTgzLUxB|289cc68a94ba58f00f9dccd849a1e23e2ba43e2e1b8acf1577e3364de374bff1"; q_c1=38db7461569348bfb52b8415d3b4ffc1|1637641249000|1601711881000; __utmz=51854390.1637641249.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100--|2=registration_date=20201003=1^3=entry_date=20201003=1; tst=r; __utma=51854390.809078608.1600400120.1637838482.1637848443.3; __utmb=51854390.0.10.1637848443; NOT_UNREGISTER_WAITING=1; __utmc=51854390; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1637838465,1637839461,1637850104,1637851896; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1637851896; KLBRSID=81978cf28cf03c58e07f705c156aa833|1637852063|1637851886'
    }
    try:
        response = requests.get(url,headers=headers_zhihu)
        response.encoding = response.apparent_encoding
        is_end = dict(response.text)["paging"]['is_end']
        topics = dict(response.text)['data']
        ls = []
        for topic in topics:
            ls.append(topic['topic']['id'])
        if is_end:
            return ls
        else:
            GetTopic(token,offset + 20)
        
    except Exception as e:
        print(e)


class ZhihuauthorSpider(scrapy.Spider):
    name = 'ZhihuAuthor'

    def start_requests(self):
        file_path = r".\Data\QuestionList\authorlist.csv"
        Data = pd.read_csv(file_path)
        # 以排序方式为essence的问题列表中的qid为种子
        authorlist = Data['author']

        for token in authorlist[0:1]:
            # 生成回答页面的初始url
            yield scrapy.Request(
                    url='https://api.zhihu.com/people/{}'.format(token),
                    callback=self.author_parse)
            yield scrapy.Request(
                    url='https://www.zhihu.com/api/v4/members/{}'
                        '/following-topic-contributions?include='
                        'data%5B*%5D.topic.introduction&offset=0&limit=20'.format(token),
                    callback=self.author_parse)

    def author_parse(self,response):
        data = json.loads(response.body.decode('utf-8'))
        token = data['url_token']
        gender = data['gender']
        follower_account = data['follower_account']
        following_count = data['following_count']
        following_topic = GetTopic(token, 0)
        yield items.People(token=token, gender=gender, following_count=following_count,
                           follower_account=follower_account, following_topic=following_topic)







