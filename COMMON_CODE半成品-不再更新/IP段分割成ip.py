#coding:utf-8
import time
def c2ip(x):
    if ' ' in x:
        a,b = x.split(' ',1)[0],x.split(' ',1)[1]
        a1,a2,a3,a4 = int(a.split('.')[0]),int(a.split('.')[1]),int(a.split('.')[2]),int(a.split('.')[3])
        b1,b2,b3,b4 = int(b.split('.')[0]),int(b.split('.')[1]),int(b.split('.')[2]),int(b.split('.')[3])
    if '-' in x:
        a,b = x.split('-',1)[0],x.split('-',1)[1]
        a1,a2,a3,a4 = int(a.split('.')[0]),int(a.split('.')[1]),int(a.split('.')[2]),int(a.split('.')[3])
        b1,b2,b3,b4 = int(b.split('.')[0]),int(b.split('.')[1]),int(b.split('.')[2]),int(b.split('.')[3])
    try:
        if a1 > b1:
            b1 = a1
        if a2 > b2:
            b2 = a2
        if a3 > b3:
            b3 = a3
        if a4 > b4:
            b4 = a4
        for c1 in range(a1,b1+1):
            if c1 == b1 + 1:
                e1 = b1 +1
            else:
                e1 = 256
            for c2 in range(a2,e1):
                if c1 == b1 + 1:
                    e1 = b1 + 1
                else:
                    e1 = 256
                for c3 in range(a3,e1):
                    for c4 in range(0,b4):
                        dd = str(c1) + '.' + str(c2) + '.' + str(c3) + '.' + str(c4)
                        with open(filename,'a+')as a:
                            a.write(dd + '\n')
    except Exception,e:
        print e
'''
传入的参数是这样的 127.0.0.1 127.0.0.5
'''
filename = time.strftime('%y-%m-%d-%H-%M-%S',time.localtime()) + '.txt'

if __name__ == '__main__':
    print ('''

             _                           _ 
            | |                         (_)
            | |     __ _ _ __   __ _ _____ 
            | |    / _` | '_ \ / _` |_  / |
            | |___| (_| | | | | (_| |/ /| |
            |______\__,_|_| |_|\__, /___|_|
                                __/ |      Langzi_C2IP
                               |___/       Version:1.0
                                           Datetime:2018年11-27-12:42:43

    ''')
    print unicode('             C段批量转换成具体IP地址', 'utf-8')
    print unicode('             支持如下格式', 'utf-8')
    print unicode('''
       ip段的数据可以是这样

        127.0.0.1 128.100.100.100
        127.5.1.2 199.12.2.1
    
        也可以是这样
    
        127.0.0.1-128.100.100.100
        127.5.1.2-199.12.2.1 
    ''', 'utf-8')


    New_start = raw_input(unicode('待需转换C段文本拖拽进来:', 'utf-8').encode('gbk'))
    list_ = list(set([x.replace('\n', '') for x in open(New_start, 'r').readlines()]))
    print 'Waiting.......'
    for u in list_:
        c2ip(u)




