from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import range
import urllib.request, urllib.error, urllib.parse, os, tempfile
import numpy as np
from cv2 import resize,imread

"""
实现一些基本的工具库，模块化设计来提高效率。
"""

def blur_image(X):
    """
    模糊操作，用于图像生成
   

    Inputs:
    - X: 图像，形状是 (N, 3, H, W)

    Returns:
    - X_blur: 模糊的 X, 形状是 (N, 3, H, W)
    """
    from cs231n.fast_layers import conv_forward_fast
    w_blur = np.zeros((3, 3, 3, 3))
    b_blur = np.zeros(3)
    blur_param = {'stride': 1, 'pad': 1}
    for i in range(3):
        w_blur[i, i] = np.asarray([[1, 2, 1], [2, 188, 2], [1, 2, 1]],
                                  dtype=np.float32)
    w_blur /= 200.0
    return conv_forward_fast(X, w_blur, b_blur, blur_param)[0]


SQUEEZENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
SQUEEZENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

def preprocess_image(img):
    """对于squeezenet做一些预处理
    
    减去像素均值
    除以标准差
    """
    return (img.astype(np.float32)/255.0 - SQUEEZENET_MEAN) / SQUEEZENET_STD


def deprocess_image(img, rescale=False):
    """逆处理图像."""
    img = (img * SQUEEZENET_STD + SQUEEZENET_MEAN)
    if rescale:
        vmin, vmax = img.min(), img.max()
        img = (img - vmin) / (vmax - vmin)
    return np.clip(255 * img, 0.0, 255.0).astype(np.uint8)


def image_from_url(url):
    """
    从一个URL链接里面读取图像
    """
    try:
        f = urllib.request.urlopen(url)
        _, fname = tempfile.mkstemp()
        with open(fname, 'wb') as ff:
            ff.write(f.read())
        img = imread(fname)
        #os.remove(fname)
        return img
    except urllib.error.URLError as e:
        print('URL Error: ', e.reason, url)
    except urllib.error.HTTPError as e:
        print('HTTP Error: ', e.code, url)


def load_image(filename, size=None):
    """加载，并且调整大小

    Inputs:
    - filename: 文件路径
    - size: 重新调整的大小
    """
    img = imread(filename)
    if size is not None:
        orig_shape = np.array(img.shape[:2])
        min_idx = np.argmin(orig_shape)
        scale_factor = float(size) / orig_shape[min_idx]
        new_shape = (orig_shape * scale_factor).astype(int)
        img = imresize(img, scale_factor)
    return img
