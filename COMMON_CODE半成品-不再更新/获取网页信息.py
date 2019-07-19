# coding:utf-8

import re
import requests
import time
import socket
from bs4 import BeautifulSoup as bs
import chardet
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 3
socket.setdefaulttimeout(timeout)
from requests.packages import urllib3
urllib3.disable_warnings()

class Get_Info:
    def __init__(self, url):
        self.url = url
        print unicode('获取网页信息中.....', 'utf-8')

    def get_ip(self):
        # 该函数的作用是获取网址的真实IP
        # 传入网址即可，获取失败则返回None
        hostname = self.url.replace('http://', '').replace('https://', '').replace('/', '')
        url_ip = 'None'
        try:
            url_ip = socket.gethostbyname(str(hostname))
        except:
            pass
        return url_ip

    def get_ipinfomation(self, *args):
        # 该函数的作用是传入一个列表
        infos_ = []
        for x in args:
            for xx in x:
                d = get_ports(str(xx))
                if d != []:
                    infos_.append('端口:' + str(xx) + '\n服务:' + str(d['name']) + '\n功能:' + str(d['description']) + '\n')
                else:
                    infos_.append(str(xx) + ':' + str('识别失败'))
        return infos_

    '''

    这个函数作用是接受一个列表,列表内是端口
    然后通过whatportis返回端口对应的服务
    返回内容如下：
        [80:http,3389:rdp]

    '''

    def get_ips(self):
        hostname = self.url.replace('http://', '').replace('https://', '').replace('/', '')
        url_ip = 'None'
        try:
            url_ip = socket.gethostbyname(str(hostname))
        except:
            pass
        if url_ip and url_ip != 'None':
            try:
                mas = masscan.PortScanner()
                mas.scan(url_ip)
                url_port = [80]
                url_port = mas.scan_result['scan'][url_ip]['tcp'].keys()
            except:
                url_port = [80]

            if 80 in url_port:
                pass
            else:
                url_port.append(80)
                # for port in ports:
                # s = socket.socket()
                # try:
                #     s.connect((url_ip,port))
                #     url_port.append(port)
                # except Exception,e:
                #     # print e
                #     pass
                # finally:
                #     s.close()
        if url_ip or url_ip != 'None':
            infos = {}
            infos['ip'] = str(url_ip)
            infos['ports_open'] = str(url_port)
            infos['ports_info'] = str(self.get_ipinfomation(url_port))
            return infos
        else:
            infos = {}
            infos['ip'] = '获取失败'
            infos['ports_open'] = '获取失败'
            infos['ports_info'] = '获取失败'
            return infos

    '''

    这个函数作用是把url转换成ip，然后用masscan扫描这个ip的全部端口
    返回一个字典，给字典有4个属性
    分别是 ip 端口 端口与对应的服务 以及位置坐标
    返回内容如下：

    {
        'ip':'127.0.0.1',
        'ports_open':'[80,3389]',
        'ports_info':'[80:http,3389:rdp]'

            }

    '''

    def get_infos(self):
        try:
            UA = random.choice(headerss)
            headers = {'User-Agent': UA}
            r = requests.get(url=self.url, headers=headers, verify=False, timeout=9)
            url_title, url_content, url_service = '获取失败', '获取失败', '获取失败'
            try:
                code = chardet.detect(r.content)['encoding']
                bp = bs(r.content.decode(code).encode('utf-8'), 'html.parser')
                url_title = bp.title.string
                # url_contents = bp.text
                try:
                    url_service = r.headers['Server']
                except:
                    url_service = '获取失败'
            except:
                url_title = re.search('<title>(.*?)</title>', r.content, re.I).group(1).decode(code).encode('utf-8')
                # url_content = re.sub('([\.\?\*~!@#{$%\^&\*()-;"<>\[\]}_\+=]|[0-9]|[a-z]|[A-Z])','',r.text)
                try:
                    url_service = r.headers['Server']
                except:
                    url_service = '获取失败'
            infos = {}
            infos['url'] = self.url
            infos['title'] = url_title
            # url_contents = ''.join(r.text.split()).replace(' ', '').replace('\r\n', '').replace('\r', '')
            # infos['content'] = re.sub('([\.\?\*~!@#{$%\^&\*()-;"<>\[\]}_\+=])', '', url_contents).replace('|',
            #                                                                                               '').replace(
            #     "'", '')
            # 下面这行的代码会过滤掉所有的英文和数字
            # infos['content'] = re.sub('([\.\?\*~!@#{$%\^&\*()-;"<>\[\]}_\+=]|[0-9]|[a-z]|[A-Z])','',url_contents).replace('|','').replace("'",'')
            infos['service'] = url_service
            if infos:
                return infos
            else:
                infos = {}
                infos['url'] = self.url
                infos['title'] = self.url
                # infos['content'] = '获取失败'
                infos['service'] = '获取失败'
                return infos
        except Exception, e:
            # print e
            infos = {}
            infos['url'] = self.url
            infos['title'] = self.url
            # infos['content'] = '获取失败'
            infos['service'] = '获取失败'
            return infos

        '''

        返回内容如下：
        {
        'url':'http://www.langzi.fun',
        'title':'浪子博客'，
        'content':'xaffa网页内容xafgasdas',
        'service':'Apache'
        }

        '''

    def get_urls(self):
        urlss = []
        live_urls = []
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        try:
            r = requests.get(url=self.url, headers=headers, verify=False, timeout=9)
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                 re.I)
            urls = re.findall(pattern, r.content)
            for x in urls:
                a1, a2 = x.split('//')[0], x.split('//')[1].split('/')[0]
                a3 = ''.join(a1) + '//' + ''.join(a2)
                urlss.append(a3.replace("'", "").replace('>', '').replace('<', ''))
            if urlss:
                for _ in list(set(urlss)):
                    UA = random.choice(headerss)
                    headers = {'User-Agent': UA}
                    try:
                        rr = requests.head(url=_, headers=headers, timeout=5, verify=False)
                        if rr.status_code == 200:
                            live_urls.append(_)
                        else:
                            pass
                    except:
                        pass
                return live_urls
            else:
                return None
        except Exception, e:
            # print e
            pass

    def get_cms(self):
        resu = {}
        for cmsxx in cms_rule:
            cmshouzhui = cmsxx.split('|', 3)[0]
            cmsmd5 = cmsxx.split('|', 3)[2]
            cmsname = cmsxx.split('|', 3)[1]
            urlcms = self.url + str(cmshouzhui)
            try:
                UA = random.choice(headerss)
                headers = {'User-Agent': UA}
                req1 = requests.head(url=urlcms, headers=headers, timeout=3, allow_redirects=False)
                if req1.status_code == 200:
                    req1_2 = requests.get(url=urlcms, headers=headers, timeout=3, allow_redirects=False)
                    md5 = hashlib.md5()
                    md5.update(req1_2.content)
                    rmd5 = md5.hexdigest()
                    if rmd5 == cmsmd5:
                        resu['cms'] = cmsname
                        return resu
                    else:
                        pass
                else:
                    pass
            except Exception, e:
                resu['cms'] = 'None'
                return resu


'''
信息采集
调用方法如下：
    a = Get_Info('http://www.langzi.fun')

    print 'IP:' + a.get_ip()
    print 'URLS:'+str(a.get_urls())
    print 'CMS:'+str(a.get_cms())
    print 'Infon:'+str(a.get_infos())
    print 'IPS:' + str(a.get_ips())

IP:180.97.158.239

URLS:['https://blog.csdn.net', 'http://www.langzi.fun', 'https://github.com']

CMS:{'cms': 'None'}

Infon:{'url': 'http://www.langzi.fun', 'content': u'DOCTYPEhtml'}

IPS:{'ip': '180.97.158.239', 'ports_info': "['80:World Wide Web HTTP', '8443:PCsync HTTPS', '8009:\\xe8\\xaf\\x86\\xe5\\x88\\xab\\xe5\\xa4\\xb1\\xe8\\xb4\\xa5', '8080:HTTP Alternate (see port 80)', '8181:Intermapper network management system', '8088:Radan HTTP', '443:http protocol over TLS/SSL']", 'ports_open': '[80, 8443, 8009, 8080, 8181, 8088, 443]'}


'''

