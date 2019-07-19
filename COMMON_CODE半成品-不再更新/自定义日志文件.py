# coding:utf-8
# 传入可以是列表或者字符串
import time
def log(*args):
    with open('log.txt', 'a+')as aa:
        for x in args:
            aa.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ':' + x + '\n')