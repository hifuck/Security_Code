# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import asyncio
import aiodns
import aiomultiprocess
import aiohttp
from urllib.parse import urlparse
import multiprocessing
import os
import random

Check_Alive_Status = [200,301,302]
# 这里可以进行设置状态码存活，符合状态码将会判断为网页存活

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

async def run(url):
    # print('Scan:'+url)
    async with asyncio.Semaphore(1000):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.get('http://'+url,timeout=15) as resp:
                    if resp.status in Check_Alive_Status:
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
                    if resp.status in Check_Alive_Status:
                        content = await resp.read()
                        #print(content)
                        if b'Service Unavailable' not in content and b'The requested URL was not found on' not in content and b'The server encountered an internal error or miscon' not in content:
                            u = urlparse(str(resp.url))
                            return u.scheme+'://'+u.netloc
            except Exception as e:
                #print(e)
                pass


async def Aio_Subdomain(subdomain,loop):
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

def Write_Database(domain,domain_lists):
    with open(domain+'.txt','a+',encoding='utf-8')as a:
        a.writelines([x+'\n' for x in domain_lists])

if __name__ == '__main__':
    result = []
    if os.path.exists('domain_log'):
        os.remove('domain_log')
    multiprocessing.freeze_support()
    loop = asyncio.get_event_loop()

    domains = list(set([x.strip() for x in open('domains.txt', 'r', encoding='utf-8').readlines()]))
    # 要扫描的保存在domains.txt
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
                Write_Database(domain,http_result)

            # 从这开始爆破三级域名，不过我直接注释掉了，感觉有些浪费时间

            # for url_1 in result_0:
            #     print('\n当前爆破二级域名为: {}'.format(url_1))
            #     dicdic = 'Sub_Sma_Dict.txt'
            #     resul_start = get_result(url_1, loop,dicdic=dicdic)
            #     print('三级域名获取数量为 : {} '.format(len(resul_start)))
            #     if resul_start != []:
            #         res = loop.run_until_complete(main(resul_start))
            #         http_result = [x for x in res if x != None]
            #         http_result = list(set(http_result))
            #         if http_result != []:
            #             print('三级域名存活数量为 : {} '.format(len(http_result)))
            #             if len(http_result) > 3:
            #                 # 三级域名还能爆破超过三个？判断检测为泛解析,那么随机选择三个就凑合了
            #                 Write_Database(domain, random.sample(http_result,3))











