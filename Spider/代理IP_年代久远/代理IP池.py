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
import re
import requests
import time
import threading
import os
reload(sys)
sys.setdefaultencoding('utf-8')
print '''
                       
        |    __   __   __  
        |_, (__( |  ) (__| 
                       __/ 

'''
time.sleep(3)
try:
    os.remove('ips.txt')
except:
    pass
starttime = time.time()
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
YE_shu1 = input(unicode('请设置爬行页数(建议不超过100):','utf-8').encode('gbk'))
YE_shu = int(YE_shu1)
def caiji1():
    print unicode('\n***第一个节点已激活***\n', 'utf-8')
    url_1 = 'http://www.66ip.cn/mo.php?sxb=&tqsl=30&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea='
    for i in range(1,YE_shu):
        print unicode('\n[-]正在爬行 第一节点 第%d页...','utf-8')%i
        try:
            req = requests.get(url=url_1,headers=headers,timeout=5)
            r1 = re.findall('		(.*?)<br />',req.content)
            os.system('color a')
            for x in r1:
                print x
                with open('ips.txt','a+')as f:
                    f.write(x + '\n')
            time.sleep(3)
        except Exception,e:
            print e
#caiji1()

def caiji2():
    print unicode('\n***第二个节点已激活***\n', 'utf-8')
    for i in range(1, YE_shu):
        print unicode('\n[-]正在爬行 第二节点 第%d页...','utf-8')%i
        url_2 = r'http://www.xicidaili.com/nn/%s'%i
        try:
            req = requests.get(url=url_2, headers=headers,timeout=5)
            r1 = re.findall('/></td>(.*?)<a href',req.content,re.S)
            os.system('color b')
            for r2 in r1:
                r3 = r2.replace('\n','').replace('<td>','').replace("</td>",':').replace('      ','').replace(':  ','')
                print r3
                with open('ips.txt', 'a+')as f:
                    f.write(r3 + '\n')
        except Exception,e:
            print e
#caiji2()

def caiji3():
    print unicode('\n***第三个节点已激活***\n', 'utf-8')
    for i in range(1, YE_shu):
        print unicode('\n[-]正在爬行 第三节点 第%d页...','utf-8')%i
        url_3 = 'http://www.kuaidaili.com/free/inha/%s'%i
        try:
            req = requests.get(url=url_3, headers=headers,timeout=5)
            r1 = re.findall('<td data-title="IP"(.*?)</tr>',req.content,re.S)
            os.system('color c')
            for xx in r1:
                c1 = xx.replace('>','').replace('                    <td data-title="PORT"','').replace('</td','').replace('\n',':').split(':                    ',1)[0]
                print c1
                with open('ips.txt','a+')as f:
                    f.write(c1 + '\n')
        except Exception,e:
            print e

#caiji3()
threads = []
t1 = threading.Thread(target=caiji1)
t2 = threading.Thread(target=caiji2)
t3 = threading.Thread(target=caiji3)
threads.append(t1)
threads.append(t3)
threads.append(t2)
for x in threads:
    x.start()
    x.join()
print 'Time:%d S'% (time.time()-starttime) + '\n'
print unicode('代理IP采集完毕,开始代理IP存活检测.....','utf-8')
time.sleep(6)

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
def bendi(xx):
    print '\nCheaking>>>' + xx
    proxies = {}
    proxies['http'] = 'http://' + str(xx)
    #print proxies
    try:
        req2 = requests.get(url='http://blog.csdn.net/lzy98', proxies=proxies, headers=headers, timeout=5)
        #print req2.content.decode("utf8", "ignore").encode("gbk", "ignore")
        if 'One puls' in req2.content:
            print unicode('该代理可正常访问网页,正在保存到本地...','utf-8')
            with open('result.txt','a+')as f:
                f.write(str(xx) + '\n')
                return ''
        else:
            print unicode('该代理无法访问网页,继续验证下一代理...', 'utf-8')
        tt = req2.headers
        tt1  =  req2.status_code
        with open('log.txt','a+')as f8:
            f8.write(tt + str(tt1) + '\n')
    except :
        print unicode('无法连接到代理服务器','utf-8')

def wangluo(xx):
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
    print '\nCheaking>>>' + str(xx)
    try:
        req = requests.post(url = 'http://www.66ip.cn/yz/post.php',headers=headers,data = 'ipadd=' + str(xx),timeout=5)
        #print req.status_code
        #print req.headers
        print req.content.decode("utf8", "ignore").encode("gbk", "ignore")
        tt = str(req.content.decode("utf8", "ignore").encode("gbk", "ignore"))
        if '/' in tt:
            with open('result.txt','a+')as f:
                f.write(str(xx) + '\n')
        with open('log.txt','a+')as f8:
            f8.write(tt + '\n')
    except :
        print unicode('连接网络验证接口失败','utf-8')
for xx in list1:
    bendi(xx)
    wangluo(xx)
