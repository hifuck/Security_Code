# coding:utf-8

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

num_classes = 36
batch_size = 128
epochs = 1266

# 输入图片尺寸
img_rows, img_cols = 12, 22

if K.image_data_format() == 'channels_first':
    input_shape = (1, img_rows, img_cols)
else:
    input_shape = (img_rows, img_cols, 1)
    
import os
os.chdir(r'./train_pictures')
import string
CHRS = string.ascii_lowercase + string.digits
from PIL import Image
import numpy as np
import glob

X, Y = [], [] 

for f in glob.glob('*.png')[:]:
    image = Image.open(f)
    im = image.point(lambda i: i != 43, mode='1')

    y_min, y_max = 0, 22
    split_lines = [5,17,29,41,53]
    ims = [im.crop([u, y_min, v, y_max]) for u, v in zip(split_lines[:-1], split_lines[1:])]

    name = f.split('.')[0]
    for i, im in enumerate(ims):
        t = 1.0 * np.array(im)
        t = t.reshape(*input_shape)
        X.append(t)  # 验证码像素列表

        s = name[i]
        Y.append(CHRS.index(s))  # 验证码字符

X = np.stack(X)
Y = np.stack(Y)

Y = keras.utils.to_categorical(Y, num_classes)

split_point = 3000
x_train, y_train, x_test, y_test = X[:split_point], Y[:split_point], X[split_point:], Y[split_point:]

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.save('../ok.h5')
################
# 模型加载
# img_rows, img_cols = 12, 22

# if K.image_data_format() == 'channels_first':
    # input_shape = (1, img_rows, img_cols)
# else:
    # input_shape = (img_rows, img_cols, 1)
    
# import string
# CHRS = string.ascii_lowercase + string.digits

# model = keras.models.load_model(r'.../xx.h5')
