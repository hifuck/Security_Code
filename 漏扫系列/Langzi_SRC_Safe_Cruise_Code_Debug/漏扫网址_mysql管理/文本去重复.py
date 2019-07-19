# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun

import os
def run(name):
    lists = [x.strip() for x in open(name,'r',encoding='utf-8').readlines()]
    result = list(set(lists))
    try:
        os.remove(name)
    except:
        pass
    with open(name,'a+',encoding='utf-8') as a:
        for i in result:
            a.write(i+'\n')

    print('去重结束')
    os.system('pause')

if __name__ == '__main__':
    na = input('Input Yours Text:')
    run(na)