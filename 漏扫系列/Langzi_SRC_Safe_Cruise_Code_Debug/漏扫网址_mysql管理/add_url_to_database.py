# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import contextlib
import pymysql
from concurrent.futures import ThreadPoolExecutor
user = 'root'
passwd = 'root'
host = '127.0.0.1'
Dbname = 'langzi_scan_3'
port = 3306
@contextlib.contextmanager
def connect_mysql():
    coon = pymysql.connect(user=user, passwd=passwd, host=host, db=Dbname, port=port, charset='utf8')
    cursor = coon.cursor()

    try:
        yield cursor
    except Exception as e:
        print(e)
        pass
    finally:
        coon.commit()
        cursor.close()
        coon.close()

def run(url):
    try:
        with connect_mysql() as coon:
            sql = "insert into sec_scan_index(url) values  ('{}')".format(url)
            print(sql)
            coon.execute(sql)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    All_Urls = [x.strip() for x in open('all_urls.txt','r',encoding='utf-8').readlines()]
    with ThreadPoolExecutor(200) as p:
        p.map(run,All_Urls)
    #for Urls in All_Urls:
        #run(Urls)