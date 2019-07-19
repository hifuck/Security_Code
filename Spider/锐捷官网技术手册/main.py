# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun

import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor

def main(keys,index):
    url = 'http://www.ruijie.com.cn/Application/HttpForward/API?1554{}86{}234{}6'.format(random.randint(1,9),random.randint(1,9),random.randint(1,9))
    data = {'interface': '/search/document',

            'data': '{"KeyWord":'+"'"+keys+"'"+',"PageIndex":'+str(index)+',"PageSize":10}'

            }
    try:
        r = requests.post(url=url, data=data)
        res = r.json()
        dd = (res['Data'])
        for x in dd:
            #print(x)
            #这个接口的全部信息
            title = x.get('SeoDescription')
            # 获取到标题了
            # 拼接下载地址
            down_url = 'http://www.ruijie.com.cn/application/Article/GetArticleFile?id={}&attachmentNo=1&download=true'.format(x.get('Url')).replace('/fw/wd/','')
            print('标题:{} 下载地址: {}'.format(title,down_url))
            # 从这里把文件名和下载地址保存到本地文件

            with open('result.txt','a+')as a:
                a.write('标题:{} 下载地址: {}'.format(title,down_url) + '\n')

            # 从这里开始下载PDF文件
            try:
                ress = requests.get(down_url,stream=True)
                with open(title+'.pdf','wb')as a:
                    for langzi in ress.iter_content():
                        a.write(langzi)
                time.sleep(30)
                # 休息30秒等待下载完毕
            except Exception as a:
                print(a)
            # 到这里结束，如果不下载pdf文件，就注释这代码即可


    except Exception as e:
        print(e)

if __name__ == '__main__':

    target = '出口网关'
    # 这里修改关键词
    url = 'http://www.ruijie.com.cn/Application/HttpForward/API?1554{}86{}234{}6'.format(random.randint(1,9),random.randint(1,9),random.randint(1,9))
    data = {'interface': '/search/document',
            'data': '{"KeyWord":'+"'"+target+"'"+',"PageIndex":1,"PageSize":10}'
            }
    try:
        r = requests.post(url=url, data=data)
        res = r.json()
        dd = res['Count']
        print('搜索 {} 存在 {} 条数据'.format(target,dd))
    except Exception as e:
        print(e)
    tasks = list(range(1,dd//10+dd%10+1))
    with ThreadPoolExecutor(3) as p:
        # 开启三个线程
        res = [p.submit(main,target,i) for i in tasks]



