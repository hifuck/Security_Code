# -*- coding: utf-8 -*-
"""
__author__ = 'Langziyanqin'
__QQ__ = '982722261'
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import re
import requests
import threading
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
def start():
    for i in range(1,100):
        url = 'https://www.siteinfourl.com/baidu_site?page=%d'%i
        req = requests.get(url=url,headers=headers,timeout=4)
        req1 = re.findall(b'="https://www.siteinfourl.com/site-info/(.*?)">',req.content)
        for xx in req1:
            print(xx)
            with open('result1111111.txt','a+')as f:
                f.write('http://' + xx + '\n')
t1 = threading.Thread(target=start)
t1.start()
