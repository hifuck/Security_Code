# coding:utf-8
import pymysql
import contextlib
# 这些都是数据库信息
HOST = '127.0.0.1'
# 数据库名字，如果修改数据库名字会创建新的数据库,注意不要重复
DATABASE = 'langzi_eyes'
USER = 'root'
PASSWORD = 'root'
PORT = 3306
DRIVER = 'pymysql'
# 线程数设置
THREADS = 10

THREADED = True
DEBUG = False


SQLALCHEMY_DATABASE_URI = 'mysql+' + DRIVER + '://' + USER + ':' + PASSWORD + '@' + HOST + ':' + str(PORT) + '/' + DATABASE + '?charset=utf8'
SQLALCHEMY_TRACK_MODIFIACTIONS = False
SQLALCHEMY_POOL_SIZE = 50
SQLALCHEMY_POOL_TIMEOUT = 30
SQLALCHEMY_POOL_RECYCLE = -1

# 这几个网址你可以替换成别的，但是注意别忘了有单引号和逗号
# 不过不必要修改，这是比较全的导航了



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



'''
sqlalchemy配置ORM
'''

# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
import time
import contextlib


# 创建数据库ORM模型
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_object(config)
db = SQLAlchemy(app)


class url_index(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    url = db.Column(db.String(80),unique=True,nullable=False)
    checks = db.Column(db.Integer,default=0,index=True)
    time = db.Column(db.String(50),default=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    def __repr__(self):
        return '%s'%self.url


# 这一行代码是创建数据
db.create_all()

@contextlib.contextmanager
def data2mysql():
    try:
        yield db
    except:
        db.session.rollback()
    finally:
        db.session.remove()

# 把几个初始网址添加进去
try:
    for url in config.urls:
        try:
            first_ins = url_index(url=url)
            with data2mysql() as dbs:
                dbs.session.add(first_ins)
                dbs.session.commit()
        except:
            db.session.rollback()

    with config.co_mysql(db=config.DATABASE) as cursor:
        cursor.execute('show databases;')
        a = cursor.fetchall()
        b = [y for x in a for y in x]
        if config.DATABASE in b:
            cursor.execute('alter table info convert to character set utf8')
            cursor.execute('alter table ips convert to character set utf8')
            cursor.execute('alter table really_url_ip convert to character set utf8')
            cursor.execute('alter table cms convert to character set utf8')
            cursor.execute('ALTER TABLE urls ENGINE=MyISAM')
            cursor.execute('ALTER TABLE cms ENGINE=MyISAM')
            cursor.execute('ALTER TABLE ips ENGINE=MyISAM')
            cursor.execute('ALTER TABLE info ENGINE=InnoDB')
            cursor.execute('set global max_connections=100;')
        else:
            cursor.execute('create database ' + config.DATABASE + ';')
            cursor.execute('alter table info convert to character set utf8')
            cursor.execute('alter table ips convert to character set utf8')
            cursor.execute('alter table really_url_ip convert to character set utf8')
            cursor.execute('alter table cms convert to character set utf8')
            cursor.execute('ALTER TABLE urls ENGINE=MyISAM')
            cursor.execute('ALTER TABLE cms ENGINE=MyISAM')
            cursor.execute('ALTER TABLE ips ENGINE=MyISAM')
            cursor.execute('ALTER TABLE info ENGINE=InnoDB')
            cursor.execute('set global max_connections=100;')
    #config.coo_mysql('alter table info convert to character set utf8mb4 collate utf8mb4_bin')

except Exception,e:
    print e
    pass




#
# res = url_index.query.filter('id').count()
# print res

# res = url_index.query.filter(url_index.checks=='10').first()
# print res



