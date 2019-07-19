# coding:utf-8
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'login' in session:
            if session['login'] == True:
                return func(*args, **kwargs)
            else:
                return redirect(url_for('web.error'))
        else:
            return redirect(url_for('web.error'))
    return wrapper

