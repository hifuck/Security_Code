# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import requests
import re
from urllib.parse import quote,urlparse
import time
import random
requests.packages.urllib3.disable_warnings()

def scan(keywords):
    result = []
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'BAIDUID=832CF61CDAEF34C68E7CA06F591DF82A:FG=1; BIDUPSID=832CF61CDAEF34C68E7CA06F591DF82A; PSTM=1544962484; BD_UPN=12314753; BDUSS=RWclRJUURtR25qZWxKZWZiN0JuSlJVTWpKRjhvb3ROdmIyNnB0eEwwY2FVOWxjSVFBQUFBJCQAAAAAAAAAAAEAAADS9fNj0-~PxM600esAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABrGsVwaxrFcck; cflag=13%3A3; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_HOME=1; delPer=0; BD_CK_SAM=1; H_PS_PSSID=1453_21088_20692_28774_28720_28832_28584; H_PS_645EC=125f66QaihdIvZJvkmYPd0RImJRfs4IXMEEUGyyaloCjY4d%2Bddrdc9x%2BWSVH22EqgFo7; PSINO=2; sug=3; sugstore=1; ORIGIN=2; bdime=0; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; BDSVRTM=39',
        'Host': 'www.baidu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

    }
    for page in range(0,20,10):
        #time.sleep(random.randint(1,5))
        # only need 5 pages
        url = 'https://www.baidu.com/s?wd={}&pn={}'.format(quote(keywords),page)
        time.sleep(random.randint(1,4))
        try:
            r = requests.get(url,headers=headers,timeout=10,verify=False)
            subdomain = re.findall(b'style="text-decoration:none;">(.*?)/.*?class="c-tools',r.content)
            for x in subdomain:
                if len(x) >6 and x.count(b'..') ==0 and b'>' not in x:
                    if b'http' in x :
                        result.append(x.decode())
                    else:
                        result.append('http://'+x.decode())
        except Exception as e:
            print(e)
    res = (list(set(result)))
    print('关键词:{} 获取到网页 : {} 个'.format(keywords,len(res)))
    with open('url.txt','a+',encoding='utf-8')as a:
        for x in res:
            a.write(x+'\n')
    if res == []:
        with open('获取失败.txt', 'a+', encoding='utf-8')as a:
            a.write(keywords + '\n')

if __name__ == '__main__':
    print('批量获取关键词网址')
    urls = input('INPUT YOUR URLS.TXT:')
    urls = list(set([x.strip() for x in open(urls,'r',encoding='utf-8').readlines()]))
    for u in urls:
        scan(u)
