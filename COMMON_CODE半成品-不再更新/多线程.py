# coding:utf-8
'''

方法1 使用threading

'''

import threading
import time
def loog(x):
    print x
    print threading.current_thread().name
    # 线程名字

    time.sleep(0.5)


'''

方法2 使用multiprocessing.dummy

'''

from multiprocessing.dummy import Pool as p
list_ = [x for x in range(100)]

if __name__ =='__main':
    px = p(processes=20)
    px.apply(loog,args=())
    px.map(loog,list_)
    px.close()
    px.join()