# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import asyncio
import aiomultiprocess
import aiohttp
import aiofiles
import time
import multiprocessing
phpmyadmin_prefix=[
'/phpmyadmin/index.php',
'/phpma/index.php',
'/phpMyAdmin/index.php',
'/MyAdmin/index.php',
'/xampp/phpmyadmin/index.php',
'/tools/phpmyadmin/index.php',
':999/phpmyadmin',
'/phpMyAdmin',
'/phpMyAdmins',
'/phpmyadmin',
'admin/phpmyadmin/',
'/phpMyAdmin0',
'/phpMyAdmin1',
'/phpMyAdmin2',
'/phpMyAdmin_0',
'/phpMyAdmin-2',
'/pma',
'/pm_Admin',
'/pmd'
]

async def run(url):
    async with asyncio.Semaphore(1000):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as resp:
                    print('{}: {}'.format(resp.url, resp.status))
                    if resp.status == 200:
                        result = await resp.text()
                        if 'name="pma_username"' in result:
                            async with aiofiles.open('phpmyadmin_url.txt', 'a+')as f:
                                await f.write(url + '\n')
            except Exception as e:
                print(e)


async def main(urls):
    async with aiomultiprocess.Pool()as pool:
        await pool.map(run, urls)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    all_tasks = []
    url_ss = input('INPUT YOUR URLS.TXT:')
    urls = [x.strip() for x in open(url_ss,'r',encoding='utf-8').readlines()]

    for p in phpmyadmin_prefix:
        for u in urls:
            all_tasks.append(u + p)
    print('任务总数:{}'.format(len(all_tasks)))

    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls))
    print('总共耗时: {}'.format(time.time() - start_time))