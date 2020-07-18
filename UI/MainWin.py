import sys

import UI.Ui_MainWin
import UI.LookResult
import BLL.ClientSocket
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog


# 主界面的操作实现类（继承了主界面的控件声明类）
class MainWin(QtWidgets.QMainWindow, UI.Ui_MainWin.Ui_MainWin):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        # 窗口组件初始化
        self.setupUi(self)
        # 设置窗口名称
        self.setWindowTitle("风格迁移")
        # 文件信息列表初始化
        self.fileInfoList = []
        # token初始化
        self.token = ""
        # 用户名初始化
        self.account = ""
        # 客户端套接字初始化
        self.clientSocket = BLL.ClientSocket.ClientSocket()
        # 点击风格图片栏中选项，触发选择风格
        self.styImgListWidget.clicked.connect(self.selectStyImg_default)
        # 点击左右按钮，滚动风格图片栏
        self.leftButton.clicked.connect(self.left)
        self.rightButton.clicked.connect(self.right)
        # 点击原图片标签，触发选择图片
        self.oriImgLabel.clicked.connect(self.selectOriImg)
        # 点击风格图片标签，触发上传本地图片作为风格
        self.styImgLabel.clicked.connect(self.selectStyImg_upload)
        # 点击开始迁移按钮
        self.transferButton.clicked.connect(self.transfer)
        # 当前正在操作的原图片路径
        self.oriImgPath = ""
        # 当前正在操作的风格图片路径
        self.styImgPath = ""
        # 生成图片弹出窗口
        self.__lookResult = None
        self.__isLookingResult = False

    # LookResult的方法
    def look_result(self, file_location: str):
        if self.__isLookingResult is False:
            self.__isLookingResult = True
            self.__lookResult = UI.LookResult.LookResult(file_location)
            if self.__lookResult.get_init_status() is True:
                self.__lookResult.closeSignal.connect(self.__change_look_result_status)
            else:
                self.__change_look_result_status()
        else:
            QtWidgets.QMessageBox.information(self, "提示", "请先关闭当前查看窗口！\n然后重试！", QtWidgets.QMessageBox.Yes)
            # 跳转到当前正在预览的窗口，方便用户关闭
            self.__lookResult.setWindowState(QtCore.Qt.WindowActive)

    # LookResult的方法
    def __change_look_result_status(self):
        self.__isLookingResult = False

    # 风格迁移(这里需要调用内核的接口)
    def transfer(self):
        if self.oriImgPath == '':
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('提示')
            messageBox.setText('请选择需要风格迁移的图片')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Yes)
            buttonY.setText('确定')
            messageBox.exec_()
            return

        if self.styImgPath == '':
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('提示')
            messageBox.setText('请选择需要迁移的风格')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Yes)
            buttonY.setText('确定')
            messageBox.exec_()
            return

        # 通过当前正在操作的原图片和风格图片的路径生成迁移后图片的名称以及路径（路径在fileSystem中指定）
        traImgPath = self.fileSystem.getTraImgPath(self.oriImgPath, self.styImgPath)
        # 调用客户端套接字的函数，发送原图片、风格图片，接收生成图片
        self.clientSocket.transfer(self.token, self.oriImgPath, self.styImgPath, traImgPath)
        # 弹出窗口显示生成图片
        self.look_result(traImgPath)

    # 向左滚动风格图片栏
    def left(self):
        curRow = self.styImgListWidget.currentRow()
        if curRow <= 0:
            return
        self.styImgListWidget.setCurrentRow(curRow-1)
        self.selectStyImg_default()

    # 向右滚动风格图片栏
    def right(self):
        curRow = self.styImgListWidget.currentRow()
        if curRow >= self.styImgListWidget.count() - 1:
            return
        self.styImgListWidget.setCurrentRow(curRow+1)
        self.selectStyImg_default()

    # 选择风格图片（用户上传的自定义风格）
    def selectStyImg_upload(self):
        file = QFileDialog.getOpenFileName(self.centralwidget, "选择图片", self.fileSystem.styImgDirPath,
                                           "jpg图片 (*jpg)")
        filePath = file[0]
        if not filePath:
            return
        # 获取图片
        img = QtGui.QImage(filePath)
        # 设置最大长宽
        maxSize = QtCore.QSize(300, 200)
        # 按比例放缩（最大长宽通过传入的QSize限制）
        styImg = QtGui.QPixmap.fromImage(
            img.scaled(maxSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        # 设置原图片标签
        self.styImgLabel.setPixmap(styImg)
        # 设置图片路径
        self.styImgPath = filePath

    # 选择风格图片（系统提供的默认风格）
    def selectStyImg_default(self):
        curRow = self.styImgListWidget.currentRow()
        filePath = self.fileInfoList[curRow]['filePath']
        # 获取图片
        img = QtGui.QImage(filePath)
        # 设置最大长宽
        maxSize = QtCore.QSize(300, 200)
        # 按比例放缩（最大长宽通过传入的QSize限制）
        styImg = QtGui.QPixmap.fromImage(img.scaled(maxSize, QtCore.Qt.KeepAspectRatio,
                                                    QtCore.Qt.SmoothTransformation))
        self.styImgLabel.setPixmap(styImg)
        # 设置图片路径
        self.styImgPath = filePath

    # 选择原图片或原视频
    def selectOriImg(self):
        file = QFileDialog.getOpenFileName(self.centralwidget, "选择图片", self.fileSystem.oriImgDirPath,
                                           "jpg图片 (*jpg);;gif图片 (*gif)")
        # 获取绝对路径
        filePath = file[0]
        if not filePath:
            return

        # 获取文件后缀，根据后缀决定显示静态图片还是gif
        suffix = file[1]
        if suffix == "jpg图片 (*jpg)" or suffix == "png图片 (*png)":
            # 获取图片
            img = QtGui.QImage(filePath)
            # 设置最大长宽
            maxSize = QtCore.QSize(300, 200)
            # 按比例放缩（最大长宽通过传入的QSize限制）
            oriImg = QtGui.QPixmap.fromImage(
                img.scaled(maxSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            # 设置原图片标签
            self.oriImgLabel.setPixmap(oriImg)
            # 设置图片路径
            self.oriImgPath = filePath
        elif suffix == "gif图片 (*gif)":
            # 获取图片
            img = QtGui.QMovie(filePath)
            # 设置最大长宽
            maxSize = QtCore.QSize(300, 200)
            # 按比例放缩（最大长宽通过传入的QSize限制）
            # oriImg = QtGui.QPixmap.fromImage(
                # img.scaled(maxSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            img.setScaledSize(maxSize)
            # 设置原图片标签
            self.oriImgLabel.setMovie(img)
            img.start()
            # 设置图片路径
            self.oriImgPath = filePath

    # 创建风格图片列表栏的复杂选项窗口
    def createStyImgListItem(self, fileInfo):
        itemWidget = QtWidgets.QWidget()
        # 设置容器名为文件名
        itemWidget.setObjectName(fileInfo['fileName'])
        vLayout = QtWidgets.QVBoxLayout(itemWidget)
        # 标题标签
        titleLabel = QtWidgets.QLabel()
        # 将过长的标题截断并加上省略号
        fontMetrics = QtGui.QFontMetrics(QtGui.QFont())
        fileName = fontMetrics.elidedText(fileInfo['fileName'], QtCore.Qt.ElideRight, 120)
        titleLabel.setText(fileName)
        titleLabel.setFont(QtGui.QFont("微软雅黑", 12, QtGui.QFont.Bold))
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        # 获取图片
        img = QtGui.QImage(fileInfo['filePath'])
        # 设置最大长宽
        maxSize = QtCore.QSize(200, 150)
        # 按比例放缩（最大长宽通过传入的QSize限制）
        styImg = QtGui.QPixmap.fromImage(img.scaled(maxSize, QtCore.Qt.KeepAspectRatio,
                                                    QtCore.Qt.SmoothTransformation))
        styImgLabel = QtWidgets.QLabel()
        styImgLabel.setPixmap(styImg)
        styImgLabel.setAlignment(QtCore.Qt.AlignCenter)
        # 将标签添加进布局
        vLayout.addWidget(titleLabel)
        vLayout.addWidget(styImgLabel)
        # 设置四方向间隔（依次为左、上、右、下）
        vLayout.setContentsMargins(10, 5, 10, 30)
        return itemWidget

    # 显示当前路径的文件列表
    def showFileList(self):
        # 清除旧的文件列表
        self.styImgListWidget.clear()
        # 更新当前路径下的文件信息列表
        self.fileInfoList = self.fileSystem.getFileInfoList(self.fileSystem.styImgDirPath)
        # 根据文件信息列表添加文件列表项
        for fileInfo in self.fileInfoList:
            itemWidget = self.createStyImgListItem(fileInfo)
            item = QtWidgets.QListWidgetItem(self.styImgListWidget)
            item.setSizeHint(QtCore.QSize(200, 150))
            self.styImgListWidget.setItemWidget(item, itemWidget)

    def setUserInfo(self, token, account):
        self.token = token
        self.account = account
        # 刷新文件列表栏
        self.showFileList()

