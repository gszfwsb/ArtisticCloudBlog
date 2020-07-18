import json
import socket
import os


class ClientSocket:
    def __init__(self, config=None):
        # 初始参数
        if config is None:
            config = {'host': '127.0.0.1', 'port': 9999,
                      'bufsize': 1024}
        # print("Host name: ", gethostbyname(gethostname()))
        # 主机IP
        self.host = config['host']
        # 端口号
        self.port = config['port']
        # 地址
        self.address = (self.host, self.port)
        # 单次接收的最大字节数
        self.bufsize = config['bufsize']

    # 删除作品
    def deleteWork(self, token, iid):
        print("deleteWork")
        # 建立连接
        clientSocket = socket.socket()
        clientSocket.connect(('localhost', self.port))
        # 发送需要调用的函数名
        function = "deleteWork"
        clientSocket.send(function.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送token
        clientSocket.send(token.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送iid，并接收结果
        clientSocket.send(iid.encode())
        response = clientSocket.recv(self.bufsize).decode()
        # 将结果返回出去
        return response

    # 获取密保问题
    def getSecurityQes(self, account):
        print("getSecurityQes")
        # 建立连接
        clientSocket = socket.socket()
        clientSocket.connect(('localhost', self.port))
        # 发送需要调用的函数名
        function = "getSecurityQes"
        clientSocket.send(function.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送account，并接收问题
        clientSocket.send(account.encode())
        response = clientSocket.recv(self.bufsize).decode()
        return response

    # 评论作品
    def comment(self, token, iid, content):
        print("comment")
        # 建立连接
        clientSocket = socket.socket()
        clientSocket.connect(('localhost', self.port))
        # 发送需要调用的函数名
        function = "comment"
        clientSocket.send(function.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送token
        clientSocket.send(token.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送iid
        clientSocket.send(iid.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送评论内容，并接收结果
        clientSocket.send(content.encode())
        response = clientSocket.recv(self.bufsize).decode()
        print("客户端 评论 response:", response)
        # 将最新评论ID返回出去
        return response

    # 点赞作品
    def star(self, token, iid):
        print("star")
        # 建立连接
        clientSocket = socket.socket()
        clientSocket.connect(('localhost', self.port))
        # 发送需要调用的函数名
        function = "star"
        clientSocket.send(function.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送token
        clientSocket.send(token.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送iid，并接收最新点赞数
        clientSocket.send(iid.encode())
        response = clientSocket.recv(self.bufsize).decode()
        # 将最新点赞数返回出去
        return response

    # 接收热门作品
    def receiveWork_browse(self, token):
        print("receiveWork_browse")
        # 建立连接
        clientSocket = socket.socket()
        clientSocket.connect(('localhost', self.port))
        # 发送需要调用的函数名
        function = "sendWork_browse"
        clientSocket.send(function.encode())
        clientSocket.recv(self.bufsize).decode()
        # 接收图片数量
        clientSocket.send("receive imgNum".encode())
        imgNum = clientSocket.recv(self.bufsize).decode()
        imgNum = int(imgNum)
        # print("imgNum: ", imgNum)
        # 接收作品
        fileInfoList = []
        for i in range(0, imgNum):
            fileInfoList.append(self.receiveWork(token, clientSocket))
        # 关闭连接
        clientSocket.close()
        # 将文件信息列表返回出去
        return fileInfoList

    # 接收用户个人作品
    def receiveWork_myWork(self, token):
        print("receiveWork_myWork")
        # 建立连接
        clientSocket = socket.socket()
        clientSocket.connect(('localhost', self.port))
        # 发送需要调用的函数名
        function = "sendWork_myWork"
        clientSocket.send(function.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送参数token
        clientSocket.send(token.encode())
        clientSocket.recv(self.bufsize).decode()
        # 接收作品数量
        clientSocket.send("receive imgNum".encode())
        imgNum = clientSocket.recv(self.bufsize).decode()
        imgNum = int(imgNum)
        # print("imgNum: ", imgNum)
        # 接收作品
        fileInfoList = []
        for i in range(0, imgNum):
            fileInfoList.append(self.receiveWork(token, clientSocket))
        # 关闭连接
        clientSocket.close()
        # 将文件信息列表返回出去
        return fileInfoList

    # 接收指定作品（根据图片id）
    def receiveWork_search(self, token, iid):
        print("receiveWork_search")
        # 建立连接
        clientSocket = socket.socket()
        clientSocket.connect(('localhost', self.port))
        # 发送需要调用的函数名
        function = "sendWork_search"
        clientSocket.send(function.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送图片id，并获得回应，若response为空值，则图片不存在
        clientSocket.send(str(iid).encode())
        clientSocket.recv(self.bufsize).decode()
        fileInfoList = []
        # 接收作品
        fileInfo = self.receiveWork(token, clientSocket)
        print("fileInfo: ", fileInfo)
        # fileInfo存在，添加进fileInfoList
        if fileInfo:
            fileInfoList.append(fileInfo)
        # 关闭连接
        clientSocket.close()
        # 将文件信息列表返回出去
        return fileInfoList

    # 接收单个作品（包括图片和图片信息）
    def receiveWork(self, token, clientSocket):
        print("receiveWork")
        # 获取文件信息列表
        clientSocket.send("receive fileInfo".encode())
        jsonFileInfo = clientSocket.recv(self.bufsize).decode('utf-8')

        # 如果jsonFileInfo为空值，则直接返回
        if not jsonFileInfo:
            return

        fileInfo = json.loads(jsonFileInfo)
        # 固定的临时地址
        imgDir = os.path.abspath("../resources/ClientFile/BrowseImage")
        imgDir = imgDir.replace('\\', '/')

        # 修改filePath属性为客户端本地路径
        fileInfo['filePath'] = imgDir + '/' + fileInfo['fileName'] + '.' + fileInfo['fileType']
        # 接收图片
        self.receiveFile(fileInfo['filePath'], clientSocket)
        # 将文件信息列表返回出去
        return fileInfo

    # 上传本地图片
    def sendWork(self, token, filePath, text):
        print("upload")
        # 建立连接
        clientSocket = socket.socket()
        clientSocket.connect(('localhost', self.port))
        # 发送需要调用的函数名
        function = "receiveWork"
        clientSocket.send(function.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送参数token
        clientSocket.send(token.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送图片配文
        clientSocket.send(text.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送图片
        self.sendFile(token, filePath, clientSocket)
        # 接收图片id
        clientSocket.send("receive iid".encode())
        iid = clientSocket.recv(self.bufsize).decode()
        # 关闭连接
        clientSocket.close()
        return iid

    # 风格迁移
    def transfer(self, token, oriImgPath, styImgPath, traImgPath):
        # 建立连接
        clientSocket = socket.socket()
        clientSocket.connect(('localhost', self.port))
        # 发送需要调用的函数名
        function = "transfer"
        clientSocket.send(function.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送生成图片的路径
        clientSocket.send(traImgPath.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送原图片和风格图片
        self.sendFile(token, oriImgPath, clientSocket)
        self.sendFile(token, styImgPath, clientSocket)
        # 等待生成完毕，服务器端发送信号
        clientSocket.send("wait".encode())
        clientSocket.recv(self.bufsize).decode()
        # 接收生成图片
        self.receiveFile(traImgPath, clientSocket)
        clientSocket.send("close".encode())
        clientSocket.recv(self.bufsize).decode()
        # 关闭连接
        clientSocket.close()

    # 接收文件
    def receiveFile(self, filePath, clientSocket):
        # 检测该路径是否存在，若不存在则创建该路径（考虑到多级目录的情况，需要用递归创建目录函数）
        # filePath为客户端本地路径（包含文件名）
        dirName = os.path.dirname(filePath)
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        # 接收文件大小
        clientSocket.send("receive fileSize".encode())
        fileSize = clientSocket.recv(self.bufsize).decode()
        # 接收文件
        clientSocket.send("receive file".encode())
        fileSize = int(fileSize)
        receivedSize = 0
        f = open(filePath, "wb")
        # 通过对比已接收字节数与文件大小来判断文件是否接收完毕
        while receivedSize < fileSize:
            data = clientSocket.recv(self.bufsize)
            f.write(data)
            receivedSize += len(data)
        f.close()

    # 发送文件（发送指定本地路径的文件，在服务器端保存为同名文件，但路径不同）
    def sendFile(self, token, filePath, clientSocket):
        # 发送参数token
        clientSocket.send(token.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送文件名（包括后缀）
        fileName = os.path.basename(filePath)
        clientSocket.send(fileName.encode())
        clientSocket.recv(self.bufsize).decode()

        # 如果路径存在，则开始发送
        if os.path.exists(filePath):
            # 发送文件大小
            fileSize = str(os.path.getsize(filePath))
            print("fileSize", fileSize)
            clientSocket.send(fileSize.encode())
            clientSocket.recv(1024)
            # 发送文件内容
            f = open(filePath, "rb")
            for line in f:
                clientSocket.send(line)
            f.close()
            # 避免粘包
            clientSocket.recv(self.bufsize).decode()
        print("sendFile: ", filePath)

    # 登录
    def login(self, account, password):
        print("login")
        # 建立连接
        clientSocket = socket.socket()
        clientSocket.connect(('localhost', self.port))
        # 发送需要调用的函数名
        function = "login"
        clientSocket.send(function.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送用户输入账户
        clientSocket.send(account.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送用户输入密码
        clientSocket.send(password.encode())
        clientSocket.recv(self.bufsize).decode()
        # 接收登录结果
        clientSocket.send("login".encode())
        response = clientSocket.recv(self.bufsize).decode()
        # 关闭连接
        clientSocket.close()
        # 返回登录结果
        return response

    # 注册
    def register(self, account, password, question, answer):
        print("register")
        # 建立连接
        clientSocket = socket.socket()
        clientSocket.connect(('localhost', self.port))
        # 发送需要调用的函数名
        function = "register"
        clientSocket.send(function.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送用户输入账户
        clientSocket.send(account.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送用户输入密码
        clientSocket.send(password.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送用户输入密保问题
        clientSocket.send(question.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送用户输入密保答案，并接收注册结果
        clientSocket.send(answer.encode())
        response = clientSocket.recv(self.bufsize).decode()
        # 关闭连接
        clientSocket.close()
        # 返回注册结果
        return response

    # 忘记密码
    def forgotPsw(self, account, password, secureAns):
        print("forgotPsw")
        # 建立连接
        clientSocket = socket.socket()
        clientSocket.connect(('localhost', self.port))
        # 发送需要调用的函数名
        function = "forgotPsw"
        clientSocket.send(function.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送用户输入账户
        clientSocket.send(account.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送用户输入新密码
        clientSocket.send(password.encode())
        clientSocket.recv(self.bufsize).decode()
        # 发送用户输入密保答案，并获得结果
        clientSocket.send(secureAns.encode())
        response = clientSocket.recv(self.bufsize).decode()
        # 关闭连接
        clientSocket.close()
        # 返回注册结果
        return response


def main():
    clientSocket = ClientSocket()
    token = clientSocket.login("123", "abc")
    # print("token: ", token)
    oriImgPath = "../resources/ClientFile/OriginalImage/gym.jpg"
    styImgPath = "../resources/ClientFile/StyleImage/muse.jpg"
    traImgPath = "../resources/ClientFile/result/gym_muse.png"
    # clientSocket.transfer(token, oriImgPath, styImgPath, traImgPath)
    clientSocket.receiveWork_search(token, 9527)


if __name__ == '__main__':
    main()
