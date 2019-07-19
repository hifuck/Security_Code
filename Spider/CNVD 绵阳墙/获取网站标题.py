# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import requests
import random
import time
import re

def scan(page):
    headers = {

        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': '__jsluid=052b5efa7852f0c4337ff90955b01439; bdshare_firstime=1554778788412; JSESSIONID=BDE44AF34847DB89F1EACBC05D9B171B',
        'Host': 'www.cnvd.org.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    url = 'http://www.cnvd.org.cn/sheepWall/list?max=100&offset={}00'.format(page)
    print('正在爬行第 {} 页....'.format(page))
    try:
        time.sleep(random.randint(1,5))
        r = requests.get(url, headers=headers)
        result = re.findall('<td width="30%">(.*?)</td>', r.text, re.S)
        print('获取到 {} 条数据'.format(len(result)))
        with open('title_result.txt','a+',encoding='utf-8')as a:
            for x in result:
                a.write(x.strip().lstrip()+'\n')
    except Exception as e:
        print(e)
        scan(page)
if __name__ == '__main__':
    for i in range(1,129):
        scan(i)