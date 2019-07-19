# -*- coding: utf-8 -*-
# @Time    : 2018/5/6 0006 9:55
# @Author  : Langzi
# @Blog    : www.langzi.fun
# @File    : zhengze test.py
# @Software: PyCharm
import sys
import re
import chardet
import requests
reload(sys)
sys.setdefaultencoding('utf-8')
url ='https://dns.aizhan.com/1.13.67.141/'
p = requests.get(url=url,timeout=20).content
if isinstance(p, unicode):
    pass
else:
    codesty = chardet.detect(p)
    a = p.decode(codesty['encoding'])
    z = re.findall('<strong>(.*?)</strong', a, re.S)
    for x in z:print x