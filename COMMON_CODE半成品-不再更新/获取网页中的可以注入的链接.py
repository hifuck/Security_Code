# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import re
import subprocess
import time
import os
from docx import Document
from docx.shared import Pt
from docx.shared import RGBColor
from docx.oxml.ns import qn
import requests
requests.packages.urllib3.disable_warnings()
import multiprocessing
from bs4 import BeautifulSoup
from urllib.parse import urlparse,urljoin
import random
from concurrent.futures import ProcessPoolExecutor



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

def writedata(x):
    with open('log.txt', 'a+')as aa:
        aa.write('***********************************' + '\n')
        aa.write(str(time.strftime('%Y-%m-%d:%H:%M:%S   ', time.localtime())) + str(x) + '\n')


def get_links(url):
    '''
    需要的有常规的注入点
        1. category.php?id=17
        2. https://www.yamibuy.com/cn/brand.php?id=566
    伪静态
        1. info/1024/4857.htm
        2. http://news.hnu.edu.cn/zhyw/2017-11-11/19605.html
        3. http://www.labothery-tea.cn/chanpin/2018-07-12/4.html
    :param url:
    :return:
    '''
    # if 'gov.cn' in url or 'edu.cn' in url:
    #     #return 0
    #     pass
    domain = url.split('//')[1].strip('/').replace('www.', '')
    result = []
    id_links = []
    html_links = []
    result_links = {}
    idid = []
    htht = []
    try:
        headers = {
            'User-Agent': random.choice(headerss),
            'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
        }
        rxww = requests.get(url, headers=headers,verify=False, timeout=10)
        soup = BeautifulSoup(rxww.content, 'html.parser',from_encoding='iso-8859-1')


        links = soup.findAll('a')
        for link in links:
            _url = link.get('href')
            res = re.search('(javascript|:;|#|%)', str(_url))
            res1 = re.search('.(jpg|png|bmp|mp3|wma|wmv|gz|zip|rar|iso|pdf|txt)', str(_url))
            if res == None and res1 == None:
                result.append(str(_url))
            else:
                pass
        # print(result)
        # time.sleep(50)
        if result != []:
            rst = list(set(result))
            for rurl in rst:
                if '//' in rurl and 'http' in rurl and domain in rurl:
                    # http // domain 都在
                    # https://www.yamibuy.com/cn/search.php?tags=163
                    # http://news.hnu.edu.cn/zhyw/2017-11-11/19605.html
                        if '?' in rurl and '=' in rurl:
                            # result_links.append(rurl)
                            id_links.append(rurl.strip())
                        if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                            if '?' not in rurl:
                                # result_links.append(rurl)
                                html_links.append(rurl.strip())
                # //wmw.dbw.cn/system/2018/09/25/001298805.shtml
                if 'http' not in rurl and domain in rurl:
                    # http 不在    domain 在
                    if '?' in rurl and '=' in rurl:
                        id_links.append('http://' + rurl.lstrip('/').strip())
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        if '?' not in rurl:
                            html_links.append('http://' + rurl.lstrip('/').strip())

                # /chanpin/2018-07-12/3.html"
                if 'http' not in rurl and domain not in rurl:
                    # http 不在  domain 不在
                    if '?' in rurl and '=' in rurl:
                        id_links.append('http://' + domain.strip() + '/' + rurl.strip().lstrip('/'))
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        if '?' not in rurl:
                            html_links.append('http://' + domain.strip() + '/' + rurl.strip().lstrip('/'))

            # print(html_links)
            # print(id_links)
            #time.sleep(50)
            if len(html_links)>50:
                html_links=random.sample(html_links,20)
            if len(id_links)>50:
                id_links = random.sample(id_links,20)

            for x1 in html_links:
                try:
                    rx1 = requests.get(url=x1,headers=headers,verify=False, timeout=10)
                    if rx1.status_code == 200:
                        htht.append(x1)
                except Exception as e:
                    writedata('[WARNING ERROR]' + str(e))
                    pass
            for x2 in id_links:
                try:
                    rx2 = requests.get(url=x2,headers=headers,verify=False, timeout=10)
                    if rx2.status_code == 200:
                        idid.append(x2)
                        if rx2.url.find('=') > 0:
                            idid.append(rx2.url)

                except Exception as e:
                    writedata('[WARNING ERROR]' + str(e))
                    pass

            idid = list(set(idid))
            htht = list(set(htht))

            hthtx = []
            ididx = []
            dic_1 = []
            dic_2 = []
            dic_3 = []
            dic_4 = []
            for i in htht:
                path = urlparse(i).path
                if path.count('/') == 1:
                    dic_1.append(i.replace('.htm', '*.htm').replace('.shtm', '*.shtm'))
                if path.count('/') == 2:
                    dic_2.append(i.replace('.htm', '*.htm').replace('.shtm', '*.shtm'))
                if path.count('/') == 3:
                    dic_3.append(i.replace('.htm', '*.htm').replace('.shtm', '*.shtm'))
                if path.count('/') > 3:
                    dic_4.append(i.replace('.htm', '*.htm').replace('.shtm', '*.shtm'))
            if dic_1:
                hthtx.append(random.choice(dic_1))
                hthtx.append(random.choice(dic_1))
                #hthtx.append(random.choice(dic_1))
            if dic_2:
                hthtx.append(random.choice(dic_2))
                hthtx.append(random.choice(dic_2))
                #hthtx.append(random.choice(dic_2))
            if dic_3:
                hthtx.append(random.choice(dic_3))
                hthtx.append(random.choice(dic_3))
                #hthtx.append(random.choice(dic_3))
            if dic_4:
                hthtx.append(random.choice(dic_4))
                hthtx.append(random.choice(dic_4))
                #hthtx.append(random.choice(dic_4))
            dic_11 = []
            dic_21 = []
            dic_31 = []
            dic_41 = []
            for i in idid:
                path = urlparse(i).path
                if path.count('/') == 1:
                    dic_11.append(i.replace('&', '^&'))
                if path.count('/') == 2:
                    dic_21.append(i.replace('&', '^&'))
                if path.count('/') == 3:
                    dic_31.append(i.replace('&', '^&'))
                if path.count('/') > 3:
                    dic_41.append(i.replace('&', '^&'))
            if dic_11:
                ididx.append(random.choice(dic_11))
                ididx.append(random.choice(dic_11))
                #ididx.append(random.choice(dic_11))
            if dic_21:
                ididx.append(random.choice(dic_21))
                ididx.append(random.choice(dic_21))
                #ididx.append(random.choice(dic_21))
            if dic_31:
                ididx.append(random.choice(dic_31))
                ididx.append(random.choice(dic_31))
                #ididx.append(random.choice(dic_31))
            if dic_41:
                ididx.append(random.choice(dic_41))
                ididx.append(random.choice(dic_41))
                #ididx.append(random.choice(dic_41))

            if hthtx == []:
                pass
            else:
                result_links['html_links'] = list(set(hthtx))

            if ididx == []:
                pass
            else:
                result_links['id_links'] = list(set(ididx))

        # print(result_links['id_links'])
        # print(result_links['html_links'])
        with open('InjEction_links.txt','a+',encoding='utf-8')as a:
            if ididx:
                for i in list(set(ididx)):
                    a.write(i + '\n')
            if hthtx:
                for u in list(set(hthtx)):
                    a.write(u+'\n')

        if result_links == {}:
            return None
        else:
            return result_links

    except Exception as e:
        writedata('[WARNING ERROR]' + str(e))
        pass
    return None