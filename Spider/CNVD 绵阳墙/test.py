# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import requests
import time
import re
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
url = 'http://www.cnvd.org.cn/sheepWall/list?max=100&offset=200'

r = requests.get(url,headers=headers)

result = re.findall('<td width="30%">(.*?)</td>',r.text,re.S)

for x in result:
    print(x.lstrip().strip())