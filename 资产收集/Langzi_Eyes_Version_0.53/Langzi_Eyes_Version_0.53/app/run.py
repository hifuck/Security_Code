# -*- coding: utf-8 -*-
# @Time    : 2018/7/19 0019 18:36
# @Author  : Langzi
# @Blog    : www.langzi.fun
# @File    : __init__.py.py
# @Software: PyCharm
import os
from datetime import timedelta
#from flask_cache import Cache
import sys
reload(sys)
sys.path.append('..')
import os
from flask import Flask
sys.setdefaultencoding('utf-8')
from web import config

'''

windows下把masscan添加到环境变量

'''
if os.name == 'nt':
    try:
        lis = (os.path.join(os.getcwd() + '\web\masscan;'))
        if lis in os.environ['PATH']:
            pass
        else:
            os.environ['PATH'] = os.environ['PATH']+ ';' + lis
    except Exception,e:
        print e



def start_Blueprint(app):
    from web import web
    app.register_blueprint(web)

def create_app():
    app = Flask(__name__,template_folder=('web/templates'),static_folder=('web/static'))
    app.config.from_object(config)
    key = os.urandom(24)
    app.config['SECRET_KEY'] = key
    start_Blueprint(app)
    return app


if __name__ == '__main__':
    app = create_app()
    print 'Waiting......'
    app.run(host='0.0.0.0',threaded=True,port=5000)