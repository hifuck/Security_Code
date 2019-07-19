# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
with open('src.txt','a+')as a:
	a.writelines(filter(lambda x:'.edu.' not in x and '.gov.' not in x,[x.lstrip() for x in list(set(open('排除台湾.txt','r').readlines()))]))