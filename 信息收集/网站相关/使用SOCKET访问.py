# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import socket
from urllib.parse import urlparse
def get_url(url,port):
    urls= urlparse(url)
    host, path = urls.netloc,urls.path
    if path == '':
        path = '/'
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    # 绑定ip与端口
    s.send('GET {}\r\nHost:{}\r\nUser-Agent:{}\r\n'.format(path, host, headers).encode('utf-8'))
    res = s.recv(1024)
    print(res.decode('utf-8','replace'))

get_url('http://36.156.81.240/manage',80)