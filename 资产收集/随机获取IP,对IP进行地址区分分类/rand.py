# coding:utf-8
import random
import os
import threading
import time
New_start = int(raw_input(unicode('设置随机获取IP个数:', 'utf-8').encode('gbk')))
#New_start = int(('设置随机获取IP个数:').encode('utf-8'))

result = set()

def rand(x, y):
    return str(random.randint(x, y))

def go(New_start):
    for n in range(New_start+1):
        A = rand(1,254)
        if A == '127':
            A = rand(129,254)
            if A == '192':
                A = rand(1, 125)

        res = A + '.' + rand(1, 254) + '.' + rand(1, 254) + '.' + rand(1, 254)+'\n'
        result.add(res)
        #print((threading.current_thread().name) + str(n) + ':数据:' + res)
try:
    os.remove('ip.txt')
except:
    pass
t = threading.Thread(target=go,args=(New_start,),name='当前生成数据子线程:')
t.start()
t.join()

filename = str(time.time())+'.txt'
with open(filename, 'a+')as a:
    a.writelines(result)

os.system('pause')
