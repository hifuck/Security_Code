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
        title = titles.decode()
    except:
        pass
    finally:
        return title

async def run(urls):
    url = urls.split('//')[0] + '//'+urls.split('//')[1].split('/')[0]

    #print(get_title(url))
    async with asyncio.Semaphore(500):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.head(urls) as resp:
                    print('当前检测:{}  状态:{}'.format(resp.url, resp.status))
                    print(resp.headers.get("Content-Length"))
                    if int(resp.headers.get("Content-Length")) > 1500000:
                        print('存在备份文件!!!!!!!!!!!!!!!!!!')
                    if int(resp.headers.get('Content-Length')) > 2000000:
                        async with aiofiles.open('vlun-result.txt','a+',encoding='utf-8')as f:
                            await f.write(str(get_title(url))+ '   ' + urls + '   ' + str(int(resp.headers["Content-Length"]) / 1000000).split('.')[0] + 'M' +'\n')
            except:
                pass

            # for b in backup_suffix:
            #     try:
            #         async with session.head(url + '/' + url.split('//')[1].split('.')[1] + b) as resp:
            #             print('当前检测:{}  状态:{}'.format(resp.url, resp.status))
            #             print(resp.headers.get("Content-Length"))
            #             if int(resp.headers.get("Content-Length")) > 1500000:
            #                 print('存在备份文件!!!!!!!!!!!!!!!!!!')
            #             if int(resp.headers.get('Content-Length')) > 2000000:
            #                 async with aiofiles.open('vlun-result.txt','a+',encoding='utf-8')as f:
            #                     await f.write(str(get_title(url))+urls + '   ' + str(int(resp.headers["Content-Length"]) / 1000000).split('.')[0] + 'M' +'\n')
            #     except Exception as e:
            #         print(e)
            #         pass


            # lis = []
            # k1 = url.split('//')[1]
            # # www.langzi.fun
            # k2 = url.split('//')[1].replace('.', '_')
            # # www_langzi_fun
            # k3 = url.split('.', 1)[1].replace('/', '')
            # # langzi.fun
            # k3_1 = url.split('.', 1)[1].replace('/', '').replace('.', '_')
            # # langzi_fun
            # k3_2 = url.split('.', 1)[1].replace('/', '').replace('.', '')
            # # langzifun
            # k4 = url.split('//')[1].split('.')[1]
            # # langzi
            # lis.append(k1)
            # lis.append(k2)
            # lis.append(k3)
            # lis.append(k3_1)
            # lis.append(k3_2)
            # lis.append(k4)
            # for par in lis:
            #     for bac in backup_suffix:
            #         try:
            #             async with session.head(url + '/' + par+bac) as resp:
            #                 print('当前检测:{}  状态:{}'.format(resp.url,resp.status))
            #                 if int(resp.headers.get('Content-Length')) > 2000000:
            #                     async with aiofiles.open('vlun-result.txt', 'a+', encoding='utf-8')as f:
            #                         await f.write(str(get_title(url)) + ':' + url + '/' + par+bac+ ':' + str(
            #                             int(resp.headers["Content-Length"]) / 1000000) + 'M' + '\n')
            #         except:
            #             pass
#
async def main(urls,backs):
    # async with aiomultiprocess.Process() as process:
    #     for u in urls:
    #         for b in backs:
    #             await process()
    all_tasks = []
    for b in backs:
        for u in urls:
            all_tasks.append(u+b)
    print('目标数量:{}'.format(len(all_tasks)))
    async with aiomultiprocess.Pool() as pool:
        await pool.map(run,all_tasks)
    # for b in backs:
    #     for u in urls:
    #         await aiomultiprocess.Process(target=run,args=(u,b))

if __name__ == '__main__':
    multiprocessing.freeze_support()
    #inp = input('INPUT YOUR URLS.TXT:')
    inp = '19425.txt'
    urls = [x.rstrip('/').strip() for x in open(inp, 'r', encoding='utf-8').readlines()]
    #inp_p = input('INPUT YOUR URLS.TXT:')
    inp_p = 'rar.txt'
    backs = [x.rstrip('/').strip() for x in open(inp_p, 'r', encoding='utf-8').readlines()]
    start_time = time.time()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls,backs))
    print('总共耗时:{}'.format(time.time() - start_time))


