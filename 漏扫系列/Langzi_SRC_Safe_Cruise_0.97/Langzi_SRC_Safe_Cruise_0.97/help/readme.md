# LANGZI\_SRC\_安全巡航 0.97版本

LANGZI\_SRC\_安全巡航 是一款集成漏扫，验证，资产监控，自动复现并且生成结果表报的工具，实现初衷是为了帮助白帽子在SRC中节约时间成本的自动化工具。


阅读完此文并配置环境大约需要20分钟，为了避免非零基础人群感到身体不适、头晕恶心、易怒及粗口，请不要查看以下内容。

本软件只做初步探测，无攻击性行为。请使用者遵守《[中华人民共和国网络安全法](http://www.npc.gov.cn/npc/xinwen/2016-11/07/content_2001605.htm)》，勿用于非授权的测试，检测目标仅限于各大SRC，补天SRC，公益SRC进行测试。

最后更新时间：2019-6-26 22:24

# 运行环境

1. 安装 Microsoft Office 
2. 安装Firefox浏览器
3. 安装vc++2015相关库
4. 安装python2，并添加到系统环境变量//即cmd下输入python进入python2交互界面
5. 安装Mysql数据库
6. 运行目录不要存在中文

# 配置环境

1. 指向目录下的 数据库安装文件.sql，安装数据库
2. 配置Config.ini配置文件
3. 准备好采集的SRC_URL文本(此步骤可不做)

# 资源消耗

对主机配置略高，最好是SSD硬盘[启动Firefox]

使用的线程数基于CPU处理核心数

实验使用16个线程，在全部启动并发情况下资源消耗


![](/Langzi_SRC_Safe_Cruise_0.97/help/image/1.png)

可以看到还是比较吃资源，所以尽量不要直接开启全部扫描模块，可以先开启部分模块做资产收集，然后开始检测。

即花一天的时间跑子域名监控功能和超链接爬行功能，等到数据库资产差不多了就关闭资产监控功能，开启漏扫功能。

# 进程销毁

当退出关闭扫描器后，其下活动进程会在3分钟内自行关闭，可以通过任务管理器查看进程是否销毁。

# 主扫描表

再开启子域名监控的条件下，通过爆破，搜索引擎获取，以及网页爬行。三种方式不间断的获取domains.txt其下受监控的子域名，保存在主扫描表

![](/Langzi_SRC_Safe_Cruise_0.97/help/image/2.png)

sec\_index主表保存大量受监控的子域名

	SELECT * from sec_index where url like '%.qq.%'

![](/Langzi_SRC_Safe_Cruise_0.97/help/image/11.png)

# 持续性WEB资产获取

在保存网址表中，保存着通过爬行获取到所有的友链数据，包括网址，标题，使用语言，服务器类型，网页内容。

![](/Langzi_SRC_Safe_Cruise_0.97/help/image/4.png)

等到数据量庞大起来后，可以做批量的数据采集调用，比如

	select * from sec_urls where title like '%腾讯%',
	select * from sec_urls where url like '%.qq.%',
	select * from sec_urls where content like '%后台管理系统%',

![](/Langzi_SRC_Safe_Cruise_0.97/help/image/6.png)



# 超链接获取

在超链接表保存着网址的超链接和静态链接，其中静态链接可以使用sqlmap尝试伪静态注入，其他的可以尝试进行不同漏洞检测

![](/Langzi_SRC_Safe_Cruise_0.97/help/image/3.png)


# 报表自动化

在漏扫中填写报告也是个体力活，于是尝试实现了自动化实现，虽然被人骂懒死，但是确实挺方便的。

![](/Langzi_SRC_Safe_Cruise_0.97/help/image/7.png)

![](/Langzi_SRC_Safe_Cruise_0.97/help/image/8.png)

![](/Langzi_SRC_Safe_Cruise_0.97/help/image/9.png)

![](/Langzi_SRC_Safe_Cruise_0.97/help/image/10.png)

# 配置文件

目录下的Config.ini是核心启动控制台，预读大约需要5分钟。

**注意，Config.ini 文件编码为 ANSI，如果不一致则会报错**

	[Server]
	# 数据库配置项
	# 可以做分布式
	host = 127.0.0.1
	username = root
	password = root
	db = langzi_scan
	port = 3306
	
	[Common_Config]
	threads = 16
	# 线程数
	# 建议4-32之间
	
	check_env = 1
	# 每次启动前是否检测运行环境是否完整
	# 可选 0/关闭  1/开启
	key = l95-la4-zh3-li0
	
	[Start_Console]
	start_on = 0
	# 选择批量扫描的URL文本，如果数据库有数据的话，也可以选择不导入文本，直接从数据库继续扫描
	# 可选 0/不提示导入URL文本，直接从数据库提取数据
	# 可选 1/提示导入URL文本
	
	check_alive = 0
	# 检测导入文本的URL存活性检测，只有在设置START_ON=1情况下有效
	# 可选 0/关闭  1/开启
	
	
	[Scan_Modules]
	
	ExtrUrs = 1
	# 提取URL的超链接
	# 可选 0/关闭  1/开启
	
	ExtrUrr = 1
	# 提取URL的超链接，不过有些臃肿，暂时移除
	# 可选 0/关闭  1/开启
	
	ExtrSql = 1
	# 扫描SQL注入漏洞
	# 可选 0/关闭  1/开启
	
	ExtrXss = 1
	# 扫描XSS漏洞
	# 可选 0/关闭  1/开启
	
	
	ExtrUrl = 1
	# 扫描URL跳转漏洞
	# 可选 0/关闭  1/开启
	
	ExtrBac = 1
	# 扫描备份文件源码泄露漏洞
	# 可选 0/关闭  1/开启
	
	
	ExtrRce = 1
	# 扫描命令执行漏洞，不过效率太低，目前版本移除该功能
	# 可选 0/关闭  1/开启
	
	ExtrLfi = 1
	# 扫描任意文件读取漏洞
	# 可选 0/关闭  1/开启
	
	ExtrSsf = 1
	# 扫描SSRF漏洞，效率和误报不算理想，目前版本移除该功能
	# 可选 0/关闭  1/开启
	
	ExtrAut = 1
	# 扫描未授权访问漏洞
	# 可选 0/关闭  1/开启
	
	ExtrInf = 1
	# 扫描信息泄露，包括url开发的敏感端口，敏感路径，后台登陆，搜索引擎寻找漏洞
	# 生成HTML信息报表，和漏扫的结果不一致，显得臃肿，目前版本移除该功能
	# 可选 0/关闭  1/开启
	
	
	ExtrGis = 1
	# git svn 源码泄露扫描
	# 可选 0/关闭  1/开启
	
	
	ExtrCor = 1
	# 扫描CORS劫持漏洞，一些大厂比较多，但是危害性比较小，所以一般都不扫描，设置为0
	# 可选 0/关闭  1/开启
	
	
	ExtrSub_Brute = 1
	# 子域名监控功能 之 子域名爆破
	# 可选 0/关闭  1/开启
	
	ExtrSub_Baidu = 1
	# 子域名监控功能 之 搜索引擎获取子域名
	# 可选 0/关闭  1/开启
	
	ExtrSub_Web = 1
	# 子域名监控功能 之 通过网址爬行获取子域名
	# 可选 0/关闭  1/开启
	
	Keep_Scan = 0
	# 获取网址中所有的友链，并且把获取到的友链保存到扫描表，基本上可以实现见谁日谁，实现无限挂机扫描
	# 扫描机制来源于Yolanda_Scan，但是这一点也是被人诟病的一点，不建议开启
	# 必须在 ExtrSub_Web = 1 的情况下才有效
	# 可选 0/关闭  1/开启
	
	[Scan_Levels]
	
	Scan_Level = 1
	# 扫描等级
	# 可选 1/低级 2/中级 3/高级
	# 默认开1就够了，当然也可选择2或者3
	
	Xss_Level = 1
	# XSS扫描等级
	# 可选 1/低级 2/中级 3/高级 4/特级
	# 默认开1就够了
	
	Back_Level = 1
	# 备份文件扫描等级
	# 可选 1/低级 2/中级 3/高级
	# 不同等级对应的扫描字典规则都不一样，越高代表字典数量越多
	# 默认开1就够了


# 数据库详情

明确每张表的功能和包含数据，方便做调试与资产监控，以及自定义的重复性扫描验证。

功能详见注释

	
	create database if not exists Langzi_Scan;
	use Langzi_Scan;
	
	create table if not exists Sec_Index(
	    id int primary key auto_increment,
	    url varchar(80),
	    extrurs int(1) default 0 comment '爬行获取静态链接和动态参数，状态：0/1',
	    extrurr int(1) default 0 comment '爬行获取命令执行需要的url，状态：0/1',
	    unauth int(1) default 0 comment '（获取未授权需要的url，状态：0/1）',
	    subdomain int(1) default 0 comment '获取子域名，既需要爬行页面相关内容，状态：0/1）',
	    gitsvn int(1) default 0 comment '扫描gitsvn源码泄露，状态：0/1）',
	    backup int(1) default 0 comment '扫描源码泄露，状态：0/1）',
	    info int(1) default 0 comment '（扫描敏感信息路径泄露与开放端口服务，状态：0/1）',
	    cors int(1) default 0 comment '（扫描sors劫持，状态：0/1）',
	    other_vlun int(1) default 0 comment '获取其他类型漏洞，状态：0/1）',
	    create_time timestamp DEFAULT CURRENT_TIMESTAMP
	
	
	)charset =utf8mb4;
	alter table Sec_Index add unique(url);
	
	
	
	create table if not exists Sec_Links_0(
	    id int primary key auto_increment,
	    url varchar(100),
	    links longtext comment '静态链接，类型是一个列表',
	    sqls int(1) default 0 comment '获取sql注入',
	    create_time timestamp DEFAULT CURRENT_TIMESTAMP
	
	)charset =utf8mb4;
	alter table Sec_Links_0 add unique(url);
	
	
	create table if not exists Sec_Links_1(
	    id int primary key auto_increment,
	    url varchar(100) comment '记住，这里是按照深度分类，数量较小',
	    links longtext comment '（一个列表，其中保存动态超链接）',
	    sqls int(1) default 0 comment '（扫描SQL注入，状态：0/1）',
	    xss int(1) default 0 comment '（扫描xss，状态：0/1）',
	    urls int(1) default 0 comment '（扫描url跳转，状态：0/1）',
	    lfi int(1) default 0 comment '（扫描文件包含，文件读取，状态：0/1）',
	    rce int(1) default 0 comment '（扫描命令执行，状态：0/1）',
	    create_time timestamp DEFAULT CURRENT_TIMESTAMP
	
	)charset =utf8mb4;
	alter table Sec_Links_1 add unique(url);
	
	
	create table if not exists Sec_Links_2(
	    id int primary key auto_increment,
	    url varchar(100)comment '记住，这里是按照路径相似度分类，数量较大',
	    links longtext comment '（一个列表，其中保存动态超链接）',
	    sqls int(1) default 0 comment '（扫描SQL注入，状态：0/1）',
	    xss int(1) default 0 comment '（扫描xss，状态：0/1）',
	    urls int(1) default 0 comment '（扫描url跳转，状态：0/1）',
	    lfi int(1) default 0 comment '（扫描文件包含，文件读取，状态：0/1）',
	    rce int(1) default 0 comment '（扫描命令执行，状态：0/1）',
	    create_time timestamp DEFAULT CURRENT_TIMESTAMP
	
	)charset =utf8mb4;
	alter table Sec_Links_2 add unique(url);
	
	
	
	
	create table if not exists Sec_R_links(
	    id int primary key auto_increment,
	    url varchar(100),
	    links longtext comment '（一个字典，其中保存按照命令执行漏洞类型的url链接，比如action，do，jsp，php等）',
	    rce int(1) default 0 comment '（扫描命令执行，状态：0/1）',
	    ssf int(1) default 0 comment '（扫描ssrf，状态：0/1）',
	    create_time timestamp DEFAULT CURRENT_TIMESTAMP
	
	)charset =utf8mb4;
	alter table Sec_R_links add unique(url);
	
	create table if not exists Sec_success(
	    id int primary key auto_increment,
	    url varchar(100),
	    vlun_type longtext comment '保存成功状态',
	    create_time timestamp DEFAULT CURRENT_TIMESTAMP
	)charset =utf8mb4;
	
	
	create table if not exists Sec_Ip_Vluns(
	    id int primary key auto_increment,
	    url varchar(100),
	    ip varchar(16),
	    unau_get int(1) default 0 comment '获取未授权访问',
	    wpas_get int(1) default 0 comment '获取弱口令',
	    port_get int(1) default 0 comment '获取开放端口的信息',
	    other_vlun int(1) default 0 comment '获取其他类型漏洞',
	    create_time timestamp DEFAULT CURRENT_TIMESTAMP
	
	)charset =utf8mb4;
	alter table Sec_Ip_Vluns add unique(ip);
	
	
	create table if not exists Sec_Urls(
	    id int primary key auto_increment,
	    url varchar(80) COMMENT '所有爬行的网页中的链接保存一下,这个功能由子域名爆破的web模块实现',
	    title varchar (80) comment '网页标题',
	    power varchar (80) comment '网址使用脚本语言',
	    server varchar (80) comment '网址服务器类型',
	    content longtext comment '网页内容，到时候可以做URL采集判断',
	    create_time timestamp DEFAULT CURRENT_TIMESTAMP
	
	)charset =utf8mb4;
	alter table Sec_Urls add unique(url);
	
	create table if not exists Sec_Fail_Links(
	    id int primary key auto_increment,
	    url varchar(80) COMMENT '所有爬行的网页中的链接访问失败的保存一下',
	    get_links int(1) default 0 comment '如果需要再次使用，可以做判断',
	    create_time timestamp DEFAULT CURRENT_TIMESTAMP
	
	)charset =utf8mb4;
	alter table Sec_Fail_Links add unique(url);
	
	
	
# 文件详情

**注:勿删文件夹或者修改文件名**

在 Modules 文件夹下的不同文本文件功能：

## domains.txt

保存需要监控的子域名资产，格式如下：

	jd.com
	baidu.com
	qq.com
	iqiyi.com
	....
	
## rar.txt

保存的扫描备份文件字典


## Sub\_Big\_Dict.txt

爆破二级域名字典

## Sub\_Sma\_Dict.txt

爆破三级域名字典

## default.docx

自动化生成报表模板

## geckodriver.exe

FireFox驱动

## result

存储扫描结果报表文件夹，勿删

## _py2.py

检测Python2环境

## black_list

存储网址爬行黑名单，其下的网址不会保存到数据库中

# 误报问题

1. 当扫描目标数量低于线程数*2时，不会开启扫描，所以尽量多导入网址
2. SQL注入使用SQLMAP提供sql注入检测功能，但是也存在误报，误报率在20%
3. XSS检测误报率在10%左右
4. COSR劫持危害性比较小，基本上都不开启扫描功能
5. 关于文件读取基本上都存在误报，不要开启
6. 总的来说，能玩的地方只有子域名监控，git/svn源码泄露扫描，备份文件泄露扫描，xss，sql，url跳转。

# 超链接爬行问题

一共实现了三种方案：

1. 使用requests简单模拟爬虫方式，获取网页下所有的目录和链接，许多通过js生成的数据是获取不到。但是节省资源。
2. 使用selenium操作浏览器，实现自动网页滑动，点击，随后通过mitmproxy中间件获取到所有的URL请求，优点是几乎能抓所有链接和ajax请求，但是消耗资源太大，故本版本移除该功能。
3. 使用pyppeteer对网页自动化操作，然后获取所有的数据请求，和第二点一样，消耗资源太大，故本版本移除该功能。

考虑到以后，提供配置功能，可以选择超链接爬行方式。

# 稳定可用持续性

1. 在运行环境检测中，使用selenium驱动打开网页，但是网页可能有时候不能打开。这一点可以通过修改host文件破解
2. URL跳转漏洞，跳转到的目标网站有时候可能会宕机，无法正确检测到结果。
3. 其他2020年可用性未知。

# 应用限制

1. 无法提供对GOV&EDU扫描功能
2. 低配主机可能无法正常运行，解决方案也很简单，降低线程数，关闭不必要不需要的扫描功能即可。
3. 在CPU使用率到达100%，可能会导致部分扫描功能子模块无法启动，弹窗警告。

# 补充

虽然不能让你在SRC称王称霸，但是在补天一个礼拜换一换桶泡面还是可以的。

试验注册一个新的账号，挂了5天，补天刷到1200名，虽然都是体力活，但是kb还是很香的。当然电费和物理机的负载也是很香的。

任何用扫描器，自动化漏洞挖掘工具找到的漏洞，质量都不会太高，对技术提升也没有太大的作用。但是如果能根据现有的漏洞基础上，加大漏洞的威胁性，对已知漏洞进行组合进一步拓展漏洞的危害，才是SRC中漏扫的意义。

目前版本为0.97版本，还有许多主机，数据库，服务类的漏洞都没有补充完善，漏扫的规则也不是特别满意。完整的后台管理可数据可视化虽然提上日程，但是还在设计阶段。对应漏扫报表的地方，还需要进一步的美化完善。

最后希望大家不要执着于排名与漏洞的数量，应该花费更多的时间去提升漏洞的质量水平，提高自己的技术水准。

# 声明

本软件只做初步探测，无攻击性行为。请使用者遵守《[中华人民共和国网络安全法](http://www.npc.gov.cn/npc/xinwen/2016-11/07/content_2001605.htm)》，勿用于非授权的测试，检测目标仅限于各大SRC，补天SRC，公益SRC进行测试。