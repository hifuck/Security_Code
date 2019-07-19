# -*- coding:utf-8 -*-
import queue
import requests
import re
import random
import time
import threading
IP_66_headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
'Connection': 'keep-alive',
'Cookie': '__jsluid_h=d26e11a062ae566f576fd73c1cd582be; __jsl_clearance=1563459072.346|0|lMwNkWbcOEZhV8NGTNIpXgDvE8U%3D',
'Host': 'www.66ip.cn',
'Referer': 'http://www.66ip.cn/mo.php?sxb=&tqsl=30&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=2',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

IP_XC_HEADERS = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTBmOWM5NDc1OWY4NjljM2ZjMzU3OTM1MGMxOTEwMjNhBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWVGT0Z1dVpKUXdTMVFEN1JHTnJ3VVhYS05WWlIzUlFEcncvM1daVER2blk9BjsARg%3D%3D--66057a30315f0a34734318d2e6963e608017f79e; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1563458856; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1563460669',
'Host': 'www.xicidaili.com',
'If-None-Match': 'W/"b7acf7140e4247040788777914f600e1"',
'Referer': 'http://www.66ip.cn/mo.php?sxb=&tqsl=30&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=2',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

IP_66_URL = 'http://www.66ip.cn/mo.php?sxb=&tqsl=30&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea='
IP_XC_URL = 'http://www.xicidaili.com/nn/'

def Get_Url_Content(url,headers):
    try:
        r = requests.get(url,headers=headers,timeout=20)
        return r.content
    except:
        return None


q = queue.Queue()
def get_ip(page):
    for i in range(1,page):
        content = Get_Url_Content(IP_66_URL+str(i),IP_66_headers)
        if content != None:
            try:
                ips = re.findall(b'\t(\d.*?:\d.*\d)<br />',content)
                for ip in ips:
                    #print('抓到IP:{}'.format(ip.decode()))
                    q.put(ip.decode())
            except:
                pass
        content = Get_Url_Content(IP_XC_URL+str(i),IP_XC_HEADERS)
        if content:
            try:
                ips = re.findall(b'<td>(\d.*\.\d.*)</td>\n.*?<td>(\d.*)</td>\n', content)
                for i in ips:
                    ip = (i[0].decode() + ':' + i[1].decode())
                    #print('抓到IP:{}'.format(ip))
                    q.put(ip)
            except:
                pass
url = 'http://www.langzi.fun/sitemap.xml'
r = requests.get(url)
urls = re.findall('<loc>(.*?)</loc>',r.content.decode(),re.S)



def scan_ip():
    while 1:
        proxies={}
        ip = q.get()
        proxies['http'] = str(ip)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        # url = random.choice(urls)
        try:
            url = 'https://www.baidu.com/link?url=wa0u02Xzbi6o8gZ9prRGLlHFpbSvyuVgN0Yf5RfJwP7&amp;wd=&amp;eqid=8cee35f300000518000000025c94e4a0'
            req2 = requests.get(url=url, proxies=proxies, headers=headers, timeout=5)
            if req2.status_code == 200:
                print('网址：{} 代理IP：{} 访问成功'.format(url,ip))
                for i in random.sample(urls,5):
                    try:
                        req3 = requests.get(url=i, proxies=proxies, headers=headers, timeout=5)
                        if req3.status_code == 200:
                            print('网址：{} 代理IP：{} 访问成功'.format(i, ip))
                    except Exception as e:
                        #print(e)
                        pass
        except Exception as e:
            #print(e)
            pass

if __name__ == '__main__':
    threading.Thread(target=get_ip, args=(200,)).start()
    for i in range(10):
        threading.Thread(target=scan_ip).start()


