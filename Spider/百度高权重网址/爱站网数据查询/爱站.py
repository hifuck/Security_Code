# -*- coding: utf-8 -*-
# @Time    : 2018/5/5 0005 19:56
# @Author  : Langzi
# @Blog    : www.langzi.fun
# @File    : 爱站.py
# @Software: PyCharm
import sys
import requests
import re
import threading
import chardet
import socket
import random
import pymysql
import ConfigParser
import time
reload(sys)
timeout = 5
socket.setdefaulttimeout(timeout)
sys.setdefaultencoding('utf-8')
cfg = ConfigParser.ConfigParser()
cfg.read('Config.ini')
user = cfg.get("Server", "username")
passwd = cfg.get("Server", "password")
host = cfg.get("Server", "host")
Dbname = cfg.get("Server","db")
thread_s = cfg.get("Config","thread_s")
print 'Start.....'
#port = [80,3306,3389,1433,1521]
port = [8080,3128,8081,21,22,23,445,3306,3389,1433,1521,81,7001,27017,6379,2181,9200,11211,2375,9000,1080,8888]
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
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24" ]

def scan(ip):
    list_port = []
    UA = random.choice(headerss)
    headers = {'User-Agent': UA}
    for popo in port:
        print '[-] Scan Port >>>>> ' +str(ip) + ' : ' + str(popo)
        try:
            s = socket.socket()
            s.connect((str(ip), int(popo)))
            s.send('langziyanqing \n')
            cc = s.recv(1024)
            list_port.append(popo)
            s.close()
        except:
            pass
    list_port1 = str(list(set(list_port)))
    uu = 'https://dns.aizhan.com/'
    try:
        print '[+] Scan URL >>>>> https://dns.aizhan.com/' +str(ip) + '/'
        time.sleep(5)
        p = requests.get(url=str(uu+ip+'/'),headers=headers,timeout=20).content
        #print p
        if isinstance(p,unicode):
            pass
        else:
            codesty = chardet.detect(p)
            a = p.decode(codesty['encoding'])
            zz = re.findall('<strong>(.*?)</strong', a, re.S)
            for z in zz:
                if z:
                    try:
                        r = re.findall('<a href="(.*?)/" rel="no.*?<td class="title">(.*?) ', a, re.S)
                        if r:
                            print z
                            for x,y in r:
                                if len(x)< 30:
                                    print x
                                    x1 = x
                                    print y.replace('<span>','').replace('\n','').replace('</span>','').replace('<td','').replace('</td>','').replace('	','').replace('												','').replace('					','')
                                    y1 =y.replace('<span>','').replace('\n','').replace('</span>','').replace('<td','').replace('</td>','').replace('	','').replace('												','').replace('					','')
                                    try:
                                        timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                        coon_svn = pymysql.connect(user=user, passwd=passwd, host=host, db=Dbname, charset='utf8')
                                        cur_svn = coon_svn.cursor()
                                        sql_svn = "INSERT INTO result(ip,address,url,urltitle,port,datatime) VALUES (%s,%s,%s,%s,%s,%s)"
                                        cur_svn.execute(sql_svn, (str(ip), str(z),str(x1),str(y1),str(list_port1), str(timenow)))
                                        coon_svn.commit()
                                        cur_svn.close()
                                        coon_svn.close()
                                    except Exception,e:
                                        print e
                                else:
                                    pass
                        else:
                            try:
                                timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                coon_svn = pymysql.connect(user=user, passwd=passwd, host=host, db=Dbname, charset='utf8')
                                cur_svn = coon_svn.cursor()
                                sql_svn = "INSERT INTO result(ip,address,url,urltitle,port,datatime) VALUES (%s,%s,%s,%s,%s,%s)"
                                cur_svn.execute(sql_svn, (str(ip), str(z),str('共有 0 个域名解析到该IP'), str('共有 0 个域名解析到该IP'), str(list_port1), str(timenow)))
                                coon_svn.commit()
                                cur_svn.close()
                                coon_svn.close()
                            except Exception, e:
                                print e
                    except Exception,e:
                        print e
    except Exception,e:
        print e
        try:
            timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            coon_svn = pymysql.connect(user=user, passwd=passwd, host=host, db=Dbname, charset='utf8')
            cur_svn = coon_svn.cursor()
            sql_svn = "INSERT INTO result(ip,address,url,urltitle,port,datatime) VALUES (%s,%s,%s,%s,%s,%s)"
            cur_svn.execute(sql_svn,(str(ip), str('获取 IP 所在地址失败'),str('共有 0 个域名解析到该IP'), str('共有 0 个域名解析到该IP'), str(list_port1), str(timenow)))
            coon_svn.commit()
            cur_svn.close()
            coon_svn.close()
        except Exception, e:
            print e




def start():
    while 1:
        try:
            time.sleep(random.randint(1, 4))
            lock.acquire()
            cooncms2 = pymysql.connect(user=user, passwd=passwd, host=host, db=Dbname)
            curcms2 = cooncms2.cursor()
            sql = "select ip from indexx where ipget=0 limit " + str(0) + ",1"  # 10表示载入10个网址
            sql1 = "update indexx set ipget='1' where ipget = 0 limit 1"
            curcms2.execute(sql)
            cooncms2.commit()
            curscms = curcms2.fetchone()
            curcms2.execute(sql1)
            cooncms2.commit()
            curcms2.close()
            cooncms2.close()
            lock.release()
            try:
                for xx in curscms:
                    xxx1cms = xx.replace("('", "").replace("',)", "")
                    scan(xxx1cms)
            except Exception, e:
                pass
        except Exception, e:
            print e
            time.sleep(150)
lock = threading.Lock()
for i in range(int(thread_s)):
    t1 = threading.Thread(target=start,name=str(' [*] SCAN IP: -%s-')%i).start()