#!/usr/bin/env python
#coding=utf-8
#author:Blus
import MySQLdb
import threading
import time
import IPy
import subprocess

def mysql_connect1(ip):

    if not(ping_ip(ip)):
        #print ip,"down"
        return
    else:
        #记录在线的ip
        ip_log("ip_up.txt",ip,"")

    #尝试数据库连接
    try:
        conn=MySQLdb.connect(host=ip,user='root',passwd='',db='',port=3306)
        cur=conn.cursor()

        #记录开放3306端口的ip
        ip_log("port_connected.txt", ip,"")


    except MySQLdb.Error,e:
        e = str(e)
        #记录报错信息
        print e

        r1 = e.find('Can\'t connect') #端口未开放 Mysql_Error: 2003: Can't connect to MySQL server on '35.164.6.48' (10060)
        r2 = e.find('Access denied')  # 端口开放但密码错误  Mysql_Error: 1045: Access denied for user 'root'@'localhost' (using password: YES)
        r3 = e.find('not allowed') #端口只允许特定ip连接  Mysql_Error: 1130: Host '172.17.14.2' is not allowed to connect to this MySQL server
        #r3 = e.find('Learn SQL!') #这限制特定了sql语句


        if (r1 != -1):
            #排除端口不开放的情况
            return

        elif(r2 != -1):
            #ip_log('port_opend.txt',ip, "密码错误")
            ip_log('port_opend.txt',ip, e)

        elif(r3 != -1):
            #ip_log('port_opend.txt', ip , "不允许该IP连接")
            ip_log('port_opend.txt', ip , e)
        else:
            #ip_log('port_opend.txt', ip, "其他错误")
            ip_log('port_opend.txt', ip, e)

        return



def ping_ip(ip):
    # 调用ping命令,如果不通，则会返回100%丢包的信息。通过匹配是否有100%关键字，判断主机是否存活

    cmd = 'ping -w 1 %s' % ip
    p = subprocess.Popen(cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)

    result = p.stdout.read()
    regex = result.find('100%')

    # 未匹配到就是-1，就是存活主机
    if (regex == -1):
        return 1
    else:
        return 0


def  ip_log(txt_name,ip,content):
    f1 = open(txt_name, 'a')
    f1.write(ip + " " + content + "\r\n")
    f1.close()


if __name__ == "__main__":

    start = time.time()

    #设置同时运行的线程数
    threads=150
    
    #要检测的IP网段
    ip1 = IPy.IP('192.168.0.0/16')



    for ip in ip1:    
        ip=str(ip)
        print ip

        while(threading.activeCount()>threads):
            time.sleep(1)
        t1=threading.Thread(target=mysql_connect1, args=(ip,))
        t1.start()

    #当线程只剩1时，说明执行完了
    while(threading.activeCount()!=1):
        time.sleep(5)

    print "检测结束"
