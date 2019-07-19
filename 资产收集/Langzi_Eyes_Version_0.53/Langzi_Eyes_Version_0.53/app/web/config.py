# coding:utf-8
import pymysql
import contextlib
# 这些都是数据库信息
HOST = '127.0.0.1'
# 数据库名字，如果修改数据库名字会创建新的数据库,注意不要重复
DATABASE = 'langzii_eyes'
USER = 'root'
PASSWORD = 'root'
PORT = 3306
DRIVER = 'pymysql'
# 线程数设置
THREADS = 10

THREADED = True
DEBUG = False

# 这两是登陆网页的账号密码
login_uesr = 'admin'
login_pass = 'admin'

SQLALCHEMY_DATABASE_URI = 'mysql+' + DRIVER + '://' + USER + ':' + PASSWORD + '@' + HOST + ':' + str(PORT) + '/' + DATABASE + '?charset=utf8'
SQLALCHEMY_TRACK_MODIFIACTIONS = False
SQLALCHEMY_POOL_SIZE = 50
SQLALCHEMY_POOL_TIMEOUT = 30
SQLALCHEMY_POOL_RECYCLE = -1

# 这几个网址你可以替换成别的，但是注意别忘了有单引号和逗号
# 不过不必要修改，这是比较全的导航了

urls = ['http://www.hao123.com',
        'http://www.cn-hack.cn',
        'https://www.5566.net/hack-.htm',
        'https://hao.360.cn',
        'https://www.2345.com',
        'https://123.sogou.com',
        'http://www.26595.com',
        'http://www.dn1234.com',
        'http://www.best918.com',
        'http://www.baidu.us',
        'http://www.world68.com',
        'http://hao.199it.com',
        'http://www.meddir.cn',
        'http://www.meddir.cn',
        'http://www.36zhen.com/t?id=152',
        'http://www.21industry.com']

@contextlib.contextmanager
def co_mysql(db='mysql'):
    conn = pymysql.connect(host=HOST,user=USER,password=PASSWORD,port=PORT,db=db,charset='utf8')
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()

# 自动创建数据库

'''

判断数据库中是否存在该数据库

'''
with co_mysql(db='mysql') as cursor:
   row_count = cursor.execute("show databases;")
   a = cursor.fetchall()
   b = [y for x in a for y in x]
   if DATABASE in b:
       pass
   else:
       cursor.execute("create database "+ DATABASE )




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
