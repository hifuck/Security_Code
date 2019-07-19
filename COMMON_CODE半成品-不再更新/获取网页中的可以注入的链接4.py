# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import contextlib
import pymysql
import re
import time
import requests
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
from urllib.parse import urlparse,urljoin
import random
from concurrent.futures import ThreadPoolExecutor




import configparser
cfg = configparser.ConfigParser()
cfg.read('../Config.ini')
user = cfg.get("Server", "username")
passwd = cfg.get("Server", "password")
host = cfg.get("Server", "host")
Dbname = cfg.get("Server", "db")
port = int(cfg.get("Server", "port"))

thread_s = int(cfg.get("Common_Config", "threads"))
scan_level_s = int(cfg.get("Scan_Levels", "Scan_Level"))

@contextlib.contextmanager
def connect_mysql():
    coon = pymysql.connect(user=user, passwd=passwd, host=host, db=Dbname, port=port, charset='utf8')
    cursor = coon.cursor()
    try:
        yield cursor
    except Exception as e:
        if '1062, "Duplicate entry ' in str(e):
            print('该网址重复')
        pass
    finally:
        coon.commit()
        cursor.close()
        coon.close()

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
        self.timeout = 15
        self.domain = urlparse(self.url).netloc.replace('www.','').replace('/','').replace('.com.cn','').replace('.org.cn','').replace('.net.cn','').replace('.com','').replace('.cn','').replace('.cc','').replace('.net','').replace('.org','').replace('.info','').replace('.fun','').replace('.one','').replace('.xyz','').replace('.name','').replace('.io','').replace('.top','').replace('.me','').replace('.club','').replace('.tv','')
        if self.domain.find('.')>0:
            self.domain = self.domain.split('.')[1]
        self.domain0 = urlparse(self.url).netloc.replace('/', '')
        self.result = {}
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
        self.mids = set()

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
            time.sleep(random.randint(1,5))
            r = requests.get(url=url,headers=self.headers,timeout=self.timeout,verify=False)
            #encoding = requests.utils.get_encodings_from_content(r.text)[0]
            #res = r.content.decode(encoding,'replace')
            return r.content
        except Exception as e:
            self.Write_Logs(str(e))
            with connect_mysql() as coon:
                sql1 = 'insert into Sec_Fail_Links(url) values ("{}")'.format(url.rstrip('/'))
                coon.execute(sql1)

    def extract_URL(self,content):
        pattern_raw = r"""
    	  (?:"|')                               # Start newline delimiter
    	  (
    	    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    	    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
    	    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
    	    |
    	    ((?:/|\.\./|\./)                    # Start with /,../,./
    	    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
    	    [^"'><,;|()]{1,})                   # Rest of the characters can't be
    	    |
    	    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    	    [a-zA-Z0-9_\-/]{1,}                 # Resource name
    	    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
    	    (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
    	    |
    	    ([a-zA-Z0-9_\-]{1,}                 # filename
    	    \.(?:php|asp|aspx|jsp|json|
    	         action|html|js|txt|xml)             # . + extension
    	    (?:\?[^"|']{0,}|))                  # ? mark with parameters
    	  )
    	  (?:"|')                               # End newline delimiter
    	"""
        pattern = re.compile(pattern_raw, re.VERBOSE)
        result = re.finditer(pattern, str(content))
        if result == None:
            return None
        js_url = []
        for match in result:
            if match.group() not in js_url:
                js_url.append(match.group().strip('"').strip("'"))
        return js_url

    def process_url(self, re_URL):
        black_url = ["javascript:"]  # Add some keyword for filter url.
        URL_raw = urlparse(self.url)
        ab_URL = URL_raw.netloc
        host_URL = URL_raw.scheme
        if re_URL[0:2] == "//":
            result = host_URL + ":" + re_URL
        elif re_URL[0:4] == "http":
            result = re_URL
        elif re_URL[0:2] != "//" and re_URL not in black_url:
            if re_URL[0:1] == "/":
                result = host_URL + "://" + ab_URL + re_URL
            else:
                if re_URL[0:1] == ".":
                    if re_URL[0:2] == "..":
                        result = host_URL + "://" + ab_URL + re_URL[2:]
                    else:
                        result = host_URL + "://" + ab_URL + re_URL[1:]
                else:
                    result = host_URL + "://" + ab_URL + "/" + re_URL
        else:
            result = self.url
        return result

    def find_last(string, str):
        positions = []
        last_position = -1
        while True:
            position = string.find(str, last_position + 1)
            if position == -1: break
            last_position = position
            positions.append(position)
        return positions

    def find_by_url(self,js=False):
        if js == False:
            html_raw = self.Extract_html(self.url)
            if html_raw == None:
                print("Fail to access " + self.url)
                return None
            # print(html_raw)
            html = BeautifulSoup(html_raw, "html.parser")
            html_scripts = html.findAll("script")
            script_array = {}
            script_temp = ""
            for html_script in html_scripts:
                script_src = html_script.get("src")
                if script_src == None:
                    script_temp += html_script.get_text() + "\n"
                else:
                    purl = self.process_url(self.url, script_src)
                    script_array[purl] = self.Extract_html(purl)
            script_array[self.url] = script_temp
            allurls = []
            for script in script_array:
                # print(script)
                temp_urls = self.extract_URL(script_array[script])
                if len(temp_urls) == 0: continue
                for temp_url in temp_urls:
                    allurls.append(self.process_url(script, temp_url))
            result = []
            for singerurl in allurls:
                url_raw = urlparse(self.url)
                domain = url_raw.netloc
                positions = self.find_last(domain, ".")
                miandomain = domain
                if len(positions) > 1: miandomain = domain[positions[-2] + 1:]
                # print(miandomain)
                suburl = urlparse(singerurl)
                subdomain = suburl.netloc
                # print(singerurl)
                if miandomain in subdomain or subdomain.strip() == "":
                    if singerurl.strip() not in result:
                        result.append(singerurl)
            return result
        else:
            temp_urls = self.extract_URL(self.Request(self.url))
            if len(temp_urls) == 0: return None
            result = []
            for temp_url in temp_urls:
                if temp_url not in result:
                    result.append(temp_url)
            return result

    def Get_All_Links(self,url):
        content = self.Request(url)
        if content == None:
            content = self.Request(url)
            if content == None:
                return None
        _links = []
        # 接收参数为网页的内容
        # 返回结果为网页中全部的链接
        # 包括动态链接和静态网址和目录
        soup = BeautifulSoup(content, 'html.parser',from_encoding='iso-8859-1')
        links = soup.findAll('a')
        if links != None:
            for link in links:
                _url = link.get('href')
                res = re.search('(javascript|:;|#|%)', str(_url))
                res1 = re.search('.(jpg|png|gif|jpeg|mp4|css|bmp|mp3|wma|wmv|gz|zip|rar|iso|pdf|txt|\.w3\.org)', str(_url))
                if res == None and res1 == None:
                    _links.append(str(_url).replace(r'\\','').rstrip('\\'))
                else:
                    pass

        links2 = self.find_by_url(self.url)
        if links2 != None:
            for link in links2:
                res = re.search('(javascript|:;|#|%)', str(link))
                res1 = re.search('.(jpg|png|gif|jpeg|mp4|css|bmp|mp3|wma|wmv|gz|zip|rar|iso|pdf|txt|\.w3\.org)', str(link))
                if res == None and res1 == None:
                    _links.append(str(link).replace(r'\\','').rstrip('\\'))
                else:
                    pass
        if _links != []:
            return _links
        else:
            return None

    def Get_Dir_Links(self,content):
        # 对上面那个获取所有链接进行整理
        dir_links = []
        if content != None:
            rst = list(set(content))
            for rurl in rst:
                if rurl.startswith('http') and '://' in rurl and self.domain in rurl:
                    # http://www.baidu.com
                    if rurl.rstrip('/') != self.url:
                        dir_links.append(rurl.strip())

                if 'http' not in rurl and self.domain in rurl:
                    if 'www' in self.url:
                        if 'www' in rurl:
                            dir_links.append(self.sche + rurl.lstrip('/').lstrip('.').rstrip('/').rstrip('.').replace('//','').replace(':',''))
                        else:
                            dir_links.append(self.sche + 'www.'+rurl.lstrip('/').lstrip('.').rstrip('/').rstrip('.').replace('//','').replace(':',''))
                    else:
                        dir_links.append(
                            self.sche + rurl.lstrip('/').lstrip('.').rstrip('/').rstrip('.').replace('//', '').replace(
                                ':', ''))

                if 'http' not in rurl and self.domain not in rurl and ':' not in rurl and '//' not in rurl:
                    # /sttd/xhm/
                    dir_links.append(self.sche  + self.domain0 + '/' + rurl.lstrip('/').lstrip('.').rstrip('/').rstrip('.').replace('//','').replace(':',''))

                if rurl.startswith('://') and 'http' not in rurl and self.domain in rurl:
                    if self.sche + rurl.replace('://','').rstrip('/') != self.url:
                        dir_links.append(self.sche + rurl.replace('://',''))
                if rurl.startswith('//') and self.domain in rurl :
                    # //order.jd.com/center/list.action
                    if self.sche + rurl.replace('//','').rstrip('/') != self.url:
                        dir_links.append(self.sche + rurl.replace('//',''))

            dir_links = list(set(dir_links))
            html_links = []
            no_html_links = []
            for i in dir_links:
                if 'htm' in i:
                    html_links.append(i)
                else:
                    no_html_links.append(i)
            if len(html_links) > 30:
                html_links = random.sample(html_links,10)
            dir_links = html_links + no_html_links
            # print(dir_links)
            if len(dir_links) > 100:
                dir_links = random.sample(dir_links,60)
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
                if rurl.startswith('http') and '://' in rurl and self.domain in rurl and '.js?' not in rurl:
                    # http://www.baidu.com
                    if '?' in rurl and '=' in rurl:
                        # result_links.append(rurl)
                        id_links.append(rurl.strip())
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        if '?' not in rurl:
                            # result_links.append(rurl)
                            html_links.append(rurl.strip())

                if 'http' not in rurl and self.domain in rurl and '.js?' not in rurl:
                    if 'www' in self.url:
                        if 'www' in rurl:
                            if '?' in rurl and '=' in rurl:
                                id_links.append(self.sche + rurl.lstrip('/').lstrip('.').rstrip('/').rstrip('.').replace('//','').replace(':',''))
                            if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                                if '?' not in rurl:
                                    # result_links.append(rurl)
                                    html_links.append(
                                        self.sche + rurl.lstrip('/').lstrip('.').rstrip('/').rstrip('.').replace('//',
                                                                                                                 '').replace(
                                            ':', ''))
                        else:
                            if '?' in rurl and '=' in rurl:
                                id_links.append(self.sche + 'www.'+rurl.lstrip('/').lstrip('.').rstrip('/').rstrip('.').replace('//','').replace(':',''))
                            if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                                if '?' not in rurl:
                                    # result_links.append(rurl)
                                    html_links.append(
                                        self.sche + 'www.' + rurl.lstrip('/').lstrip('.').rstrip('/').rstrip(
                                            '.').replace('//', '').replace(':', ''))
                    else:
                        if '?' in rurl and '=' in rurl:
                            id_links.append(
                            self.sche + rurl.lstrip('/').lstrip('.').rstrip('/').rstrip('.').replace('//', '').replace(
                                ':', ''))
                        if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                            if '?' not in rurl:
                                # result_links.append(rurl)
                                html_links.append(self.sche + rurl.lstrip('/').lstrip('.').rstrip('/').rstrip('.').replace('//', '').replace(
                                ':', ''))

                if 'http' not in rurl and self.domain not in rurl and ':' not in rurl and '//' not in rurl and '.js?' not in rurl:
                    # /sttd/xhm/
                    if '?' in rurl and '=' in rurl:
                        id_links.append(self.sche  + self.domain0 + '/' + rurl.lstrip('/').lstrip('.').rstrip('/').rstrip('.').replace('//','').replace(':',''))
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        if '?' not in rurl:
                            # result_links.append(rurl)
                            html_links.append(
                                self.sche + self.domain0 + '/' + rurl.lstrip('/').lstrip('.').rstrip('/').rstrip(
                                    '.').replace('//', '').replace(':', ''))

                if rurl.startswith('://') and 'http' not in rurl and self.domain in rurl and '.js?' not in rurl:
                    if '?' in rurl and '=' in rurl:
                        id_links.append(self.sche + rurl.replace('://',''))
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        if '?' not in rurl:
                            # result_links.append(rurl)
                            html_links.append(self.sche + rurl.replace('://',''))

                if rurl.startswith('//') and self.domain in rurl and '.js?' not in rurl:
                    # //order.jd.com/center/list.action
                    if '?' in rurl and '=' in rurl:
                        id_links.append(self.sche + rurl.replace('//',''))
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        if '?' not in rurl:
                            # result_links.append(rurl)
                            html_links.append(self.sche + rurl.replace('//',''))


                if '//' in rurl and rurl.startswith('http') and self.domain in rurl and '.js?' not in rurl:
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
                if 'http' not in rurl and self.domain in rurl and '.js?' not in rurl:
                    # http 不在    domain 在
                    if '?' in rurl and '=' in rurl:
                        id_links.append(self.sche + rurl.lstrip('/').lstrip('.').strip().lstrip('/'))
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        if '?' not in rurl:
                            html_links.append(self.sche + rurl.lstrip('/').lstrip('.').strip().lstrip('/'))

                # /chanpin/2018-07-12/3.html"
                if 'http' not in rurl and self.domain not in rurl and '.js?' not in rurl:
                    # http 不在  domain 不在
                    if '?' in rurl and '=' in rurl:
                        id_links.append(self.sche + self.domain0.strip() + '/' + rurl.strip().lstrip('/').lstrip('.').lstrip('/'))
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        if '?' not in rurl:
                            html_links.append(self.sche + self.domain0.strip() + '/' + rurl.strip().lstrip('/').lstrip('.').lstrip('/'))

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
                #print(e)
                self.Write_Logs(str(e))

    def Get_Result(self):
        Link = self.Get_All_Links(self.url)
        #print(Link)
        if Link:
            self.html_links.extend(self.Get_Ht_Id_Links(Link).get('HT'))
            #print('静态链接:{}'.format(len(self.html_links)))
            #print(self.html_links)
            self.id_links.extend(self.Get_Ht_Id_Links(Link).get('ID'))
            #print('动态链接:{}'.format(len(self.id_links)))
            #print(self.id_links)
            Dirs = self.Get_Dir_Links(Link)
            if Dirs:
                # print('目录链接:{}'.format(len(Dirs)))
                # print(Dirs)
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


            ididt = list(set(self.id_links))
            ididx = []
            dic_11 = []
            dic_21 = []
            dic_31 = []
            dic_41 = []
            for i in ididt:
                path = urlparse(i).path
                if path.count('/') == 1:
                    dic_11.append(i)
                if path.count('/') == 2:
                    dic_21.append(i)
                if path.count('/') == 3:
                    dic_31.append(i)
                if path.count('/') > 3:
                    dic_41.append(i)
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



            #self.html_links = hthtx

            #print(self.html_links)
            #print('静态页面数：{}'.format(len(hthtx)))


            p = filter_url()
            for i in self.id_links:
                mid = str(re.sub('{.*?}','.*?',str(p.filter_url(i))))
                if mid in self.mids:
                    pass
                else:
                    self.mids.add(mid)
                    idido.append(i)
            idido = list(set(idido))
            if len(idido)>100:
                idido = random.sample(idido,100)


            ididz = []
            hthtz = []
            for i in idido:
                try:
                    r = requests.get(url=i,headers=self.headers,timeout=self.timeout,verify=False)
                    if r.status_code == 200:
                        ididz.append(i.replace('\n',''))
                        if '?' in r.url and '=' in r.url:
                            ididz.append(r.url.replace('\n',''))
                except Exception as e:
                    self.Write_Logs(str(e))
            for i in hthtx:
                try:
                    r = requests.get(url=i.replace('*',''),headers=self.headers,timeout=self.timeout,verify=False)
                    if r.status_code == 200:
                        hthtz.append(i.replace('\n',''))
                except Exception as e:
                    self.Write_Logs(str(e))


            with connect_mysql() as coon:
                if list(set(hthtz)) != []:
                    print(self.url+':'+str(list(set(hthtz))))
                    sql1 = 'insert into Sec_Links_0(url,links) values ("{}","{}")'.format(self.url,str(list(set(hthtz))))
                    coon.execute(sql1)

                if list(set(ididx)) != []:
                    print(self.url+':'+str(ididx))
                    sql3 = 'insert into Sec_Links_1(url,links) values ("{}","{}")'.format(self.url,str(list(set(ididx))))
                    coon.execute(sql3)

                if list(set(ididz)) != []:
                    print(self.url+':'+str(list(set(ididz))))
                    sql2 = 'insert into Sec_Links_2(url,links) values ("{}","{}")'.format(self.url,str(list(set(ididz))))
                    coon.execute(sql2)

                print('\n')

                #return result_links
            #return self.result




def Get_Linkss(sem):
    time.sleep(random.randint(1,20))
    while 1:
        try:
            sem.acquire()
            with connect_mysql() as coon:
                sql1 = 'select url from Sec_Index where extrurs=0 limit 0,1'
                sql2 = 'update Sec_Index set extrurs=1 where extrurs = 0 limit 1'
                coon.execute(sql1)
                min_res1 = coon.fetchone()
                if min_res1 == None:
                    sem.release()
                    return
                res_url1 = min_res1[0]
                coon.execute(sql2)
            sem.release()
            link = Get_Links(res_url1)
            link.Get_Result()
        except Exception as e:
            print('数据库总控制台错误:'+str(e))

if __name__ == '__main__':
    import threading
    sem = threading.BoundedSemaphore(1)
    p = ThreadPoolExecutor()
    for i in range(thread_s):
        p.submit(Get_Linkss, sem)

