# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import contextlib
import pymysql
user = 'root'
passwd = 'root'
host = '127.0.0.1'
Dbname = 'lang_cms_finds'
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

def run(count):
    '''
    从数据库中获取到count数值的数据
    并且将这些数据的读取状态改成已读
    :param count:
    :return:
    '''
    get_data_sql = 'select url from vlun_url where get=0 LIMIT 0,{}'.format(count)
    with connect_mysql() as coon:
        coon.execute(get_data_sql)
        res = coon.fetchall()
    for x in res:
        print(x[0])
        with open('urls.txt','a+',encoding='utf-8')as a:
            a.write(x[0] + '\n')

    #     for x in res:
    #

    update_data_sql = 'update vlun_url set get=1 where get=0 limit {}'.format(count)
    with connect_mysql() as coon:
        coon.execute(update_data_sql)


if __name__ == '__main__':
    import os
    if os.path.exists('urls.txt'):
        os.remove('urls.txt')
    run(1000)