import os
from sqlalchemy import create_engine
import pandas as pd
import requests
from ZhihuReply.header import gen_header
import re

cur_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(cur_dir,"Data","Cookies","cookies.db")
engine = create_engine(r'sqlite:///{}'.format(file_path))

def get_d_c0(cookie):

    if "d_c0" in cookie:
        kv_list = cookie.split(";")
        for kv in kv_list:
            while "d_c0" in kv:
                d_c0 = re.search('d_c0=(.*)', kv)
                d_c0 = d_c0.group()[len('d_c0='):]
                return d_c0
    else:
        return None


def valid_check(d_c0):

    url_part = "/api/v5.1/topics/19566933/feeds/essence?offset=0&limit=10&include=data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content"
    headers = gen_header(url_part=url_part, d_c0=d_c0)

    session = requests.Session()
    content = session.get(url='https://www.zhihu.com{}'.format(url_part), headers=headers, timeout=1).json()

    if content['data']:
        return d_c0
    else:
        return None


def cookie(type='cookie'):

    if type not in ["cookie","d_c0"]:
        raise KeyError('''Only support type "cookie" or "d_c0"''')

    cookies = pd.read_sql('Cookies',con=engine, index_col='Agent')

    cookies['d_c0'] = cookies['Cookie'].apply(get_d_c0)
    cookies.dropna(inplace=True)

    cookies['d_c0'].apply(valid_check)
    cookies.dropna(inplace=True)

    if type=='cookie':
       return cookies['Cookie'].to_list()
    elif type=='d_c0':
       return cookies['d_c0'].to_list()

# print(cookie("cookie"))
# print(cookie("d_c0"))
# cookie("aaa")
