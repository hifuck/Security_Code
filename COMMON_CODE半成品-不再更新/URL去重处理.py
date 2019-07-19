# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
# coding: utf-8
'''
Created on 2018年7月1日

@author: guimaizi
'''
import urllib.parse,os.path,re
class filter_url:
    def __init__(self):
        self.list_url_static=[]
    def filter_url(self,url):
        url=urllib.parse.urlparse(url)
        if url.query!='':
            print(self.params_filter(url))
            pass
        elif url.query=='':
            self.static_filter(url)
        elif url.path=='':
            print(url)
    def static_filter(self,url):
        #伪静态与url路径处理
        urls=os.path.splitext(url.path)
        if urls[1]!='':
            list_url=[]
            for i in urls[0].split('/'):
                if i!='':list_url.append('{%s:%s}'%(self.judgetype(i),len(i)))
            url_path="/".join(list_url)
            print(url.scheme + '://' + url.netloc +'/'+ url_path + urls[1])
        else:
            list_url=[]
            for i in url.path.split('/'):
                if i!='':list_url.append('{%s:%s}'%(self.judgetype(i),len(i)))
            url_path="/".join(list_url)
            print(url.scheme + '://' + url.netloc +'/'+ url_path)
    def params_filter(self,url):
        #url参数处理
        liststr = []
        try:
            liststr = []
            for i in url.query.split('&'):
                para = i.split('=')
                length_int = len(para[1])
                if self.judgetype(para[1]) == 'int':
                    para[1] = '{int:%s}' % length_int
                else:
                    para[1] = '{str:%s}' % length_int
                para = '='.join(para)
                liststr.append(para)
            url_paras='&'.join(liststr)
            return url.scheme + '://' + url.netloc + url.path + '?' + url_paras
        except:
            length_int = len(url.query)
            url_paras = '{'+self.judgetype(url.query) + ':%s}' % length_int
            return url.scheme + '://' + url.netloc + url.path + '?' + url_paras
    def callback_content(self,content):
        ret = re.split(r'-|_|\.',content)
    def judgetype(self, strs):
        try:
            int(strs)
            return 'int'
        except:
            return 'str'
if __name__ == '__main__':
    urlss = ['http://www.target.cn/zxft/20483.htm?dsdsa','http://www.target.cn/zxft.php',\
             'http://www.target.cn/zxft/20483.htm','http://www.target.cn/zxft/20483.htm?dsdsa=dsadsa&dada=1',\
             'http://www.target.cn/zxft/31231.htm','http://www.target.cn/zxft/31231',\
             'http://www.target.cn/','http://www.target.cn/zxft/20483.htm?dsdsa=ds1adsa&dada=231231',\
             'http://www.target.cn/dsadsa/','http://www.target.cn/2131','http://www.target.cn/user',\
             'http://www.target.cn/da1s_dasd/','http://www.target.cn/das_dasd?das=121','http://www.target.cn/index.php/thanks',\
             'http://www.target.cn/?a=dasd']
    p = filter_url()
    for i in urlss:
        p.filter_url(i)