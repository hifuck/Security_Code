# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import requests
import re
import time
import random

url = 'http://www.yunsee.cn/home/getInfo'

data = {
'type': 'webinfo',
'string': 'd879af672g54df45',
'url': 'www.jd.com/',
'_token': 'OeBAPzNTt4rEwiVj1nKBpVbstLVjnUr43j1eFwT9'
}

headers = {
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7',
'Connection': 'keep-alive',
'Content-Length': '117',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Cookie': '__cfduid=ddde54d9fc0df55cab8f9b6983db13add1554878797; yjs_id=54b5fe5840365503f65dea7d1e08ad5a; ctrl_time=1; Hm_lvt_020d18ec72d744884bf6b81cc118775b=1555143391,1555149604,1555395995,1555399505; laravel_session=eyJpdiI6InNjeFRDXC96ZnVMd0t2K0JpaVFqalhBPT0iLCJ2YWx1ZSI6Img2QXVmaWQyeEoycXE4K043TGVySHlFTEdKRGc1UkxjTzBUNnRwcDlzYVBaZGYwMlZiRnpIUlEyMTZwUmJ6clNhOTRrb3l6RFhRNXBOXC9BVm5NcGhoQT09IiwibWFjIjoiMDJhYjI4YzhiYTI3M2UzYWMxOTVmYjY0YTg5YjRkOTVkYWEwYWMxMjlhY2MxOTY5YTgwYTNjOTYzNzJmOGExYSJ9; Hm_lpvt_020d18ec72d744884bf6b81cc118775b=1555399506',
'Host': 'www.yunsee.cn',
'Origin': 'http://www.yunsee.cn',
'Referer': 'http://www.yunsee.cn/info.html',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'
}

proxy = {'http':'117.191.11.80:80'}
r = requests.post(url,headers=headers,data=data,proxies=proxy)

#datas = {'code': 1, 'mess': 'success', 'res': {'idc': '北京市 青云电信节点', 'ip': '139.199.94.136', 'os': 'Windows', 'whois_date': '2021-11-09 15:51:47', 'cms': '', 'whois_isp': 'Bizcn.com,Inc.', 'language': 'ASP.NET', 'cdn': '', 'icp_id': '宁ICP备11000933号', 'waf': '', 'whois_name': 'YinChuan QianHuiXinXiJiShuYouXianGongSi', 'title': '【官网推荐 年终盛典】宁夏枸杞网-中宁枸杞-青海黑枸杞直销官方网站-宁夏枸杞直销网-高品质纯天然正宗中宁枸杞', 'icp_name': '银川千回信息技术有限公司', 'parse': 0, 'fingers': {'front': [{'name': 'jQuery', 'desc': 'https://jquery.com', 'version': '1.7.2'}], 'frame': [{'name': 'Microsoft ASP.NET', 'desc': '基于.NET Framework的Web开发平台', 'version': ''}], 'language': [{'name': 'PHP', 'desc': 'http://php.net', 'version': ''}], 'server': [{'name': 'IIS', 'desc': 'http://www.iis.net', 'version': '8.5'}], 'id': [121, 131, 908, 7958]}, 'status_code': 200, 'whois_mail': 'abuse@bizcn.com', 'server': 'Microsoft-IIS/8.5', 'whois_dns': 'ns10.cdncenter.com,ns11.cdncenter.com,ns8.cdncenter.com,ns7.cdncenter.com,ns9.cdncenter.com,ns12.cdncenter.com', 'create': '2019-04-16 15:34:37', 'record_id': 175630}}
datas = r.json()
print(datas.get('mess'))
datass = (datas.get('res'))

ip = datass.get('ip')
address = datass.get('idc')
os = datass.get('os')
wcm = datass.get('cms')
for x,y in datass.items():
    print(x,':',y)