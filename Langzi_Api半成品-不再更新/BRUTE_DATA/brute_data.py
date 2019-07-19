# coding:utf-8
import re
import time
import pymysql
import pymssql
import psycopg2
import cx_Oracle
import telnetlib
import paramiko
paramiko.util.logging.getLogger('paramiko.transport').addHandler(paramiko.util.logging.NullHandler())
from ftplib import FTP
from smb.SMBConnection import SMBConnection
import socket
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 5
socket.setdefaulttimeout(timeout)

def brute_mssql(ip,username,password,port=1433):
    try:
        connx = pymssql.connect(server=str(ip), port=port, user=username, password=password)
        return ip + ':' + str(port) + '|' + username + ':' + password
    except:
        return None

def brute_mysql(ip,username,password,port=3306):
    try:
        connx = pymysql.connect(host=ip, user=username, passwd=password, db='mysql', port=port)
        return ip + ':' + str(port) + '|' + username + ':' + password
    except:
        return None



def brute_postql(ip,username,password,port=5432):
    try:
        connx = psycopg2.connect(host=ip, port=port, user=username, password=password)
        return ip + ':' + str(port) + '|' + username + ':' + password
    except:
        return None




def brute_oralce(ip,username,password,port=1521):
    try:
        connx = cx_Oracle.connect(username, password, ip + ':%s/orcl' % str(port))
        return ip + ':' + str(port) + '|' + username + ':' + password
    except:
        return None


def brute_ssh(ip,username,password,port=22):
    try:
        # telnetlib.Telnet(ip, 111, timeout=2)#判断额外端口的
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 跳过了远程连接中选择‘是’的环节,
        ssh.connect(ip, 22, '', '', timeout=timeout)
        ssh.close()
    except Exception as e:
        if 'Authentication' in str(e):  # 捕获所有的异常，根据返回信息，判断是否是ssh的，决定是否往下爆破。
            try:
                ssh.connect(ip, 22, username, password, timeout=timeout)
                # print(colored(ip + ' ' + us + ' ' + pa + ' ' + '连接成功~~~~~~~', 'red'))
                # open(outfile, 'a', encoding='utf-8').write(ip + ' ' + us + ' ' + pa + '\n')  # 成功了，就写入文本
                # data_text = ip + ' ' + us + ' ' + pa
                ssh.close()
                return ip + ':' + str(port) + '|' + username + ':' + password
            except Exception as e:
                #print e
                ssh.close()
        else:
            pass
            #print(ip, str(e))



def brute_ftp(ip,username,password,port=21):
    try:
        ftp = FTP(ip)
        ftp.connect(ip, port)
        ftp.login(username, password)
        if 'Not implemented' in ftp.dir():
            pass
        else:
            return ip + ':' + str(port) + '|' + username + ':' + password
        ftp.quit()
    except Exception, e:
        return None


def brute_telnet(ip,username,password,port=23):
    try:
        res = ''
        s = socket.socket()
        s.connect((str(ip), port))
        s.send('langzi \n')
        cc = s.recv(1024)
        s.close()
        if 'not allowed to' not in cc:
            tn = telnetlib.Telnet(ip,timeout=timeout)
            tn.set_debuglevel(5)
            time.sleep(0.5)
            oss = tn.read_some()
            s.close()
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
                        res = ip + ':' + str(port) + '|' + username + ':' + password
                except Exception, e:
                    pass
            else:
                try:
                    info = tn.read_until(user_match, timeout=2)
                except Exception, e:
                    pass
                if re.search(user_match, info):
                    try:
                        tn.write(username + '\r\n')
                        tn.read_until(pass_match, timeout=2)
                        tn.write(password + '\r\n')
                        login_info = tn.read_until(login_match, timeout=3)
                        tn.close()
                        if re.search(login_match, login_info):
                            res = ip + ':' + str(port) + '|' + username + ':' + password
                    except Exception, e:
                        pass
                elif re.search(pass_match, info):
                    tn.read_until(pass_match, timeout=2)
                    tn.write(password + '\r\n')
                    login_info = tn.read_until(login_match, timeout=3)
                    tn.close()
                    if re.search(login_match, login_info):
                        res = ip + ':' + str(port) + '|' + username + ':' + password
        else:
            pass
    except Exception ,e:
        pass

    if res == '':
        return None
    else:
        return res


def ip2hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except:
        pass
    try:
        query_data = "\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x20\x43\x4b\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x00\x00\x21\x00\x01"
        dport = 137
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.sendto(query_data, (ip, dport))
        x = _s.recvfrom(1024)
        tmp = x[0][57:]
        hostname = tmp.split("\x00", 2)[0].strip()
        hostname = hostname.split()[0]
        return hostname
    except:
        pass

def brute_smb(ip,username,password,port=445):
    try:
        hostname = ip2hostname(ip)
        if hostname:
            try:
                conn = SMBConnection(username,password, 'xunfeng', hostname)
                if conn.connect(ip) == True:
                    return ip + ':' + str(port) + '|' + username + ':' + password
            except Exception, e:
                return None
    except Exception, e:
        return None
