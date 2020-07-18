from webdav3.client import Client
from datetime import datetime
from webdav3.exceptions import LocalResourceNotFound

import math
# invoke this function every day.
def upload():
    options = {
        'webdav_hostname': "https://dav.jianguoyun.com/dav/backup/",
        'webdav_login': "1192637965@qq.com",
        'webdav_password': "avqcr6ztpywahxzs",
        # 'disable_check': True, #有的网盘不支持check功能
    }
    client = Client(options)
        # 我选择用时间戳为备份文件命名
    file_name = str(math.floor(datetime.now().timestamp())) + '.bak'
    try:
        # 写死的路径，第一个参数是网盘地址
        client.upload('backup/' + file_name, '/home/shaobowang/programming/风格迁移前端测试/BLL/image1.jpg')
        # 打印结果，之后会重定向到log
        print('upload at ' + file_name)
    except LocalResourceNotFound as exception:
        print('An error happen: LocalResourceNotFound ---'  + file_name)

# 如果是直接调用文件，执行upload()
if __name__ == '__main__':
    print('run upload')
    upload()
