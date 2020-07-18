# coding=utf-8
import cv2
import imageio
from PIL import Image



class GIFProcesser():

    #需要一个list保存视频转化形成的图片
    def __init__(self):
        self.imageList = []

    # 函数功能：将gif按帧截取，每一帧保存成图片，并将图片名称保存到列表
    # 函数参数：Str类型的videoPath，视频路径，精确到.mp4  .avi
    def GIFToFrame(self,gPath):
        # 变量初始化工作
        img = Image.open(gPath)    #读入gif文件
        timeF = 3    #控制变量：视频帧计数间隔频率
        c = 1    #控制变量：控制视频每隔多少帧进行一次图片保存
        i = 1    #用来生成图片路径 e.g： image1、image2、image3

        from os import getcwd
        result = getcwd()
        for c in range(img.n_frames):
            if (c % timeF == 0):
                img.seek(c)
                new = Image.new("RGB", img.size)
                new.paste(img)
                new.save('image' + str(i) + '.jpg')
                imageName = result + '/image' + str(i) + '.jpg'  # 图片名称
                self.imageList.append(imageName)    #添加到保存图片名称的列表
                i = i+1
            c = c + 1

        return self.imageList


    #函数功能：对self.imageList中所存储的图片进行风格转换，转换结果重新写入self.imageList
    # def translation(self):
    #     pass


    #函数功能：将self.imageList中的图片转换成GIF格式
    #函数参数：Str类型的gif_name，生成gif路径，精确到.gif
    #          duration是生成gif时每张图片的延时
    def createGIF(self,gif_name,duration=0.15):
        image_list = self.imageList
        frames = []
        for image_name in image_list:
            frames.append(imageio.imread(image_name))
        imageio.mimsave(gif_name, frames, 'GIF', duration=duration)


# if __name__ == "__main__":
#     #测试用例
#     #与GUI结合时，需要从GUI传入1、原gif路径，2、生成gif路径
#     #在这里暂时用sPath，GifPath代替
#     #每一次上传新的视频都需要重新生成VideoProcesser对象
#
#     sPath  = '''test.gif'''
#     GifPath = '''tttt2.gif'''
#
#     vp = GIFProcesser()
#     vp.GIFToFrame(sPath)
#     #vp.translation()  #translation函数还未实现
#     vp.createGIF(GifPath)
#     # print(vp.imageList[:5])