# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import requests
import random

headerss = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]



# url,title,weights,ip,ages,whois_id,whois_type,whois_name,whois_time
# 网址，标题，百度权重，ip信息，年龄，备案号，备案性质，备案名称，备案时间
# include_baidu,request,text,service,language
# 百度收录，，协议类型，页面类型，服务器类型，程序语言
title_parrten = 'class="w61-0"><div class="ball">(.*?)</div></td>'  # group(1) 正常
ip_parrten = '>IP：(.*?)</a></div>'  # group(1) 正常
# 下面会报错
ages = '" target="_blank">(.*?)</a></div></div>'  # group(1)
whois_id = '备案号：</span><a href=.*?" target="_blank">(.*?)</a></div>'  # 需group(1)
whois_type = '<span>性质：</span><strong>(.*?)</strong></div>'  # 需group(1)
whois_name = '<span>名称：</span><strong>(.*?)</strong></div>'  # 需group(1)
whois_time = '<span>审核时间：</span><strong>(.*?)</strong></div>'  # 需group(1)
include_baidu = '<div class="Ma01LiRow w12-1 ">(.*?)</div>'  # group(1)
infos = '<div class="MaLi03Row w180">(.*?)</div>'  # 要findall 0，1，2，3


def get_baidu_weights(url):
    x = str(random.randint(1, 9))
    data = {
        't': 'rankall',
        'on': 1,
        'type': 'baidupc',
        'callback': 'jQuery111303146901980779846_154444474116%s' % (x),
        'host': url
    }

    headers = {

        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'UM_distinctid=165af67ee6f352-07238a34ed3941-9393265-1fa400-165af67ee70473; CNZZDATA5082706=cnzz_eid%3D832961605-1544438317-null%26ntime%3D1544443717; Hm_lvt_aecc9715b0f5d5f7f34fba48a3c511d6=1544443985; Hm_lpvt_aecc9715b0f5d5f7f34fba48a3c511d6=1544443985; qHistory=aHR0cDovL3JhbmsuY2hpbmF6LmNvbS9iYWlkdW1vYmlsZS8r55m+5bqm56e75Yqo5p2D6YeNfGh0dHA6Ly9yYW5rLmNoaW5hei5jb20vcmFua2FsbC8r5p2D6YeN57u85ZCI5p+l6K+ifGh0dHA6Ly9yYW5rLmNoaW5hei5jb20r55m+5bqm5p2D6YeN5p+l6K+ifGh0dHA6Ly9pbmRleC5jaGluYXouY29tLyvlhbPplK7or43lhajnvZHmjIfmlbB8aHR0cDovL3JhbmsuY2hpbmF6LmNvbS9yYW5rL2hpc3RvcnkuYXNweCvmnYPph43ljoblj7Lmn6Xor6I=',
        'Host': 'rank.chinaz.com',
        'Origin': 'http://rank.chinaz.com',
        'Referer': 'http://rank.chinaz.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'

    }
    try:
        urls = 'http://rank.chinaz.com/ajaxseo.aspx?t=rankall&on=1&type=undefined&callback=jQuery111303146901980779846_154444474116%s' % (
            x)

        r = requests.post(url=urls, headers=headers, data=data)
        try:
            res = re.search(',"br":(\d),"beforBr', r.content).group(1)
        except:
            pass
        if res:
            return res
        else:
            return '无权重'
    except:
        return '无权重'

def get_info(pattren,result):
	try:
		res = re.search(pattren,result).group(1)
		return res
		#return str(res.encode('utf-8'))
	except:
		return '暂无信息'


def scan_seo(url):

	UA = random.choice(headerss)
	headers = {'User-Agent':UA}
	urls = 'http://seo.chinaz.com/' + url.replace('https://','').replace('http://','').replace('/','').replace('www.','')
	print urls
	# url,title,weights,ip,ages,whois_id,whois_type,whois_name,whois_time
	# 网址，标题，百度权重，ip信息，年龄，备案号，备案性质，备案名称，备案时间
	# include_baidu,request,text,service,language
	# 百度收录，，协议类型，页面类型，服务器类型，程序语言
	res = {}
	try:
		r = requests.get(urls,headers,timeout=5).content
	except Exception,e:
		print e
	res['百度权重'] = str(get_baidu_weights(url))
	res['网站网址'] = url
	res['网站标题'] = get_info(title_parrten,r)
	res['IP  信息'] = get_info(ip_parrten,r)
	res['网站年龄'] = get_info(ages,r)
	res['备案编号'] = get_info(whois_id,r)
	res['备案性质'] = get_info(whois_type,r)
	res['备案名称'] = get_info(whois_name,r)
	res['备案时间'] = get_info(whois_time,r)
	res['百度收录'] = get_info(include_baidu,r)


	dd = re.findall(infos,r,re.S)
	resu = ['暂无信息' if x.replace(' ','') is '' else x for x in dd  ]
	res['协议类型'] = resu[0]
	res['页面类型'] = resu[1]
	res['服务类型'] = resu[2]
	res['程序语言'] = resu[3]
	for x,y in res.items():
		print x,y


import time

print ('''
         _                           _
        | |                         (_)
        | |     __ _ _ __   __ _ _____
        | |    / _` | '_ \ / _` |_  / |
        | |___| (_| | | | | (_| |/ /| |
        |______\__,_|_| |_|\__, /___|_|
                            __/ |
                           |___/

''')

time.sleep(1)
print unicode('     LangZi 信息综合查询', 'utf-8')
time.sleep(1)


scan_seo('https://blog.csdn.net/')



