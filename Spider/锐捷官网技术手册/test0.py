# -*- coding:utf-8 -*-
# __author__:langzi
# __blog__:www.langzi.fun
import requests
import re
import time
import random
import json
headers = {
'Access-Control-Allow-Origin':'*',
'Cache-Control':'private',
'Connection':'keep-alive',
'Content-Encoding':'gzip',
'Content-Type':'application/json; charset=utf-8',
'Date':'Thu, 11 Apr 2019 12:38:45 GMT',
'Server':'marco/2.9',
'Set-Cookie':'27ac707d740f3c591d65c003c315b7f9_70DF3AF92DC77C4E4C1E2415F3185179=; domain=.ruijie.com.cn; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'ruijie_user_name=; domain=.ruijie.com.cn; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'ruijie_user_type=; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'UserCenter=; domain=.ruijie.com.cn; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'ruijieportal=; domain=.ruijie.com.cn; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'PartnerUser=; domain=.ruijie.com.cn; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'_nc=; domain=.ruijie.com.cn; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'27ac707d740f3c591d65c003c315b7f9_70DF3AF92DC77C4E4C1E2415F3185179=; domain=.ruijie.com.cn; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'ruijie_user_name=; domain=.ruijie.com.cn; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'ruijie_user_type=; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'UserCenter=; domain=.ruijie.com.cn; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'ruijieportal=; domain=.ruijie.com.cn; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'PartnerUser=; domain=.ruijie.com.cn; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Set-Cookie':'_nc=; domain=.ruijie.com.cn; expires=Wed, 10-Apr-2019 12:38:45 GMT; path=/',
'Content-Encoding': 'gzip',
'Vary':'Accept-Encoding',
'Via':'S.mix-js-czx-100, T.101.-, V.mix-js-czx-106, T.71.-, M.cun-js-nkg-075',
'X-Aspnet-Version':'4.0.30319',
'X-Aspnetmvc-Version':'5.2',
'X-Powered-By':'ASP.NET',
'X-Request-Id':'bfd9d6241d23596b3e79c3a97eea02e7',
'X-Source':'C/200',
}

data = {'interface': '/search/document',

'data': '{"KeyWord":"出口网关","PageIndex":1,"PageSize":10}'

}
url = 'http://www.ruijie.com.cn/Application/HttpForward/API?1554986323496'

#r=requests.post(url=url,data=data)

#res = r.json()
# res = {'Count': 361, 'TotalPages': 37, 'Data': [{'ID': 39241, 'Name': 'RG-EG系列<font color="red">出口</font><font color="red">网关</font>硬件安装手册(V1.43)', 'SeoDescription': 'RG-EG系列出口网关硬件安装手册（V1.43）;锐捷网络;EG;出口网关;硬件安装手册', 'PDF': '', 'UNIID': 'f28e8d67-51c6-4f37-a93a-7eac807b52b5', 'Url': '/fw/wd/39241', 'VisitLevel': '', 'Order': 12255, 'Date': '2017-03-21', 'CreateTime': '2014-10-31', 'Recommond': False}, {'ID': 37034, 'Name': 'RG-EG系列<font color="red">出口</font><font color="red">网关</font>RGOS 10.3(4b11)版本命令手册(V3.0)', 'SeoDescription': 'RG-EG系列出口网关RGOS 10.3（4b11）版本命令手册（V3.0）;EG系列;出口网关;10.3（4b11）;命令手册;锐捷网络', 'PDF': '', 'UNIID': '28f751a7-5d63-4bc2-a44c-155710397b3a', 'Url': '/fw/wd/37034', 'VisitLevel': '', 'Order': 12211, 'Date': '2013-12-05', 'CreateTime': '2013-12-05', 'Recommond': False}, {'ID': 37033, 'Name': 'RG-EG系列<font color="red">出口</font><font color="red">网关</font>RGOS 10.3(4b11)版本配置手册(V3.0)', 'SeoDescription': 'RG-EG系列出口网关RGOS 10.3（4b11）版本配置手册（V3.0）;EG系列;出口网关;10.3（4b11）;配置手册;锐捷网络', 'PDF': '', 'UNIID': '664673e4-d7dd-432d-ae23-ff0aa0f1d4b7', 'Url': '/fw/wd/37033', 'VisitLevel': '', 'Order': 12211, 'Date': '2013-12-05', 'CreateTime': '2013-12-05', 'Recommond': False}, {'ID': 37172, 'Name': 'RG-EG系列<font color="red">出口</font><font color="red">网关</font>RGOS 10.3(4b11)版本WEB管理手册(V3.0)', 'SeoDescription': 'RG-EG系列出口网关RGOS 10.3(4b11)版本WEB管理手册(V3.0);EG;出口网关;10.3(4b11);WEB管理手册', 'PDF': '', 'UNIID': '9b9a55d9-dc0a-485f-95a6-28d457f1b059', 'Url': '/fw/wd/37172', 'VisitLevel': '', 'Order': 12207, 'Date': '2014-02-11', 'CreateTime': '2014-02-20', 'Recommond': False}, {'ID': 37169, 'Name': 'RG-EG系列<font color="red">出口</font><font color="red">网关</font>RGOS 10.3(4b11)版本配置手册(V4.0)', 'SeoDescription': 'RG-EG系列出口网关RGOS 10.3(4b11)版本配置手册(V4.0);锐捷网络;EG;出口网关;10.3(4b11);配置手册', 'PDF': '', 'UNIID': '0c9ecfed-8899-465b-9f62-30c013c185a9', 'Url': '/fw/wd/37169', 'VisitLevel': '', 'Order': 12199, 'Date': '2014-02-11', 'CreateTime': '2014-02-20', 'Recommond': False}, {'ID': 37168, 'Name': 'RG-EG系列<font color="red">出口</font><font color="red">网关</font>RGOS 10.3(4b11)版本命令手册(V4.0)', 'SeoDescription': 'RG-EG系列出口网关RGOS 10.3(4b11)版本命令手册(V4.0);锐捷网络;EG;出口网关;10.3(4b11);命令手册', 'PDF': '', 'UNIID': '9967a3af-5248-4e27-9532-dd4bf7e99280', 'Url': '/fw/wd/37168', 'VisitLevel': '', 'Order': 12199, 'Date': '2014-02-11', 'CreateTime': '2014-02-20', 'Recommond': False}, {'ID': 39245, 'Name': 'RG-EG系列<font color="red">出口</font><font color="red">网关</font>RGOS 10.3(4b11)p4版本配置手册(V1.0)', 'SeoDescription': 'RG-EG系列出口网关RGOS 10.3(4b11)p4版本配置手册(V1.0);锐捷网络;EG;出口网关;10.3(4b11)p4;配置手册', 'PDF': '', 'UNIID': '9d2c7d50-d87d-493e-8052-40b171eb7c3d', 'Url': '/fw/wd/39245', 'VisitLevel': '', 'Order': 12191, 'Date': '2014-10-31', 'CreateTime': '2014-10-31', 'Recommond': False}, {'ID': 39244, 'Name': 'RG-EG系列<font color="red">出口</font><font color="red">网关</font>RGOS 10.3(4b11)p4版本命令手册(V1.0)', 'SeoDescription': 'RG-EG系列出口网关RGOS 10.3(4b11)p4版本命令手册(V1.0);锐捷网络;EG;出口网关;10.3(4b11)p4;命令手册', 'PDF': '', 'UNIID': '3307c4bb-c964-41a6-8e87-123c015a3444', 'Url': '/fw/wd/39244', 'VisitLevel': '', 'Order': 12191, 'Date': '2014-10-31', 'CreateTime': '2014-10-31', 'Recommond': False}, {'ID': 39247, 'Name': 'RG-NBR系列<font color="red">出口</font><font color="red">网关</font>RGOS 10.3(4b11)p4版本WEB管理手册(V1.0)', 'SeoDescription': 'RG-NBR系列出口网关RGOS 10.3(4b11)p4版本WEB管理手册(V1.0);锐捷网络;出口网关;10.3(4b11)p4;WEB管理手册', 'PDF': '', 'UNIID': '7a0bed80-36cd-4884-87bb-aa8ce4946140', 'Url': '/fw/wd/39247', 'VisitLevel': '', 'Order': 12181, 'Date': '2014-10-31', 'CreateTime': '2014-10-31', 'Recommond': False}, {'ID': 39243, 'Name': 'RG-EG系列<font color="red">出口</font><font color="red">网关</font>RGOS 10.3(4b11)p4版本WEB管理手册(V1.0)', 'SeoDescription': 'RG-EG系列出口网关RGOS 10.3（4b11）p4版本WEB管理手册（V1.0）;锐捷网络;EG;出口网关;10.3（4b11）p4;WEB管理手册', 'PDF': '', 'UNIID': '1326737b-a085-4fc7-bda4-7e43a9add7e9', 'Url': '/fw/wd/39243', 'VisitLevel': '', 'Order': 12179, 'Date': '2014-10-31', 'CreateTime': '2014-10-31', 'Recommond': False}], 'Status': True, 'Code': None, 'Message': None, 'Other': None}
#
# print(res['Count'])
# print(res['TotalPages'])
# print(res['Status'])
#
# dd=(res['Data'])
# for x in dd:
#     print(x)
#     print(x.get('SeoDescription'))
#     print('http://www.ruijie.com.cn'+x.get('Url'))

down_url = 'http://www.ruijie.com.cn/application/Article/GetArticleFile?id=41098&attachmentNo=1&download=true'
r = requests.get(down_url,stream=True)
with open('a.pdf','wb')as a:
    for dataa in r.iter_content():
        a.write(dataa)