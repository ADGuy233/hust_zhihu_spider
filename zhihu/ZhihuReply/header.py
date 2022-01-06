import execjs
import os
import hashlib

def gen_header(url_part, d_c0='"AOCZbcULsRKPTmJKb9A50mFqiq7Neud6dsg=|1613898999"'):
    # 生成加密的明文
    f = "+".join(["101_3_2.0", url_part, d_c0])
    fmd5 = hashlib.new('md5', f.encode()).hexdigest()
    # 读取并运行用于加密的js脚本
    current_directory = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(current_directory, "spiders//x-zse-96//g_encrypt.js"), 'r') as f:
        ctx1 = execjs.compile(f.read(), cwd=os.path.join(current_directory, "spiders//x-zse-96"))
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