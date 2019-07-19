# -*- coding: utf-8 -*-
# python2
import multiprocessing
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import re
import requests
import random
import time
import masscan
import os
import struct
import socket, string, struct
from tinydb import TinyDB, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from collections import namedtuple

Port = namedtuple("Port", ["name", "port", "protocol", "description"])

__BASE_PATH__ = os.path.dirname(os.path.abspath(__file__))
__DATABASE_PATH__ = os.path.join(__BASE_PATH__, 'ports.json')
__DB__ = TinyDB(__DATABASE_PATH__, storage=CachingMiddleware(JSONStorage))


def get_ports(port, like=False):
    """
    This function creates the SQL query depending on the specified port and
    the --like option.

    :param port: the specified port
    :param like: the --like option
    :return: all ports matching the given ``port``
    :rtype: list
    """
    where_field = "port" if port.isdigit() else "name"
    if like:
        ports = __DB__.search(where(where_field).search(port))
    else:
        ports = __DB__.search(where(where_field) == port)
    try:
        return ports[0]  # flake8: noqa (F812)
    except:
        return []


headerss = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

# url,title,weights,ip,ages,whois_id,whois_type,whois_name,whois_time
# 网址，标题，百度权重，ip信息，年龄，备案号，备案性质，备案名称，备案时间
# include_baidu,request,text,service,language
# 百度收录，，协议类型，页面类型，服务器类型，程序语言
title_parrten = 'class="w61-0"><div class="ball">(.*?)</div></td>'  # group(1) 正常
ip_parrten = '>IP：(.*?)</a></div>'  # group(1) 正常
# 下面会报错
ages = '" target="_blank">(.*?)</a></div></div>'  # group(1)
whois_id = '备案号：</span><a href=.*?" target="_blank">(.*?)</a></div>'  # 需group(1)
whois_type = '<span>性质：</span><strong>(.*?)</strong></div>'  # 需group(1)
whois_name = '<span>名称：</span><strong>(.*?)</strong></div>'  # 需group(1)
whois_time = '<span>审核时间：</span><strong>(.*?)</strong></div>'  # 需group(1)
include_baidu = '<div class="Ma01LiRow w12-1 ">(.*?)</div>'  # group(1)
infos = '<div class="MaLi03Row w180">(.*?)</div>'  # 要findall 0，1，2，3


def get_baidu_weights(url):
    x = str(random.randint(1, 9))
    data = {
        't': 'rankall',
        'on': 1,
        'type': 'baidupc',
        'callback': 'jQuery111303146901980779846_154444474116%s' % (x),
        'host': url
    }

    headers = {

        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'UM_distinctid=165af67ee6f352-07238a34ed3941-9393265-1fa400-165af67ee70473; CNZZDATA5082706=cnzz_eid%3D832961605-1544438317-null%26ntime%3D1544443717; Hm_lvt_aecc9715b0f5d5f7f34fba48a3c511d6=1544443985; Hm_lpvt_aecc9715b0f5d5f7f34fba48a3c511d6=1544443985; qHistory=aHR0cDovL3JhbmsuY2hpbmF6LmNvbS9iYWlkdW1vYmlsZS8r55m+5bqm56e75Yqo5p2D6YeNfGh0dHA6Ly9yYW5rLmNoaW5hei5jb20vcmFua2FsbC8r5p2D6YeN57u85ZCI5p+l6K+ifGh0dHA6Ly9yYW5rLmNoaW5hei5jb20r55m+5bqm5p2D6YeN5p+l6K+ifGh0dHA6Ly9pbmRleC5jaGluYXouY29tLyvlhbPplK7or43lhajnvZHmjIfmlbB8aHR0cDovL3JhbmsuY2hpbmF6LmNvbS9yYW5rL2hpc3RvcnkuYXNweCvmnYPph43ljoblj7Lmn6Xor6I=',
        'Host': 'rank.chinaz.com',
        'Origin': 'http://rank.chinaz.com',
        'Referer': 'http://rank.chinaz.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'

    }
    try:
        urls = 'http://rank.chinaz.com/ajaxseo.aspx?t=rankall&on=1&type=undefined&callback=jQuery111303146901980779846_154444474116%s' % (
            x)

        r = requests.post(url=urls, headers=headers, data=data)
        try:
            res = re.search(',"br":(\d),"beforBr', r.content).group(1)
        except:
            pass
        if res:
            return res
        else:
            return '无权重'
    except:
        return '无权重'


class IPLocator:
    def __init__(self, ipdbFile):
        self.ipdb = open(ipdbFile, "rb")
        str = self.ipdb.read(8)
        (self.firstIndex, self.lastIndex) = struct.unpack('II', str)
        self.indexCount = (self.lastIndex - self.firstIndex) / 7 + 1

    def getVersion(self):
        s = self.getIpAddr(0xffffff00L)
        return s

    def getAreaAddr(self, offset=0):
        if offset:
            self.ipdb.seek(offset)
        str = self.ipdb.read(1)
        (byte,) = struct.unpack('B', str)
        if byte == 0x01 or byte == 0x02:
            p = self.getLong3()
            if p:
                return self.getString(p)
            else:
                return ""
        else:
            self.ipdb.seek(-1, 1)
            return self.getString(offset)

    def getAddr(self, offset, ip=0):
        self.ipdb.seek(offset + 4)
        countryAddr = ""
        areaAddr = ""
        str = self.ipdb.read(1)
        (byte,) = struct.unpack('B', str)
        if byte == 0x01:
            countryOffset = self.getLong3()
            self.ipdb.seek(countryOffset)
            str = self.ipdb.read(1)
            (b,) = struct.unpack('B', str)
            if b == 0x02:
                countryAddr = self.getString(self.getLong3())
                self.ipdb.seek(countryOffset + 4)
            else:
                countryAddr = self.getString(countryOffset)
            areaAddr = self.getAreaAddr()
        elif byte == 0x02:
            countryAddr = self.getString(self.getLong3())
            areaAddr = self.getAreaAddr(offset + 8)
        else:
            countryAddr = self.getString(offset + 4)
            areaAddr = self.getAreaAddr()
        return countryAddr + " " + areaAddr

    def dump(self, first, last):
        if last > self.indexCount:
            last = self.indexCount
        for index in range(first, last):
            offset = self.firstIndex + index * 7
            self.ipdb.seek(offset)
            buf = self.ipdb.read(7)
            (ip, of1, of2) = struct.unpack("IHB", buf)
            address = self.getAddr(of1 + (of2 << 16))
            # 把GBK转为utf-8
            address = unicode(address, 'gbk').encode("utf-8")
            print
            "%d\t%s\t%s" % (index, self.ip2str(ip), \
                            address)

    def setIpRange(self, index):
        offset = self.firstIndex + index * 7
        self.ipdb.seek(offset)
        buf = self.ipdb.read(7)
        (self.curStartIp, of1, of2) = struct.unpack("IHB", buf)
        self.curEndIpOffset = of1 + (of2 << 16)
        self.ipdb.seek(self.curEndIpOffset)
        buf = self.ipdb.read(4)
        (self.curEndIp,) = struct.unpack("I", buf)

    def getIpAddr(self, ip):
        L = 0
        R = self.indexCount - 1
        while L < R - 1:
            M = (L + R) / 2
            self.setIpRange(M)
            if ip == self.curStartIp:
                L = M
                break
            if ip > self.curStartIp:
                L = M
            else:
                R = M
        self.setIpRange(L)
        # version information,255.255.255.X,urgy but useful
        if ip & 0xffffff00L == 0xffffff00L:
            self.setIpRange(R)
        if self.curStartIp <= ip <= self.curEndIp:
            address = self.getAddr(self.curEndIpOffset)
            # 把GBK转为utf-8
            address = unicode(address, 'gbk').encode("utf-8")
        else:
            address = "未找到该IP的地址"
        return address

    def getIpRange(self, ip):
        self.getIpAddr(ip)
        range = self.ip2str(self.curStartIp) + ' - ' \
                + self.ip2str(self.curEndIp)
        return range

    def getString(self, offset=0):
        if offset:
            self.ipdb.seek(offset)
        str = ""
        ch = self.ipdb.read(1)
        (byte,) = struct.unpack('B', ch)
        while byte != 0:
            str = str + ch
            ch = self.ipdb.read(1)
            (byte,) = struct.unpack('B', ch)
        return str

    def ip2str(self, ip):
        return str(ip >> 24) + '.' + str((ip >> 16) & 0xffL) + '.' \
               + str((ip >> 8) & 0xffL) + '.' + str(ip & 0xffL)

    def str2ip(self, s):
        (ip,) = struct.unpack('I', socket.inet_aton(s))
        return ((ip >> 24) & 0xffL) | ((ip & 0xffL) << 24) \
               | ((ip >> 8) & 0xff00L) | ((ip & 0xff00L) << 8)

    def getLong3(self, offset=0):
        if offset:
            self.ipdb.seek(offset)
        str = self.ipdb.read(3)
        (a, b) = struct.unpack('HB', str)
        return (b << 16) + a


def get_ip_address(ip):
    IPL = IPLocator("qqwry.dat")
    address = IPL.getIpAddr(IPL.str2ip(ip))
    return address


def get_ipinfomation(lis):
    # 该函数的作用是传入一个列表
    infos_ = []
    for ip in lis:
        d = get_ports(str(ip))
        if d != []:
            infos_.append('\n端口:' + str(ip) + '\n服务:' + str(d['name']) + '\n功能:' + str(d['description']) + '\n')
        else:
            infos_.append(str(ip) + ':' + str('识别失败') + '\n')

    return infos_


def get_ips(ip):
    url_ip = ip
    url_port = []
    try:
        mas = masscan.PortScanner()
        mas.scan(url_ip)
        url_port = mas.scan_result['scan'][url_ip]['tcp'].keys()
    except:
        url_port = [80]

    if 80 in url_port:
        pass
    else:
        url_port.append(80)

    try:
        infos = {}
        infos['开放端口'] = str(url_port)
        infos['端口信息'] = str(get_ipinfomation(url_port))
        return infos
    except Exception, e:
        print
        e


def get_info(pattren, result):
    try:
        res = re.search(pattren, result).group(1)
        return res
    # return str(res.encode('utf-8'))
    except:
        return '暂无信息'


import socket


def iiip(url):
    try:
        return socket.gethostbyname(
            url.replace('https://', '').replace('http://', '').replace('/', '').replace('www.', ''))
    except:
        return '获取失败'


def scan_seo(url):
    print
    'Scan : ' + url
    UA = random.choice(headerss)
    headers = {'User-Agent': UA}
    urls = 'http://seo.chinaz.com/' + url.replace('https://', '').replace('http://', '').replace('/', '').replace(
        'www.', '')
    # url,title,weights,ip,ages,whois_id,whois_type,whois_name,whois_time
    # 网址，标题，百度权重，ip信息，年龄，备案号，备案性质，备案名称，备案时间
    # include_baidu,request,text,service,language
    # 百度收录，，协议类型，页面类型，服务器类型，程序语言
    res = {}
    try:
        r = requests.get(urls, headers, timeout=20).content
    except Exception, e:
        print
        e
        return False
    res['百度权重'] = str(get_baidu_weights(url))
    res['网站网址'] = url
    res['网站标题'] = get_info(title_parrten, r)
    ip_infos = get_info(ip_parrten, r)
    if '[' in ip_infos:
        ip, address = ip_infos.split('[')[0], ip_infos.split('[')[1]
        ress = get_ips(ip)
        res['IP__坐标'] = address.replace(']', '')
        res['所属__IP'] = ip
        res.update(ress)
    else:
        res['所属__IP'] = iiip(url)
        if res['所属__IP'] == '获取失败':
            res['IP__坐标'] = '获取失败'
            res['开放端口'] = '[80]'
            res['端口信息'] = '["获取失败"]'
        else:
            res['IP__坐标'] = get_ip_address(res['所属__IP'])
            ress = get_ips(res['所属__IP'])
            res.update(ress)

    res['网站年龄'] = get_info(ages, r)
    res['备案编号'] = get_info(whois_id, r)
    res['备案性质'] = get_info(whois_type, r)
    res['备案名称'] = get_info(whois_name, r)
    res['备案时间'] = get_info(whois_time, r)
    res['百度收录'] = get_info(include_baidu, r)

    dd = re.findall(infos, r, re.S)
    resu = ['暂无信息' if x.replace(' ', '') is '' else x for x in dd]
    try:
        res['协议类型'] = resu[0]
    except:
        res['协议类型'] = '获取失败'

    try:
        res['页面类型'] = resu[1]
    except:
        res['页面类型'] = '获取失败'

    try:
        res['服务类型'] = resu[2]
    except:
        res['服务类型'] = '获取失败'

    try:
        res['程序语言'] = resu[3]
    except:
        res['程序语言'] = '获取失败'

    return res


def run(url):
    result = scan_seo(url)
    if result == False:
        return None

    title = result['网站标题']
    try:
        with open('result/' + title.decode('utf-8') + '__InforMationReport.txt', 'a+')as a:
            a.write('                             【 网站信息 】 \n')
            a.write('【网站网址】 ' + result['网站网址'] + '\n')
            a.write('【网站标题】 ' + result['网站标题'] + '\n')
            a.write('【百度权重】 ' + result['百度权重'] + '\n')
            a.write('【网站年龄】 ' + result['网站年龄'] + '\n')
            a.write('【所属__IP】 ' + result['所属__IP'] + '\n')
            a.write('【IP__坐标】 ' + result['IP__坐标'] + '\n')
            a.write('【页面类型】 ' + result['页面类型'] + '\n')
            a.write('【服务类型】 ' + result['服务类型'] + '\n')
            a.write('【程序语言】 ' + result['程序语言'] + '\n')
            a.write('【开放端口】 ' + result['开放端口'] + '\n')
            a.write('【端口信息】 ' + '\n')
            ds = eval(result['端口信息'])
            for x in ds:
                a.write(x + '\n')
            a.write('【备案编号】 ' + result['备案编号'] + '\n')
            a.write('【备案性质】 ' + result['备案性质'] + '\n')
            a.write('【备案名称】 ' + result['备案名称'] + '\n')
            a.write('【备案时间】 ' + result['备案时间'] + '\n')
            a.write('【百度收录】 ' + result['百度收录'] + '\n')
    except:
        with open('result/' + url.replace('https://', '').replace('http://', '').replace('/', '').replace('www.',
                                                                                                          '') + '__InforMationReport.txt',
                  'a+')as a:
            a.write('                             【 网站信息 】 \n')
            a.write('【网站网址】 ' + result['网站网址'] + '\n')
            a.write('【网站标题】 ' + result['网站标题'] + '\n')
            a.write('【百度权重】 ' + result['百度权重'] + '\n')
            a.write('【网站年龄】 ' + result['网站年龄'] + '\n')
            a.write('【所属__IP】 ' + result['所属__IP'] + '\n')
            a.write('【IP__坐标】 ' + result['IP__坐标'] + '\n')
            a.write('【页面类型】 ' + result['页面类型'] + '\n')
            a.write('【服务类型】 ' + result['服务类型'] + '\n')
            a.write('【程序语言】 ' + result['程序语言'] + '\n')
            a.write('【开放端口】 ' + result['开放端口'] + '\n')
            a.write('【端口信息】 ' + '\n')
            ds = eval(result['端口信息'])
            for x in ds:
                a.write(x + '\n')
            a.write('【备案编号】 ' + result['备案编号'] + '\n')
            a.write('【备案性质】 ' + result['备案性质'] + '\n')
            a.write('【备案名称】 ' + result['备案名称'] + '\n')
            a.write('【备案时间】 ' + result['备案时间'] + '\n')
            a.write('【百度收录】 ' + result['百度收录'] + '\n')


if __name__ == '__main__':
    if os.path.exists('result'):
        pass
    else:
        os.mkdir('result')

    print('''
             _                           _
            | |                         (_)
            | |     __ _ _ __   __ _ _____
            | |    / _` | '_ \ / _` |_  / |
            | |___| (_| | | | | (_| |/ /| |
            |______\__,_|_| |_|\__, /___|_|
                                __/ |
                               |___/

    ''')

    time.sleep(1)
    print unicode('     LangZi 一键信息综合查询', 'utf-8')
    time.sleep(1)
    New_start = raw_input(unicode('导入网址文本(可拖拽):', 'utf-8').encode('gbk'))  # line:190
    New_start = New_start.replace('"', '').replace("'", '')
    list_ = list(set(
        [x.replace('\n', '') if x.startswith('http') else 'http://' + x.replace('\n', '') for x in
         open(New_start, 'r').readlines()]))
    for u in list_:
        run(u)
        time.sleep(random.randint(1, 5))