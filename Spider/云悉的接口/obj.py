# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import requests
import time
import re


class Url_Infos:
    def __init__(self,url):
        '''
        因为信息收集需要的参数较多，如果使用单个函数式编程不好对编程进行传递交换
        使用面向对象编程，可以把所有的结果保存在类的实例中
        :param url: 接受参数为传入网址
        '''
        self.url = url
        # 传入网址
        self.language=None
        # 脚本语言
        self.cms = None
        # 使用CMS
        self.os = None
        # 服务器类型
        self.waf = None
        # 防火墙
        self.cdn = None
        # CDN
        self.title=None
        # 网页标题
        self.server=None
        # WEB容器
        self.ip = None
        # IP地址
        self.idc = None
        # 机房位置
        self.icp_name=None
        # 备案公司名称
        self.icp_id=None
        # 备案号
        self.whois_name = None
        # WHOIS 用户信息
        self.whois_dns = None
        # DNS 服务器信息
        self.whois_date = None
        # 域名到期事件
        self.whois_isp = None
        # 域名注册商
        self.whois_mail = None
        # 域名注册人邮箱