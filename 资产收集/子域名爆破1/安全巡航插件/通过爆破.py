# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import asyncio
import aiodns
import aiomultiprocess
import aiohttp
from urllib.parse import urlparse
import multiprocessing
import configparser
import pymysql
import contextlib
import os

cfg = configparser.ConfigParser()
cfg.read('../Config.ini')
user = cfg.get("Server", "username")
passwd = cfg.get("Server", "password")
host = cfg.get("Server", "host")
Dbname = cfg.get("Server", "db")
port = int(cfg.get("Server", "port"))

@contextlib.contextmanager
def connect_mysql():
    coon = pymysql.connect(user=user, passwd=passwd, host=host, db=Dbname, port=port, charset='utf8')
    cursor = coon.cursor()
    try:
        yield cursor
    except Exception as e:
        print(e)
        pass
    finally:
        coon.commit()
        cursor.close()
        coon.close()


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

async def run(url):
    # print('Scan:'+url)
    async with asyncio.Semaphore(1000):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.get('http://'+url,timeout=15) as resp:
                    if resp.status == 200 or resp.status == 301 or resp.status==302:
                        content = await resp.read()
                        #print(content)
                        if b'Service Unavailable' not in content and b'The requested URL was not found on' not in content and b'The server encountered an internal error or miscon' not in content:
                            u = urlparse(str(resp.url))
                            return u.scheme+'://'+u.netloc
            except Exception as e:
                #print(e)
                pass

            try:
                async with session.get('https://' + url,timeout=15) as resp:
                    if resp.status == 200 or resp.status == 301 or resp.status==302:
                        content = await resp.read()
                        #print(content)
                        if b'Service Unavailable' not in content and b'The requested URL was not found on' not in content and b'The server encountered an internal error or miscon' not in content:
                            u = urlparse(str(resp.url))
                            return u.scheme+'://'+u.netloc
            except Exception as e:
                #print(e)
                pass


async def Aio_Subdomain(subdomain,loop):
    # print(subdomain)
    async with asyncio.Semaphore(1000):
        resolver = aiodns.DNSResolver(loop=loop)
        try:
            await resolver.query(subdomain,'A')
            return subdomain
        except Exception as e:
            pass

def get_result(inp,loop,dicdic):
    try:
        result = []
        dict_counts = len([subdoma.strip() for subdoma in open(dicdic, 'r').readlines()])
        dicts = [subdoma.strip() for subdoma in open(dicdic, 'r').readlines()]
        use_dicts = []
        if dict_counts > 500:
            start_count = dict_counts // 500
            end_count = dict_counts / 500
            if end_count>start_count:
                counts = start_count+1
            else:
                counts = start_count

            for i in range(counts + 1):
                use_dicts.append((dicts[500 * i:500 * (i + 1)]))
        else:
            use_dicts = dicts

        for use in use_dicts:

            if use != []:
                tasks1 = [loop.create_task(Aio_Subdomain(subdoma.strip() + '.' + inp, loop)) for subdoma in
                          use]
                loop.run_until_complete(asyncio.wait(tasks1))
                result1 = [x.result() for x in tasks1 if x.result() != None]
                result.extend(result1)

        return list(set(result))
    except:
        pass



async def main(urls):
    async with aiomultiprocess.Pool() as pool:
        result = await pool.map(run, urls)
    return result


if __name__ == '__main__':
    result = []
    if os.path.exists('domain_log'):
        os.remove('domain_log')
    multiprocessing.freeze_support()
    loop = asyncio.get_event_loop()

    domains = list(set([x.strip() for x in open('domains.txt', 'r', encoding='utf-8').readlines()]))


    for domain in domains:
        print('当前检测域名为:{}'.format(domain))
        dicdic = 'Sub_Big_Dict.txt'
        result_0 = get_result(domain, loop,dicdic=dicdic)
        print('二级域名获取数量为 : {} '.format(len(result_0)))
        if result_0 != []:
            for url in result_0:
                with open('domain_log', 'a+', encoding='utf-8')as a:
                    a.write(url + '\n')
            res = loop.run_until_complete(main(result_0))
            http_result = [x for x in res if x != None]
            http_result = list(set(http_result))
            if http_result != []:
                print('二级域名存活数量为 : {} '.format(len(http_result)))
                for url in http_result:
                    if '.blog.sohu.' not in url and '.photo.qq.com' not in url  and '.auto.sohu.' not in url and '.anjuke.com' not in url and '.zhidao.163.' not in url and '.i.sohu.com' not in url and '.1688.com' not in url and '.chinadaily.com.cn' not in url and '.auto.sina.com.cn' not in url and 'house.163.com' not in url:
                        print('插入子域名:' + url)
                        with connect_mysql() as conn:
                            sql1 = "insert into Sec_Index(url) values  ('{}')".format(url)
                            conn.execute(sql1)


            for url_1 in result_0:
                print('\n当前爆破二级域名为: {}'.format(url_1))
                dicdic = 'Sub_Sma_Dict.txt'
                resul_start = get_result(url_1, loop,dicdic=dicdic)
                print('三级域名获取数量为 : {} '.format(len(resul_start)))
                if resul_start != []:
                    res = loop.run_until_complete(main(resul_start))
                    http_result = [x for x in res if x != None]
                    http_result = list(set(http_result))
                    if http_result != []:
                        print('三级域名存活数量为 : {} '.format(len(http_result)))
                        for url in http_result:
                            if '.blog.sohu.' not in url and '.photo.qq.com' not in url and '.auto.sohu.' not in url and '.anjuke.com' not in url and '.zhidao.163.' not in url and '.i.sohu.com' not in url and '.1688.com' not in url and '.chinadaily.com.cn' not in url and '.auto.sina.com.cn' not in url and 'house.163.com' not in url:
                                print('插入子域名:' + url)
                                with connect_mysql() as conn:
                                    sql1 = "insert into Sec_Index(url) values  ('{}')".format(url)
                                    conn.execute(sql1)


        # if os.path.exists(domain + '__.txt'):
        #     print('开始对文本进行去重复处理...')
        #     all_url = list(set([x.strip() for x in open(domain + '__.txt', 'r', encoding='utf-8').readlines()]))
        #     if os.path.exists(domain + '__.txt'):
        #         os.remove(domain + '__.txt')
        #     for u in all_url:
        #         with open(domain + '__.txt', 'a+', encoding='utf-8')as a:
        #             a.write(u + '\n')
        # else:
        #     print('无子域名检测爆破成功...\n')
        # print('检测完成......')

















    #
    #
    #
    #
    #
    #
    #
    #
    # for domain in domains:
    #     tasks = [loop.create_task(Aio_Subdomain(subdoma.strip()+domain,loop)) for subdoma in open('subdomaindict.txt','r').readlines()[0:500]]
    #     loop.run_until_complete(asyncio.wait(tasks))
    #     result = [x.result() for x in tasks if x.result()!= None]
    #     result = list(set(result))
    #     for url in result:
    #         with open('domain_log','a+',encoding='utf-8')as a:
    #             a.write(url + '\n')
    #     if result != []:
    #         res = loop.run_until_complete(main(result))
    #         http_result = [x for x in res if x!= None]
    #         http_result = list(set(http_result))
    #         print(http_result)
    #         for u in http_result:
    #
    # if os.path.exists('domain_log'):
    #     domains = list(set(['.'+x.strip() for x in open('domain_log','r',encoding='utf-8').readlines()]))
    #     for domain in domains:
    #         tasks = [loop.create_task(Aio_Subdomain(subdoma.strip() + domain, loop)) for subdoma in
    #                  open('subdomaindict.txt', 'r').readlines()[0:500]]
    #         loop.run_until_complete(asyncio.wait(tasks))
    #         result = [x.result() for x in tasks if x.result() != None]
    #         result = list(set(result))
    #         for url in result:
    #             with open('domain_log', 'a+', encoding='utf-8')as a:
    #                 a.write(url + '\n')
    #         if result != []:
    #             res = loop.run_until_complete(main(result))
    #             http_result = [x for x in res if x != None]
    #             http_result = list(set(http_result))
    #             print(http_result)
    #             for u in http_result:
    #                 print('插入子域名:' + u)
    #                 with connect_mysql() as conn:
    #                     sql1 = "insert into Sec_Index(url) values  ('{}')".format(u)
    #                     conn.execute(sql1)
    #
    #
    #
    #


