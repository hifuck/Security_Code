# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun

import os
def run(name,count):
    lists = [x.strip()+'\n' for x in open(name,'r',encoding='utf-8').readlines()]
    result = list(set(lists))
    start_counts = len(result)//count
    print('目标总行数: {} 将切割成: {} 份，每份: {} 行'.format(len(result),count,start_counts))
    for i in range(count+1):
        with open(name.replace('.txt','_'+str(i)+'.txt'),'a+',encoding='utf-8') as a:
            a.writelines(result[start_counts*i:start_counts*(i+1)])

    print('去重结束')
    #os.system('pause')

if __name__ == '__main__':
    na = input('Input Yours Text:')
    cou = int(input('Set How much target:'))
    run(na,cou)