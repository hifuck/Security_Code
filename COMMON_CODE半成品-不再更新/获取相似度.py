# -*- coding: utf-8 -*-

import difflib
import requests
url_0 = 'http://www.langzi.fun/56454'
url_1 = 'http://www.langzi.fun/admin/666'
url_2 = 'http://www.langzi.fun/'

def content(url):
    return requests.get(url).content
url_0_ = content(url_0)
url_1_ = content(url_1)
url_2_ = content(url_2)

print(difflib.SequenceMatcher(None, url_1_, url_0_).quick_ratio())
print(difflib.SequenceMatcher(None, url_1_, url_2_).quick_ratio())

# 这个数字方便做判断
didx = int(str(difflib.SequenceMatcher(None, url_0, url_1).quick_ratio() * 10000).split('.')[0])
print didx