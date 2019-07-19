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

class url_subdomain(db.Model):
    __tablename__ = 'subdomain'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    url_s = db.Column(db.String(80),unique=True,nullable=False)

    def __repr__(self):
        return '%s'%self.url_s

class url_info(db.Model):
    __tablename__ = 'info'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    url_i = db.Column(db.String(50), unique=True,nullable=False)    # 网址
    title_i = db.Column(db.String(100),index=True,nullable=False)   # 标题
    content_i = db.Column(db.Text,nullable=False)                   # 网页内容
    cms_i = db.Column(db.String(30),index=True,nullable=False)      # cms类型
    port_open_i = db.Column(db.String(600),index=True,nullable=False)# 端口开放的
    port_info_i = db.Column(db.Text,nullable=False)                 # 端口开放信息
    service_i = db.Column(db.String(600),nullable=False)            # web容器
    ip_i = db.Column(db.String(20),index=True,nullable=False)       # ip
    address_i = db.Column(db.Text,nullable=False)                   # ip坐标
    time = db.Column(db.String(50),default=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


    def __repr__(self):
        return '%s' % self.url_i

class ips_info(db.Model):
    __tablename__ = 'ips'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    url_p = db.Column(db.String(50), unique=True,nullable=False)  # www.langzi.fun
    ip_p = db.Column(db.String(20), unique=True,nullable=False)   # 127.0.0.1
    port_p = db.Column(db.String(600),index=True,nullable=False)  # 端口
    info_s_p = db.Column(db.Text,nullable=False)                  # 端口信息
    address_p = db.Column(db.Text,nullable=False)                 # ip地址
    time = db.Column(db.String(50),default=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


    def __repr__(self):
        return '%s' % self.url_p

class really_url_ip(db.Model):
    __doc__ = '这张表专门给用于获取网址真实IP，原理是扫描ip全开放端口后，用http协议请求，获取相关信息,使用方法是在这个中搜索标题或者内容，请求到网页判断是否一致'
    __tablename__ = 'really_url_ip'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    url_r = db.Column(db.String(100),unique=True,nullable=False) # 网址
    ip_r = db.Column(db.String(100),unique=True,nullable=False)  # ip
    title_r = db.Column(db.String(100),nullable=False,index=False)# 标题
    content_r = db.Column(db.Text,nullable=False)                # 网页内容
    service_r = db.Column(db.String(100),nullable=False)        # web容器
    time = db.Column(db.String(50), default=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    def __repr__(self):
        return '%s' % self.url_r

class cms_info(db.Model):
    __tablename__ = 'cms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url_c = db.Column(db.String(50), unique=True,nullable=False)
    cms_c = db.Column(db.String(20), index=True,nullable=False)
    time = db.Column(db.String(50),default=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


    def __repr__(self):
        return '%s' % self.url_c



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



