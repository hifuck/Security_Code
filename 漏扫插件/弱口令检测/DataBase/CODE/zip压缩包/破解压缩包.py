# -*- coding: utf-8 -*-
# @Time    : 2018/4/28 0028 11:49
# @Author  : Langzi
# @Blog    : www.langzi.fun
# @File    : 破解压缩包.py
# @Software: PyCharm
import sys
import zipfile
from multiprocessing.dummy import  Pool as tp
import time
reload(sys)
import os
sys.setdefaultencoding('utf-8')
list_pass=list(set([i.replace("\n", "") for i in open("password.txt", "r").readlines()]))
# 破解的字典名为password.txt
zip_=raw_input("set zip file:")
zname = os.path.join(os.getcwd(),zip_)
print zname
zFile = zipfile.ZipFile(zname)
def scan(passw):
    try:
        zFile.extractall(pwd=passw)
        print '[+] Found password ' + passw + '\n'
        time.sleep(50)
    except Exception,e:
        pass
pool = tp(processes=8)
pool.map(scan,list_pass)
pool.close()
pool.join()
