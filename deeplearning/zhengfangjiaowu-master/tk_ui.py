# coding:utf-8
model_file_path = 'ok.h5'  
import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
# UI
import tkinter as tk

student_id = ''
password = ''
student_name = ''

class LoginFrame(tk.Frame):
    def __init__(self, master):
        '''
        https://stackoverflow.com/questions/28156719/how-can-i-integrate-tkinter-with-python-log-in-screen
        '''
        super().__init__(master)

        self.label_1 = tk.Label(self, text="账号")
        self.label_2 = tk.Label(self, text="密码")

        self.entry_1 = tk.Entry(self)
        self.entry_2 = tk.Entry(self, show="*")

        self.label_1.grid(row=0, sticky=tk.E)
        self.label_2.grid(row=1, sticky=tk.E)
        self.entry_1.grid(row=0, column=1)
        self.entry_2.grid(row=1, column=1)

        self.logbtn = tk.Button(self, text="登录", command = self._login_btn_clickked)
        self.logbtn.grid(row=0, column=2, rowspan=2)
        
        self.text = tk.Text(self, width=34)
        self.text.insert("end", "请输入校园账号和密码...\n")
        self.text.focus()
        self.text.grid(row=2, columnspan=3)
        self.pack()

    def _login_btn_clickked(self):
        # print("Clicked")
        global student_id, password
        
        student_id = self.entry_1.get()
        password = self.entry_2.get()
        # print(student_id, password)
        score = get_history_scores()
        
        self.text.insert("end", "%s\n" % student_name)
        
        self.text.insert("end", "%s\n" % '\n'.join([i['课程名称'] + ' -> ' + i['成绩'] for i in score]))
        self.text.see(tk.END)
        

# 登录
import keras
from keras import backend as K
import requests
from PIL import Image
import io
import numpy as np
from bs4 import BeautifulSoup
from requests.utils import quote

img_rows, img_cols = 12, 22

if K.image_data_format() == 'channels_first':
    input_shape = (1, img_rows, img_cols)
else:
    input_shape = (img_rows, img_cols, 1)
    
import string
CHRS = string.ascii_lowercase + string.digits

model = keras.models.load_model(model_file_path)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}

url_base = requests.get('http://xsweb.scuteo.com/default2.aspx').url.replace('default2.aspx', '')
session = requests.session()
session.headers.update(headers)

def login():
    url_login = url_base + 'default2.aspx'  # 其他风格的登录页面: default3 或 default5 都有验证码

    res = session.get(url_login)
    soup = BeautifulSoup(res.text, "lxml")
    csrf_token = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    ## 先获取csrf_token
    veri_code = predict_image(handle_split_image(get_image()))
    login_data = {
        '__VIEWSTATE': csrf_token,
        'txtUserName': student_id,
        'TextBox2': password,
        'txtSecretCode': veri_code,
        'RadioButtonList1': '学生'.encode('gbk'),
        'Button1': '',
        'lbLanguage': '',
        'hidPdrs': '',
        'hidsc':  '',
    }
    res = session.post(url_login, data=login_data)
    return res

def get_history_scores():

    import re
    try_times = 0
    while 1:
        try:
            global student_name
            res = login()
            student_name = re.search('&xm=(\w+)&gnmkdm', res.text).group(1)
        except Exception as e:
            # print(e)
            try_times += 1
            if try_times >= 2:
                return None
        else:
            # print('成功登录')
            break
    new_referer = {'referer': url_base + 'xs_main.aspx?xh=%s' % student_id}
    session.headers.update(new_referer)

    url_history_grade = url_base + (
        'xscjcx.aspx?'
        'xh={0}'
        '&xm={1}'
        '&gnmkdm=N121605'
    ).format(student_id, quote(student_name.encode('gbk')))

    res = session.get(url_history_grade)
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

    res = session.post(url_history_grade, headers=headers, data=data)
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


def get_image():

    url_veri_img = url_base + 'CheckCode.aspx'
    res = session.get(url_veri_img)
    image_file = io.BytesIO(res.content)
    image = Image.open(image_file)
    return image

def handle_split_image(image):
    
    im = image.point(lambda i: i != 43, mode='1')
    # im = im.convert('L') # .filter(ImageFilter.MedianFilter())    ## 放大后滤波再二值
    # im = im.point(lambda i: i > 25, mode='1')
    y_min, y_max = 0, 22 # im.height - 1 # 26
    split_lines = [5,17,29,41,53]
    ims = [im.crop([u, y_min, v, y_max]) for u, v in zip(split_lines[:-1], split_lines[1:])]
    # w = w.crop(w.getbbox()) # 切掉白边 # 暂不需要
    return ims
   
def predict_image(images): 
    Y = []
    for i in range(4):
        im = images[i]
        # test_input = np.concatenate(np.array(im))
        test_input = np.array(im)
        test_input = test_input.reshape(1, *input_shape)
        y_probs = model.predict(test_input)
        y = CHRS[y_probs[0].argmax(-1)]
        Y.append(y)
        # plt.subplot(1,4,i+1)
        # plt.imshow(im, interpolation='none')
        # plt.title("Predicted {}".format(y)) 
    return ''.join(Y) 
    # plt.show()


    
root = tk.Tk()
lf = LoginFrame(root)
root.mainloop()
