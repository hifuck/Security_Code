# coding:utf-8
import os
import time
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
from functools import wraps
from flask import render_template,url_for,request,g,send_from_directory
from flask import flash,get_flashed_messages,redirect
from flask import make_response,session
from . import web
# 导入蓝图
from database import url_info,cms_info,ips_info,really_url_ip,url_subdomain
# 导入数据库
from cms_db import cms_types,cms_counts
# 导入cms指纹种类
from get_info import Get_Info
from get_info import write_data,read_data
from config import login_pass,login_uesr
# 从配置文件导入登陆账号密码

from crawl import run_gogogo
# g.login_success = 0
# 登陆校验

# 导入爬数据函数
'''

因为功能比较少，所以全部功能代码放在一个文件里面
以后拓展功能变多后，不同功能会放在不同文件导入使用

'''

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'login' in session:
            if session['login'] == True:
                return func(*args, **kwargs)
            else:
                return redirect(url_for('web.error'))
        else:
            return redirect(url_for('web.error'))
    return wrapper




@web.route('/')
def index():
    if 'login' in session:
        if session['login'] == True:
            result_count = str(url_info.query.filter('id').count())
            cms_count = str(cms_info.query.filter('id').count())
            ips_count = str(really_url_ip.query.filter('id').count())
            return render_template('search.html',da=result_count,daa=cms_count,daaa=cms_types,daaaa=cms_counts,ad=ips_count)
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')


@web.route('/error/')
def error():
    return render_template('404.html')


# 网页登陆页面
@web.route('/login/',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['pass']
        if user == login_uesr and password == login_pass:
            # res = make_response()
            # res.set_cookie('whoami',login_pass)
            # print request.cookies
            '''
            这里cookies生成失败了，but why？
            '''
            session['login'] = True
            result_count = str(url_info.query.filter('id').count())
            cms_count = str(cms_info.query.filter('id').count())
            ips_count = str(really_url_ip.query.filter('id').count())
            return render_template('search.html',da=result_count,daa=cms_count,daaa=cms_types,daaaa=cms_counts,ad=ips_count)
        else:
            return render_template('404.html')
    else:
        return render_template('404.html')





@web.route('/searchs/',methods=['POST','GET'])
@login_required
def searchs():
    result = {}
    if request.method == 'POST':
        url,title,content,service,ip,port,cms,address,server = request.form['url'],request.form['title'],request.form['content'],request.form['service'],request.form['ip'],request.form['port'],request.form['cms'],request.form['address'],request.form['server']
        if url == '' and title == '' and content == '' and service == '' and ip == '' and port == '' and cms == '' and address == '' and server == '':
            return '请在选项栏输入要求范围内的参数'
        if url != '':
            urls = url_info.query.filter(url_info.url_i.like('%' + str(url) + '%')).all()
            result['urls']=urls
        if title != '':
            titles = url_info.query.filter(url_info.title_i.like('%' + str(title) + '%')).all()
            result['titles'] = titles
        if content != '':
            contents = url_info.query.filter(url_info.content_i.like('%' + str(content) + '%')).all()
            result['contents'] = contents
        if service != '':
            services = url_info.query.filter(url_info.service_i.like('%' + str(service) + '%')).all()
            result['services'] = services
        if ip != '':
            ips = url_info.query.filter(url_info.ip_i.like('%' + str(ip) + '%')).all()
            result['ips'] = ips
        if port != '':
            ports = url_info.query.filter(url_info.port_open_i.like('%' + str(port) + '%')).all()
            result['ports'] = ports
        if cms != '':
            cmss = url_info.query.filter(url_info.cms_i.like('%' + str(cms) + '%')).all()
            result['cms'] = cmss
        if address != '':
            addresss = url_info.query.filter(url_info.address_i.like('%'+ str(address) + '%')).all()
            result['address'] = addresss
        if server != '':
            servers = url_info.query.filter(url_info.port_info_i.like('%'+str(server)+'%')).all()
            result['server'] = servers

        '''
        
        result 字典是这样内容
            {'urls': [http://pt.597.com/, http://school.jjoobb.cn/}
            {'ips': [http://pt.597.com/, http://school.jjoobb.cn/}
            {'ports': [http://pt.597.com/, http://school.jjoobb.cn/}
        字典的键取决于网页是否在相关输入框设置数值
        但是字典的值都是网址，类型为列表
        
        '''
        all_urlss = []
        all_infos = {}
        _ = 0
        result_url = set([x for i in result.values() for x in i])
        # 所有的网址放在一个列表中
        for y in result_url:
            _ += 1
            infos = {}
            _x = str(y)
            inf = url_info.query.filter(url_info.url_i == _x).first()
            infos['url'] = inf.url_i
            infos['title'] = inf.title_i.replace('\\/','-').replace(' ','-')
            infos['cms'] = inf.cms_i.replace('\\/','-').replace(' ','-')
            #infos['content'] = inf.content
            infos['service'] = inf.service_i.replace('\\/','-').replace(' ','-')
            infos['ip'] = inf.ip_i.replace('\\/','-').replace(' ','-')
            infos['port'] = inf.port_open_i.replace('\\/','').replace(' ','')
            infos['server'] = inf.port_info_i.replace('\\/','-').replace(' ','-')
            infos['address'] = inf.address_i.replace('\\/','-').replace(' ','-')
            all_urlss.append(inf.url_i)
            all_urlss.append(inf.ip_i)

            all_infos['Information_' + str(_)] = infos
        #print all_infos
        if all_infos == {}:
            return '数据库没有匹配到此相关网址'
        #all_infos = eval(str(all_infos).decode('unicode-escape'))

        '''
        
        最终的结果，返回的是一个字典类型，格式如下：
        all_infos = {'1':{'url':'http://www.langzi.fun','title'='浪子博客'......}}
        
        '''
        #all_urlss = eval(str(all_urlss).decode('unicode-escape'))
        all_urlss = list(set(all_urlss))
        #write_data(name='data.txt',datas=str(all_urlss))
        dtime = 'data/' + time.strftime('%y-%m-%d-%H-%M-%S',time.localtime())
        write_data(name=dtime + 'url.txt',datas=[x for x in all_urlss if '://' in x])
        write_data(name=dtime + 'ip.txt',datas=[y for y in all_urlss if '://' not in y])
        time.sleep(2)
        return render_template('result.html',all_infos=all_infos,dtime=dtime)

    else:
        return redirect(url_for('web.error'))



@web.route('/cms_map/')
@login_required

def cms_map():
    cms_cou = cms_info.query.filter(cms_info.id).count()
    cms_result = {}
    res = cms_info.query.filter(cms_info.id).all()
    for x in res:
        cms_result.setdefault(x.cms_c,[]).append(x.url_c)
    # if res != []:
    #     flash(cms_result)
    return render_template('cms_map.html',data=cms_result,co=cms_cou)

    '''
    
    查询cms数量数据
    返回格式如下
    
    {
    'dedecms':['http://www.langzi.fun','http://www.123.com'],
    'wordpress':['http://www.wordpress.cn']
    }
    
    '''

@web.route('/cms_list/')
@login_required
def cms_list():
    cms_sss = {}
    _a = 0
    cms_s = []
    cm = cms_info.query.filter(cms_info.cms_c==str(request.args.get('name'))).all()
    for u in cm:
        cms_ss = {}
        cms_ss['url'] = u.url_c
        cms_s.append(u.url_c)
        cms_ss['cms'] = u.cms_c
        _a += 1
        cms_sss['Information_'+str(_a)] = cms_ss
    #write_data(name='data.txt',datas=str(cms_s))
    dtime = 'data/' + time.strftime('%y-%m-%d-%H-%M-%S',time.localtime())
    write_data(name=dtime+'url.txt', datas=[x for x in cms_s if '://' in x])
    write_data(name=dtime+'ip.txt', datas=[y for y in cms_s if '://' not in y])
    flash(cms_s)
    return render_template('result.html',all_infos=cms_sss,dtime=dtime)


@web.route('/ip_map/')
@login_required
def ip_map():
    port_info = []
    port_count = []
    server_p = ips_info.query.filter('id').all()
    for x in server_p:
        dx = eval(x.info_s_p)
        for _ in dx:
            port_info.append(_.split(':')[1])
        try:
            xd = eval(str(x.port_p))
        except:
            xd = eval(str(x.port_p) + ']')
        for _a in xd:
            port_count.append(_a)

    port_infos = dict.fromkeys(port_info,0)
    for xx in port_info:
        port_infos[xx] += 1
        '''
        
        这里返回的是一个字典，存储的是端口服务和数量
        
        {
        'mysql':39,
        'http':10
        }
        
        '''
    port_counts = dict.fromkeys(port_count,0)
    for aa in port_count:
        port_counts[aa] += 1

    po_cs = len(port_count)
    for x,y in port_counts.iteritems():
        port_counts[x] = str(str((format(float(y*100)/float(po_cs),'.5f'))) + '%')
        '''
        
        {
        80端口：’30%‘,
        ...
        }
        
        '''
    banner_count = len(port_info)
    ips_count = len(server_p)

    return render_template('ip_map.html',data=port_infos,bc=banner_count,ic=ips_count,dataa=port_counts)

@web.route('/ip_lists/')
@login_required
def ip_lists():
    ipf_sss = {}
    _a = 0
    ipf_s = []
    ipfs = ips_info.query.filter(ips_info.info_s_p.like('%'+request.args.get('name') + '%')).all()
    for u in ipfs:
        ipf_ss = {}
        ipf_ss['url'] = u.url_p
        ipf_s.append(u.url_p)
        ipf_ss['ip'] = u.ip_p
        ipf_s.append(u.ip_p)
        ipf_ss['port'] = u.port_p
        ipf_ss['portf'] = u.info_s_p
        ipf_ss['address'] = u.address_p
        _a += 1
        ipf_sss['Information_'+str(_a)] = ipf_ss
    dtime = 'data/' + time.strftime('%y-%m-%d-%H-%M-%S',time.localtime())
    #write_data(name='data.txt',datas=str(ipf_s))
    write_data(name=dtime+'url.txt', datas=[x for x in ipf_s if '://' in x])
    write_data(name=dtime+'ip.txt', datas=[y for y in ipf_s if '://' not in y])
    return render_template('result.html',all_infos=ipf_sss,dtime=dtime)


@web.route('/ip_list/')
@login_required
def ip_list():
    lis = []
    d = Get_Info(str(request.args.get('url')))
    d1 = d.get_infos()
    d_title,d_content = d1['title'],d1['content']
    res_1 = really_url_ip.query.filter(really_url_ip.title_r==d_title).first()
    res_2 = really_url_ip.query.filter(really_url_ip.content_r==d_content).first()

    if res_1 == None and res_2 == None:
        return '数据库暂时没有匹配检测到该URL真实IP'
    else:
        if res_1 != None:
            really_ip = res_1.ip_r
            lis.append(res_1.url_r)
        else:
            really_ip = res_2.ip_i
            lis.append(res_2.url_r)

    '''
    
    这段代码的作用是检测传入网址的真实IP地址
    原理是获取传入网址的标题和网页内容
    然后与 really_url_ip 这个表中的标题和网页内容进行对比
    因为这个表的作用是扫描ip的全部端口
    然后以http协议请求开放的端口，如果正常就返回网页的标题和内容
    
    '''
    infos={}
    inf = url_info.query.filter(url_info.ip_i==really_ip).first()
    infos['url'] = inf.url_i
    infos['title'] = inf.title_i.replace('\\/', '-').replace(' ', '-')
    infos['cms'] = inf.cms_i.replace('\\/', '-').replace(' ', '-')
    infos['service'] = inf.service_i.replace('\\/', '-').replace(' ', '-')
    infos['ip'] = inf.ip_i.replace('\\/', '-').replace(' ', '-')
    infos['port'] = inf.port_open_i.replace('\\/', '').replace(' ', '')
    infos['server'] = inf.port_info_i.replace('\\/', '-').replace(' ', '-')
    infos['address'] = inf.address_i.replace('\\/', '-').replace(' ', '-')
    lis.append(really_ip)

    #write_data(name='data.txt',datas=str(lis))
    dtime = 'data/' + time.strftime('%y-%m-%d-%H-%M-%S',time.localtime())
    write_data(name=dtime+'url.txt', datas=[x for x in lis if '://' in x])
    write_data(name=dtime+'ip.txt', datas=[y for y in lis if '://' not in y])
    flash(lis)
    return render_template('result.html',all_info=infos,dtime=dtime)


@web.route('/subip/')
@login_required
def subip():
    urlips = url_subdomain.query.filter(url_subdomain.url_s.like('%'+str(request.args.get('url')) + '%')).all()
    if urlips == None or urlips == [] or urlips == '':
        return '数据库暂时无该网址子域名'
    else:
        return render_template('subdomain.html',data=urlips)



@web.route('/urls/')
@login_required
def urls():
    try:
        dt = request.args.get('dtime')
        data = read_data(name=dt+'url.txt')
        data = list(set([x for x in data if '://' in x]))
        if data == [] or data =='' or data == None:
            return '返回上一步刷新页面后重试，如果还是如此说明该表无URL相关数据，请在主页进行搜索'
        else:
            return render_template('urls.html',data=data)
    except:
        return '返回上一页并且刷新页面后重新下载'



@web.route('/ips/')
@login_required
def ips():
    try:
        dt = request.args.get('dtime')
        data = read_data(name=dt+'ip.txt')
        data = list(set([x for x in data if '://' not in x]))
        data = [x for x in data if x.count('.') == 3]
        if data == [] or data =='' or data == None:
            return '返回上一步刷新页面后重试，如果还是如此说明该表无IP相关数据，请在主页进行搜索'
        else:
            return render_template('urls.html',data=data)
    except:
        return '返回上一页并且刷新页面后重新下载'



'''

下面这两个函数是下载文件用的
分别用来下载网址和IP

'''
@web.route('/durls/')
@login_required
def durls():
    try:
        directory = os.getcwd()  # 假设在当前目录
        finename=request.args.get('dtime')+'url.txt'
        response = make_response(send_from_directory(directory, finename, as_attachment=True))
        response.headers["Cache-Control"] = 'no-cache'
        response.headers["Content-Disposition"] = "attachment; filename={}".format(finename.encode().decode('latin-1'))
        return response
    except:
        return '返回上一页并且刷新页面后重新下载'

@web.route('/dips/')
@login_required
def dips():
    try:
        directory = os.getcwd()  # 假设在当前目录
        finename=request.args.get('dtime')+'ip.txt'
        response = make_response(send_from_directory(directory, finename, as_attachment=True))
        response.headers["Cache-Control"] = 'no-cache'
        response.headers["Content-Disposition"] = "attachment; filename={}".format(finename.encode().decode('latin-1'))
        return response
    except:
        return '返回上一页并且刷新页面后重新下载'

run_gogogo()
