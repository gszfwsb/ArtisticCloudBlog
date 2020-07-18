from BLL.image_style_transfer.style_transfer import *
from BLL.GIFprocessor.vp import *

class Transformer():
    #给定风格图片和对应的参数
    def __init__(self,content,style_img,usr_name):
        self.style_image = style_img
        self.content = content
        self.usr = usr_name
        self.param = None
        self.getParams()
        # print(content)
        # print(style_img)
        # print(usr_name)

    def getParams(self):
        name = getName(self.style_image)

        if name=='composition_vii':
            self.param = {
                'image_size': 192,
                'style_size': 512,
                'content_layer': 3,
                'content_weight': 5e-2,
                'style_layers': (1, 4, 6, 7),
                'style_weights': (20000, 500, 12, 1),
                'tv_weight': 5e-2,
                'epoch': 200
            }
        elif name=='the_scream':
            self.param = {
                'image_size': 192,
                'style_size': 224,
                'content_layer': 3,
                'content_weight': 3e-2,
                'style_layers': [1, 4, 6, 7],
                'style_weights': [200000, 800, 12, 1],
                'tv_weight': 2e-2
            }
        elif name=='starry_night':
            self.param = {
                'image_size': 192,
                'style_size': 192,
                'content_layer': 3,
                'content_weight': 6e-2,
                'style_layers': [1, 4, 6, 7],
                'style_weights': [300000, 1000, 15, 3],
                'tv_weight': 2e-2
            }
        else:
            self.param={
                'image_size': 192,
                'style_size': 192,
                'content_layer': 3,
                'content_weight': 6e-2,
                'style_layers': [1, 4, 6, 7],
                'style_weights': [300000, 1000, 15, 3],
                'tv_weight': 2e-2,
                'epoch': 200
            }

        self.param['content_image'] = self.content
        self.param['style_image'] = self.style_image
        self.param['user_dir'] = self.usr

    def image_transform(self):
        style_transfer(**self.param)

    def video_transform(self):
        '''
        这里视频，每次迭代的时候，需要修改content_image和usr_dir
        :return:
        '''
        vp = GIFProcesser()
        image = vp.GIFToFrame(self.content)
        n = len(image)
        # for i in image:
        #     print(i)
        for i in range(n):
            self.param['content_image']=image[i]
            self.param['user_dir'] = image[i]
            style_transfer(**self.param)

        vp.createGIF(self.usr)




if __name__ == '__main__':
    # import os
    # print(os.getcwd())
    #image
    style_img = '/home/shaobowang/programming/风格迁移前端测试/resources/ClientFile/StyleImage/muse.jpg'
    content_img = '/home/shaobowang/programming/风格迁移前端测试/resources/ClientFile/OriginalImage/hit.jpg'
   # image_transfer = Transformer(content_img,style_img,'/home/shaobowang/programming/风格迁移前端测试/resources/ClientFile/result/a.png')
   # image_transfer.image_transform()

    #video
    import time

    time_start = time.time()

    content_video='/home/shaobowang/programming/风格迁移前端测试/BLL/GIFprocessor/test.gif'
    video_transfer = Transformer(content_video,style_img,'/home/shaobowang/programming/风格迁移前端测试/resources/ClientFile/result/a.gif')
    video_transfer.video_transform()

    time_end = time.time()
    print('time cost', time_end - time_start, 's')

