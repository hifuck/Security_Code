# coding:utf-8

import multiprocessing

'''

方法1 进程池

'''

def loop(x):
    print x

list_ = [x for x in range(100)]
if __name__ == '__main__':
    p = multiprocessing.Pool(8)
    for x in list_:
        p.apply_async(loop,args=(x,))
        #p.apply_async(func=loop,args=(x,))
    p.close()
    p.join()

