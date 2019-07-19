# coding:utf-8

import os
import masscan
import whatportis
import socket, struct
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 3
socket.setdefaulttimeout(timeout)


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
            print "%d\t%s\t%s" % (index, self.ip2str(ip), \
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



def get_ip_ports(ip):
    try:
        mas = masscan.PortScanner()
        mas.scan(ip)
        url_port = mas.scan_result['scan'][ip]['tcp'].keys()
        if url_port == [] or url_port == None or url_port == '':
            return None
        else:
            return url_port
    except Exception,e:
        return None


def get_ip_address(ip):
    if os.path.exists('Langzi_Api'):
        dat = os.getcwd() + '\Langzi_Api\GET_IP\qqwry.dat'
    else:
        dat = sys.prefix + '\Lib\site-packages\Langzi_Api\GET_IP\qqwry.dat'
    IPL = IPLocator(dat)
    address = IPL.getIpAddr(IPL.str2ip(ip))
    return address

if __name__ == '__main__':
    IPL = IPLocator('qqwry.dat')
    address = IPL.getIpAddr(IPL.str2ip('123.121.123.121'))
    address = unicode(address,'utf-8')
    print address

    print address[:2]
    # res = get_ip_ports('118.24.11.235')
    # print res

