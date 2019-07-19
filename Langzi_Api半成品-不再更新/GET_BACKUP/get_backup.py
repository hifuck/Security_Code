# -*- coding: utf-8 -*-
import sys
import requests
import random
requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf-8')



dir_list=['www','data','backup']
backup_name_A = ['.rar','.zip','.tar','.tar.bz2','.sql','.7z','.bak','.txt','.tar.gz','.iso','.gz']
backup_name_C = ['/user.txt', '/uploads.tar', '/config.7z', '/html.tar.bz2', '/deploy.tar.gz', '/db.tar', '/data.zip', '/backup.sql', '/hdocs.tar', '/123.gz', '/backup.tgz', '/root.rar', '/wz.zip', '/www.tar', '/3.tar', '/users.txt', '/bak.rar', '/vip.tar.gz', '/123.tar', '/2015.rar', '/upload.tar', '/back.rar', '/date.zip', '/date.tar', '/web.gz', '/old.tar.bz2', '/bak/wwwroot.rar', '/package.zip', '/htdocs.gz', '/uploads.tar.bz2', '/admin.tar', '/temp.zip', '/123.zip', '/3.rar', '/data.tar', '/old.rar', '/wwwroot.zip', '/beifen.7z', '/config/db.jsp.bak', '/2017.rar', '/2018.zip', '/tools.tar.gz', '/bak/htdocs.tar.gz', '/1.tar', '/upfile.zip', '/2015.bz2', '/admin/admin.tar.gz', '/test.sql', '/database.tar.gz', '/2015.7z', '/website.gz', '/hdocs.zip', '/dump.sql.gz', '/config/config.jsp.bak', '/Release.zip', '/beifen.tar.gz', '/databackup/dvbbs7.mdb', '/123.tar.gz', '/ftp.zip', '/a.tar', '/build.tar.gz', '/ftp.7z', '/wangzhan.rar', '/userlist.tar', '/web.tar.gz', '/website.tgz', '/ftp.tar.gz', '/2014.tar', '/bbs.zip', '/2018.tar', '/tmp.tar.gz', '/backup.sql.gz', '/a.zip', '/beian.rar', '/database.7z', '/ftp.rar', '/index.bak', '/bak.tar.gz', '/2017.tar', '/uploads.tar.gz', '/template.tar', '/webroot.zip', '/test.zip', '/index.tar.tz', '/web.tgz', '/oa.tar.gz', '/site.tar.gz', '/2014.gz', '/wwwroot.tar.bz2', '/upload.zip', '/flashfxp.tar', '/bak.zip', '/upload.tgz', '/bak/wwwroot.zip', '/website.tar.bz2', '/back.tar.gz', '/error_log', '/htdocs.bz2', '/2017.7z', '/code.tar.gz', '/template.zip', '/htdocs.tar.gz', '/test.tar', '/upload.tar.gz', '/upfile.tar', '/oa.tar', '/2014.bz2', '/web.bz2', '/back.tar.bz2', '/2016.bz2', '/date.rar', '/2.tar.gz', '/tmp.zip', '/tmp.tgz', '/flashfxp.tar.gz', '/admin/admin.rar', '/HYTop.mdb', '/old.zip', '/oa.7z', '/index.rar', '/backup.gz', '/html.zip', '/database.tgz', '/uploads.zip', '/2018.gz', '/html.gz', '/bbs.tar', '/2016.tar.bz2', '/update.rar', '/database/PowerEasy2006.mdb', '/db.zip', '/temp.tar.bz2', '/admin.7z', '/�½��ļ���.7z', '/err_log.db', '/2017.zip', '/Release.rar', '/old.7z', '/www.root.zip', '/www.root.tar.gz', '/upload.7z', '/www.tgz', '/temp.7z', '/wz.rar', '/2.rar', '/website.7z', '/sql.tgz', '/inc/config.php.bak', '/config.rar', '/config/config_ucenter.php.bak', '/data.tgz', '/2.0.3.0.sql', '/src.tar.gz', '/www.tar.gz', '/test.tar.gz', '/2.7z', '/db.rar', '/bbs.rar', '/123.bz2', '/template.7z', '/temp.tar.gz', '/userlist.txt', '/beifen.zip', '/wangzhan.tar', '/temp.tgz', '/webserver.tar.gz', '/sql.7z', '/admin.tgz', '/package.rar', '/www.rar', '/wangzhan.zip', '/htdocs.rar', '/bak/2012-12-25.rar', '/wwwroot.tar', '/www.7z', '/bak.tar', '/123.rar', '/beian.tar', '/upload.rar', '/inc/conn.asp.bak', '/www.zip', '/db.7z', '/database.sql.gz', '/users.rar', '/html.tar.gz', '/database.sql', '/uploads.7z', '/htdocs.7z', '/sql.zip', '/data.tar.bz2', '/www.root.7z', '/admin.rar', '/x.tar.gz', '/index.7z', '/database.zip', '/install.tar.gz', '/old.tar.gz', '/www.bz2', '/wwroot.rar', '/admin.sql', '/123.7z', '/hdocs.tar.gz', '/www.root.tar', '/backup.rar', '/back.zip', '/2016.tar', '/bak/2012-12-25.tar.gz', '/a.rar', '/beian.7z', '/inc/db.php.bak', '/1.gz', '/1.rar', '/wwwroot.tar.gz', '/admin.txt', '/website.bz2', '/bbs.7z', '/website.tar', '/include/conn.asp.bak', '/admin.tar.gz', '/tmp.rar', '/users.sql', '/config/config_global.php.bak', '/config.tar.gz', '/backup.bz2', '/2016.zip', '/2016.gz', '/Release.7z', '/2018.tar.bz2', '/package.tar.bz2', '/gg.rar', '/2015.tar.gz', '/wwwroot.7z', '/tmp.tar.bz2', '/update.gz', '/beian.zip', '/2017.tar.bz2', '/2015.tar.bz2', '/back.7z', '/web.7z', '/2.7z.tar.g', '/2014.7z', '/root.tar.gz', '/ewebeditor/db/ewebeditor.mdb', '/2.zip', '/ftp.tar', '/conn.php.bak', '/admin.tar.bz2', '/bak.7z', '/backup.tar', '/www.root.rar', '/oa.zip', '/test.tgz', '/proxy.pac', '/upload.tar.bz2', '/fdsa.rar', '/beifen.rar', '/conf/conf.zip', '/db.sql', '/template.rar', '/output.tar.gz', '/ftp.tar.bz2', '/config.zip', '/index.tar.gz', '/bak.sql', '/include/conn.php.bak', '/a.7z', '/bak/htdocs.rar', '/back.tar', '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php', '/invoker/readonly', '/sql.tar.bz2', '/2014.rar', '/users.zip', '/database.tar.bz2', '/uploads.rar', '/bbs.tar.gz', '/include/config.inc.php.bak', '/2014.tar.bz2', '/database.rar', '/bak/htdocs.zip', '/update.bz2', '/upload.bz2', '/web.tar', '/�½��ļ���.zip', '/website.tar.gz', '/ftp.txt', '/wz.tar.gz', '/1.7z.tar.gz', '/flashfxp.zip', '/a.tar.gz', '/wls-wsat/CoordinatorPortType', '/upload.gz', '/dump.sql', '/Release.tar.gz', '/beifen.tar', '/data.rar', '/db.sqlite', '/update.tar.bz2', '/uploads.bz2', '/html.rar', '/test.tar.bz2', '/db.tgz', '/2015.gz', '/hdocs.7z', '/Release.tar', '/package.tgz', '/2015.zip', '/2016.tar.gz', '/test.7z', '/include/db.php.bak', '/date.tar.gz', '/db.sql.tar', '/html.bz2', '/2.tar', '/website.rar', '/wwwroot.tgz', '/vip.rar', '/2018.tar.gz', '/backup.zip', '/wangzhan.tar.gz', '/db.sql.gz', '/dev.tar', '/db.tar.gz', '/2018.7z', '/web.rar', '/upfile.tar.gz', '/error.log', '/2017.tar.gz', '/wwwroot.rar', '/www.gz', '/1.tar.gz', '/admin.zip', '/2016.7z', '/vip.7z', '/flashfxp.7z', '/o.tar.gz', '/root.zip', '/�½��ļ���.tar.gz', '/bak/2012.tar.gz', '/conf.tar.gz', '/sql.rar', '/wz.7z', '/backup.7z', '/config/db.php.bak', '/2018.rar', '/2.gz', '/root.tar', '/server.cfg', '/2018.bz2', '/htdocs.zip', '/index.tar.bz2', '/2017.bz2', '/vip.tar', '/wwwroot.bz2', '/db.tar.bz2', '/data.sql.gz', '/uploads.gz', '/update.tar.gz', '/2016.rar', '/config/config.php.bak', '/inc/conn.php.bak', '/update.tar', '/backup.tar.bz2', '/bak/wwwroot.tar.gz', '/sql.tar', '/wz.tar', '/db.sql.tar.gz', '/editor/db/ewebeditor.mdb', '/flashfxp.rar', '/www.tar.bz2', '/package.tar.gz', '/ftp.tgz',  '/temp.rar', '/2017.gz', '/bak/2012.rar', '/sql.tar.gz', '/test.rar', '/update.zip', '/config.inc.php.bak', '/2015.tar', '/old.tgz', '/3.zip', '/wwwroot.gz', '/upfile.rar', '/oa.rar', '/update.7z', '/2014.tar.gz', '/root.7z', '/3.7z', '/data.tar.gz', '/html.tar', '/users.tar.gz', '/3.tar.gz', '/backup.tar.gz', '/conn.asp.bak', '/website.zip', '/users.tar', '/beian.tar.gz', '/1.7z', '/wangzhan.7z', '/database/PowerEasy5.mdb', '/upfile.7z', '/hdocs.rar', '/data.7z', '/web.zip', '/temp.tar', '/date.7z', '/template.tar.gz', '/htdocs.tar.bz2', '/vip.zip', '/index.zip', '/2014.zip', '/123.tar.bz2', '/web.tar.bz2', '/html.7z', '/1.zip', '/data.sql']



headerss = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]


def get_backup_file(urlx):
    result = []
    backup_name_B=[]
    #result_list=[]
    # http://www.langzi.fun 或者 http://www.hao.langzi.fun
    k1 = urlx.split('//')[1]
    # www.langzi.fun
    k2 = urlx.split('//')[1].replace('.', '_')
    # www_langzi_fun
    k3 = urlx.split('.', 1)[1].replace('/', '')
    # langzi.fun
    k3_1 = urlx.split('.', 1)[1].replace('/', '').replace('.','_')
    # langzi_fun
    k3_2 = urlx.split('.', 1)[1].replace('/', '').replace('.','')
    # langzifun
    k3_3 = urlx.split('.', 1)[1].replace('/', '').replace('.','-')
    # langzi-fun
    k4 = urlx.split('//')[1].split('.')[1]
    # langzi
    k4_2 = urlx.split('//')[1].split('.')[0] if urlx.split('//')[1].split('.')[0] !='www' else urlx.split('//')[1].split('.')[1]
    # www
    if urlx.find('.')==3:
        k4_1 = urlx.split('//')[1].split('.')[2]
        # fun
        k29 = k4_1 + '2015'
        k30 = k4_1 + '2016'
        k31 = k4_1 + '2017'
        k32 = k4_1 + '2018'
        backup_name_B.append(k4_1)
        backup_name_B.append(k29)
        backup_name_B.append(k30)
        backup_name_B.append(k31)
        backup_name_B.append(k32)

    k17 = k2 + '2015'
    k18 = k2 + '2016'
    k19 = k2 + '2017'
    k20 = k2 + '2018'

    k21 = k3_1 + '2015'
    k22 = k3_1 + '2016'
    k23 = k3_1 + '2017'
    k24 = k3_1 + '2018'

    k25 = k3_2 + '2015'
    k26 = k3_2 + '2016'
    k27 = k3_2 + '2017'
    k28 = k3_2 + '2018'

    k5 = k4 + '2015'
    k6 = k4 + '2016'
    k7 = k4 + '2017'
    k8 = k4 + '2018'
    # langzi2015
    k9 = k1 + '2015'
    k10 = k1 + '2016'
    k11 = k1 + '2017'
    k12 = k1 + '2018'
    # www.langzi.fun2015
    k13 = k3 + '2015'
    k14 = k3 + '2016'
    k15 = k3 + '2017'
    k16 = k3 + '2018'

    backup_name_B.append(k1)
    backup_name_B.append(k2)
    backup_name_B.append(k3)
    backup_name_B.append(k4)
    backup_name_B.append(k5)
    backup_name_B.append(k6)
    backup_name_B.append(k7)
    backup_name_B.append(k8)
    backup_name_B.append(k9)
    backup_name_B.append(k10)
    backup_name_B.append(k11)
    backup_name_B.append(k12)
    backup_name_B.append(k13)
    backup_name_B.append(k14)
    backup_name_B.append(k15)
    backup_name_B.append(k16)
    backup_name_B.append(k17)
    backup_name_B.append(k18)
    backup_name_B.append(k19)
    backup_name_B.append(k20)
    backup_name_B.append(k21)
    backup_name_B.append(k22)
    backup_name_B.append(k23)
    backup_name_B.append(k24)
    backup_name_B.append(k25)
    backup_name_B.append(k26)
    backup_name_B.append(k27)
    backup_name_B.append(k28)
    backup_name_B.append(k3_3)
    backup_name_B.append(k3_2)
    backup_name_B.append(k3_1)
    backup_name_B.append(k4_2)
    try:
        backup_name_B = list(set(backup_name_B))
    except:
        pass

    if urlx.endswith('/'):
        url = urlx
    else:
        url = urlx+'/'

    url_svn = url + '.svn/entries'
    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        r_svn = requests.head(url=url_svn, headers=headers,allow_redirects=False, timeout=5)

        if r_svn.status_code == 200:
            try:
                r_svn_1 = requests.get(url=url_svn, headers=headers, allow_redirects=False, timeout=5)
                if 'dir' in r_svn_1.content and 'svn://' in r_svn_1.content:
                    _ = str(r_svn_1.url) + ':SVN源码泄露'
                    result.append(_)
            except Exception as e:
                pass

        else:
            pass
    except Exception as e:
        pass


    url_git = url + '.git/config'
    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        r_git = requests.head(url=url_git, headers=headers,allow_redirects=False,  timeout=5)

        if r_git.status_code == 200:

            try:
                r_git_1 = requests.get(url=url_git, headers=headers, allow_redirects=False, timeout=5)
                if 'repositoryformatversion' in r_git_1.content:
                    _ = str(r_git_1.url) + ':GIT源码泄露'
                    result.append(_)
                else:
                    pass
            except Exception as e:
                pass
    except Exception as e:
        pass

    url_info = url + 'WEB-INF/web.xml'
    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        r_info = requests.head(url=url_info, headers=headers, allow_redirects=False, timeout=5)
        if r_info.status_code == 200:
            try:
                r_info_1 = requests.get(url=url_info, headers=headers, allow_redirects=False, timeout=5)
                if '<web-app' in r_info_1.content:
                    _ = str(r_info_1.url) + str(':WEBinfo信息泄露')
                    result.append(_)
                else:
                    pass
            except Exception as e:
                pass
    except Exception as e:
        pass

    for x in backup_name_B:
        for y in backup_name_A:
            urll = url.strip('/') + '/' + x + y
            try:
                UA = random.choice(headerss)
                headers = {'User-Agent': UA}
                r_domain = requests.head(url=urll, headers=headers, allow_redirects=False, timeout=5)
                if r_domain.status_code == 200:
                    try:
                        if int(r_domain.headers["Content-Length"]) > 2000000:
                            rar_size = str(int(r_domain.headers["Content-Length"]) / 1000000) + 'M'
                            _ = str(r_domain.url) + ':' + str(rar_size)
                            result.append(_)
                        else:
                            pass
                    except Exception as e:
                        pass
                else:
                    pass
            except Exception, e:
                pass



    for x in backup_name_C:
        urll = url.strip('/')  + x
        try:
            UA = random.choice(headerss)
            headers = {'User-Agent': UA}
            r_domain = requests.head(url=urll, headers=headers, allow_redirects=False, timeout=5)
            if r_domain.status_code == 200:

                try:
                    if int(r_domain.headers["Content-Length"]) > 2000000:
                        rar_size = str(int(r_domain.headers["Content-Length"]) / 1000000) + 'M'
                        _ = str(r_domain.url) + ':' + str(rar_size)
                        result.append(_)

                    else:
                        pass
                except Exception as e:
                    pass
            else:
                pass
        except Exception, e:
            pass

    for x in dir_list:
        for y in backup_name_B:
            for z in backup_name_A:
                urll = url.strip('/') + '/' + x + '/' + y + z
                try:
                    UA = random.choice(headerss)
                    headers = {'User-Agent': UA}
                    r_domain = requests.head(url=urll, headers=headers, allow_redirects=False, timeout=5)

                    if r_domain.status_code == 200:

                        try:
                            if int(r_domain.headers["Content-Length"]) > 2000000:
                                rar_size = str(int(r_domain.headers["Content-Length"]) / 1000000) + 'M'
                                _ = str(r_domain.url) + ':' + str(rar_size)
                                result.append(_)
                            else:
                                pass
                        except Exception as e:
                            pass
                    else:
                        pass
                except Exception, e:
                    pass

    for x in dir_list:
        for y in backup_name_C:
            urll = url.strip('/') + '/' + x + y
            try:
                UA = random.choice(headerss)
                headers = {'User-Agent': UA}
                r_domain = requests.head(url=urll, headers=headers, allow_redirects=False, timeout=5)
                if r_domain.status_code == 200:

                    try:
                        if int(r_domain.headers["Content-Length"]) > 2000000:
                            rar_size = str(int(r_domain.headers["Content-Length"]) / 1000000) + 'M'
                            _ = str(r_domain.url) + ':' + str(rar_size)
                            result.append(_)

                        else:
                            pass
                    except Exception as e:
                        pass
                else:
                    pass
            except Exception, e:
                pass
    if result == []:
        return None
    else:
        return result


if __name__ == '__main__':
    print ('''

             _                           _ 
            | |                         (_)
            | |     __ _ _ __   __ _ _____ 
            | |    / _` | '_ \ / _` |_  / |
            | |___| (_| | | | | (_| |/ /| |
            |______\__,_|_| |_|\__, /___|_|
                                __/ |      Backup_File find
                               |___/       Version:1.0

    ''')
    res = get_backup_file('http://127.0.0.1')
    print res


            
            