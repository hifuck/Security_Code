# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 0023 13:54
# @Author  : Langzi
# @Blog    : www.langzi.fun
# @File    : 权重.py
# @Software: PyCharm
import sys
import re
import requests
import time
reload(sys)
sys.setdefaultencoding('utf-8')
urlx = 'http://top.chinaz.com/all/index_%d.html'
def scan(urlx):
    for x in range(2,1888):
        url = urlx%x
        print url
        try:
            r = requests.get(url=url,timeout=8).content
            try:
                rr = re.findall('class="col-gray">(.*?)</span>',r)
                for x in rr:
                    if not '-' in x:
                        with open('result.txt','a+')as a:
                            a.write(str('http://'+x+'\n'))
            except Exception,e:
                print e
        except Exception,e:
            print e
scan(urlx)