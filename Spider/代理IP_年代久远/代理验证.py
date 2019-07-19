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
import sys
import os
import requests
import re
import time
import threadpool
reload(sys)
sys.setdefaultencoding('utf-8')
print '''

        |    __   __   __  
        |_, (__( |  ) (__| 
                       __/ 

'''
time.sleep(3)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
yzurl = 'http://blog.csdn.net/lzy98'
try:
    req = requests.get(url=yzurl,headers=headers)
    if 'One puls' in req.content:
        print unicode('开始代理IP存存活验证...')
    else:
        print req.status_code
except Exception,e:
    print e


YE_shu1 = input(unicode('设置验证方式1/0(1:本地访问验证[取决网速] 0:网络接口验证[有误报]):','utf-8').encode('gbk'))
YE_shu = int(YE_shu1)
list1 = []
with open('ips.txt') as f:
    for x in f:
        x = x.replace('\n','')
        list1.append(x)
f = open('ips.txt')
f1 = f.readlines()
f.close()
hangshu = len(f1)
print unicode('等待存活验证代理IP总数:','utf-8') + str(hangshu)


def bendi():
    for url in list1:
        print '\nCheaking>>>' + url
        proxies = {}
        proxies['http'] = 'http://' + str(url)
        #print proxies
        try:
            req2 = requests.get(url='http://blog.csdn.net/lzy98', proxies=proxies, headers=headers, timeout=5)
            #print req2.content.decode("utf8", "ignore").encode("gbk", "ignore")
            if 'One puls' in req2.content:
                print unicode('该代理可正常访问网页,正在保存到本地...','utf-8')
                with open('result.txt','a+')as f:
                    f.write(str(url) + '\n')
            else:
                print unicode('该代理无法访问网页,继续验证下一代理...', 'utf-8')
            tt = req2.headers
            tt1  =  req2.status_code
            with open('log.txt','a+')as f8:
                f8.write(tt + str(tt1) + '\n')
        except :
            print unicode('无法连接到代理服务器','utf-8')


def wangluo():
    headers={
        'Host': 'www.66ip.cn',
        'Content-Length': '24',
        'Accept': '*/*',
        'Origin': 'http://www.66ip.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://www.66ip.cn/yz/',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': '__jsluid=a437846badc1becdf40e5029827e6f34; UM_distinctid=1602aaac372179-0e64bb3308315c-5d4e211f-1fa400-1602aaac373185; CNZZDATA1253901093=1797993904-1512540810-null%7C1512567916; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1512544322,1512544748,1512559273,1512559573; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1512572148',
        'Connection': 'keep - alive'}
    for url in list1:
        print '\nCheaking>>>' + str(url)
        try:
            req = requests.post(url = 'http://www.66ip.cn/yz/post.php',headers=headers,data = 'ipadd=' + str(url),timeout=5)
            #print req.status_code
            #print req.headers
            print req.content.decode("utf8", "ignore").encode("gbk", "ignore")
            tt = str(req.content.decode("utf8", "ignore").encode("gbk", "ignore"))
            if '/' in tt:
                with open('result.txt','a+')as f:
                    f.write(str(url) + '\n')
            with open('log.txt','a+')as f8:
                f8.write(tt + '\n')
        except :
            print unicode('连接网络验证接口失败','utf-8')



if YE_shu == 1:
    os.system('color a')
    # pool = threadpool.ThreadPool(set_thread)
    # requests = threadpool.makeRequests(bendi,list1)
    # [pool.putRequest(req1) for req1 in requests]
    # pool.wait()
    bendi()
else:
      pass


if YE_shu == 0:
    os.system('color e')
    # set_thread1 = input(unicode('设置线程数量(没意义，太大了接口堵死，设置1完全OJ8K):', 'utf-8').encode('gbk'))
    # set_thread = int(set_thread1)
    # pool = threadpool.ThreadPool(set_thread)
    # requests = threadpool.makeRequests(wangluo,list1)
    # [pool.putRequest(req) for req in requests]
    # pool.wait()
    wangluo()
else:
    pass

os.system('pause')
