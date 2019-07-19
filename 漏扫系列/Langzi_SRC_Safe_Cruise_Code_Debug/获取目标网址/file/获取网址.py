# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import os
import re
all_lists = []
for a,b,c in os.walk('.'):
    for i in c:
        all_lists.append(os.path.join(a,i))
        print(os.path.join(a,i))
    #print(os.path.join(a,b,c))
import requests
from concurrent.futures import ThreadPoolExecutor

all_urls = []
all_ips = []
for z in all_lists:
    try:
        urls = [x for x in open(z,'r',encoding='utf-8').readlines()]
        if '开放端口' in urls[0]:
            print('存在端口+域名')
            for i in urls[1:]:
                domain,ip = i.split('	')[0],i.split('	')[1]
                print('域名:'+domain)
                all_urls.append(domain)
                print('IP:'+ip)
                all_ips.append(ip)
        else:
            print('只存在域名')
            all_urls.extend(urls)
    except:
        pass

with open('url.txt','a+',encoding='utf-8')as a:
    for i in all_urls:
        a.write(i+'\n')

with open('ip.txt','a+',encoding='utf-8')as a:
    for i in all_ips:
        a.write(i+'\n')
