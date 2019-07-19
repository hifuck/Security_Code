# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import requests
from concurrent.futures import ThreadPoolExecutor
import time

def run(url):
    try:
        r = requests.get(url, timeout=20)
        print('{} : {}'.format(r.url, r.status_code))
        if b'name="pma_username"' in r.content:
            print('网址:{} 发现PHPMYADMIN后台地址'.format(url))
            with open('phpmyadmin_url.txt', 'a+')as a:
                a.write(r.url + '\n')
    except:
        pass


if __name__ == '__main__':
    urls = [x.strip() + '/phpmyadmin/index.php' for x in open('url.txt', 'r').readlines()]
    start_time = time.time()
    with ThreadPoolExecutor(200)as p:
        p.map(run, urls)
    print('总共耗时: {} 扫描网址个数: {}'.format(time.time()-start_time),len(urls))