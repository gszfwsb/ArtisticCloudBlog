from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
import BLL.ClientSocket
import BLL.FileSystem


# 登录界面
class LoginWin(QWidget):
    def __init__(self):
        super(LoginWin, self).__init__()
        # 设置窗口背景颜色为白色
        pe = QtGui.QPalette()
        pe.setColor(pe.Background, QtGui.QColor(255, 255, 255))
        self.setPalette(pe)
        # 调整初始窗口位置
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
        self.MainWin = None
        # 设置窗体为只有关闭按钮
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # 窗口总布局
        layout = QHBoxLayout(self.window())
        # 设置总布局内部的间距
        layout.setContentsMargins(0, 0, 0, 0)

        # 放置图片的窗口
        imgWidget = QtWidgets.QWidget()
        imgLayout = QVBoxLayout(imgWidget)

        # 图片标签
        imgLabel = QtWidgets.QLabel()
        # 填充图片
        fileSystem = BLL.FileSystem.FileSystem()
        iconPath = fileSystem.iconPath
        path = iconPath + '/' + "loginImg.png"
        img = QtGui.QImage(path)
        # 设置最大长宽
        maxSize = QtCore.QSize(500, 500)
        # 按比例放缩（最大长宽通过传入的QSize限制）
        loginImg = QtGui.QPixmap.fromImage(img.scaled(maxSize, QtCore.Qt.KeepAspectRatio,
                                                      QtCore.Qt.SmoothTransformation))
        imgLabel.setPixmap(loginImg)
        # 居中
        imgLabel.setAlignment(QtCore.Qt.AlignCenter)
        # 设置图片窗口的内部间距
        imgLayout.setContentsMargins(0, 0, 0, 0)

        # 加入布局
        imgLayout.addWidget(imgLabel)

        # 放置登录界面的窗口
        loginWidget = QtWidgets.QWidget()
        loginWidget.setMinimumSize(300, 400)
        loginWidget.setContentsMargins(0, 5, 5, 0)
        loginLayout = QVBoxLayout(loginWidget)

        # 关闭按钮
        closeButton = QPushButton()
        path = iconPath + '/' + "close.png"
        closeButton.setStyleSheet("QPushButton{border-image: url(%s)}" % path)
        closeButton.setFixedSize(30, 30)
        closeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 介绍词
        welcomeLabel = QTextBrowser()
        welcomeLabel.setText("艺术云博客")
        welcomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        welcomeLabel.setFont(QtGui.QFont("华文彩云", 24, QtGui.QFont.Bold))
        welcomeLabel.setStyleSheet("background:transparent;border-width:0;border-style:outset")

        # 账号与密码框
        self.accountEdit = QLineEdit()
        self.accountEdit.setStyleSheet(
            """background:white;
            padding-left:10px ;
            padding-top:1px ;
            border: 2px solid rgb(209 , 209 , 209);
            border-top:transparent;
            border-left:transparent;
            border-right:transparent;
            """)
        self.accountEdit.setPlaceholderText("请输入用户名")
        self.accountEdit.setMinimumSize(240, 40)

        self.passwordEdit = QLineEdit()
        self.passwordEdit.setStyleSheet(
            """background:white;
            padding-left:10px ;
            padding-top:1px ;
            border: 2px solid rgb(209 , 209 , 209);
            border-top:transparent;
            border-left:transparent;
            border-right:transparent;

            """)
        self.passwordEdit.setPlaceholderText("请输入密码")
        self.passwordEdit.setMinimumSize(240, 40)
        # 设置密码不可见
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        # 按钮
        loginButton = QPushButton()
        loginButton.setFixedSize(240, 40)
        loginButton.setText("登   录")
        loginButton.setStyleSheet("""
            color:white;
            background-color:rgb(14 , 150 , 254);
            border-radius:10px;
            """)
        loginButton.setFont(QtGui.QFont("微软雅黑", 10, QtGui.QFont.Normal))
        loginButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        registerButton = QPushButton("还没有账号？点此注册")
        registerButton.setFlat(True)
        registerButton.setStyleSheet("QPushButton{background: transparent;}")
        registerButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        forgotPswButton = QPushButton("忘记密码")
        forgotPswButton.setFlat(True)
        forgotPswButton.setStyleSheet("color:blue;")
        forgotPswButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # 登录布局添加
        loginLayout.setContentsMargins(0, 0,0 ,0)
        loginLayout.addWidget(closeButton, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        loginLayout.addWidget(welcomeLabel, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(self.accountEdit, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(self.passwordEdit, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(forgotPswButton, 1, QtCore.Qt.AlignRight)
        loginLayout.addWidget(loginButton, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(registerButton, 1, QtCore.Qt.AlignCenter)

        # 总布局添加
        layout.addWidget(imgWidget)
        layout.addWidget(loginWidget)

        # 按钮响应
        loginButton.clicked.connect(self.login)
        registerButton.clicked.connect(self.register)
        forgotPswButton.clicked.connect(self.forgotPsw)
        closeButton.clicked.connect(self.close)
        # 密码栏回车激活登录
        self.passwordEdit.returnPressed.connect(self.login)
        # 设置初始焦点
        self.accountEdit.setFocus()

    # 设置后续要打开以及传入参数的主窗口
    def setMainWin(self, MainWin):
        self.MainWin = MainWin

    # 登录
    def login(self):
        account = self.accountEdit.text()
        password = self.passwordEdit.text()
        if not account or not password:
            simpleMessageBox('提示', '请完整填写输入框')
            return
        try:
            client = BLL.ClientSocket.ClientSocket()
            response = client.login(account, password)
        except Exception as e:
            print(e)
            simpleMessageBox('错误', '无法连接到服务器')
            return
        # 登录失败
        if not response:
            self.accountEdit.clear()
            self.passwordEdit.clear()
            simpleMessageBox('提示', '用户名或密码错误')
        # 登录成功
        else:
            self.MainWin.setUserInfo(response, account)
            self.MainWin.show()
            self.close()

    # 弹出注册窗口
    def register(self):
        self.setVisible(False)
        registerDialog = RegisterDialog()
        registerDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        registerDialog.exec_()
        self.setVisible(True)

    # 弹出忘记密码窗口
    def forgotPsw(self):
        # 首先获取密保问题
        # 弹出窗口，获取用户输入的新笔记名
        account, okPressed = QtWidgets.QInputDialog.getText(self, "忘记密码", "请输入用户名:",
                                                            QtWidgets.QLineEdit.Normal)
        # 若用户未输入或未点击确定按钮，则返回
        if not okPressed or not account:
            return
        # 调用客户端函数获取密保问题
        client = BLL.ClientSocket.ClientSocket()
        response = client.getSecurityQes(account)
        # 查询失败
        if not response:
            self.accountEdit.clear()
            self.passwordEdit.clear()
            simpleMessageBox('提示', '用户名不存在')
            return
        # 查询成功，弹出窗口
        self.setVisible(False)
        forgotPswDialog = ForgotPswDialog(response, account)
        forgotPswDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        forgotPswDialog.exec_()
        self.setVisible(True)

    # 跳过输入阶段，快速启动
    def quickStart(self):
        token = "796ae392-55dd-30cd-be61-6f15e2477771"
        account = "123"
        self.MainWin.setUserInfo(token, account)
        self.MainWin.show()
        self.close()


# 注册窗口
class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        # 设置窗口背景颜色为白色
        pe = QtGui.QPalette()
        pe.setColor(pe.Background, QtGui.QColor(255, 255, 255))
        self.setPalette(pe)
        # 调整初始窗口位置
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
        # 设置窗体为只有关闭按钮
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # 窗口总布局
        layout = QHBoxLayout(self.window())
        # 设置总布局内部的间距
        layout.setContentsMargins(0, 0, 0, 0)

        # 放置图片的窗口
        imgWidget = QtWidgets.QWidget()
        imgLayout = QVBoxLayout(imgWidget)

        # 图片标签
        imgLabel = QtWidgets.QLabel()
        # 填充图片
        fileSystem = BLL.FileSystem.FileSystem()
        iconPath = fileSystem.iconPath
        path = iconPath + '/' + "loginImg.png"
        img = QtGui.QImage(path)
        # 设置最大长宽
        maxSize = QtCore.QSize(500, 500)
        # 按比例放缩（最大长宽通过传入的QSize限制）
        loginImg = QtGui.QPixmap.fromImage(img.scaled(maxSize, QtCore.Qt.KeepAspectRatio,
                                                      QtCore.Qt.SmoothTransformation))
        imgLabel.setPixmap(loginImg)
        # 居中
        imgLabel.setAlignment(QtCore.Qt.AlignCenter)
        # 设置图片窗口的内部间距
        imgLayout.setContentsMargins(0, 0, 0, 0)

        # 加入布局
        imgLayout.addWidget(imgLabel)

        # 放置登录界面的窗口
        loginWidget = QtWidgets.QWidget()
        loginWidget.setMinimumSize(300, 400)
        loginWidget.setContentsMargins(0, 5, 5, 0)
        loginLayout = QVBoxLayout(loginWidget)
        # 设置统一格式
        loginWidget.setStyleSheet(
            """QLineEdit{background:white;
            padding-left:10px ;
            padding-top:1px ;
            border: 2px solid rgb(209 , 209 , 209);
            border-top:transparent;
            border-left:transparent;
            border-right:transparent;
            }
            """)

        # 关闭按钮
        closeButton = QPushButton()
        path = iconPath + '/' + "close.png"
        closeButton.setStyleSheet("QPushButton{border-image: url(%s)}" % path)
        closeButton.setFixedSize(30, 30)
        closeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 介绍词
        welcomeLabel = QTextBrowser()
        welcomeLabel.setText("艺术云博客")
        welcomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        welcomeLabel.setFont(QtGui.QFont("华文彩云", 24, QtGui.QFont.Bold))
        welcomeLabel.setStyleSheet("background:transparent;border-width:0;border-style:outset")

        # 账号、密码、密保问题、密保答案
        self.accountEdit = QLineEdit()
        self.accountEdit.setPlaceholderText("请输入用户名")
        self.accountEdit.setMinimumSize(240, 40)

        self.passwordEdit = QLineEdit()
        self.passwordEdit.setPlaceholderText("请输入密码")
        self.passwordEdit.setMinimumSize(240, 40)

        self.questionEdit = QLineEdit()
        self.questionEdit.setPlaceholderText("请输入密码保护问题")
        self.questionEdit.setMinimumSize(240, 40)

        self.answerEdit = QLineEdit()
        self.answerEdit.setPlaceholderText("请输入密码保护答案")
        self.answerEdit.setMinimumSize(240, 40)

        # 设置密码不可见
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        # 按钮
        registerButton = QPushButton()
        registerButton.setFixedSize(240, 40)
        registerButton.setText("注   册")
        registerButton.setStyleSheet("""
                    color:white;
                    background-color:rgb(14 , 150 , 254);
                    border-radius:10px;
                    """)
        registerButton.setFont(QtGui.QFont("微软雅黑", 10, QtGui.QFont.Normal))
        registerButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        forgotPswButton = QPushButton("忘记密码")
        forgotPswButton.setFlat(True)
        forgotPswButton.setStyleSheet("color:blue;")
        forgotPswButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # 登录布局添加
        loginLayout.setContentsMargins(0, 0, 0, 0)
        loginLayout.addWidget(closeButton, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        loginLayout.addWidget(welcomeLabel, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(self.accountEdit, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(self.passwordEdit, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(self.questionEdit, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(self.answerEdit, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(registerButton, 1, QtCore.Qt.AlignCenter)

        # 总布局添加
        layout.addWidget(imgWidget)
        layout.addWidget(loginWidget)

        # 按钮响应
        registerButton.clicked.connect(self.register)
        closeButton.clicked.connect(self.close)
        # 设置初始焦点
        self.accountEdit.setFocus()

    # 注册
    def register(self):
        account = self.accountEdit.text()
        password = self.passwordEdit.text()
        question = self.questionEdit.text()
        answer = self.answerEdit.text()
        if not account or not password or not question or not answer:
            simpleMessageBox('提示', '请完整填写输入框')
            return

        try:
            client = BLL.ClientSocket.ClientSocket()
            response = client.register(account, password, question, answer)
        except Exception as e:
            print(e)
            simpleMessageBox('错误', '无法连接到服务器')
            return

        if not response:
            simpleMessageBox('提示', '用户名已存在')
        else:
            simpleMessageBox('提示', '账号注册成功')
            self.close()


# 忘记密码窗口
class ForgotPswDialog(QDialog):
    def __init__(self, question, account):
        super().__init__()
        self.account = account
        # 设置窗口背景颜色为白色
        pe = QtGui.QPalette()
        pe.setColor(pe.Background, QtGui.QColor(255, 255, 255))
        self.setPalette(pe)
        # 调整初始窗口位置
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
        # 设置窗体为只有关闭按钮
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # 窗口总布局
        layout = QHBoxLayout(self.window())
        # 设置总布局内部的间距
        layout.setContentsMargins(0, 0, 0, 0)

        # 放置图片的窗口
        imgWidget = QtWidgets.QWidget()
        imgLayout = QVBoxLayout(imgWidget)

        # 图片标签
        imgLabel = QtWidgets.QLabel()
        # 填充图片
        fileSystem = BLL.FileSystem.FileSystem()
        iconPath = fileSystem.iconPath
        path = iconPath + '/' + "loginImg.png"
        img = QtGui.QImage(path)
        # 设置最大长宽
        maxSize = QtCore.QSize(500, 500)
        # 按比例放缩（最大长宽通过传入的QSize限制）
        loginImg = QtGui.QPixmap.fromImage(img.scaled(maxSize, QtCore.Qt.KeepAspectRatio,
                                                      QtCore.Qt.SmoothTransformation))
        imgLabel.setPixmap(loginImg)
        # 居中
        imgLabel.setAlignment(QtCore.Qt.AlignCenter)
        # 设置图片窗口的内部间距
        imgLayout.setContentsMargins(0, 0, 0, 0)

        # 加入布局
        imgLayout.addWidget(imgLabel)

        # 放置登录界面的窗口
        loginWidget = QtWidgets.QWidget()
        loginWidget.setMinimumSize(300, 400)
        loginWidget.setContentsMargins(0, 5, 5, 0)
        loginLayout = QVBoxLayout(loginWidget)
        # 设置统一格式
        loginWidget.setStyleSheet(
            """QLineEdit{background:white;
            padding-left:10px ;
            padding-top:1px ;
            border: 2px solid rgb(209 , 209 , 209);
            border-top:transparent;
            border-left:transparent;
            border-right:transparent;
            }
            """)

        # 关闭按钮
        closeButton = QPushButton()
        path = iconPath + '/' + "close.png"
        closeButton.setStyleSheet("QPushButton{border-image: url(%s)}" % path)
        closeButton.setFixedSize(30, 30)
        closeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 介绍词
        welcomeLabel = QTextBrowser()
        welcomeLabel.setText("艺术云博客")
        welcomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        welcomeLabel.setFont(QtGui.QFont("华文彩云", 24, QtGui.QFont.Bold))
        welcomeLabel.setStyleSheet("background:transparent;border-width:0;border-style:outset")

        # 新的密码、密保问题、密保答案
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setPlaceholderText("请输入新的密码")
        self.passwordEdit.setMinimumSize(240, 40)

        self.questionLabel = QLabel()
        self.questionLabel.setText('问题：' + question)
        self.questionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.questionLabel.setMinimumSize(240, 40)

        self.answerEdit = QLineEdit()
        self.answerEdit.setPlaceholderText("请输入密码保护答案")
        self.answerEdit.setMinimumSize(240, 40)

        # 设置密码不可见
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        # 按钮
        forgotPswButton = QPushButton()
        forgotPswButton.setFixedSize(240, 40)
        forgotPswButton.setText("重置密码")
        forgotPswButton.setStyleSheet("""
                            color:white;
                            background-color:rgb(14 , 150 , 254);
                            border-radius:10px;
                            """)
        forgotPswButton.setFont(QtGui.QFont("微软雅黑", 10, QtGui.QFont.Normal))
        forgotPswButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 登录布局添加
        loginLayout.setContentsMargins(0, 0, 0, 0)
        loginLayout.addWidget(closeButton, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        loginLayout.addWidget(welcomeLabel, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(self.questionLabel, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(self.answerEdit, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(self.passwordEdit, 1, QtCore.Qt.AlignCenter)
        loginLayout.addWidget(forgotPswButton, 1, QtCore.Qt.AlignCenter)

        # 总布局添加
        layout.addWidget(imgWidget)
        layout.addWidget(loginWidget)

        # 按钮响应
        forgotPswButton.clicked.connect(self.forgotPsw)
        closeButton.clicked.connect(self.close)
        # 设置初始焦点
        self.answerEdit.setFocus()

    # 忘记密码
    def forgotPsw(self):
        answer = self.answerEdit.text()
        password = self.passwordEdit.text()
        account = self.account
        if not account or not password or not answer:
            simpleMessageBox('提示', '请完整填写输入框')
            return
        try:
            client = BLL.ClientSocket.ClientSocket()
            response = client.forgotPsw(account, password, answer)
            if response:
                simpleMessageBox('提示', '密码重置成功，新的密码为:' + response)
                self.close()
            else:
                simpleMessageBox('提示', '密保答案错误，密码重置失败')
        except Exception as e:
            print(e)
            simpleMessageBox('错误', '无法连接到服务器')
            return


def simpleMessageBox(title, text):
    messageBox = QMessageBox()
    messageBox.setWindowTitle(title)
    messageBox.setText(text)
    messageBox.setStandardButtons(QMessageBox.Yes)
    buttonY = messageBox.button(QMessageBox.Yes)
    buttonY.setText('确定')
    messageBox.exec_()
