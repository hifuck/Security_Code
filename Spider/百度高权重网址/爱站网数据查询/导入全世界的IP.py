# -*- coding: utf-8 -*-
# @Time    : 2018/5/5 0005 21:22
# @Author  : Langzi
# @Blog    : www.langzi.fun
# @File    : 导入全世界的IP.py
# @Software: PyCharm
import sys
import pymysql
import threading
import ConfigParser
import time
reload(sys)
sys.setdefaultencoding('utf-8')
cfg = ConfigParser.ConfigParser()
cfg.read('Config.ini')
user = cfg.get("Server", "username")
passwd = cfg.get("Server", "password")
host = cfg.get("Server", "host")
Dbname = cfg.get("Server","db")
thread_s = cfg.get("Config","thread_s")
list_ip=list(set([i.replace('\n','')for i in open('c.txt','r').readlines()]))
def start():
    for i in list_ip:
        print '[+] Insert : ' + str(i)
        try:
            timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            coon_svn = pymysql.connect(user=user, passwd=passwd, host=host, db=Dbname, charset='utf8')
            cur_svn = coon_svn.cursor()
            sql_svn = "INSERT INTO indexx(ip,ipget,datatime) VALUES (%s,%s,%s)"
            cur_svn.execute(sql_svn, (str(i), str(0), str(timenow)))
            coon_svn.commit()
            cur_svn.close()
            coon_svn.close()
        except Exception,e:
            print e
t = threading.Thread(target=start)
