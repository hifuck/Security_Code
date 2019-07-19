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



import urllib.parse,os.path,re
class filter_url:
    def __init__(self):
        self.list_url_static=[]
    def filter_url(self,url):
        url=urllib.parse.urlparse(url)
        if url.query!='':
            return (self.params_filter(url))
            pass
        elif url.query=='':
            self.static_filter(url)
        elif url.path=='':
            return (url)
    def static_filter(self,url):
        #伪静态与url路径处理
        urls=os.path.splitext(url.path)
        if urls[1]!='':
            list_url=[]
            for i in urls[0].split('/'):
                if i!='':list_url.append('{%s:%s}'%(self.judgetype(i),len(i)))
            url_path="/".join(list_url)
            return (url.scheme + '://' + url.netloc +'/'+ url_path + urls[1])
        else:
            list_url=[]
            for i in url.path.split('/'):
                if i!='':list_url.append('{%s:%s}'%(self.judgetype(i),len(i)))
            url_path="/".join(list_url)
            return (url.scheme + '://' + url.netloc +'/'+ url_path)
    def params_filter(self,url):
        #url参数处理
        liststr = []
        try:
            liststr = []
            for i in url.query.split('&'):
                para = i.split('=')
                length_int = len(para[1])
                if self.judgetype(para[1]) == 'int':
                    para[1] = '{int:%s}' % length_int
                else:
                    para[1] = '{str:%s}' % length_int
                para = '='.join(para)
                liststr.append(para)
            url_paras='&'.join(liststr)
            return url.scheme + '://' + url.netloc + url.path + '?' + url_paras
        except:
            length_int = len(url.query)
            url_paras = '{'+self.judgetype(url.query) + ':%s}' % length_int
            return url.scheme + '://' + url.netloc + url.path + '?' + url_paras
    def callback_content(self,content):
        ret = re.split(r'-|_|\.',content)
    def judgetype(self, strs):
        try:
            int(strs)
            return 'int'
        except:
            return 'str'



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

import random
class Get_Links:
    def __init__(self,url):
        self.url = url
        self.headers = {'User-Agent':random.choice(headerss)}
        self.timeout = 8
        self.domain = urlparse(self.url).netloc.replace('www.','').replace('/','').replace('.com.cn','').replace('.org.cn','').replace('.net.cn','').replace('.com','').replace('.cn','').replace('.cc','').replace('.net','').replace('.org','').replace('.info','').replace('.fun','').replace('.one','').replace('.xyz','').replace('.name','').replace('.io','').replace('.top','').replace('.me','').replace('.club','').replace('.tv','')
        if self.domain.find('.')>0:
            self.domain = self.domain.split('.')[1]
        self.domain0 = urlparse(self.url).netloc.replace('www.', '').replace('/', '')
        self.result = {'id_links':None,'html_links':None}
        self.all_links = []
        # 一开始获取所有的链接
        self.id_links = []
        # 带参数的动态链接
        self.html_links = []
        # 静态网页
        self.sche = 'http://'
        if 'http://' in self.url:
            self.sche = 'http://'
        else:
            self.sche = 'https://'
        print(self.domain)

    def Write_Logs(self,content):
        # 写入日志文件
        # 传入参数为字符串类型
        with open('log.txt', 'a+')as aa:
            aa.write('*********************************************' + '\n')
            aa.write(str(time.strftime('%Y-%m-%d:%H:%M:%S   ', time.localtime())) + str(content) + '\n')

    def Request(self,url):
        # 发起请求
        # 传入参数为url
        # 返回结果为没有编码的结果
        try:
            r = requests.get(url=url,headers=self.headers,timeout=self.timeout,verify=False)
            #encoding = requests.utils.get_encodings_from_content(r.text)[0]
            #res = r.content.decode(encoding,'replace')
            return r.content
        except Exception as e:
            self.Write_Logs(str(e))

    def Get_All_Links(self,url):
        content = self.Request(url)
        if content == None:
            return None
        _links = []
        # 接收参数为网页的内容
        # 返回结果为网页中全部的链接
        # 包括动态链接和静态网址和目录
        soup = BeautifulSoup(content, 'html.parser',from_encoding='iso-8859-1')
        links = soup.findAll('a')
        for link in links:
            _url = link.get('href')
            res = re.search('(javascript|:;|#|%)', str(_url))
            res1 = re.search('.(jpg|png|bmp|mp3|wma|wmv|gz|zip|rar|iso|pdf|txt)', str(_url))
            if res == None and res1 == None:
                _links.append(str(_url))
            else:
                pass
        if _links != []:
            return _links
        else:
            return None

    def Get_Dir_Links(self,content):
        # 对上面那个获取所有链接进行整理
        # 分别获取静态网页，动态链接，目录
        dir_links = []
        if content != None:
            rst = list(set(content))
            for rurl in rst:
                if '//' in rurl and 'http' in rurl and self.domain in rurl:
                    if '.htm' not in rurl and '.shtm' not in rurl and '?' not in rurl:
                        dir_links.append(rurl.strip())
                if 'http' not in rurl and self.domain in rurl:
                    if '.htm' not in rurl and '.shtm' not in rurl and '?' not in rurl:
                        dir_links.append(self.sche + rurl.lstrip('/').lstrip('.').strip())
                if 'http' not in rurl and self.domain not in rurl:
                    if '.htm' not in rurl and '.shtm' not in rurl and '?' not in rurl:
                        dir_links.append(self.sche + self.domain0.strip() + '/' + rurl.strip().lstrip('/').lstrip('.'))

            dir_links = list(set(dir_links))
            if len(dir_links) > 150:
                dir_links = random.sample(dir_links,100)
            if dir_links != []:
                return dir_links
            else:
                return None

    def Get_Ht_Id_Links(self,content):
        # 接受的参数content 是列表
        # 返回结果是一个字典
        id_links = []
        html_links = []
        ht_id_result = {'ID':id_links,'HT':html_links}
        if content != None:
            rst = list(set(content))
            for rurl in rst:
                if '//' in rurl and rurl.startswith('http') and self.domain in rurl:
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
                if 'http' not in rurl and self.domain in rurl:
                    # http 不在    domain 在
                    if '?' in rurl and '=' in rurl:
                        id_links.append(self.sche + rurl.lstrip('/').lstrip('.').strip())
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        if '?' not in rurl:
                            html_links.append(self.sche + rurl.lstrip('/').lstrip('.').strip())

                # /chanpin/2018-07-12/3.html"
                if 'http' not in rurl and self.domain not in rurl:
                    # http 不在  domain 不在
                    if '?' in rurl and '=' in rurl:
                        id_links.append(self.sche + self.domain0.strip() + '/' + rurl.strip().lstrip('/').lstrip('.'))
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        if '?' not in rurl:
                            html_links.append(self.sche + self.domain0.strip() + '/' + rurl.strip().lstrip('/').lstrip('.'))

            if len(html_links)>100:
                html_links=random.sample(html_links,50)
            if len(id_links)>100:
                id_links = random.sample(id_links,50)
            ht_id_result['ID'] = list(set(id_links))
            ht_id_result['HT'] = list(set(html_links))
            return ht_id_result

    def Filter(self,par1,lis1):
        for i in lis1:
            try:
                #print('开始对比 {}:::::::::::::::::{}'.format(par1.encode(),i.encode()))
                res = re.search(par1.encode(),i.encode())
                if res:
                    #print('发现对比存活!!!!!!!!')
                    return i
            except Exception as e:
                print(e)
                self.Write_Logs(str(e))

    def Get_Result(self):
        Link = self.Get_All_Links(self.url)
        print(Link)
        if Link:
            self.html_links.extend(self.Get_Ht_Id_Links(Link).get('HT'))
            print('静态链接:{}'.format(len(self.html_links)))
            print(self.html_links)
            self.id_links.extend(self.Get_Ht_Id_Links(Link).get('ID'))
            print('动态链接:{}'.format(len(self.id_links)))
            print(self.id_links)
            Dirs = self.Get_Dir_Links(Link)
            if Dirs:
                print('目录链接:{}'.format(len(Dirs)))
                print(Dirs)
                for dir in Dirs:
                    Links = self.Get_All_Links(dir)
                    if Links:
                        self.html_links.extend(self.Get_Ht_Id_Links(Links).get('HT'))
                        self.id_links.extend(self.Get_Ht_Id_Links(Links).get('ID'))
                self.html_links = list(set(self.html_links))
                self.id_links = list(set(self.id_links))
                # print('------------------------------------------')
                # print('静态链接:{}'.format(len(self.html_links)))
                # print(self.html_links)
                # print('动态链接:{}'.format(len(self.id_links)))
                # print(self.id_links)
                # print('-------------')

            idido = []
            htht = list(set(self.html_links))
            hthtx = []
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
            #self.html_links = hthtx

            #print(self.html_links)
            #print('静态页面数：{}'.format(len(hthtx)))
            p = filter_url()
            ididx = set()
            for i in self.id_links:
                ididx.add(re.sub('{.*?}','.*?',str(p.filter_url(i.replace('?','\?').replace('[','\[').replace(']','\]')))))
            #print(ididx)
            #print('动态页面页数:'+str(len(ididx)))
            ididx = list(ididx)

            for par in ididx:
                r = self.Filter(par,self.id_links)
                if r:
                    idido.append(r)

            ididz = []
            hthtz = []
            for i in idido:
                try:
                    r = requests.get(url=i,headers=self.headers,timeout=self.timeout,verify=False)
                    if r.status_code == 200:
                        ididz.append(i)
                except Exception as e:
                    self.Write_Logs(str(e))
            for i in hthtx:
                try:
                    r = requests.get(url=i.replace('*',''),headers=self.headers,timeout=self.timeout,verify=False)
                    if r.status_code == 200:
                        hthtz.append(i)
                except Exception as e:
                    self.Write_Logs(str(e))

            self.result['id_links'] = ididz
            self.result['html_links'] = hthtz

            return self.result





if __name__ == '__main__':
    links = Get_Links('https://www.taobao.com/')
    print(links.Get_Result())