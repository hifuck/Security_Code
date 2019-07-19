# coding:utf-8

import re
import os
import requests
import time
import socket
from bs4 import BeautifulSoup as bs
import chardet
from cms_db import cms_rule
from config import headerss
import random
import hashlib
import masscan
import whatportis
import socket,string,struct
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 3
socket.setdefaulttimeout(timeout)
from requests.packages import urllib3
urllib3.disable_warnings()
# ports = [
#     21,
#     22,
#     23,
#     25,
#     53,
#     69,
#     139,
#     445,
#     389,
#     1433,
#     1521,
#     2181,
#     3306,
#     3389,
#     5432,
#     5984,
#     6379,
#     7001,
#     7002,
#     8069,
#     11211,
#     27017,
#     27018,
#     50070,
#     50030
# ]


class IPLocator :
    def __init__( self, ipdbFile ):
        self.ipdb = open( ipdbFile, "rb" )
        str = self.ipdb.read( 8 )
        (self.firstIndex,self.lastIndex) = struct.unpack('II',str)
        self.indexCount = (self.lastIndex - self.firstIndex)/7+1
        #print self.getVersion()," 纪录总数: %d 条 "%(self.indexCount)

    def getVersion(self):
        s = self.getIpAddr(0xffffff00L)
        return s

    def getAreaAddr(self,offset=0):
        if offset :
            self.ipdb.seek( offset )
        str = self.ipdb.read( 1 )
        (byte,) = struct.unpack('B',str)
        if byte == 0x01 or byte == 0x02:
            p = self.getLong3()
            if p:
                return self.getString( p )
            else:
                return ""
        else:
            self.ipdb.seek(-1,1)
            return self.getString( offset )

    def getAddr(self,offset,ip=0):
        self.ipdb.seek( offset + 4)
        countryAddr = ""
        areaAddr = ""
        str = self.ipdb.read( 1 )
        (byte,) = struct.unpack('B',str)
        if byte == 0x01:
            countryOffset = self.getLong3()
            self.ipdb.seek( countryOffset )
            str = self.ipdb.read( 1 )
            (b,) = struct.unpack('B',str)
            if b == 0x02:
                countryAddr = self.getString( self.getLong3() )
                self.ipdb.seek( countryOffset + 4 )
            else:
                countryAddr = self.getString( countryOffset )
            areaAddr = self.getAreaAddr()
        elif byte == 0x02:
            countryAddr = self.getString( self.getLong3() )
            areaAddr = self.getAreaAddr( offset + 8 )
        else:
            countryAddr = self.getString( offset + 4 )
            areaAddr = self.getAreaAddr()
        return countryAddr + " " + areaAddr

    def dump(self, first ,last ):
        if last > self.indexCount :
            last = self.indexCount
        for index in range(first,last):
            offset = self.firstIndex + index * 7
            self.ipdb.seek( offset )
            buf = self.ipdb.read( 7 )
            (ip,of1,of2) = struct.unpack("IHB",buf)
            address = self.getAddr( of1 + (of2 << 16) )
            #把GBK转为utf-8
            address = unicode(address,'gbk').encode("utf-8")
            print "%d\t%s\t%s" %(index, self.ip2str(ip), \
                address )

    def setIpRange(self,index):
        offset = self.firstIndex + index * 7
        self.ipdb.seek( offset )
        buf = self.ipdb.read( 7 )
        (self.curStartIp,of1,of2) = struct.unpack("IHB",buf)
        self.curEndIpOffset = of1 + (of2 << 16)
        self.ipdb.seek( self.curEndIpOffset )
        buf = self.ipdb.read( 4 )
        (self.curEndIp,) = struct.unpack("I",buf)

    def getIpAddr(self,ip):
        L = 0
        R = self.indexCount - 1
        while L < R-1:
            M = (L + R) / 2
            self.setIpRange(M)
            if ip == self.curStartIp:
                L = M
                break
            if ip > self.curStartIp:
                L = M
            else:
                R = M
        self.setIpRange( L )
        #version information,255.255.255.X,urgy but useful
        if ip&0xffffff00L == 0xffffff00L:
            self.setIpRange( R )
        if self.curStartIp <= ip <= self.curEndIp:
            address = self.getAddr( self.curEndIpOffset )
            #把GBK转为utf-8
            address = unicode(address,'gbk').encode("utf-8")
        else:
            address = "未找到该IP的地址"
        return address

    def getIpRange(self,ip):
        self.getIpAddr(ip)
        range = self.ip2str(self.curStartIp) + ' - ' \
            + self.ip2str(self.curEndIp)
        return range

    def getString(self,offset = 0):
        if offset :
            self.ipdb.seek( offset )
        str = ""
        ch = self.ipdb.read( 1 )
        (byte,) = struct.unpack('B',ch)
        while byte != 0:
            str = str + ch
            ch = self.ipdb.read( 1 )
            (byte,) = struct.unpack('B',ch)
        return str

    def ip2str(self,ip):
        return str(ip>>24)+'.'+str((ip>>16)&0xffL)+'.' \
            +str((ip>>8)&0xffL)+'.'+str(ip&0xffL)

    def str2ip(self,s):
        (ip,) = struct.unpack('I',socket.inet_aton(s))
        return ((ip>>24)&0xffL)|((ip&0xffL)<<24) \
            |((ip>>8)&0xff00L)|((ip&0xff00L)<<8)

    def getLong3(self,offset = 0):
        if offset :
            self.ipdb.seek( offset )
        str = self.ipdb.read(3)
        (a,b) = struct.unpack('HB',str)
        return (b << 16) + a


class Get_Info:
    def __init__(self,url):
        self.url = url

    def get_ip(self):
        hostname = self.url.replace('http://','').replace('https://','').replace('/','')
        url_ip = 'None'
        try:
            url_ip= socket.gethostbyname(str(hostname))
        except:
            pass
        return url_ip


    def get_ipinfomation(self,*args):
        infos_ = []
        for x in args:
            for xx in x:
                d = whatportis.get_ports(str(xx))
                if d != []:
                    infos_.append(str(xx) + ':' + str(d[0][3]))
                else:
                    infos_.append(str(xx) + ':' + str('识别失败'))
        return infos_

    '''
    
    这个函数作用是接受一个列表,列表内是端口
    然后通过whatportis返回端口对应的服务
    返回内容如下：
        [80:http,3389:rdp]
        
    '''
    def get_ips(self):
        hostname = self.url.replace('http://','').replace('https://','').replace('/','')
        url_ip = 'None'
        try:
            url_ip= socket.gethostbyname(str(hostname))
        except:
            pass
        if url_ip and url_ip!= 'None':
            mas = masscan.PortScanner()
            mas.scan(url_ip)
            url_port = [80]
            url_port = mas.scan_result['scan'][url_ip]['tcp'].keys()
            if 80 in url_port:
                pass
            else:
                url_port.append(80)
            #for port in ports:
                # s = socket.socket()
                # try:
                #     s.connect((url_ip,port))
                #     url_port.append(port)
                # except Exception,e:
                #     # print e
                #     pass
                # finally:
                #     s.close()
        if url_ip or url_ip != 'None':
            infos = {}
            infos['ip'] = str(url_ip)
            infos['ports_open'] = str(url_port)
            infos['ports_info'] = str(self.get_ipinfomation(url_port))
            IPL = IPLocator("qqwry.dat")
            address = IPL.getIpAddr(IPL.str2ip(str(url_ip)))
            infos['ports_address'] = address
            return infos
        else:
            infos = {}
            infos['ip'] = '获取失败'
            infos['ports_open'] = '获取失败'
            infos['ports_info'] = '获取失败'
            infos['ports_address'] = '获取失败'
            return infos
    '''
    
    这个函数作用是把url转换成ip，然后用masscan扫描这个ip的全部端口
    返回一个字典，给字典有4个属性
    分别是 ip 端口 端口与对应的服务 以及位置坐标
    返回内容如下：
    
    {
        'ip':'127.0.0.1',
        'ports_open':'[80,3389]',
        'ports_info':'[80:http,3389:rdp]',
        'ports_address':'中国'
        
            }
    
    '''
    def get_infos(self):
        try:
            UA = random.choice(headerss)
            headers = {'User-Agent': UA}
            r = requests.get(url=self.url,headers=headers,verify=False,timeout=5)
            url_title,url_content,url_service = '获取失败','获取失败','获取失败'
            try:
                code = chardet.detect(r.content)['encoding']
                bp = bs(r.content.decode(code).encode('utf-8'),'html.parser')
                url_title = bp.title.string
                # url_contents = bp.text
                try:
                    url_service = r.headers['Server']
                except:
                    url_service = '获取失败'
            except:
                url_title = re.search('<title>(.*?)</title>',r.content,re.I).group(1).decode(code).encode('utf-8')
                #url_content = re.sub('([\.\?\*~!@#{$%\^&\*()-;"<>\[\]}_\+=]|[0-9]|[a-z]|[A-Z])','',r.text)
                try:
                    url_service = r.headers['Server']
                except:
                    url_service = '获取失败'
            infos = {}
            infos['url'] = self.url
            infos['title'] = url_title
            url_contents = ''.join(r.text.split()).replace(' ','').replace('\r\n','').replace('\r','')
            infos['content'] = re.sub('([\.\?\*~!@#{$%\^&\*()-;"<>\[\]}_\+=])','',url_contents).replace('|','').replace("'",'')
            # 下面这行的代码会过滤掉所有的英文和数字
            #infos['content'] = re.sub('([\.\?\*~!@#{$%\^&\*()-;"<>\[\]}_\+=]|[0-9]|[a-z]|[A-Z])','',url_contents).replace('|','').replace("'",'')
            infos['service'] = url_service
            if infos:
                return infos
            else:
                infos = {}
                infos['url'] = self.url
                infos['title'] = '获取失败'
                infos['content'] = '获取失败'
                infos['service'] = '获取失败'
                return infos
        except Exception,e:
            #print e
            infos = {}
            infos['url'] = self.url
            infos['title'] = '获取失败'
            infos['content'] = '获取失败'
            infos['service'] = '获取失败'
            return infos

        '''
        
        返回内容如下：
        {
        'url':'http://www.langzi.fun',
        'title':'浪子博客'，
        'content':'xaffa网页内容xafgasdas',
        'service':'Apache'
        }
        
        '''


    def get_urls(self):
        urlss = []
        live_urls = []
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        try:
            r = requests.get(url=self.url, headers=headers, verify=False, timeout=5)
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.I)
            urls = re.findall(pattern,r.content)
            for x in urls:
                a1, a2 = x.split('//')[0], x.split('//')[1].split('/')[0]
                a3 = ''.join(a1) + '//' + ''.join(a2)
                urlss.append(a3.replace("'","").replace('>','').replace('<',''))
            if urlss:
                for _ in list(set(urlss)):
                    UA = random.choice(headerss)
                    headers = {'User-Agent': UA}
                    try:
                        rr = requests.head(url=_,headers=headers,timeout=5,verify=False)
                        if rr.status_code == 200:
                            live_urls.append(_)
                        else:
                            pass
                    except:
                        pass
                return live_urls
            else:
                return None
        except Exception,e:
            #print e
            pass

    def get_cms(self):
        resu = {}
        for cmsxx in cms_rule:
            cmshouzhui = cmsxx.split('|', 3)[0]
            cmsmd5 = cmsxx.split('|', 3)[2]
            cmsname = cmsxx.split('|', 3)[1]
            urlcms = self.url + str(cmshouzhui)
            try:
                UA = random.choice(headerss)
                headers = {'User-Agent': UA}
                req1 = requests.head(url=urlcms, headers=headers, timeout=3, allow_redirects=False)
                if req1.status_code == 200:
                    req1_2 = requests.get(url=urlcms, headers=headers, timeout=3, allow_redirects=False)
                    md5 = hashlib.md5()
                    md5.update(req1_2.content)
                    rmd5 = md5.hexdigest()
                    if rmd5 == cmsmd5:
                        resu['cms'] = cmsname
                        return resu
                    else:
                        pass
                else:
                    pass
            except Exception,e:
                resu['cms'] = 'None'
                return resu

def get_really(url):
    try:
        d = Get_Info(url)
        d1 = d.get_infos()
        '''
        url
        content  获取失败
        title
        service
        '''
        d1['ip'] = str(url.replace('https://','').replace('http://','').split(':')[0])
        return d1
    except Exception,e:
        print e


'''

其实下面的函数可以包括在一个类里面
但是后面两个生成数据我是在最后才想起来的
为了不修改主程序中的代码只能继续挖坑了....

'''
def write_data(name,datas):
    try:
        with open(name,'a+')as a:
            try:
                for x in datas:
                    a.write(x + '\n')
            except:
                a.write(datas)
    except Exception,e:
        pass


def read_data(name):
    try:
        if os.path.exists(name):
            a = open(name).readlines()
            return a
    except Exception,e:
        pass


def remove_data(dir):
    try:
        dirs = os.listdir(dir)
        for x in dirs:
            os.remove(x)
    except:
        pass

    '''
    
    
    类方法调用（当前目录下有qqwry.dat 纯真数据库）：
        
        1. 传入一个ip 获取他的坐标
            IPL = IPLocator( "qqwry.dat" )
            ip = "127.0.0.1"
            address = IPL.getIpAddr( IPL.str2ip(ip) )
            print "%s 属于 %s" % (ip,address)
            
        2. 传入一个网址，获取他的信息
        
        inf = Get_Info(url='http://www.langzi.fun')
        d = inf.get_ips()
        
        2.1 返回对象是一个字典，内容大致如下：
                {
                    'ip':'127.0.0.1',
                    'ports_open':'[80,3389]',
                    'ports_info':'[80:http,3389:rdp]',
                    'ports_address':'中国'
                        
                 }
         
        2.2 传入对象是一个列表，列表内容是端口号，返回对象是一个列表
        d1 = inf.get_ipinfomation([80,110,3389])
        内容大致如下：

                    [80:http,3389:rdp]
        
        2.3 返回的是一个字典获取网址信息
        d2 = inf.get_infos()
        内容如下：
        
                        {
                        'url':'http://www.langzi.fun',
                        'title':'浪子博客'，
                        'content':'xaffa网页内容xafgasdas',
                        'service':'Apache'
                        }
        
        2.4 获取所有友链
        
        d3 = inf.get_urls()
        
        返回对象是一个列表，内容是inf初始化传入网址的所有友链

        2.5 获取cms类型
        
        d4 = inf.get_cms()
        
        返回对象是识别出cms的名字，类型是字典，如果没识别数来就返回None
        
        2.6 单纯的接受网址返回IP
        
        d5 = inf.get_ip()
        
        直接返回ip地址
    
    '''


# CODE DEOM RUN
# d = Get_Info('http://www.langzi.fun')
# d1 = d.get_cms()
# print 'cms:' + str(d1)
#
# d2 = d.get_ips()
# print 'ips:' + str(d2)
#
# d3 = d.get_infos()
# print 'info:' + str(d3)
#
# d4 = d.get_urls()
# print 'urls:' + str(d4)

# IPL = IPLocator("qqwry.dat")
# ip = "127.0.0.1"
# address = IPL.getIpAddr(IPL.str2ip(ip))
# print "%s 属于 %s" % (ip, address)


# url = 'http://hotel.tuniu.com'
#
# d = Get_Info(url)
# d1 = d.get_infos()
# for x,y in d1.iteritems():
#     print x,':',y
