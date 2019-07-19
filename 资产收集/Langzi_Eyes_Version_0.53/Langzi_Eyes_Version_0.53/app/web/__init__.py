# coding:utf-8
import sys
sys.path.append('..')
reload(sys)
from flask import Blueprint
web = Blueprint('web',__name__)

from web import runmain
