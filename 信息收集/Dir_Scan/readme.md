依赖

	1. requests


URL跳转方式可以分成两种，第一种是客户端跳转，第二种是服务的跳转。

如果是客户端跳转，如果不进行修改的话，返回的状态码是301或者302，然后开始跳转到下一个页面。

服务端跳转，是由服务器进行处理结请求后，将结果从后端发送给前端，获取的状态码是200

URL的404页面的识别，按照经验有如下几种情况

1. 直接返回404状态码
2. 将错误页面重定向到一个新的页面，重定向方式是上面说的两种。
3. 程序员在后端代码中，将错误页面的状态码设置成200的错误页面，然后直接返回到前端
4. 程序员在后段代码张，将错误页面的请求直接从后端重定向到首页

常见的情况大概这么多，尝试使用python实现对404页面的检测识别

但是这里存在一个问题，即你扫描网站的目录结果还是扫描网站的文件，如果扫描网站的文件，那么适用上面的规则，如果是扫描
网站的目录结构，那么会误杀许多请求，比如很多网站的后台管理地址为

	localhost/admin/admin.php

当你请求如下链接的时候

	local/admin

这个时候会自动跳转到

	localhost/admin/admin.php

但是如果适用上面的规则就会造成一定的错误率。解决办法则是不检测状态码但是进行关键词识别，即如果请求链接，链接网页的内容出现关键词比如【管理员登录】这些字样，则直接保存结果。

除了这种方式，还有许多比如排除法，即进行一定的规则检测，比如判断状态码并且进行跳转页面相似度检测。

识别404分通用型与制定型，制定型即制定一个网站进行目录扫描，单独写一个文件。这个比较容易，这里不做讨论。

按照常见情况可以分出下面两种检测方式

这里判断条件为：

1. requests参数设置allow_redirects=False
2. 首先进行状态码检测 只检测如果状态码 404，则立即抛出错误

上面一种是新手很常见的用法，速度快但是会存在误报情况。

1. requests参数设置allow_redirects=True
1. 获取网站首页的内容 保存为 Content_1 固定变量，用来做相似度判读
2. 获取错误页面的内容 保存为 Content_2，状态码 保存为 Status_2 固定变量，用来做相似度判读
3. 获取检测目录的内容 保存为 Content_3，状态码 保存为 Status_3
4. 如果固定变量 Status_2 == Status_3 == 404, 直接抛出错误，省下 检测相似度的时间
5. 如果上面没有异常出现 则对 Content_3 与Content_1 和 Content_2 进行相似度判读
6. 如果相似度超过制定的阈值，则直接触发错误，判读为404页面

构建了一下代码工程

	# coding:utf-8
	import requests
	requests.packages.urllib3.disable_warnings()
	import difflib



	Dir_Path=['/admin','/login','/manage','/log_home','/admin.php','/categories/']


	def Return_Http_Content(url):
	    try:
		headers = {
		    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
		r = requests.get(url, headers=headers, verify=False, timeout=5)
		encoding = 'utf-8'
		try:
		    encoding = requests.utils.get_encodings_from_content(r.text)[0]
		except:
		    pass
		content = r.content.decode(encoding, 'replace')
		return (content, r.status_code)
	    except Exception as e:
		return ('langzi', 404)


	def Return_Content_Difflib(original, compare):
	    res = (str(difflib.SequenceMatcher(None,original, compare).quick_ratio())[2:6])
	    if res == '0':
		res = 0
		return res
	    else:
		res = res.lstrip('0')
		return int(res)
	    # return 4 integer like 1293 or 9218


	class Check_Page_404:
	    def __new__(cls, url):
		cls.url_200 = Return_Http_Content(url)
		cls.url_404 = Return_Http_Content(url.rstrip('/')+'/langzi.html')
		return object.__new__(cls)

	    def __init__(self,url):
		self.url = url

	    def Check_404(self,suffix):
		chekc_url = Return_Http_Content(self.url.rstrip('/')+suffix)
		if chekc_url[1] == 404:
		    return False
		Dif_1 = Return_Content_Difflib(chekc_url[0],self.url_200[0])
		Dif_2 = Return_Content_Difflib(chekc_url[0],self.url_404[0])
		if Dif_1>200 and Dif_2<5000:
		    return True
		else:
		    return False


	if __name__ == '__main__':
	    url = 'http://www.langzi.fun'
	    test = Check_Page_404(url)
	    for suffix in Dir_Path:
		print('Check Url : ' + url + suffix +' : ')
		print(test.Check_404(suffix=suffix))


封装后，使用方法如下

	url = 'http://www.langzi.fun'
	# 扫描目标
	Dir_Path=['/admin','/login','/manage','/log_home','/admin.php','/categories/']
	# 目录字典
	Check = Check_Page_404(url)
	# 实例化对象
	for suffix in Dir_Path():
	# 对字典进行遍历
	    if Check.Check_404(suffix=suffix):
		print('Url is Alive : '+ url + suffix)



如何使用相似度判读，之前写

[本文链接](http://langzi.fun/Python实现404页面识别.html)

[Python 路径测试](http://langzi.fun/URL%E8%B7%AF%E5%BE%84%E6%A8%A1%E7%B3%8A%E6%B5%8B%E8%AF%95.html)




