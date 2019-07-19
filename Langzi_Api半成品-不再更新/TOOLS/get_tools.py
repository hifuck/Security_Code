# coding:utf-8
import time
import base64
import chardet
from hashlib import *
from urllib import quote

def print_w(x):
    '''白色'''
    print time.strftime('[%H:%M:%S]  ',time.localtime()) + str(x)

def print_r(x):
    '''红色'''
    print time.strftime('[%H:%M:%S]  ',time.localtime()) + '\033[1;31m %s \033[0m'%str(x)

def print_g(x):
    '''绿色'''
    print time.strftime('[%H:%M:%S]  ',time.localtime()) + '\033[1;32m %s \033[0m'%str(x)

def print_y(x):
    '''黄色'''
    print time.strftime('[%H:%M:%S]  ',time.localtime()) + '\033[1;33m %s \033[0m'%str(x)

def print_b(x):
    '''蓝色'''
    print time.strftime('[%H:%M:%S]  ',time.localtime()) + '\033[1;34m %s \033[0m'%str(x)

def print_p(x):
    '''紫色'''
    print time.strftime('[%H:%M:%S]  ',time.localtime()) + '\033[1;35m %s \033[0m'%str(x)


def log(x):
    with open('log.txt','a+')as a:
        a.write(str(time.strftime('%Y-%m-%d:%H:%M:%S   ',time.localtime()))+str(x) + '\n')

class CODING:
    def __init__(self,data):
        self.data = str(data)
        #self.data = repr(data)
        self.res = []

    def hex_decode(self):
        try:
            return self.data.decode('hex')
        except:
            return None

    def ascii_decode(self):
        try:
            return map(ord,self.data)
        except:
            return None

    def url_decode(self):
        try:
            return quote(self.data)
        except:
            return None

    def base64_decode(self):
        try:
            return base64.b64encode(self.data)
        except:
            return None

    def md5_decode(self):
        try:
            m = md5()
            m.update(self.data)
            return m.hexdigest()
        except:
            return None


    def sha1_decode(self):
        try:
            m = sha1()
            m.update(self.data)
            return m.hexdigest()
        except:
            return None

    def chinese_decode(self):
        try:
            self.res.append(self.data.encode('utf-8'))
        except:
            pass
        try:
            self.res.append(self.data.encode('gbk'))
        except:
            pass
        try:
            self.res.append(self.data.encode('gb2312'))
        except:
            pass
        try:
            self.res.append(self.data.encode('ISO-8859'))
        except:
            pass
        try:
            self.res.append(self.data.encode('GB18030'))
        except:
            pass
        try:
            self.res.append(self.data.encode('cp936'))
        except:
            pass
        try:
            self.res.append(unicode(self.data,'utf-8'))
        except:
            pass
        try:
            code = chardet.detect(self.data)['encoding']
            self.res.append(self.data.encode(code))
        except:
            pass
        try:
            code = chardet.detect(self.data)['encoding']
            self.res.append(self.data.decode(code).encode('utf-8'))
        except:
            pass
        try:
            self.res.append(self.data.decode("unicode-escape"))
        except:
            pass
        try:
            self.res.append(self.data.decode("string-escape"))
        except:
            pass
        try:
            self.res.append(self.data.encode('ISO-8859'))
        except:
            pass
        return self.res


if __name__ == '__main__':
    print_w(113322335644)
    print_g('adadad')
