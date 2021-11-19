from bs4 import  BeautifulSoup as bs
import urllib.request
import json
import time

class DoubanSpider(object):
# 一个爬取豆瓣的爬虫
      def __init__(self):
          self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
          self.url = "https://movie.douban.com/top250"
          self.file_name = open("DoubanTop250.txt", "w", encoding="utf-8")

          self.run()

      def run(self):
          # 生成待爬取的所有影片url
          start_page = 1
          end_page = 10
          for page in range(start_page, end_page + 1):
              print("正在处理第" + str(page) + "页")
              pn = (page-1)*25
              # 接接成完整的url地址
              full_url = self.url + "?start=" + str(pn)
              # 获取招聘详情链接:l square
              print(full_url)
              link_list = self.getPositions(full_url)
              print(link_list)
              for link in link_list:
                  self.getPositionInfo(link)
          self.file_name.close()

      def loadPage(self,url):
          request = urllib.request.Request(url,headers= self.header)
          response = urllib.request.urlopen(request)
          time.sleep(0.2)
          html = response.read()
          return html

      def getPositions(self,url):
          html = self.loadPage(url)
          html = html.decode("utf-8")
          # 创建 Beautiful Soup 对象，指定lxml解析器
          soup = bs(html,"html.parser")
          link_list = []
          for link in soup.find_all(class_='pic'):
              text = link.a['href']
              print(text)
              link_list.append(text)
          return link_list


      def getPositionInfo(self,url):
          html = self.loadPage(url)
          html = html.decode("utf-8")
          soup = bs(html, "html.parser")
          item = {}
          try:
              name = soup.find(property="v:itemreviewed").string
              print(name)
              year = soup.find(class_='year').string
              print(year)
              director = soup.find(rel="v:directedBy").string
              print(director)
              actorslist = soup.find_all(rel="v:starring")
              genrelist = soup.find_all(property="v:genre")
              actor = ''
              for actors in actorslist:
                  actor += (actors.string + '、')
              print(actor)
              genre = ''
              for genres in genrelist:
                  genre += (genres.string + '、')
              print(genre)
              ReleaseDate = soup.find(property="v:initialReleaseDate")['content']
              print(ReleaseDate)
              runtime = soup.find(property="v:runtime")['content']
              print(runtime)
              score = soup.find(class_="ll rating_num",property="v:average").string
              print(score)

              item['name'] = name
              item['year'] = year
              item['director'] = director
              item['actor'] = actor
              item['genre'] = genre
              item['ReleaseDate'] = ReleaseDate
              item['runtime'] = runtime
              item['score'] = score
          except:
              pass

          if item:
              line = json.dumps(item, ensure_ascii=False) + "\n"
              self.file_name.write(line)

if __name__ == '__main__':
    my_spider = DoubanSpider()





