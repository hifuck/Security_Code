# coding:utf-8
from database import url_info,url_index,db,cms_info,ips_info,really_url_ip,data2mysql,url_subdomain
from get_info import Get_Info,get_really,remove_data
from config import THREADS
import threading
import time
import random

def run():
    time.sleep(random.randint(1,20))
    time.sleep(random.randint(1,20))
    time.sleep(random.randint(1, 10))
    time.sleep(random.randint(1, 10))
    time.sleep(random.randint(1, 10))
    while 1:
        time.sleep(random.randint(1, 10))
        time.sleep(random.randint(1, 10))
        '''
        这个函数作用是从数据库获取网址
        然后爬行友链
        然后对友链信息监测
        友链保存到数据库
        信息保存到数据库
        '''
        try:
            res = url_index.query.filter(url_index.checks == 0).first()
            res_url = res.url
            res.checks = 1
            with data2mysql() as dbs:
                dbs.session.commit()
            #print res_url
            d = Get_Info(res_url)
            d4 = d.get_urls()
            if d4 != None:
                for x in d4:
                    try:
                        neww = url_index(url=x)
                        with data2mysql() as dbs:
                            dbs.session.add(neww)
                            dbs.session.commit()
                    except Exception,e:
                        db.session.rollback()
                        # print e
                        pass
                    try:
                        newww = url_subdomain(url_s=x)
                        with data2mysql() as dbs:
                            dbs.session.add(newww)
                            dbs.session.commit()
                    except Exception, e:
                        db.session.rollback()

                        # print e
                        pass
            try:
                ip_check = ips_info.query.filter(ips_info.ip_p==str(d.get_ip())).first()
                '''
                这个是判断数据库是否扫描该ip端口
                '''
                d1 = {}
                if ip_check == None:
                    d1 = d.get_ips()
                else:
                    d1['ip'] = ip_check.ip_p
                    d1['ports_open'] = ip_check.port_p
                    d1['ports_info'] = ip_check.info_s_p
                    d1['ports_address'] = ip_check.address_p

                d2 = d.get_infos()
                d2_ = d.get_cms()
                d3 = dict(d1.items() + d2.items() + d2_.items())
                # print '*'*50
                # for x,y in d3.iteritems():
                #     print x + ':' + y
                # print '*'*50

                try:
                    new = url_info(url_i=str(d3['url']), title_i=str(d3['title']), content_i=str(d3['content']),cms_i=str(d3['cms']),
                                   port_open_i=str(d3['ports_open']),port_info_i=str(d3['ports_info']),
                                   service_i=str(d3['service']), ip_i=str(d3['ip']),address_i=str(d3['ports_address']))
                    with data2mysql() as dbs:
                        dbs.session.add(new)
                        dbs.session.commit()
                    
                except Exception,e:
                    #print e
                    db.session.rollback()
                    
                    pass
                try:
                    if d3['cms'] != 'None':
                        new_1 = cms_info(url_c=str(d3['url']),cms_c=str(d3['cms']))
                        with data2mysql() as dbs:
                            dbs.session.add(new_1)
                            dbs.session.commit()
                        
                except Exception,e:
                    #print e
                    db.session.rollback()
                    
                    pass
                try:
                    new_2 = ips_info(url_p=str(d3['url']),ip_p=str(d3['ip']),port_p=str(d3['ports_open']),info_s_p=str(d3['ports_info']),address_p=str(d3['ports_address']))
                    with data2mysql() as dbs:
                        dbs.session.add(new_2)
                        dbs.session.commit()
                    
                except:
                    db.session.rollback()
                    
                    pass

                try:
                    ports = eval(d3['ports_open'])
                    ip = str(d3['ip'])
                    for port in ports:
                        if port == 443:
                            urls = 'https://' + str(ip) + ':' + str(port)
                        else:
                            urls = 'http://' + str(ip) + ':' + str(port)

                        dd = get_really(urls)
                        # print '*'*50
                        # print dd
                        # print '*'*50
                        if dd['title'] == '获取失败' or dd['content'] == '获取失败':
                            pass
                        else:
                            try:
                                new_3 = really_url_ip(url_r=str(dd['url']), ip_r=str(dd['ip']), title_r=str(dd['title']),
                                                      content_r=str(dd['content']),service_r=str(dd['service']))
                                with data2mysql() as dbs:
                                    dbs.session.add(new_3)
                                    dbs.session.commit()
                                
                            except:
                                db.session.rollback()
                                
                                pass
                except Exception,e:
                    pass
                    #print e
            except Exception,e:
                db.session.rollback()
                
                #print e
                pass

        except Exception,e:
            db.session.rollback()
            #print e
            time.sleep(20)

def rems():
    while 1:
        time.sleep(random.randint(100,500))
        time.sleep(random.randint(100,500))
        time.sleep(random.randint(100,500))
        time.sleep(random.randint(100,500))
        remove_data('data')


def run_gogogo():
    for x in range(THREADS):
        t = threading.Thread(target=run).start()
    for i in range(1):
        t1 = threading.Thread(target=rems).start()