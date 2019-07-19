# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3', 'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Cache-Control': 'max-age=0', 'referer': 'http://www.soso.com', 'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3'}
backup_suffix = ['.rar', '.zip', '.tar', '.tar.bz2', '.sql', '.7z', '.bak',  '.tar.gz','.gz',]
def get_title(url):
    title = '获取失败'
    try:
        r = requests.get(url,headers=headers)
        titles = re.search(b'<title>(.*?)</title>',r.content,re.S).group(1)
        title = titles.decode()
    except:
        pass
    finally:
        return title

def scan(url):
    try:
        r = requests.head(url,headers=headers,timeout=3)
        if (r.headers.get("Content-Length")):
            print('当前检测:{}'.format(url))
            print(r.headers.get("Content-Length"))
            if int(r.headers.get("Content-Length")) > 1500000:
                print('存在注入!!!!!!!!!!!!!!!!!!')
                return '{} ：{} ：{}'.format(str(get_title(url.split('//')[0] + url.split('//')[1].split('/')[0])),url,str(int(r.headers["Content-Length"]) / 1000000) + 'M')
    except Exception as e:
        #print(e)
        pass
def write_data(content):
    with open('vlun-result.txt','a+',encoding='utf-8')as a:
        a.write(content+'\n')

def run(urls):
    print(urls)
    res1 = scan(urls)
    if res1:
        write_data(res1)
    # url = urls.split('//')[0] + urls.split('//')[1].split('/')[0]
    # lis = []
    # k1 = url.split('//')[1]
    # # www.langzi.fun
    # k2 = url.split('//')[1].replace('.', '_')
    # # www_langzi_fun
    # k3 = url.split('.', 1)[1].replace('/', '')
    # # langzi.fun
    # k3_1 = url.split('.', 1)[1].replace('/', '').replace('.','_')
    # # langzi_fun
    # k3_2 = url.split('.', 1)[1].replace('/', '').replace('.','')
    # # langzifun
    # k4 = url.split('//')[1].split('.')[1]
    # # langzi
    # lis.append(k1)
    # lis.append(k2)
    # lis.append(k3)
    # lis.append(k3_1)
    # lis.append(k3_2)
    # lis.append(k4)
    # print(lis)
    # for u in lis:
    #     for b in backup_suffix:
    #         try:
    #             res2 = scan(url+'/'+u+b)
    #             if res2:
    #                 write_data(res2)
    #         except Exception as e:
    #             print(e)
if __name__ == '__main__':
    #inp = input('INPUT YOUR URLS.TXT:')
    inp = '19425.txt'
    urls = [x.rstrip('/').strip() for x in open(inp, 'r', encoding='utf-8').readlines()]
    #inp_p = input('INPUT YOUR URLS.TXT:')
    inp_p = 'rar.txt'
    backs = [x.rstrip('/').strip() for x in open(inp_p, 'r', encoding='utf-8').readlines()]
    print(backs)
    start_time = time.time()

    # all_tasks = [x+y for x in urls for y in backs]
    # print(len(all_tasks))
    all_tasks = []
    for b in backs:
        for u in urls:
            all_tasks.append(u+b)

    with ThreadPoolExecutor(max_workers=500) as executor:
        executor.map(run,all_tasks)

    print('总共耗时:{}'.format(time.time() - start_time))
