# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import requests
import time
import aiohttp
import aiofiles
import aiomultiprocess
import multiprocessing
import asyncio
import re

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3', 'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Cache-Control': 'max-age=0', 'referer': 'http://www.soso.com', 'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3'}
backup_suffix = ['.rar', '.zip', '.tar', '.tar.bz2', '.sql', '.7z', '.bak',  '.tar.gz','.gz',]
def get_title(url):
    title = '获取失败'
    try:
        r = requests.get(url)
        titles = re.search(b'<title>(.*?)</title>',r.content,re.S).group(1)
        title = titles.decode().strip()
    except:
        pass
    finally:
        return title

async def run(urls):
    url = urls.split('//')[0] + '//'+urls.split('//')[1].split('/')[0]
    async with asyncio.Semaphore(500):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.head(urls) as resp:
                    print('当前检测:{}  状态:{}'.format(resp.url, resp.status))
                    print(resp.headers.get("Content-Length"))
                    if int(resp.headers.get("Content-Length")) > 1500000:
                        print('存在备份文件!!!!!!!!!!!!!!!!!!')
                    if int(resp.headers.get('Content-Length')) > 1500000:
                        async with aiofiles.open('vlun-result.txt','a+',encoding='utf-8')as f:
                            await f.write(str(get_title(url))+ '   ' + urls + '   ' + str(int(resp.headers["Content-Length"]) / 1024000).split('.')[0] + 'M' +'\n')
            except:
                pass



async def main(urls,backs):

    all_tasks = []
    for b in backs:
        for u in urls:
            all_tasks.append(u+b)
    for b in backup_suffix:
        for u in urls:
            try:
                all_tasks.append(u+'/'+u.split('//')[1].split('.')[1]  + b)
            except:
                pass
            try:
                all_tasks.append(u+'/'+u.split('//')[1]  + b)
            except:
                pass
            try:
                all_tasks.append(u+'/'+u.split('.', 1)[1].replace('/', '') + b)
            except:
                pass
    print('目标数量:{}'.format(len(all_tasks)))
    time.sleep(2)
    if len(all_tasks)>2000000:
        print('目标数量过于庞大，可能会导致扫描过程中内存溢出')
    async with aiomultiprocess.Pool() as pool:
        await pool.map(run,all_tasks)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    print('''

             _                           _
            | |                         (_)
            | |     __ _ _ __   __ _ _____
            | |    / _` | '_ \ / _` |_  / |
            | |___| (_| | | | | (_| |/ /| |
            |______\__,_|_| |_|\__, /___|_|
                                __/ |      Langzi_BackUp_FileScan
                               |___/       Version:3.8
                                           Datetime:2019-04-27
                                           

    ''')
    time.sleep(1)
    print('''

            /*禁止对GOV-EDU进行检测(检测到则秒退)*/
            基于多进程异步协程构架
            广度优先原则，避免拦截或者扫死服务器
            如机器配置内存低于16G
            宽带低于100M不建议一次超过200个网址

    ''')
    time.sleep(3)

    inp = input('INPUT YOUR URLS.TXT:')
    #inp = '19425.txt'
    urls = [x.rstrip('/').strip() for x in open(inp, 'r', encoding='utf-8').readlines()]
    inp_p = input('INPUT YOUR BACKUP_FILE.Dict:')
    #inp_p = 'rar.txt'
    backs = [x.rstrip('/').strip() for x in open(inp_p, 'r', encoding='utf-8').readlines()]
    start_time = time.time()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls,backs))
    print('总共耗时:{}'.format(time.time() - start_time))
    time.sleep(500)
    time.sleep(500)
    time.sleep(500)
    time.sleep(500)
    time.sleep(500)
    time.sleep(500)
    time.sleep(500)
    time.sleep(500)
    time.sleep(500)
    time.sleep(500)
    time.sleep(500)
    time.sleep(500)
    time.sleep(500)


