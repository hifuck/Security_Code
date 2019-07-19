# coding:utf-8
model_file_path = 'ok.h5'
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import keras
from keras import backend as K

from PIL import Image
import numpy as np


img_rows, img_cols = 12, 22

if K.image_data_format() == 'channels_first':
    input_shape = (1, img_rows, img_cols)
else:
    input_shape = (img_rows, img_cols, 1)

import string

CHRS = string.ascii_lowercase + string.digits

model = keras.models.load_model(model_file_path)

def login():
    veri_code = predict_image(handle_split_image(get_image()))
    return veri_code

def get_image():
    image = Image.open('coda.png')
    return image


def handle_split_image(image):
    im = image.point(lambda i: i != 43, mode='1')
    # im = im.convert('L') # .filter(ImageFilter.MedianFilter())    ## 放大后滤波再二值
    # im = im.point(lambda i: i > 25, mode='1')
    y_min, y_max = 0, 22  # im.height - 1 # 26
    split_lines = [5, 17, 29, 41, 53]
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


print(login())
