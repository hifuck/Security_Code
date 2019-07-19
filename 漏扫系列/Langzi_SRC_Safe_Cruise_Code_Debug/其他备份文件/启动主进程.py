# -*- coding:utf-8 -*-
# __author__:langzi
# __blog__:www.langzi.fun
import pymysql
import random
from selenium import webdriver
import os
import shutil
import re
import datetime

import configparser
import contextlib
import pymysql
import time
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
import psutil
import os
import time
import shutil
import urllib.parse,os.path,re

cfg = configparser.ConfigParser()
cfg.read('Config.ini')
user = cfg.get("Server", "username")
passwd = cfg.get("Server", "password")
host = cfg.get("Server", "host")
Dbname = cfg.get("Server", "db")
port = int(cfg.get("Server", "port"))
thread_s = int(cfg.get("Config", "thread_s"))
check_env = int(cfg.get("Config", "check_env"))
start_on = int(cfg.get("Config", "start_on"))

check_ = '不检测运行环境' if check_env == 0 else '检测运行环境'
start_ = '从数据库加载数据扫描' if start_on == 1 else '重新导入文本扫描'

@contextlib.contextmanager
def connect_mysql():
    coon = pymysql.connect(user=user, passwd=passwd, host=host, db=Dbname, port=port, charset='utf8')
    cursor = coon.cursor()
    try:
        yield cursor
    except Exception as e:
        if 'Duplicate entry' in str(e):
            print('数据库已存在该网址')
    finally:
        coon.commit()
        cursor.close()
        coon.close()


class Check_Env:
    def __init__(self):
        print('\n')
        print('***配置文件相关信息***')
        print(f'账号:{user}')
        print(f'密码:{passwd}')
        print(f'数据库:{host}')
        print(f'端口号:{port}')
        print(f'线程数:{thread_s}')
        print(f'检测环境:{check_}')
        print(f'扫描文件:{start_}')
        print('***配置文件相关信息***')
        print('\n')

        time.sleep(2)

    def check_mysql(self):
        try:
            print('\n')

            print('[*] 开始数据库检测......')
            coon = pymysql.connect(user=user, passwd=passwd, host=host, db=Dbname, port=port, charset='utf8')
            print('[+] 数据库连接成功')
            coon.close()
        except Exception as e:
            print('[-] 数据库连接失败[{}]'.format(str(e)))
            os.system('pause')

    def check_python(self):
        try:
            print('\n')

            print('[*] 开始Python2环境检测......')
            content = os.popen('python _py2.py')
            res = int(content.read())
            if res == 2:
                print('[+] Python 2.x 环境安装成功')
            else:
                print('[-] Python 2.x 环境未安装')
                os.system('pause')
        except Exception as e:
            print('[-] Python 2.x 环境检查失败[{}]'.format(str(e)))
            os.system('pause')

    def check_selenium(self):
        try:
            print('\n')

            print('[*] 开始FireFox浏览器检测......')
            dirver = webdriver.Firefox()
            dirver.get('http://www.langzi.fun')
            time.sleep(3)
            dirver.close()
            print('[+] FireFox 安装成功')
        except Exception as e:
            print('[-] FireFox 未成功安装 [{}]'.format(str(e)))
            os.system('pause')

    def check_docx(self):
        try:
            print('\n')

            print('[*] 开始原DOCX文件检测......')
            if os.path.exists('default.docx'):
                print('[+] 存在自动报表目标文件')
            else:
                print('[-] 当前目录不存在自动报表目标文件')
                os.system('pause')
        except Exception as e:
            print('[-] 检查文档失败 [{}]'.format(str(e)))
            os.system('pause')

    def start_check(self):
        self.check_mysql()
        self.check_python()
        self.check_docx()
        self.check_selenium()
        print('----------------------------------------------------')
        print('-------------运行环境检测完毕状态正常---------------')
        print('----------------------------------------------------')
        time.sleep(5)
        print('\n')


def run(url):
    try:
        with connect_mysql() as coon:
            sql = "insert into sec_scan_index(url) values  ('{}')".format(url)
            print('[+] 开始添加网址: {} 到数据库'.format(url))
            coon.execute(sql)
    except Exception as e:
        if 'Duplicate entry' in str(e):
            print('数据库已存在该网址:{}'.format(url))


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
                        dir_links.append(self.sche + rurl.lstrip('/').lstrip('.').strip().lstrip('/'))
                if 'http' not in rurl and self.domain not in rurl:
                    if '.htm' not in rurl and '.shtm' not in rurl and '?' not in rurl:
                        dir_links.append(self.sche + self.domain0.strip() + '/' + rurl.strip().lstrip('/').lstrip('.').lstrip('/'))

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
                        id_links.append(self.sche + rurl.lstrip('/').lstrip('.').strip().lstrip('/'))
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        if '?' not in rurl:
                            html_links.append(self.sche + rurl.lstrip('/').lstrip('.').strip().lstrip('/'))

                # /chanpin/2018-07-12/3.html"
                if 'http' not in rurl and self.domain not in rurl:
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
                res = re.search(par1.encode(),i.encode())
                if res:
                    return i
            except Exception as e:
                self.Write_Logs(str(e))

    def Get_Result(self):
        Link = self.Get_All_Links(self.url)
        #print(Link)
        if Link:
            self.html_links.extend(self.Get_Ht_Id_Links(Link).get('HT'))
            self.id_links.extend(self.Get_Ht_Id_Links(Link).get('ID'))
            Dirs = self.Get_Dir_Links(Link)
            if Dirs:
                for dir in Dirs:
                    Links = self.Get_All_Links(dir)
                    if Links:
                        self.html_links.extend(self.Get_Ht_Id_Links(Links).get('HT'))
                        self.id_links.extend(self.Get_Ht_Id_Links(Links).get('ID'))
                self.html_links = list(set(self.html_links))
                self.id_links = list(set(self.id_links))
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
            if dic_2:
                hthtx.append(random.choice(dic_2))
                hthtx.append(random.choice(dic_2))
            if dic_3:
                hthtx.append(random.choice(dic_3))
                hthtx.append(random.choice(dic_3))
            if dic_4:
                hthtx.append(random.choice(dic_4))
                hthtx.append(random.choice(dic_4))
            p = filter_url()
            for i in self.id_links:
                mid = str(re.sub('{.*?}','.*?',str(p.filter_url(i))))
                if mid in self.mids:
                    pass
                else:
                    self.mids.add(mid)
                    idido.append(i)
            idido = list(set(idido))
            ididz = []
            hthtz = []
            for i in idido:
                try:
                    r = requests.get(url=i,headers=self.headers,timeout=self.timeout,verify=False)
                    if r.status_code == 200:
                        ididz.append(i)
                        if '?' in r.url and '=' in r.url:
                            ididz.append(r.url)
                except Exception as e:
                    self.Write_Logs(str(e))
            for i in hthtx:
                try:
                    r = requests.get(url=i.replace('*',''),headers=self.headers,timeout=self.timeout,verify=False)
                    if r.status_code == 200:
                        hthtz.append(i)
                except Exception as e:
                    self.Write_Logs(str(e))
            with open('InjEction_links.txt', 'a+', encoding='utf-8')as a:
                if ididz:
                    self.result['id_links'] = list(set(ididz))
                    for i in list(set(ididz)):
                        a.write(i + '\n')
                if hthtz:
                    self.result['html_links'] = list(set(hthtz))
                    for i in list(set(hthtz)):
                        a.write(i + '\n')
            if self.result == {}:
                return None
            else:
                with connect_mysql() as coon:
                    print('网址超链接入库中:'+self.url+':'+str(self.result))
                    sql1 = 'insert into sec_get_links(url,links) values ("{}","{}")'.format(self.url,str(self.result))
                    coon.execute(sql1)

def Get_Linkss(sem):
    while 1:
        try:
            sem.acquire()
            with connect_mysql() as coon:
                sql1 = 'select url from sec_scan_index where links_get=0 limit 0,1'
                sql2 = 'update sec_scan_index set links_get=1 where links_get = 0 limit 1'
                coon.execute(sql1)
                min_res1 = coon.fetchone()
                if min_res1 == None:
                    sem.release()
                    return
                else:
                    res_url1 = min_res1[0]
                coon.execute(sql2)
            sem.release()
            link = Get_Links(res_url1)
            link.Get_Result()
        except Exception as e:
            print(e)

def Start(start):

    sql_start = "start " + os.path.join(os.getcwd(), 'ExtrSql.dll')
    xss_start = "start " + os.path.join(os.getcwd(), 'ExtrXss.dll')
    url_start = "start " + os.path.join(os.getcwd(), 'ExtrUrs.dll')
    back_end = "start " + os.path.join(os.getcwd(), 'ExtrBae.dll')




    def check(name):
        while 1:
            list_ = []
            for pnum in psutil.pids():
                p = psutil.Process(pnum).name()
                list_.append(p)
            if name in list_:
                print('{} : 正在运行...'.format(name.replace('dll','')))
                time.sleep(927)
            else:
                print('{} : 停止运行....启动下一程序....'.format(name.replace('dll','')))
                return 'OVER'


    print('[+] 开始SQL注入漏洞扫描')
    os.system(sql_start)
    time.sleep(15)

    if start == 0:
        res = check('ExtrBas.dll')
        if res == 'OVER':
            print('[+] 开始备份文件提取数据')
        os.system(back_end)
        time.sleep(15)
        res = check('ExtrBae.dll')
        if res == 'OVER':
            print('[+] 备份文件数据提取完毕')

    print('[+] 开始URL跳转漏洞扫描')
    os.system(url_start)
    time.sleep(15)
    res = check('ExtrUrs.dll')
    if res == 'OVER':
        print('[+] URL跳转漏洞提取完毕')

    print('[+] 开始XSS漏洞扫描')
    os.system(xss_start)
    time.sleep(15)
    res = check('ExtrXss.dll')
    if res == 'OVER':
        print('[+] 开始xss文件提取数据')

    if res == 'OVER':
        print('[+] 全部漏洞扫描完毕~')
        os.system('pause')

if __name__ == '__main__':
    print('''
         _____  __    __  _____   _____        ___   _____   _____  
        | ____| \ \  / / |_   _| |  _  \      /   | /  ___| |_   _| 
        | |__    \ \/ /    | |   | |_| |     / /| | | |       | |   
        |  __|    }  {     | |   |  _  /    / / | | | |       | |   
        | |___   / /\ \    | |   | | \ \   / /  | | | |___    | |   
        |_____| /_/  \_\   |_|   |_|  \_\ /_/   |_| \_____|   |_|   

                                                        主控制台
                                                        19年5月20礼物    
    ''')
    time.sleep(8)

    a = Check_Env()
    if check_env == 1:
        a.start_check()

    import threading

    if start_on == 0:
        inp_url = input('Input Target Url.txt:')
        All_Urls = list(set([x.strip() for x in open(inp_url,'r',encoding='utf-8').readlines()]))

        if len(All_Urls) > 200:
            print('----------------------------------------------------')
            print('----目标数量超过200，将从中提取200个网址加载扫描----')
            print('----------------------------------------------------')
            All_Urls = All_Urls[:200]


        if os.path.exists('urls.txt'):
            os.remove('urls.txt')
        time_now_txt = str(datetime.datetime.now()).replace(':', '-').replace(' ', '-').split('.')[0] + '.txt'
        if os.path.exists('result.txt'):
            shutil.move('result.txt',time_now_txt)

        with open('urls.txt','a+') as a:
            for i in All_Urls:
                a.write(i+'\n')

        with ThreadPoolExecutor(5) as p:
            p.map(run,All_Urls)

        print('[+] 网址加载数据库成功')
        time.sleep(2)
        print('[+] 开始备份文件扫描')
        back_start = "start " + os.path.join(os.getcwd(), 'ExtrBas.dll')
        os.system(back_start)
        time.sleep(3)

        print('[+] 开始从数据库提取有效链接')
        time.sleep(3)
        sem = threading.BoundedSemaphore(1)
        p = ThreadPoolExecutor()
        for i in range(thread_s):
            p.submit(Get_Linkss, sem)
        p.shutdown()
        print('[+] 网站超链接提取完毕，开始漏洞扫描检测')
        time.sleep(2)
        Start(start_on)

    if start_on == 1:
        Start(start_on)

