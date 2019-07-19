# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import asyncio
import aiomultiprocess
import aiohttp
import aiofiles
import time
import multiprocessing

async def run(url):
    async with asyncio.Semaphore(1000):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=20) as resp:
                    print('{}: {}'.format(resp.url, resp.status))
                    if resp.status == 200:
                        result = await resp.text()
                        if 'Documentation.html' in result:
                            async with aiofiles.open('phpmyadmin_url.txt', 'a+')as f:
                                await f.write(url + '\n')
            except Exception as e:
                print(e)


async def main(urls):
    async with aiomultiprocess.Pool()as pool:
        await pool.map(run, urls)


if __name__ == '__main__':
    multiprocessing.freeze_support()  
    url_ss = input('INPUT YOUR URLS.TXT:')
    urls = [x.strip() + '/phpmyadmin/index.php' for x in open(url_ss,'r',encoding='utf-8').readlines()] + [x.strip().lstrip('/') + ':999/phpmyadmin/index.php' for x in open(url_ss,'r',encoding='utf-8').readlines()]
    counts = len(urls)
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls))
    print('总共耗时: {} 扫描网址个数: {}'.format(time.time() - start_time), counts)