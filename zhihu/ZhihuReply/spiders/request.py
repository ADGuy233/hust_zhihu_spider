import urllib.request
from bs4 import BeautifulSoup as bs
import json
#from lxml import etree
import re



if __name__ == '__main__':
    #url = 'https://www.zhihu.com/topic/19566933/organize/entire'
    #url = 'https://www.zhihu.com/topic/19603085/hot'
    url = "https://www.zhihu.com/question/506271561/answers/updated"
    headers_zhihu={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'cookie':'__snaker__id=qxvYG030DxDOhb61; SESSIONID=3U1KhGFNnUdFBPvI4z3I7dGWUIjwYsx5DPE8JusXCnE; '
                 'osd=UF8SCknmtyL2vN6tVO0y_anIpVNAwJQP3p_4jnnFkQHblP2LdxkbuJy526NRfE3Qg9K_OHKmP0KyWR_j8qhaZgw=; '
                 'JOID=V1kWAErhsSb8v9mrUOcx-q_Mr1BHxpAF3Zj-inPGlgffnv6McR0Ru5u_36lSe0vUidG4PnasPEW0XRXg9a5ebA8=; _zap=b8487359-95b8-471c-8f0d-15a769d1032e; d_c0="ANBbFp3l5xGPTmp0unQOjQTYLzMMOM8yxts=|1600400115"; _ga=GA1.2.809078608.1600400120; _xsrf=TWyhmiyMmvpC4G1iya2UEdD3dI8mWdsn; _9755xjdesxxd_=32; YD00517437729195:WM_TID=ipzKuKwpK+BFFEAFBAJ+07kzCgHvBevm; __snaker__id=TCvgXmAmnGFpMNxw; captcha_session_v2="2|1:0|10:1637481450|18:captcha_session_v2|88:eFNxOU5tZHN6a0RIM1pSeVM1aTlRM2lhVjlIN3RpZjJOVkNTTTVvTGw1a3h4VmRGcU1hNzBKaHdVYyt5RmtRNg==|5d50d212eddd8ed992af37a6eade88cf8956ff14dd248a096abc029c273aeeaa"; gdxidpyhxdE=WXS/mqX2dZp4urzya4jKnljDun30Ha0\QEMEIjCN1T71EGRNuQCQG+TQu4Dz9cdL/qHuC3ysU018z+w5HK2iuC9rdqsrEDzLBTRHQjSeRKD+61OoycyO+Y7nGlKa+wX1IIgU7EXGpCzq9wnCvUjqMvmw+rY4NHfrgJKP/qcdo2D+EkiX:1637482351714; YD00517437729195:WM_NI=0oKvnSeXO9MUR80BaFvck+/PFSqFvnuIMD7fgmrsWlaBAw4C0IxzSv/V5ZyGfaoCQxMqKm87199P8Z7cWSkCHJfAkGL+Smvz+37wVioyud2lg+9XunjpvTyVitqtHud+QlE=; YD00517437729195:WM_NIKE=9ca17ae2e6ffcda170e2e6ee8dc77f8397ff96cb47f48a8fa3d15e838b9b85b633f19b8d88d84a958887b2d42af0fea7c3b92af4b18597ed59a78881dad05f92e800a3e44eb6bda5ccae5c868dbfa7f566b79783a5b66ea5b3be94d668a39e8f98b749f497b89bd27eed8afbbbfc4da6bfa1a4d4748faf858ebb3df3e7f7b1bb52f5bd99b4ea498c96aaa2ea4d90f59d8ef572e9edf998d563ada7bb85b168a5f5f7b9f866aab0bab5fc5eabacbf95cb7fa8f59f8dc837e2a3; captcha_ticket_v2="2|1:0|10:1637481459|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfNzlrcUVydEZQMTZYaXU0d05kLnJSdklYaFE0OVA5NXA2VjRVODR1MU1rR0xZb2hUVHVhNF9tTklCVGVTbmxjVjdaRXNEazlvTUpUdGo5QVZFY3NvRUlwQ2U0Vkh2cTVLeHZHdElMWnk5OWRDVzg4T2lIMVV2MEl2S1Z5dmRHMHlJU3VxbmFLcVFXaW1EdjRpMUNNYkp2MHpiUnhlbzdLeDlNanJZX2VSV1A0SHlUelBENjRfWmIwLTkuLUptLkU2VG44LUM1WHZCNDY5dWFGRnhGYWR3b3p5dVQ4UDhpcXd5NlJsS1hPeF9FR09xLU9pVlY5Sm1feXYwcGFKX1VrTlprdmM2d2JPcy4xVkJqdjlEWlFjb29MQzRkV1NDd2NXQ01FaXEtZmNZNXNuamJBTS5ZLmtXTUF3NllVbFlFaURDN2t3Q00tLVlMbzZXRUg4UnlyLWdFdTZTQy5oTTZiUWdEcjlDS0d2THZZT081Y3Nac0F1QmpzV3JudWNycVJjdWg5dzFMYWhqZzZHMU5SYTJhNEpnUVh5TDRyem43ODVDMHNkWEE5eHpEdXRIb3NZTHJ6QlVjNjZudHZMa1JYRXUtaVN3OEM2bnNpTUlpVy56czcucjlOdWMxS3A1bVNCTnFGX0U1RG02LmR4MDFXZU5vRmQwekFYcEFaMyJ9|59d15d3e12b1e38b09c7f27c48bf6aa88cdcded5e269e1887ab1fbcdd5d9ab39"; z_c0="2|1:0|10:1637481475|4:z_c0|92:Mi4xY0lHZEh3QUFBQUFBMEZzV25lWG5FU1lBQUFCZ0FsVk5BMHFIWWdDV3REUUNJblRTcHUzM3FQU1dRcVVNVTgzLUxB|289cc68a94ba58f00f9dccd849a1e23e2ba43e2e1b8acf1577e3364de374bff1"; q_c1=38db7461569348bfb52b8415d3b4ffc1|1637641249000|1601711881000; __utmz=51854390.1637641249.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100--|2=registration_date=20201003=1^3=entry_date=20201003=1; tst=r; __utma=51854390.809078608.1600400120.1637838482.1637848443.3; __utmb=51854390.0.10.1637848443; NOT_UNREGISTER_WAITING=1; __utmc=51854390; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1637838465,1637839461,1637850104,1637851896; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1637851896; KLBRSID=81978cf28cf03c58e07f705c156aa833|1637852063|1637851886'
    }

    request = urllib.request.Request(url,headers= headers_zhihu)
    response = urllib.request.urlopen(request)
    html = response.read()
    html = html.decode("utf-8")
    soup = bs(html,"html.parser")
    topic_list = soup.find('div',attrs={'data-zop-question':True})['data-zop-question']
    topics = json.loads(topic_list)['topics']  # 解析话题列表
    print(topics)
    numboard = soup.find(class_="NumberBoard QuestionFollowStatus-counts NumberBoard--divider")
    numboard = numboard.find_all(class_="NumberBoard-itemValue")
    follow = numboard[0]["title"]
    view = numboard[1]["title"]
    print("关注者",follow," ","浏览",view)
    def clean(string):
        string = string.replace(' ', '')
        string = string.replace("\u200B", '') #注意解析结果有异常制表符
        string = string.replace("好问题", '')
        string = string.replace("添加评论", '0')
        string = string.replace("条评论", '')
        if string == "":
            return 0
        else:
            return eval(string)
    goodquestion = clean(soup.find(class_='GoodQuestionAction').get_text())
    comment = clean(soup.find(class_='QuestionHeader-Comment').get_text())












