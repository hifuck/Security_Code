# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import socket
socket.setdefaulttimeout(0.5)
import queue
import threading

def scan_port(ip,pool,port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        c = s.connect_ex((ip, port))
        if c == 0:
            s.close()
            print "%s:%s is open" % (ip, port)
            with open('open_port.txt','a+')as a:
                a.write(ip + '\n')
            pool.add_thread()  # 执行完毕后，再向线程池中添加一个线程类

        else:
            print "%s:%s is not open" % (ip,port)
            pass
    except Exception, e:
        print e
    finally:
        pool.add_thread()  # 执行完毕后，再向线程池中添加一个线程类


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
    print ('''

             _                           _ 
            | |                         (_)
            | |     __ _ _ __   __ _ _____ 
            | |    / _` | '_ \ / _` |_  / |
            | |___| (_| | | | | (_| |/ /| |
            |______\__,_|_| |_|\__, /___|_|
                                __/ |      
                               |___/       Easy Port Scan
                                           2018-15-25-00-15
                                                                   
    ''')
    time.sleep(3)
    pool = MyThreadPool(20)  # 设定线程池中最多只能有5个线程类
    New_start = raw_input('Import IP.txt:')  # line:190
    New_start = New_start.replace('"', '').replace("'", '')
    IP_list = list(set([x.strip() for x in open(New_start,'r').readlines()]))
    set_port = raw_input('Set Scan Port:')  # line:190
    port = int(set_port)
    for i in IP_list:
        t = pool.get_thread()   # 每个t都是一个线程类
        obj = t(target=scan_port, args=(i, pool,port)) # 这里的obj才是正真的线程对象
        obj.start()
    import os
    os.system('pause')