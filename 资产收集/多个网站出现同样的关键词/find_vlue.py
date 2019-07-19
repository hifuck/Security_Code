# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 0023 13:17
# @Author  : Langzi
# @Blog    : www.langzi.fun
# @File    : find_vlue.py
# @Software: PyCharm
import sys
import jieba
import random
import requests
from collections import Counter
from prettytable import PrettyTable
import time
import os
reload(sys)
sys.setdefaultencoding('utf-8')
print '''

|    __   __   __  
|_, (__( |  ) (__| 
               __/ 

'''
time.sleep(5)
headerss = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
ll = []
def scan(url):
    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        r = requests.get(url=url, headers=headers, timeout=5).content.decode("utf8","ignore").encode("gbk","ignore")
        for x in jieba.cut_for_search(r,HMM=True):
            ll.append(x)
    except Exception, e:
        print e
url_input = raw_input(unicode('请输入需要扫描的网址文本:','utf-8').encode('gbk'))
list_url = list(set([i.replace('\n','') for i in open(url_input,'r').readlines()]))
for url in list_url:
    print 'Scan: '+(url)
    scan(url)
d=dict(Counter(ll))
d1 = dict(sorted(zip(d.values(),d.keys())))
x = PrettyTable(["出现次数", "元素"])
for k,v in d1.iteritems():
    x.add_row([k, v])
with open ('result.txt','a+')as a:
    a.write(str(x))
print x
time.sleep(10)
def get(data_str):
    try:
        for xx in list_url:
            print 'Scan:' + xx
            UA = random.choice(headerss)
            headers = {'User-Agent': UA}
            r1 = requests.get(url=xx, headers=headers, timeout=5).content.decode("utf8","ignore").encode("gbk","ignore")
            if data_str in r1:
                with open(str(data_str+'.txt'),'a+')as aa:
                    aa.write(xx+'\n')
    except Exception,e:
        print e
while 1:
    data_str=raw_input(unicode('请输入需要寻找所在网站的关键词:','utf-8').encode('gbk'))
    get(data_str)
    print unicode('当前关键词扫描完毕....','utf-8')
    time.sleep(10)