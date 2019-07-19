# -*- coding: utf-8 -*-
import re
import requests
import time
from multiprocessing.dummy import Pool as tpl
import random
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
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24" ]

print ('''

         _                           _ 
        | |                         (_)
        | |     __ _ _ __   __ _ _____ 
        | |    / _` | '_ \ / _` |_  / |
        | |___| (_| | | | | (_| |/ /| |
        |______\__,_|_| |_|\__, /___|_|
                            __/ |      Langzi_URL-IP-URL
                           |___/       Version:1.0
                                       Datetime:2017-10-11-13:05:36
                                       WEB_API:www.webscan.cc

''')

result_dir = str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())).replace(' ', '')
import os
os.mkdir(result_dir)
def success_url_ip(result_dir,url,ip):
    with open(str(result_dir + '/' + 'result.txt'),'a+')as a:
        a.write(ip + '\n')
    with open(str(result_dir + '/' + 'log.txt'),'a+')as a:
        a.write(url + ':' + str(ip) + '\n')


def url_ip(url):
    urls = 'http://www.webscan.cc/?action=getip&domain='+url
    print 'Search IP From URL : ' + url
    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        res = requests.get(url=urls,headers=headers,timeout=5)
        rr = re.findall('{"ip":"(.*?)",',res.content)
        ip = str(rr).replace("'",'').replace('[','').replace(']','')
        if ip != '' and ip != None and ip != 'Error':
            print 'Success Found IP : ' + str(ip)
            success_url_ip(result_dir,url,ip)
    except Exception,e:
        print e

def ip_url(ip):
    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        urls = 'http://www.webscan.cc/?action=query&ip='+str(ip)
        print 'Search URL From IP : ' + str(ip)
        result = requests.get(url=urls,headers=headers,timeout=5)
        r = re.findall('domain":"(.*?)",',result.content)
        for x in r:
            xx = x.replace('\\','')
            if xx != '' and xx != None and xx != 'Error':
                print 'Success Found URL : ' + xx
                success_url_ip(result_dir,ip,xx)
    except Exception,e:
        print e

print '\n'

print unicode('批量IP转换成URL输入: 0   批量URL转换成IP输入: 1 ', 'utf-8')
time.sleep(3)
print '\n'
setstart = raw_input(unicode('请选择启动方式(选项:0/1):', 'utf-8').encode('gbk'))
print '\n'
urltxt = raw_input(unicode('输入网址文本名(可拖拽进来) : ', 'utf-8').encode('gbk'))
urllist = list(set([x.replace('\n', '') for x in open(urltxt, 'r').readlines()]))

# 单线程
for x in urllist:
    if int(setstart) == 0:
        ip_url(x)
    else:
        url_ip(x)
print unicode('转换完成','utf-8')

# 多线程
# if int(setstart) == 0:
#     tp = tpl(processes=8)
#     tp.map(ip_url,urllist)
#     tp.close()
#     tp.join()
# else:
#     tp = tpl(processes=8)
#     tp.map(url_ip,urllist)
#     tp.close()
#     tp.join()

os.system('pause')
