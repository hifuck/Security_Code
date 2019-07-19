# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun

import requests
requests.packages.urllib3.disable_warnings()
from urllib.parse import urlparse

from concurrent.futures import ThreadPoolExecutor
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

def run(url):
    try:
        r = requests.get('http://'+url,headers=headers,timeout=5,verify=False)
        print('Scan:{} Code:{}'.format(r.url,r.status_code))
        if r.status_code == 200:
            u = urlparse(r.url)
            with open('alive_url.txt','a+',encoding='utf-8')as a:
                a.write(u.scheme+'://'+u.netloc+'\n')
            return 'Scan over~'
    except:
        pass
    try:
        r = requests.get('https://'+url,headers=headers,timeout=5,verify=False)
        print('Scan:{} Code:{}'.format(r.url,r.status_code))
        if r.status_code == 200:
            u = urlparse(r.url)
            with open('alive_url.txt','a+',encoding='utf-8')as a:
                a.write(u.scheme+'://'+u.netloc+'\n')
            return 'Scan over~'
    except:
        pass

if __name__ == '__main__':
    urls = list(set([x.strip() for x in open('url.txt','r',encoding='utf-8').readlines()]))
    print('总行数:{}'.format(len(urls)))
    with ThreadPoolExecutor(300) as p:
        p.map(run,urls)
    print('扫描结束~，开始去重')
    urlss = list(set([x.strip() for x in open('alive_url.txt','r',encoding='utf-8').readlines()]))
    with open('result.txt','a+',encoding='utf-8')as a:
        for z in urlss:
            a.write(z+'\n')