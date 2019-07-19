from PIL import Image
import io
from bs4 import BeautifulSoup
from requests.utils import quote

from flask import Flask
from flask import request
from flask import jsonify
import gevent
import requests

from gevent import monkey; monkey.patch_all() # 为requests异步打补丁
 
from captcha_predict import predict_image # 需要后于mokey patch
# def predict_image():
    # pass
import datetime; now = datetime.datetime.now

class score_crawler():
    
    def __init__(self, student_id, password):
        '''
        该类需要外部引入 predict_image 函数用于预测验证码
        '''
        self.student_id = student_id
        self.password = password
        self.url_base = requests.get('http://xsweb.scuteo.com/default2.aspx').url.replace('default2.aspx', '')
        self.session = requests.session()
        self.session.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        })

    def _get_image(self):
        '''
        获取验证码
        '''
        url_veri_img = self.url_base + 'CheckCode.aspx'
        res = self.session.get(url_veri_img)
        # print(res.status_code) # 200
        image_file = io.BytesIO(res.content)
        image = Image.open(image_file)
        return image

    def _login(self):
        '''
        单次登录, 调用_get_image()获取验证码
        '''
        url_login = self.url_base + 'default2.aspx'  # 其他风格的登录页面: default3 或 default5 都有验证码
        
        print(url_login)
        res = self.session.get(url_login)
        soup = BeautifulSoup(res.text, "lxml")
        csrf_token = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        ## 先获取csrf_token
        im = self._get_image()
        print('验证码获取完成, 开始预测')
        veri_code = predict_image(im)
        print('预测结果为:', veri_code)
        
        login_data = {
            '__VIEWSTATE': csrf_token,
            'txtUserName': self.student_id,
            'TextBox2': self.password,
            'txtSecretCode': veri_code,
            'RadioButtonList1': '学生'.encode('gbk'),
            'Button1': '',
            'lbLanguage': '',
            'hidPdrs': '',
            'hidsc':  '',
        }
        res = self.session.post(url_login, data=login_data)
        return res

    def _retry_login(self, limit_times=2):
        '''
        尝试指定次数登录, 若成功则返回学生姓名, 调用_login()
        '''
        import re
        try_times = 0
        
        while 1:
            try:
                res = self._login()
                student_name = re.search('&xm=(\w+)&gnmkdm', res.text).group(1)
                print('成功登录')
                return student_name
            except Exception as e:
                print(e)
                try_times += 1
                print('第', try_times, '次尝试失败')
                if try_times >= limit_times:
                    return None
        
    def get_history_scores(self):
        '''
        一般登录成功即可获取成绩, todo: 异常处理
        '''
        student_name = self._retry_login()
        
        if not student_name: 
            return 'error'
            
        new_referer = {'referer': self.url_base + 'xs_main.aspx?xh=%s' % self.student_id}
        self.session.headers.update(new_referer)

        url_history_grade = self.url_base + (
            'xscjcx.aspx?'
            'xh={0}'
            '&xm={1}'
            '&gnmkdm=N121605'
        ).format(self.student_id, quote(student_name.encode('gbk')))

        res = self.session.get(url_history_grade)
        soup = BeautifulSoup(res.text, "lxml")
        csrf_token = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']

        data = {
            '__EVENTTARGET':'',
            '__EVENTARGUMENT':'',
            'hidLanguage': '',
            '__VIEWSTATE': csrf_token,
            'ddLXN':'',
            'ddLXQ':'',
            'ddl_kcxz':'',
            'btn_zcj': '', # 经试验该项可为空 # '历年成绩', # ,'%EF%BF%BD%EF%BF%BD%EF%BF%BD%EF%BF%BD%C9%BC%EF%BF%BD'
        }

        res = self.session.post(url_history_grade, data=data)
        soup = BeautifulSoup(res.text, "lxml")
        table = soup.select_one('.datelist')
        keys = [i.text for i in table.find('tr').find_all('td')]
        scores = [
            dict(zip(
                keys, [i.text.strip() for i in tr.find_all('td')]))
            for tr in table.find_all('tr')[1:]]
        # debug: 
        # print(sorted([[i['成绩'], i['课程名称']] for i in scores], reverse=True))
        return scores

# flask app
# use https://gist.github.com/viksit/b6733fe1afdf5bb84a40
# or can use celery https://stackoverflow.com/questions/31866796/making-an-asynchronous-task-in-flask


app = Flask(__name__)

@app.route('/get_scores', methods=['POST'])
def get_scores():

    student_id = request.form.get('student_id')
    password = request.form.get('password')
    
    origin = request.headers.get('X-Forwarded-For', request.remote_addr)
    app.logger.info(' Time: {0}\n IP: {1}\n'.format(now(), origin))
    
    if student_id and password:
        return jsonify(
            score_crawler(student_id, password).get_history_scores())

    return jsonify(success=False)


if __name__ == '__main__':
    import gevent.pywsgi
    app.debug = False
    print('server on 0.0.0.0:5000')
    gevent_server = gevent.pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    gevent_server.serve_forever()