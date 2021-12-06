# Scrapy settings for zhihu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhihu'

SPIDER_MODULES = ['zhihu.spiders']
NEWSPIDER_MODULE = 'zhihu.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhihu (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'cookie':'_zap=b8487359-95b8-471c-8f0d-15a769d1032e;'
             ' d_c0="ANBbFp3l5xGPTmp0unQOjQTYLzMMOM8yxts=|1600400115"; '
             '_ga=GA1.2.809078608.1600400120; _xsrf=TWyhmiyMmvpC4G1iya2UEdD3dI8mWdsn; _9755xjdesxxd_=32; YD00517437729195:WM_TID=ipzKuKwpK+BFFEAFBAJ+07kzCgHvBevm; __snaker__id=TCvgXmAmnGFpMNxw; captcha_session_v2="2|1:0|10:1637481450|18:captcha_session_v2|88:eFNxOU5tZHN6a0RIM1pSeVM1aTlRM2lhVjlIN3RpZjJOVkNTTTVvTGw1a3h4VmRGcU1hNzBKaHdVYyt5RmtRNg==|5d50d212eddd8ed992af37a6eade88cf8956ff14dd248a096abc029c273aeeaa"; gdxidpyhxdE=WXS/mqX2dZp4urzya4jKnljDun30Ha0\QEMEIjCN1T71EGRNuQCQG+TQu4Dz9cdL/qHuC3ysU018z+w5HK2iuC9rdqsrEDzLBTRHQjSeRKD+61OoycyO+Y7nGlKa+wX1IIgU7EXGpCzq9wnCvUjqMvmw+rY4NHfrgJKP/qcdo2D+EkiX:1637482351714; YD00517437729195:WM_NI=0oKvnSeXO9MUR80BaFvck+/PFSqFvnuIMD7fgmrsWlaBAw4C0IxzSv/V5ZyGfaoCQxMqKm87199P8Z7cWSkCHJfAkGL+Smvz+37wVioyud2lg+9XunjpvTyVitqtHud+QlE=; YD00517437729195:WM_NIKE=9ca17ae2e6ffcda170e2e6ee8dc77f8397ff96cb47f48a8fa3d15e838b9b85b633f19b8d88d84a958887b2d42af0fea7c3b92af4b18597ed59a78881dad05f92e800a3e44eb6bda5ccae5c868dbfa7f566b79783a5b66ea5b3be94d668a39e8f98b749f497b89bd27eed8afbbbfc4da6bfa1a4d4748faf858ebb3df3e7f7b1bb52f5bd99b4ea498c96aaa2ea4d90f59d8ef572e9edf998d563ada7bb85b168a5f5f7b9f866aab0bab5fc5eabacbf95cb7fa8f59f8dc837e2a3; captcha_ticket_v2="2|1:0|10:1637481459|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfNzlrcUVydEZQMTZYaXU0d05kLnJSdklYaFE0OVA5NXA2VjRVODR1MU1rR0xZb2hUVHVhNF9tTklCVGVTbmxjVjdaRXNEazlvTUpUdGo5QVZFY3NvRUlwQ2U0Vkh2cTVLeHZHdElMWnk5OWRDVzg4T2lIMVV2MEl2S1Z5dmRHMHlJU3VxbmFLcVFXaW1EdjRpMUNNYkp2MHpiUnhlbzdLeDlNanJZX2VSV1A0SHlUelBENjRfWmIwLTkuLUptLkU2VG44LUM1WHZCNDY5dWFGRnhGYWR3b3p5dVQ4UDhpcXd5NlJsS1hPeF9FR09xLU9pVlY5Sm1feXYwcGFKX1VrTlprdmM2d2JPcy4xVkJqdjlEWlFjb29MQzRkV1NDd2NXQ01FaXEtZmNZNXNuamJBTS5ZLmtXTUF3NllVbFlFaURDN2t3Q00tLVlMbzZXRUg4UnlyLWdFdTZTQy5oTTZiUWdEcjlDS0d2THZZT081Y3Nac0F1QmpzV3JudWNycVJjdWg5dzFMYWhqZzZHMU5SYTJhNEpnUVh5TDRyem43ODVDMHNkWEE5eHpEdXRIb3NZTHJ6QlVjNjZudHZMa1JYRXUtaVN3OEM2bnNpTUlpVy56czcucjlOdWMxS3A1bVNCTnFGX0U1RG02LmR4MDFXZU5vRmQwekFYcEFaMyJ9|59d15d3e12b1e38b09c7f27c48bf6aa88cdcded5e269e1887ab1fbcdd5d9ab39"; z_c0="2|1:0|10:1637481475|4:z_c0|92:Mi4xY0lHZEh3QUFBQUFBMEZzV25lWG5FU1lBQUFCZ0FsVk5BMHFIWWdDV3REUUNJblRTcHUzM3FQU1dRcVVNVTgzLUxB|289cc68a94ba58f00f9dccd849a1e23e2ba43e2e1b8acf1577e3364de374bff1"; q_c1=38db7461569348bfb52b8415d3b4ffc1|1637641249000|1601711881000; __utmv=51854390.100--|2=registration_date=20201003=1^3=entry_date=20201003=1; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1637902299,1638108251,1638160132,1638361206; NOT_UNREGISTER_WAITING=1; SESSIONID=9mm3NnCfybrqDtJFf9zutrHGCBDI3oWBlEB993wG6u0; JOID=Vl0UBkh557_zmlc9XnhhYKLpJsBKQY7WxtM4ejwHhMmG2CR2HASPGpOcUj1crDUnY0DLWcbJtVFmazUuNQTJPzE=; osd=U1gQBkl84rvzm1I4WnhgZaftJsFPRIrWx9Y9fjwGgcyC2CVzGQCPG5aZVj1dqTAjY0HOXMLJtFRjbzUvMAHNPzA=; __utma=51854390.809078608.1600400120.1638160144.1638361211.6; __utmb=51854390.0.10.1638361211; __utmc=51854390; __utmz=51854390.1638361211.6.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/topic/19566933/hot; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1638361243; KLBRSID=4efa8d1879cb42f8c5b48fe9f8d37c16|1638361396|1638361206',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhihu.middlewares.ZhihuSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'zhihu.middlewares.ZhihuDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'zhihu.pipelines.ZhihuPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
