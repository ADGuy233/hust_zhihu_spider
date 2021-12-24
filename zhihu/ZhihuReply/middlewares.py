# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http.headers import Headers
import base64
import hashlib
import execjs
import os
import base64
import time

class ZhihuSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ZhihuDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def gen_header(self, url_part, d_c0='"AOCZbcULsRKPTmJKb9A50mFqiq7Neud6dsg=|1613898999"'):
        # 生成加密的明文
        f = "+".join(["101_3_2.0", url_part, d_c0])
        fmd5 = hashlib.new('md5', f.encode()).hexdigest()
        # 读取并运行用于加密的js脚本
        current_directory = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(current_directory,"spiders//x-zse-96//g_encrypt.js"), 'r') as f:
            ctx1 = execjs.compile(f.read(), cwd=os.path.join(current_directory,"spiders//x-zse-96"))
        encrypt_str = ctx1.call('b', fmd5)
        # 生成url对应的header
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            'cookie': 'd_c0={}'.format(d_c0),
            "x-api-version": "3.0.91",
            "x-zse-93": "101_3_2.0",
            "x-zse-96": "2.0_{}".format(encrypt_str)
        }
        return header


    def process_request(self, request, spider):
        proxyServer = "https://dynamic.xingsudaili.com:10010"
        proxyUser = "ZhihuReply"
        proxyPass = "ZhihuReply"
        proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
        # request.meta["proxy"] = proxyServer
        if 'encrypt' in request.meta.keys():
            headers = self.gen_header(request.meta['encrypt'])
            # request.headers["Proxy-Authorization"] = proxyAuth
            request.headers = Headers(headers)
        # else:
            # request.headers["Proxy-Authorization"] = proxyAuth

        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth
        return None

    # 用于记录异常请求
    def process_response(self, request, response, spider):
        if response.status != 200:
            name = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            with open((str(name) + ".txt"), 'w+') as file:
                file.write(response.url)
                return response
        else:
            return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
