# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import requests
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote,urlparse

def scan(keywords):
    result = []
    if '//' in keywords:
        keywords = keywords.split('//')[1].replace('www.','')
    keywords=keywords.replace('www.','')
    domain = keywords.split('.')[0].encode()
    for page in range(0,100,10):
        url = 'https://www.baidu.com/s?wd=site%3A{}&pn={}'.format(quote(keywords),page)
        print(url)
        try:
            headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'BAIDUID=832CF61CDAEF34C68E7CA06F591DF82A:FG=1; BIDUPSID=832CF61CDAEF34C68E7CA06F591DF82A; PSTM=1544962484; BD_UPN=12314753; BDUSS=RWclRJUURtR25qZWxKZWZiN0JuSlJVTWpKRjhvb3ROdmIyNnB0eEwwY2FVOWxjSVFBQUFBJCQAAAAAAAAAAAEAAADS9fNj0-~PxM600esAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABrGsVwaxrFcck; cflag=13%3A3; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_HOME=1; delPer=0; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; H_PS_PSSID=1453_21088_20692_28774_28720_28558_28832_28584; B64_BOT=1; BD_CK_SAM=1; PSINO=1; sug=3; sugstore=1; ORIGIN=2; bdime=0; H_PS_645EC=87ecpN5CzJjR5UwprsIowJPhqh6m9t1xGvxRkjeNmvcXBhI86ytKIjXLMhQ',
            'Host': 'www.baidu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

            }
            r = requests.get(url,headers=headers,timeout=20)
            subdomain = re.findall(b'-decoration:none;">(.*?)/&nbsp',r.content)
            for x in subdomain:
                if domain in x:
                    if b'http' in x:
                        result.append(x.decode())
                    else:
                        result.append('http://'+x.decode())
                    print(x)
            subdomain = re.findall(b'style="text-decoration:none;">(.*?)/.*?class="c-tools',r.content)
            for x in subdomain:
                if domain in x:
                    if b'http' in x:
                        result.append(x.decode())
                    else:
                        result.append('http://'+x.decode())
                    print(x)

        except Exception as e:
            print(e)
    print(list(set(result)))

scan('www.baidu.com')
