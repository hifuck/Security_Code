# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
with open('政府教育.txt','a+')as a:
	a.writelines(filter(lambda x:'edu.cn'  in x or 'gov.cn'  in x,[x.lstrip() for x in list(set(open('alive_urllll.txt','r').readlines()))]))
