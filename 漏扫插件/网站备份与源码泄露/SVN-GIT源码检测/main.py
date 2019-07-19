# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun

import asyncio
import aiohttp
import aiofiles
import aiomultiprocess
import time
import multiprocessing
import re
import requests
info_prefix = ['/phpinfo.php'
        ,'/info.php'
        ,'/pi.php'
        ,'/php.php'
        , '/i.php'
        ,'/mysql.php'
        ,'/sql.php'
        ,'/test.php'
        , '/x.php'
        ,'/1.php'
        ,'/tz/tz.php'
        ,'/env.php'
        ,'/tz.php'
        ,'/p1.php'
        ,'/p.php'
        ,'/admin_aspcheck.asp'
        ,'/tz/tz.asp'
        ,'/env.asp'
        ,'/tz.asp'
        ,'/p1.asp'
        ,'/p.asp'
        ,'/aspcheck.asp']
tomcat_prefix=[

    ':8081/manager/html',
    ':8080/manager/html',
'/RetainServer/Manager/login.jsp',
'/Manager/login.jsp',
'/servlets-examples/'

]

weblogic_prefix=[
'/console/login/LoginForm.jsp'
,':7001/console/login/LoginForm.jsp'
,':7002/console/login/LoginForm.jsp'
]
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

async def run(url):
    print('当前检测:{}'.format(url))
    async with asyncio.Semaphore(1000):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.get(url+'/.svn/entries') as resp:
                    res = await resp.text()
                    if 'dir' in res and 'svn://' in res:
                        async with aiofiles.open('vlun-result.txt', 'a+',encoding='utf-8')as f:
                            await f.write(str(get_title(url))+'  SVN 源码泄露 :'+url+'/.svn/entries' + '\n')
            except Exception as e:
                #print(e)
                pass

            try:
                async with session.get(url+'/.git/config') as resp:
                    res1 = await resp.text()
                    if 'repositoryformatversion' in res1:
                        async with aiofiles.open('vlun-result.txt', 'a+',encoding='utf-8')as f:
                            await f.write(str(get_title(url))+'  GIT 源码泄露 :'+url+'/.git/config' + '\n')
            except Exception as e:
                #print(e)
                pass

            # try:
            #     async with session.get(url+'/WEB-INF/web.xml') as resp:
            #         res1 = await resp.text()
            #         if '<web-app' in res1:
            #             async with aiofiles.open('vlun-result.txt', 'a+',encoding='utf-8')as f:
            #                 await f.write(str(get_title(url))+'  WEB INFO 源码泄露 :'+url+'/WEB-INF/web.xml' + '\n')
            # except Exception as e:
            #     #print(e)
            #     pass



            # for prefix in info_prefix:
            #     try:
            #         async with session.get(url + prefix) as resp:
            #             res2 = await resp.text()
            #             if 'upload_max_filesize' in res2 or 'SoftArtisans.FileManager' in res2:
            #                 async with aiofiles.open('vlun-result.txt', 'a+', encoding='utf-8')as f:
            #                     await f.write('服务器探针 :'+url + prefix + '\n')
            #     except Exception as e:
            #         print(e)
            #
            # for t_prefix in tomcat_prefix:
            #     try:
            #         async with session.get(url + t_prefix) as resp:
            #             res3 = await resp.text()
            #             if 'servlet/RequestParamExample' in res3 or 'onkeypress="if(event.keyCode==13)' in res3 or  'Manager App HOW-TO' in res3:
            #                 async with aiofiles.open('vlun-result.txt', 'a+', encoding='utf-8')as f:
            #                     await f.write('TOMCAT 敏感文件地址 :'+url + t_prefix + '\n')
            #     except Exception as e:
            #         print(e)
            #
            # for w_prefix in weblogic_prefix:
            #     try:
            #         async with session.get(url + t_prefix) as resp:
            #             res3 = await resp.text()
            #             if 'WebLogic' in res3:
            #                 async with aiofiles.open('vlun-result.txt', 'a+', encoding='utf-8')as f:
            #                     await f.write('WEBLOGIC 敏感文件地址 :'+url + w_prefix + '\n')
            #     except Exception as e:
            #         print(e)
            #
            #
            # for p_prefix in phpmyadmin_prefix:
            #     try:
            #         async with session.get(url + p_prefix) as resp:
            #             res3 = await resp.text()
            #             if 'upload_max_filesize' in res3 or 'SoftArtisans.FileManager' in res3:
            #                 async with aiofiles.open('vlun-result.txt', 'a+', encoding='utf-8')as f:
            #                     await f.write('PHPMYADMIN 后台地址 :'+url + p_prefix + '\n')
            #     except Exception as e:
            #         print(e)

async def main(urls):
    async with aiomultiprocess.Pool() as pool:
        await pool.map(run,urls)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    print('''

             _                           _
            | |                         (_)
            | |     __ _ _ __   __ _ _____
            | |    / _` | '_ \ / _` |_  / |
            | |___| (_| | | | | (_| |/ /| |
            |______\__,_|_| |_|\__, /___|_|
                                __/ |      Langzi_GIT_SVN_SCAN
                               |___/       Version:0.5
                                           Datetime:2019-05-01


    ''')
    time.sleep(1)
    print('''

            基于多进程异步协程构架
            广度优先原则，避免拦截或者扫死服务器
            如机器配置内存低于16G
            宽带低于100M不建议一次超过200个网址
    
    ''')
    time.sleep(3)
    inp = input('INPUT YOUR URLS.TXT:')
    urls = [x.rstrip('/').strip() for x in open(inp,'r',encoding='utf-8').readlines()]
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls))
    print('总共耗时:{}'.format(time.time()-start_time))
