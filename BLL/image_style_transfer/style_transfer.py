import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as T
import PIL
import os

import numpy as np

from cv2 import imread
from collections import namedtuple
import matplotlib.pyplot as plt

from BLL.image_style_transfer.image_utils import SQUEEZENET_MEAN, SQUEEZENET_STD

dtype = torch.cuda.FloatTensor
# 导入预训练的SqueezeNet模型
cnn = torchvision.models.squeezenet1_1(pretrained=True).features
cnn.type(dtype)
# 因为不需要更新不必要的参数，我们进一步设置一下
for param in cnn.parameters():
    param.requires_grad = False

def preprocess(img, size=512):
    transform = T.Compose([
        T.Resize(size),
        T.ToTensor(),
        T.Normalize(mean=SQUEEZENET_MEAN.tolist(),
                    std=SQUEEZENET_STD.tolist()),
        T.Lambda(lambda x: x[None]),
    ])
    return transform(img)


def deprocess(img):
    transform = T.Compose([
        T.Lambda(lambda x: x[0]),
        T.Normalize(mean=[0, 0, 0], std=[1.0 / s for s in SQUEEZENET_STD.tolist()]),
        T.Normalize(mean=[-m for m in SQUEEZENET_MEAN.tolist()], std=[1, 1, 1]),
        T.Lambda(rescale),
        T.ToPILImage(),
    ])
    return transform(img)


def rescale(x):
    low, high = x.min(), x.max()
    x_rescaled = (x - low) / (high - low)
    return x_rescaled


def rel_error(x, y):
    return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))


# 提取特征函数
def extract_features(x, cnn):
    """
    用CNN来提取输入图片的特征

    Inputs:
    - x:Tensor (N, C, H, W)
    - cnn: PyTorch model

    Returns:
    - features: 一些列feature，用list呈现A，每一个features[i]都是 (N, C_i, H_i, W_i);
    """
    features = []
    prev_feat = x
    for i, module in enumerate(cnn._modules.values()):
        next_feat = module(prev_feat)
        features.append(next_feat)
        prev_feat = next_feat
    return features

def features_from_img(imgpath, imgsize):
    img = preprocess(PIL.Image.open(imgpath), size=imgsize)
    img_var = img.type(dtype)
    return extract_features(img_var, cnn), img_var


def content_loss(content_weight, content_current, content_original):
    """
    内容损失函数的定义

    Inputs:
    - content_weight: 内容损失的权重Scalar giving the weighting for the content loss.
    - content_current: 当前图片的特征，形状是(1, C_l, H_l, W_l).
    - content_target: 内容图片的特征f，形状是(1, C_l, H_l, W_l).

    Returns:
    - scalar content loss
    """

    N_l, C_l, H_l, W_l = content_current.shape
    M = H_l * W_l
    F = content_current.view(C_l, M)
    P = content_original.view(C_l, M)
    loss = content_weight * torch.sum((F - P) ** 2)

    return loss


def gram_matrix(features, normalize=True):
    """
    计算Gram矩阵

    Inputs:
    - features: 一个张量，形状是(N, C, H, W)
    - normalize: 可选参数，决定是否要归一化矩阵，形状是 (H * W * C)

    Returns:
    - gram: 一个张量，形状是 (N, C, C) 给出N个输入图片的Gram矩阵
    """

    N, C, H, W = features.shape
    F = features.view(N, C, H * W)
    F_T = F.permute(0, 2, 1)  # (N,H*W,C)
    gram = torch.matmul(F, F_T)

    if normalize:
        gram /= (H * W * C)

    return gram


def style_loss(feats, style_layers, style_targets, style_weights):
    """
    计算一系列层的损失函数

    Inputs:
    - feats: 当前每一层的特征
    - style_layers: 层特征的索引
    - style_targets: 风格损失的Gram矩阵，对应的原风格图片
    - style_weights: 风格损失权重

    Returns:
    - style_loss: 风格损失
    """
    loss = 0.
    for i in range(len(style_layers)):
        loss += style_weights[i] * torch.sum((gram_matrix(feats[style_layers[i]].clone()) - style_targets[i]) ** 2)
    return loss


def tv_loss(img, tv_weight):
    """
    总变异loss的权重

    Inputs:
    - img: 图片，形状是 (1, 3, H, W)
    - tv_weight:  TV loss权重

    Returns:
    - loss: 加权的TV loss
    """
    tv1 = torch.sum((img[:, :, 1:, :] - img[:, :, :-1, :]) ** 2)
    tv2 = torch.sum((img[:, :, :, 1:] - img[:, :, :, :-1]) ** 2)

    return tv_weight * (tv1 + tv2)

def getName(path):
    base = os.path.basename(path)
    # print(os.path.splitext(base))
    return os.path.splitext(base)[0]

def style_transfer(user_dir,content_image, style_image, image_size, style_size, content_layer, content_weight,
                   style_layers, style_weights, tv_weight, init_random=False, epoch=200):
    """

    Inputs:
    - content_image: 内容图片文件名
    - style_image: 风格图片文件名
    - image_size: 最小图片的维度大小 (用于content loss和生成图像)
    - style_size: 最小样式图像尺寸
    - content_layer: 用于content loss的层
    - content_weight: 内容损失权重
    - style_layers: 层特征的索引
    - style_weights: 风格损失权重
    - tv_weight:  TV loss权重
    - init_random: 将起始图像初始化为均匀随机噪声
    """

    # 提取内容图像的特征
    content_img = preprocess(PIL.Image.open(content_image), size=image_size).type(dtype)
    feats = extract_features(content_img, cnn)
    content_target = feats[content_layer].clone()

    # 提取样式图像的特征
    style_img = preprocess(PIL.Image.open(style_image), size=style_size).type(dtype)
    feats = extract_features(style_img, cnn)
    style_targets = []
    for idx in style_layers:
        style_targets.append(gram_matrix(feats[idx].clone()))

    # 将输出图像初始化为内容图像或噪声
    if init_random:
        img = torch.Tensor(content_img.size()).uniform_(0, 1).type(dtype)
    else:
        img = content_img.clone().type(dtype)

    # 不计算任何的梯度
    img.requires_grad_()

    # 设定超参数
    initial_lr = 3.0
    decayed_lr = 0.1
    decay_lr_at = 180

    # 最优化。
    optimizer = torch.optim.Adam([img], lr=initial_lr)

    f, axarr = plt.subplots(1, 2)
    axarr[0].axis('off')
    axarr[1].axis('off')
    axarr[0].set_title('Content Source Img.')
    axarr[1].set_title('Style Source Img.')
    axarr[0].imshow(deprocess(content_img.cpu()))
    axarr[1].imshow(deprocess(style_img.cpu()))
    plt.show()
    plt.figure()

    for t in range(epoch):
        if t < 190:
            img.data.clamp_(-1.5, 1.5)
        optimizer.zero_grad()

        feats = extract_features(img, cnn)

        # 计算损失函数
        c_loss = content_loss(content_weight, feats[content_layer], content_target)
        s_loss = style_loss(feats, style_layers, style_targets, style_weights)
        t_loss = tv_loss(img, tv_weight)
        loss = c_loss + s_loss + t_loss

        loss.backward()

        # 对于图片的像素值，进行梯度下降
        if t == decay_lr_at:
            optimizer = torch.optim.Adam([img], lr=decayed_lr)
        optimizer.step()

        if t % 100 == 0:
            print('Iteration {}'.format(t))
            plt.axis('off')
            plt.imshow(deprocess(img.data.cpu()))
            plt.show()
    # print('Iteration {}'.format(t))
    plt.axis('off')
    plt.imshow(deprocess(img.data.cpu()))
    s1 = getName(content_image)
    s2 = getName(style_image)
    # name = s1 + '_' + s2
    #print('result/' + name + '.png')
    plt.savefig(user_dir, dpi=300)
    #plt.show()


















