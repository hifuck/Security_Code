# coding:utf-8

import re
import os
import requests
from bs4 import BeautifulSoup as bs
import chardet
import random
import hashlib
import socket
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 3

requests.packages.urllib3.disable_warnings()


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


class Get_Info:
    def __init__(self, url):
        self.url = url

    def get_ip(self):
        hostname = self.url.replace('http://', '').replace('https://', '').replace('/', '')
        url_ip = 'None'
        try:
            url_ip = socket.gethostbyname(str(hostname))
        except:
            pass
        return url_ip

    def get_infos(self):
        try:
            UA = random.choice(headerss)
            headers = {'User-Agent': UA}
            r = requests.get(url=self.url, headers=headers, verify=False, timeout=5)
            url_title, url_content, url_service = None,None,None
            try:
                code = chardet.detect(r.content)['encoding']
                bp = bs(r.content.decode(code).encode('utf-8'), 'html.parser')
                url_title = bp.title.string
                # url_contents = bp.text
                try:
                    url_service = r.headers['Server']
                except:
                    url_service = None
            except:
                url_title = re.search('<title>(.*?)</title>', r.content, re.I).group(1).decode(code).encode('utf-8')
                # url_content = re.sub('([\.\?\*~!@#{$%\^&\*()-;"<>\[\]}_\+=]|[0-9]|[a-z]|[A-Z])','',r.text)
                try:
                    url_service = r.headers['Server']
                except:
                    url_service = None
            infos = {}
            infos['url'] = self.url
            infos['title'] = url_title
            url_contents = ''.join(r.text.split()).replace(' ', '').replace('\r\n', '').replace('\r', '')
            infos['content'] = re.sub('([\.\?\*~!@#{$%\^&\*()-;"<>\[\]}_\+=])', '', url_contents).replace('|',
                                                                                                          '').replace(
                "'", '')
            # 下面这行的代码会过滤掉所有的英文和数字
            # infos['content'] = re.sub('([\.\?\*~!@#{$%\^&\*()-;"<>\[\]}_\+=]|[0-9]|[a-z]|[A-Z])','',url_contents).replace('|','').replace("'",'')
            infos['service'] = url_service
            if infos:
                return infos
            else:
                infos = {}
                infos['url'] = self.url
                infos['title'] = None
                infos['content'] = None
                infos['service'] = None
                return infos
        except Exception, e:
            # print e
            infos = {}
            infos['url'] = self.url
            infos['title'] = None
            infos['content'] = None
            infos['service'] = None
            return infos

        '''

        返回内容如下：
        {
        'url':'http://www.langzi.fun',
        'title':'浪子博客'，
        'content':'xaffa网页内容xafgasdas',
        'service':'Apache'
        }

        '''

    def get_urls(self):
        urlss = []
        live_urls = []
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        try:
            r = requests.get(url=self.url, headers=headers, verify=False, timeout=5)
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                 re.I)
            urls = re.findall(pattern, r.content)
            for x in urls:
                a1, a2 = x.split('//')[0], x.split('//')[1].split('/')[0]
                a3 = ''.join(a1) + '//' + ''.join(a2)
                urlss.append(a3.replace("'", "").replace('>', '').replace('<', ''))
            if urlss:
                for _ in list(set(urlss)):
                    UA = random.choice(headerss)
                    headers = {'User-Agent': UA}
                    try:
                        rr = requests.head(url=_, headers=headers, timeout=5, verify=False)
                        if rr.status_code == 200:
                            live_urls.append(_)
                        else:
                            pass
                    except:
                        pass
                return live_urls
            else:
                return None
        except Exception, e:
            print e

