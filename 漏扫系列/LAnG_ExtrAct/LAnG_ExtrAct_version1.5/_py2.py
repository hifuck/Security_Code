# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun
import platform
def run():
    return (platform.python_version()).split('.')[0]
print(run())


