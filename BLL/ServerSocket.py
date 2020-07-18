import json
import os
import socketserver
import sqlite3
import DAL.DBController
from BLL.image_style_transfer.stylize import Transformer


class ServerSocket(socketserver.BaseRequestHandler):
    # 连接建立后
    def handle(self):
        try:
            # 接收需要调用的函数名
            function = self.request.recv(1024).decode()
            # 避免粘包
            self.request.send("function received".encode())
            print("function:", function)
            # 调用对应函数
            self.callFunction(function)
        except Exception as e:
            print(self.client_address, "error:", str(e))
        finally:
            self.request.close()

    # 连接建立时
    def setup(self):
        print("connection start:", self.client_address)

    # 连接结束后
    def finish(self):
        print("connection finish:", self.client_address)

    # 调用函数
    def callFunction(self, function):
        # 函数字典
        functionDict = {'login': self.login,
                        'register': self.register,
                        'transfer': self.transfer,
                        'forgotPsw': self.forgotPsw,
                        'receiveWork': self.receiveWork,
                        'sendWork_browse': self.sendWork_browse,
                        'sendWork_search': self.sendWork_search,
                        'sendWork_myWork': self.sendWork_myWork,
                        'star': self.star,
                        'comment': self.comment,
                        'deleteWork': self.deleteWork,
                        'getSecurityQes': self.getSecurityQes}
        # 根据函数名查询函数字典，自动执行相应函数
        functionDict.get(function)()

    # 删除作品
    def deleteWork(self):
        print("deleteWork")
        # 接收token
        token = self.request.recv(1024).decode()
        self.request.send("token received".encode())
        # 接收作品iid
        iid = self.request.recv(1024).decode()

        # 数据库操作，删除作品
        dbc = DAL.DBController.DBController()
        response = dbc.deleteWork(token, iid)

        # 发送删除的作品ID或者空值
        self.request.send(str(response).encode())

    # 接收用户评论
    def comment(self):
        print("comment")
        # 接收token
        token = self.request.recv(1024).decode()
        self.request.send("token received".encode())
        # 接收作品iid
        iid = self.request.recv(1024).decode()
        self.request.send("iid received".encode())
        # 接收评论内容
        content = self.request.recv(1024).decode()

        # 数据库操作，在数据库中插入评论
        dbc = DAL.DBController.DBController()
        response = dbc.comment(token, iid, content)

        # 发送最新评论ID
        self.request.send(str(response).encode())

    # 接收用户点赞
    def star(self):
        print("star")
        # 接收token
        token = self.request.recv(1024).decode()
        self.request.send("token received".encode())
        # 接收作品iid
        iid = self.request.recv(1024).decode()

        # 数据库操作，查询点赞表，判断该用户是否给该iid的作品点过赞了，如果点过赞就不再增加
        dbc = DAL.DBController.DBController()
        response = dbc.star(token, iid)
        print("服务器 用户点赞 点赞数: ", response)

        # 发送最新点赞数
        self.request.send(str(response).encode())

    # 浏览高点赞数图片
    def sendWork_browse(self):
        # 定义发送图片的数量上限
        N = 5

        # 数据库操作，从数据库中通过iid找到对应作品的相关信息
        dbc = DAL.DBController.DBController()
        response = dbc.getHotWork(N)

        if not response:
            iidList = []
        else:
            iidList = response

        imgNum = len(iidList)
        # print("imgNum ", imgNum)

        # 发送图片数量
        self.request.recv(1024).decode()
        self.request.send(str(imgNum).encode())

        # 发送作品
        for i in range(0, imgNum):
            self.sendWork(iidList[i])

    # 发送用户文件夹内的所有文件
    def sendWork_myWork(self):
        print("sendWork_myWork")
        # 接收token
        token = self.request.recv(1024).decode()
        self.request.send("token received".encode())

        # 数据库操作，从数据库中通过iid找到对应作品的相关信息
        dbc = DAL.DBController.DBController()
        response = dbc.getUserWork(token)

        # 如果返回值为空
        if not response:
            iidList = []
        else:
            iidList = response

        # 暂时指定一个iid列表用于测试
        imgNum = len(iidList)
        # print("imgNum ", imgNum)

        # 发送图片数量
        self.request.recv(1024).decode()
        self.request.send(str(imgNum).encode())

        # 发送作品
        for i in range(0, imgNum):
            self.sendWork(iidList[i])

    # 发送指定图片（根据图片id）
    def sendWork_search(self):
        print("sendWork_search")
        # 接收图片id
        iid = self.request.recv(1024).decode()
        self.request.send("iid received".encode())
        # 发送作品
        self.sendWork(iid)

    # 发送单个作品，包括图片文件以及图片相关信息（传入参数为图片id）
    # 是其他三种发送方式共同调用的基础函数
    def sendWork(self, iid):
        print("sendWork")
        # 存储格式  [图片ID、图片名、路径、账户、点赞、配文、[评论群]]
        # 数据库操作，从数据库中通过iid找到对应作品的相关信息
        dbc = DAL.DBController.DBController()
        response = dbc.getWorkInfo(iid)
        # 返回为空值
        if not response:
            self.request.recv(1024).decode()
            self.request.send(response.encode('utf-8'))
        else:
            fileInfo = response
            # 用json封装发送文件信息字典
            jsonFileInfoList = json.dumps(fileInfo)
            self.request.recv(1024).decode()
            self.request.send(jsonFileInfoList.encode('utf-8'))
            # 最后发送图片文件
            self.sendFile(fileInfo['filePath'])

    # 接收客户端上传的作品并保存在数据库中（只有通过这个函数接收的图片才加入数据库）
    def receiveWork(self):
        print("receiveWork")
        # 接收token
        token = self.request.recv(1024).decode()
        self.request.send("text received".encode())
        # 接收图片配文信息
        text = self.request.recv(1024).decode()
        self.request.send("text received".encode())
        # 接收图片
        filePath, account = self.receiveFile()
        filePath = filePath.replace('\\', '/')
        fileName = os.path.basename(filePath)
        if '.' in fileName:
            fileName, suffix = fileName.split('.', 1)

        # 数据库操作，插入作品
        dbc = DAL.DBController.DBController()
        response = dbc.insertWork(token, fileName, filePath, text)
        # 发送图片id
        self.request.recv(1024).decode()
        self.request.send(str(response).encode())

    # 风格迁移（调用内核接口）
    def transfer(self):
        # 接收生成文件路径（包括文件名与后缀）
        traImgClientPath = self.request.recv(1024).decode()
        self.request.send("traImgPath received".encode())
        print("traImgClientPath", traImgClientPath)
        baseName = os.path.basename(traImgClientPath)

        # 接收原图片与风格图片并获取本地路径
        oriImgPath, account = self.receiveFile()
        styImgPath, account = self.receiveFile()
        self.request.recv(1024).decode()
        print("oriImgPath: ", oriImgPath)
        print("styImgPath: ", styImgPath)

        traImgPath = "../resources/ServerFile" + '/' + account + '/' + baseName
        traImgPath = os.path.abspath(traImgPath)
        print("traImgPath: ", traImgPath)

        name, suffix = oriImgPath.split('.', 1)
        if suffix == 'gif':
            # 这里调用内核的gif风格迁移函数（等待替换）
            content_video = '/home/shaobowang/programming/风格迁移前端测试/BLL/GIFprocessor/test.gif'
            video_transfer = Transformer(oriImgPath, styImgPath, traImgPath)
            video_transfer.video_transform()
            print("gif 内核调用，传入参数为原图片路径、风格图片路径、生成图片路径")
        else:
            print('png')
            # 这里调用内核的png风格迁移函数（等待替换）
            image_transfer = Transformer(oriImgPath, styImgPath, traImgPath)
            image_transfer.image_transform()
            print("png 内核调用，传入参数为原图片路径、风格图片路径、生成图片路径")

        # 图片生成完毕，给客户端发送消息
        self.request.send("OK".encode())
        # 发送生成的文件
        self.sendFile(traImgPath)

        # 迁移流程完毕，把服务器端的临时文件都删除
        os.remove(oriImgPath)
        os.remove(styImgPath)
        # os.remove(traImgPath) # 暂时不删，用于测试

        # 用于阻塞客户端，防止客户端提前关闭连接
        self.request.recv(1024).decode()
        self.request.send("close".encode())

    # 登录
    def login(self):
        # 接收用户输入账户
        account = self.request.recv(1024).decode()
        self.request.send("account received".encode())
        # 接收用户输入密码
        password = self.request.recv(1024).decode()
        self.request.send("password received".encode())
        # 数据库操作，从数据库中查询并对比用户名和密码，如果符合就返回token，否则返回相应错误提示
        dbc = DAL.DBController.DBController()
        response = dbc.login(account, password)
        # 避免粘包
        self.request.recv(1024).decode()
        # 发送结果
        self.request.send(response.encode())

    # 获取密保问题
    def getSecurityQes(self):
        # 接收用户输入账户
        account = self.request.recv(1024).decode()
        # 数据库操作，从数据库中查询并用户名，如果存在就返回问题，否则返回空值
        dbc = DAL.DBController.DBController()
        response = dbc.getSecurityQes(account)
        # 发送结果
        self.request.send(response.encode())

    # 忘记密码
    def forgotPsw(self):
        # 接收账户
        account = self.request.recv(1024).decode()
        self.request.send("account received".encode())
        # 接收新密码
        password = self.request.recv(1024).decode()
        self.request.send("password received".encode())
        # 接收密保答案
        secureAns = self.request.recv(1024).decode()
        # 数据库操作
        dbc = DAL.DBController.DBController()
        response = dbc.forgotPassword(account, password, secureAns)
        print("服务器端 忘记密码， 新密码：", response)
        # 发送结果
        self.request.send(response.encode())

    # 注册
    def register(self):
        # 接收用户输入账户
        account = self.request.recv(1024).decode()
        self.request.send("account received".encode())
        # 接收用户输入密码
        password = self.request.recv(1024).decode()
        self.request.send("password received".encode())
        # 接收用户输入问题
        question = self.request.recv(1024).decode()
        self.request.send("question received".encode())
        # 接收用户输入答案
        answer = self.request.recv(1024).decode()
        # 数据库操作，从数据库中查询并对比用户名和密码，如果未注册就返回成功提示，否则返回空值
        dbc = DAL.DBController.DBController()
        response = dbc.register(account, password, question, answer)
        # 发送注册结果
        self.request.send(str(response).encode())

    # 接收文件
    def receiveFile(self):
        # 接收token
        token = self.request.recv(1024).decode()
        self.request.send("token received".encode())
        # 接收文件名（带后缀）
        fileName = self.request.recv(1024).decode()
        self.request.send("fileName received".encode())
        # 数据库操作，根据token从数据库中获取用户名
        dbc = DAL.DBController.DBController()
        response = dbc.getUSRByToken(token)
        # 查找失败，则返回
        if not response:
            return
        else:
            account = response[1]
        # 服务器本地文件路径
        filePath = "../resources/ServerFile" + '/' + account + '/' + fileName
        filePath = os.path.abspath(filePath)
        # 检测路径是否存在，不存在则递归创建目录
        dirName = os.path.dirname(filePath)
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        # 接收文件大小
        fileSize = self.request.recv(1024).decode()
        # 接收文件
        self.request.send("receive file".encode())
        fileSize = int(fileSize)
        receivedSize = 0
        f = open(filePath, "wb")
        # 通过对比已接收的文件大小来判断文件是否接收完毕
        while receivedSize < fileSize:
            data = self.request.recv(1024)
            f.write(data)
            receivedSize += len(data)
        f.close()
        # 避免粘包
        self.request.send("file received".encode())
        return filePath, account

    # 发送文件
    def sendFile(self, filePath):
        # 如果服务器本地路径存在，则开始发送
        if not os.path.exists(filePath):
            print("错误，未找到文件:", filePath)
            return
        # 发送文件大小
        fileSize = str(os.path.getsize(filePath))
        self.request.recv(1024).decode()
        self.request.send(fileSize.encode())
        # 避免粘包
        self.request.recv(1024)
        # 发送文件
        f = open(filePath, "rb")
        for line in f:
            self.request.send(line)
        f.close()


def main():
    host = "localhost"
    port = 9999
    address = (host, port)
    loginServer = socketserver.ThreadingTCPServer(address, ServerSocket)
    loginServer.serve_forever()


if __name__ == '__main__':
    main()
