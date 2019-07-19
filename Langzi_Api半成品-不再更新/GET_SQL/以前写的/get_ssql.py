# coding:utf-8
import subprocess
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def check(result):
    sql_result={}
    if 'CRITICAL' not in result:
        if result.count('Type')>1:
            pattern = 'Parameter: (.*?)    Type: (.*?)    Title: (.*?)    Payload: (.*?)    .*DBMS is (.*?)web server operating system: (.*?)web application technology: (.*?)back-end DBMS: (.*?)\['
            r = re.findall(pattern,result,re.S)
            for parameter, type, title, Payload, db, system, application, dbms in r:
                sql_result['parameter'] = parameter
                sql_result['type'] = type
                sql_result['title'] = title
                sql_result['Payload'] = Payload
                sql_result['db'] = db
                sql_result['system'] = system
                sql_result['application'] = application
                sql_result['dbms'] = dbms
            return sql_result
        else:
            pattern = 'Parameter: (.*?)    Type: (.*?)    Title: (.*?)    Payload: (.*?)---\[.*DBMS is (.*?)web server operating system: (.*?)web application technology: (.*?)back-end DBMS: (.*?)\['
            r = re.findall(pattern,result,re.S)
            for parameter, type, title, Payload, db, system, application, dbms in r:
                sql_result['parameter'] = parameter
                sql_result['type'] = type
                sql_result['title'] = title
                sql_result['Payload'] = Payload
                sql_result['db'] = db
                sql_result['system'] = system
                sql_result['application'] = application
                sql_result['dbms'] = dbms
            return sql_result
    else:
        return None

def scan_level_1(url):
    comm = 'sqlmap.py -u %s --batch --random-agent' % url
    print 'Level 1 : ' + comm
    try:
        res = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read().replace('\n','')
        res_1 = check(result)
    except Exception, e:
        print e
    finally:
        res.terminate()
    if res_1 == None:
        pass
    else:
        return res_1
    return None


def scan_level_2(url):
    urls,datas = url.split('?')[0],url.split('?')[1]
    comm_cookie = 'sqlmap.py -u {} --cookie {} --level 2 --batch --random-agent'.format(urls,datas)
    print 'Level 2 : ' + comm_cookie
    comm_post = 'sqlmap.py -u {} --data {} --level 2 --batch --random-agent '.format(urls,datas)
    print 'Level 2 : ' + comm_post

    try:
        res = subprocess.Popen(comm_cookie, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read().replace('\n', '').replace(' ', '')
        res_1 = check(result)
    except Exception, e:
        print e
    finally:
        res.terminate()

    if res_1 == None:
        pass
    else:
        return res_1

    try:
        res = subprocess.Popen(comm_post, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read().replace('\n', '').replace(' ', '')
        res_1 = check(result)
    except Exception, e:
        print e
    finally:
        res.terminate()
    if res_1 == None:
        pass
    else:
        return res_1
    return None


def scan_level_3(url):
    comm = 'sqlmap.py -u %s --batch --tamper space2comment.py --random-agent' % url
    print 'Level 3 : ' + comm
    try:
        res = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read().replace('\n','')
        res_1 = check(result)
    except Exception, e:
        print e
    finally:
        res.terminate()
    if res_1 == None:
        pass
    else:
        return res_1
    return None

def scan_level_4(url):
    urls,datas = url.split('?')[0],url.split('?')[1]
    comm_cookie = 'sqlmap.py -u {} --cookie {} --level 2 --tamper space2comment.py --batch --random-agent '.format(urls,datas)
    print 'Level 4 : ' + comm_cookie

    comm_post = 'sqlmap.py -u {} --data {} --level 2 --tamper space2comment.py --batch --random-agent '.format(urls,datas)
    print 'Level 4 : ' + comm_post

    try:
        res = subprocess.Popen(comm_cookie, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read().replace('\n','')
        res_1 = check(result)
    except Exception, e:
        print e
    finally:
        res.terminate()
    if res_1 == None:
        pass
    else:
        return res_1

    try:
        res = subprocess.Popen(comm_post, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read().replace('\n','')
        res_1 = check(result)
    except Exception, e:
        print e
    finally:
        res.terminate()
    if res_1 == None:
        pass
    else:
        return res_1
    return None


def scan_level_5(url):
    # 获取完整注入url即可
    comm = 'sqlmap.py -u %s --batch --tamper space2comment.py --delay 2 --time-sec=15 --timeout=20  --level 5 --random-agent' % url
    print 'Level 5 : ' + comm
    try:
        res = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE)
        result = res.stdout.read().replace('\n','')
        res_1 = check(result)
    except Exception, e:
        print e
    finally:
        res.terminate()
    if res_1 == None:
        pass
    else:
        return res_1
    return None

res = scan_level_1('http://127.0.0.1/sqli/Less-1/?id=1')
print res
print '/'*50
res = scan_level_2('http://127.0.0.1/sqli/Less-1/?id=1')
print res
print '/'*50
res = scan_level_3('http://127.0.0.1/sqli/Less-1/?id=1')
print res
print '/'*50
res = scan_level_4('http://127.0.0.1/sqli/Less-1/?id=1')
print res
print '/'*50
res = scan_level_5('http://127.0.0.1/sqli/Less-1/?id=1')
print res
print '/'*50