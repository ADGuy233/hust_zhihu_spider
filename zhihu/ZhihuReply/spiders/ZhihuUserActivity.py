import asyncio
import pyppeteer

def get_activity(response):
    resourceType = response.request.resourceType
    if resourceType=='fetch':
        url = response.url
        if "activities" in url:
            print(url)

# async def filter_request(req):
#     """请求过滤"""
#     if req.resourceType in ['image']:
#         await req.abort()
#     else:
#         await req.continue_()

async def main():
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
    # page.on('request', filter_request)
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
    cookie_str = '''_zap=e30e24fb-a6be-4a99-b228-fb129208e354; d_c0="AOCZbcULsRKPTmJKb9A50mFqiq7Neud6dsg=|1613898999"; _9755xjdesxxd_=32; YD00517437729195%3AWM_TID=0lx2cpYrN4JABBBEEEYv0791i7jbyrsO; _xsrf=5GdiCGsPQQEqErDsSu1WWSezgFR8dMjA; __snaker__id=TvmXgr6biqVzKIQh; q_c1=d1036d7a6f164ee0b6906497cd7c3c59|1638090380000|1638090380000; __utmv=51854390.100--|2=registration_date=20150709=1^3=entry_date=20150709=1; __utmz=51854390.1639897944.5.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/topic/19566933/intro; __utma=51854390.1810339604.1638090382.1639641168.1639897944.5; gdxidpyhxdE=H%2BwPrKmuMN8slHwB1dahujU8qDxAzWf%2BHyAlAXG%2FTRzfY8tW%2BRK6yKuUkEMIjoDCeqBRAMuAjke6axmc%2B7DDy%5C%5Ca73KA0YUWhkly1gAxW6rAGBE%2BZZx%5CCRzlec6NjIyMPtnetCkcgPTpE2ZwDky%5CKY68Gcy2jtdr47H%2FAhRs%2F16w%5Cs%2Bh%3A1640871128088; YD00517437729195%3AWM_NI=hq1KWZRSTbbcnQXWbVchS6k46Qej5YzzosI89OtnFb3ZPPt%2FC8FikNi74Tep8E8bPrcemiSbEDapIrlgBuXKO89JlxqKX13UuToQa4w%2FS6BowhC6MEQODBX3HsvIu46tdWQ%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb2c543f3bfa7abf268acbc8aa3d14b828f8faef13d879c8482f45da8e9afa6c22af0fea7c3b92aacafffacd652928d9c83e169ae8f98b8e15ea1b89dd7ea40f68fab8bb853baa6a194cc34fb91bc8fc56af186a0b1f72581e88a8aea46abe9fcb5e87cfc9bf883d37aa1bba38ad26a879caf91cc7ab0b98e96db418de8f7abef74b39598d2b25fb78ca1b2e440b5f19dd7c165b5b88dd7d04f93918ca3db398cadbaaaf840f6acacb8d437e2a3; captcha_session_v2="2|1:0|10:1640870234|18:captcha_session_v2|88:dUdRKzNUVCtKTmxQdUtCSjJDSEx4Z1RxQytDRWVxVzBRUmRFUjNScnpQbXIvQk9iRjg2SVRhM1hBd3BEV1pQTQ==|af37d4bc6727ff8b7b4600a4cbf46f7317c2a4ba4f85aa727325534c0da61dbc"; r_cap_id="MmI3NTNkYmU4NmMyNGFlNjgyNDg4ZmYwZjc3NGYxMjg=|1640870245|8541136dc9cf86c9b339b218f59acd362285fd35"; cap_id="NzUyNDMxMTc2ZGU2NDg2MThmMGY5NzY3NTUwZTk0MzY=|1640870245|25d3b1e2622af11bb8dbedd270945166d58f4bc8"; l_cap_id="Mjc4MTcyMmU1OTgxNDBhOWIxYjcxZmM4NGFjNWVmNTM=|1640870245|fd49ea4bb83fddcfcab94e3fc8bf22bbd8a007a2"; z_c0=Mi4xR0NMVkFRQUFBQUFBNEpsdHhRdXhFaGNBQUFCaEFsVk5jUC02WWdCQnV3RmhXTnYyS0M0THVQR2w5X0xKWlMzQW1B|1640870256|7f52963a8e1522a5afb515ec2f6db03432a587fb; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1641027416,1641299189,1641299903,1641300437; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1641302588; KLBRSID=975d56862ba86eb589d21e89c8d1e74e|1641303280|1641299175'''
    for line in cookie_str.split('; '):
        key, value = line.split('=',1)
        item = {'url':'https://www.zhihu.com/org/jing-ji-guan-cha-bao','name':key,'value':value}
        await page.setCookie(item)
    page.on('response', get_activity)
    await page.goto('https://www.zhihu.com/org/jing-ji-guan-cha-bao')
    await page.evaluate("""
            () =>{
                   Object.defineProperties(navigator,{
                     webdriver:{
                       get: () => false
                     }
                   })
            }
        """)
    # await page.waitFor(0.5*1000)
    await browser.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())



