# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import time
import asyncio
import aiohttp
import aiomultiprocess
import aiofiles
import multiprocessing

async def run(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3'}
    async with aiohttp.ClientSession()as session:
        try:
            async with session.head(url,headers=headers,timeout=5) as resp:
                await resp.text()
                if resp.status == 200:
                    print('*当前分端口允许访问*  网址:{}  状态:{}'.format(resp.url, resp.status))
                    #async with aiofiles.open('result.txt','a+',encoding='utf-8')as a:
                else:
                    print('当前分端口访问异常  网址:{}  状态:{}'.format(resp.url,resp.status))

        except:
            pass

async def main():
    url = 'https://www.52pojie.cn:{}'
    urls = [url.format(i)for i in range(1,50000)]
    async with aiomultiprocess.Pool() as pool:
        # 开启进程池
        await pool.map(run, urls)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
