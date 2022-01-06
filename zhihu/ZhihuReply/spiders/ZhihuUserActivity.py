import os

import pandas as pd
from sqlalchemy import create_engine
import random
import asyncio
import pyppeteer
from ZhihuReply.cookies import cookie
from ZhihuReply.config_generator import proj_dir

# set_navigator_js="""() =>{Object.defineProperties(navigator,{webdriver:{get: () => false}})}"""
print(proj_dir)
file_path = os.path.join(proj_dir,"Data","Replies","ZhihuTest.db")
engine = create_engine(r'sqlite:///{}'.format(file_path))

def filter_request(request):
    if "activities" in request.url:
        url = request.url
        print(author, url)

def get_cookie_item(cookie_str, author):
    cookie = []
    for line in cookie_str.split('; '):
        key, value = line.split('=',1)
        item = {'url':'https://www.zhihu.com/org/{}'.format(author),'name':key,'value':value}
        cookie.append(item)
    return cookie

async def main(cookie_str, author):
    # 设置浏览器基本参数
    browser = await pyppeteer.launch({
        'headless': True,
        # 从 https://www.chromium.org/getting-involved/download-chromium 下载，并获取chrome.exe的目录
        'executablePath': "D:\\chrome-win\\chrome.exe",
        'args': [
            '--disable-gpu',
        ],
    })
    page = await browser.newPage()
    page.on('request', filter_request)
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
    for item in get_cookie_item(cookie_str,author):
        await page.setCookie(item)
    await page.goto('https://www.zhihu.com/org/{}'.format(author))
    # await page.evaluate(set_navigator_js)

if __name__ == '__main__':
    cookie_list = cookie(type="cookie")
    author = pd.read_sql("Auhtor",engine).sample(50)
    author_list = author['author'].to_list()
    for author in author_list:
        cookie_str = random.choice(cookie_list)
        asyncio.get_event_loop().run_until_complete(main(cookie_str,author))



