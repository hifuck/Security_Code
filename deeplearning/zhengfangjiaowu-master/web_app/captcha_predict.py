from keras.models import load_model
from keras.backend import image_data_format
import numpy as np
import tensorflow as tf

# https://github.com/fchollet/keras/issues/2397

# vars for predict_image(
img_rows, img_cols = 12, 22

if image_data_format() == 'channels_first':
    input_shape = (1, img_rows, img_cols)
else:
    input_shape = (img_rows, img_cols, 1)
    
import string
CHRS = string.ascii_lowercase + string.digits

model = load_model(r'./cnn_dama_final.h5')
graph = tf.get_default_graph()
# keras模型应用于flask app时会报bug !!
# model._make_predict_function() # 不能解决问题
# https://github.com/fchollet/keras/issues/6124
# 以下链接可以解决问题
# https://github.com/fchollet/keras/issues/2397

# vars for predict_image)

def handle_split_image(image):
    '''
    input: image is PIL.Image.open return value
    '''
    im = image.point(lambda i: i != 43, mode='1')
    ## 放大后滤波再二值
    im = im.convert('L') # .filter(ImageFilter.MedianFilter())
    im = im.point(lambda i: i > 25, mode='1')
    y_min, y_max = 0, 22 # im.height - 1 # 26
    split_lines = [5,17,29,41,53]
    ims = [im.crop([u, y_min, v, y_max]) for u, v in zip(split_lines[:-1], split_lines[1:])]
    # w = w.crop(w.getbbox()) # 切掉白边 # 暂不需要
    return ims
   
def _predict_image(images): 
    global graph
    Y = []
    for i in range(4):
        im = images[i]
        test_input = np.concatenate(np.array(im))
        test_input = test_input.reshape(1, *input_shape)
        y_probs = None
        with graph.as_default():
            y_probs = model.predict(test_input)
        y = CHRS[y_probs[0].argmax(-1)]
        Y.append(y)
        # plt.subplot(1,4,i+1)
        # plt.imshow(im, interpolation='none')
        # plt.title("Predicted {}".format(y)) 
    return ''.join(Y) 
    # plt.show()

def predict_image(image):
    '''
    面向外部调用
    '''
    return _predict_image(handle_split_image(image))
    
    
if __name__ == '__main__':
    print('加载模型成功')