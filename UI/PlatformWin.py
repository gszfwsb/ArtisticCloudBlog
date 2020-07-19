import sys
import UI.Ui_PlatformWin
import BLL.FileSystem
import BLL.ClientSocket
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import UI.TransferWin
import UI.CommentDialog
from PIL import Image
from UI.LoginWin import simpleMessageBox


# 用户界面类
class PlatformWin(QtWidgets.QMainWindow, UI.Ui_PlatformWin.Ui_PlatformWin):
    def __init__(self, parent=None):
        super(PlatformWin, self).__init__(parent)
        # 调整初始窗口位置
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = QtCore.QSize(1200, 800)
        print(size)
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
        # 窗口组件初始化
        self.setupUi(self)
        # 设置窗口名称
        self.setWindowTitle("云艺术博客")
        # 文件信息列表初始化
        self.fileInfoList = []
        # token初始化
        self.token = ""
        # 用户名初始化
        self.account = ""
        # 客户端套接字初始化
        self.clientSocket = BLL.ClientSocket.ClientSocket()

        # 动作与函数绑定
        # 上传本地图片
        self.upLoadButton.clicked.connect(self.upLoadWork)
        # 查看指定作品
        self.downLoadButton.clicked.connect(self.downLoadWork_search)
        # 双击文件列表栏中列表项打开文件
        self.listWidget.doubleClicked.connect(self.fileOpen)
        # 点击迁移按钮打开迁移窗口
        self.transferButton.clicked.connect(self.transfer)
        # 点击浏览热门作品按钮
        self.browseButton.clicked.connect(self.downLoadWork_browse)
        # 点击查看我的作品按钮
        self.myWorkButton.clicked.connect(self.downLoadWork_myWork)
        # 点击评论按钮
        self.commentButton.clicked.connect(self.comment)
        # 点击点赞按钮
        self.starButton.clicked.connect(self.star)
        # 点击另存为按钮
        self.saveAsButton.clicked.connect(self.fileSaveAs)
        # 点击删除按钮
        self.deleteButton.clicked.connect(self.fileDelete)
        # 弹出的工作窗口
        self.mainWin = None

    # 点赞
    def star(self):
        # 调用客户端的评论函数发送评论
        # 获取目前选中的列表项的行数
        curRow = self.listWidget.currentRow()
        # 获取作品id
        iid = self.fileInfoList[curRow]['iid']
        response = self.clientSocket.star(self.token, iid)
        if not response:
            simpleMessageBox('提示', '已点赞过该作品')
        else:
            simpleMessageBox('提示', '点赞成功，当前点赞数: ' + response)

    # 评论
    def comment(self):
        # 显示评论这里需要用评论弹窗代替，暂时打印
        print("comment:")
        curRow = self.listWidget.currentRow()
        commentList = self.fileInfoList[curRow]['comment']

        # 获取作品id
        iid = self.fileInfoList[curRow]['iid']
        cDlg = UI.CommentDialog.CommentDialog(self.token, iid, commentList)
        cDlg.exec_()

    # 设置工作界面
    def setMainWin(self, mainWin):
        self.mainWin = mainWin

    # 打开工作界面
    def transfer(self):
        self.mainWin.setUserInfo(self.token, self.account)
        self.mainWin.show()

    # 导出文件至本地
    def fileSaveAs(self):
        # 弹窗获取导出路径
        filePath, fileType = QFileDialog.getSaveFileName(self.centralwidget, '选择导出路径',
                                                         self.fileSystem.traImgDirPath, "png (*.png);;gif (*.gif)")
        # 若用户未选择则返回
        if filePath == '':
            return
        # 获取目前选中的列表项的行数
        curRow = self.listWidget.currentRow()
        # 获取文件原地址
        oldFilePath = self.fileInfoList[curRow]['filePath']
        # 调用BLL层，将文件另存为至导出路径
        self.fileSystem.fileSaveAs(oldFilePath, filePath)

    # 打开文件
    def fileOpen(self):
        # 获取目前选中的列表项的行数
        curRow = self.listWidget.currentRow()
        # 获取图片路径
        path = self.fileInfoList[curRow]['filePath']
        if self.fileInfoList[curRow]['fileType'] == "gif":
            # 获取图片
            img = QtGui.QMovie(path)
            image = Image.open(path)
            imgWidth = image.width
            imgHeight = image.height
            # 设置最大长宽
            maxSize = (500, 500)
            # 按比例放缩（最大长宽通过maxSize限制）
            while imgWidth > maxSize[0] or imgHeight > maxSize[1]:
                imgWidth = imgWidth * 0.9
                imgHeight = imgHeight * 0.9
            newSize = QtCore.QSize(imgWidth, imgHeight)
            img.setScaledSize(newSize)

            # 设置原图片标签
            self.imgLabel.setMovie(img)
            # gif开始播放
            img.start()
        else:
            img = QtGui.QImage(path)
            print(img.size())
            # 设置最大长宽
            maxSize = QtCore.QSize(500, 500)
            # 按比例放缩（最大长宽通过传入的QSize限制）
            if img.width() > maxSize.width() or img.height() > maxSize.height():
                img = QtGui.QPixmap.fromImage(img.scaled(maxSize, QtCore.Qt.KeepAspectRatio,
                                                         QtCore.Qt.SmoothTransformation))
            else:
                img = QtGui.QPixmap.fromImage(img)
            self.imgLabel.setPixmap(img)
        # 设置标题栏
        self.titleEdit.setText(self.fileInfoList[curRow]['fileName'])
        # 设置配文栏
        self.textLabel.setText(self.fileInfoList[curRow]['text'])
        # 启用右侧页面
        self.pageWidget.setEnabled(True)
        # 显示按钮
        self.starButton.setVisible(True)
        self.commentButton.setVisible(True)
        self.saveAsButton.setVisible(True)
        self.titleEdit.setVisible(True)
        if self.fileInfoList[curRow]['account'] == self.account:
            self.deleteButton.setVisible(True)
        else:
            self.deleteButton.setVisible(False)

    # 文件删除
    def fileDelete(self):
        # 弹出提示窗口询问
        messageBox = QMessageBox()
        messageBox.setWindowTitle('提示')
        messageBox.setText('确定删除该作品？')
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = messageBox.button(QMessageBox.Yes)
        buttonY.setText('确定')
        buttonN = messageBox.button(QMessageBox.No)
        buttonN.setText('取消')
        messageBox.exec_()
        response = messageBox.clickedButton()
        if response == buttonN:
            return

        # 获取目前选中的列表项的行数
        curRow = self.listWidget.currentRow()
        # 获取作品id
        iid = self.fileInfoList[curRow]['iid']
        response = self.clientSocket.deleteWork(self.token, iid)
        if response:
            simpleMessageBox('提示', '删除成功，作品id: ' + iid)
            # 刷新文件列表
            self.downLoadWork_myWork()
        else:
            simpleMessageBox('提示', '删除失败')

    # 创建文件列表栏的单个复杂窗口
    def createFileListItem(self, fileInfo):
        print("createFileListItem")
        itemWidget = QtWidgets.QWidget()
        # 设置容器名为文件名
        itemWidget.setObjectName(fileInfo['fileName'])
        vLayout = QtWidgets.QVBoxLayout(itemWidget)
        # 标题标签
        titleLabel = QtWidgets.QLabel(itemWidget)
        # 将过长的标题截断并加上省略号
        fontMetrics = QtGui.QFontMetrics(QtGui.QFont())
        fileName = fontMetrics.elidedText(fileInfo['fileName'], QtCore.Qt.ElideRight, 120)
        titleLabel.setText(fileName)
        titleLabel.setFont(QtGui.QFont("微软雅黑", 12, QtGui.QFont.Bold))
        # 类型标签
        commentNum = len(fileInfo['comment'])
        commentNumLabel = QtWidgets.QLabel(itemWidget)
        commentNumLabel.setText("评论：" + str(commentNum))
        # id标签
        IDLabel = QtWidgets.QLabel(itemWidget)
        IDLabel.setText("序号：" + fileInfo['iid'])
        # 用户名标签
        accountLabel = QtWidgets.QLabel(itemWidget)
        accountLabel.setText("作者：" + fileInfo['account'])
        # 点赞数标签
        starNumLabel = QtWidgets.QLabel(itemWidget)
        starNumLabel.setText("点赞：" + fileInfo['starNum'])
        # 将标签添加进布局
        vLayout.addWidget(titleLabel)
        vLayout.addWidget(IDLabel)
        vLayout.addWidget(accountLabel)
        vLayout.addWidget(starNumLabel)
        vLayout.addWidget(commentNumLabel)
        # 设置四方向间隔
        vLayout.setContentsMargins(10, 10, 0, 10)
        # 设置容器高度（宽度为自适应）
        itemWidget.setFixedHeight(180)
        return itemWidget

    # 更新文件列表
    def showFileList(self):
        print("showFileList")
        # 清除旧的文件列表
        self.listWidget.clear()
        # 根据当前的文件信息列表添加文件列表项
        for fileInfo in self.fileInfoList:
            itemWidget = self.createFileListItem(fileInfo)
            item = QtWidgets.QListWidgetItem(self.listWidget)
            item.setSizeHint(QtCore.QSize(200, 180))
            self.listWidget.setItemWidget(item, itemWidget)

    # 切换过程中隐藏右侧页面
    def disablePage(self):
        self.pageWidget.setEnabled(False)
        # 隐藏按钮
        self.titleEdit.setVisible(False)
        self.starButton.setVisible(False)
        self.commentButton.setVisible(False)
        self.deleteButton.setVisible(False)
        self.saveAsButton.setVisible(False)
        # 将当前显示的图片标签清空（防止无法删除gif）
        img = QtGui.QMovie("")
        self.imgLabel.setMovie(img)
        # 将当前显示的配文标签清空
        self.textLabel.clear()
        # 删除BrowseImage临时本地文件夹内的旧文件
        self.fileSystem.dirDelete(self.fileSystem.browsePath)

    # 显示热门作品的文件列表
    def downLoadWork_browse(self):
        print("downLoadWork_browse")
        # 隐藏右侧页面
        self.disablePage()
        # 调用客户端函数获取文件以及文件信息列表更新
        self.fileInfoList = self.clientSocket.receiveWork_browse(self.token)
        # 更新文件列表
        self.showFileList()

    # 查找用户个人已上传的作品
    def downLoadWork_myWork(self):
        print("downLoadWork_myWork")
        # 隐藏右侧页面
        self.disablePage()
        # 调用客户端函数获取文件以及文件信息列表更新
        self.fileInfoList = self.clientSocket.receiveWork_myWork(self.token)
        # 更新文件列表
        self.showFileList()

    # 查找特定作品（根据图片id）
    def downLoadWork_search(self):
        print("downLoadWork_search")
        # 弹出窗口，获取用户输入的新笔记名
        iid, okPressed = QtWidgets.QInputDialog.getText(self, "查找", "图片id:",
                                                        QtWidgets.QLineEdit.Normal)
        # 若用户未输入或未点击确定按钮，则返回
        if iid == '' or not okPressed:
            return
        # 隐藏右侧页面
        self.disablePage()
        # 调用客户端函数获取文件信息列表
        self.fileInfoList = self.clientSocket.receiveWork_search(self.token, iid)
        # 更新文件列表
        self.showFileList()
        # 成功查找到文件，弹窗提示
        if self.listWidget.count() >= 1:
            simpleMessageBox('提示', '查找成功')
            # 将焦点设置到唯一的结果并打开
            self.listWidget.setCurrentRow(0)
            self.fileOpen()
        # 查找失败
        else:
            simpleMessageBox('提示', '查找失败')

    # 将本地作品上传至服务器
    def upLoadWork(self):
        # 弹窗获取导出路径
        filePath, fileType = QFileDialog.getOpenFileName(self.centralwidget, '选择需要的上传图片',
                                                         self.fileSystem.traImgDirPath, "png (*.png);;gif (*.gif)")
        # 若用户未选择则返回
        if filePath == '':
            return
        # 弹出窗口，获取图片的配文
        text, okPressed = QtWidgets.QInputDialog.getText(self, "配文", "输入一行文字与图片相配",
                                                         QtWidgets.QLineEdit.Normal)
        if not okPressed:
            return
        # 作品上传至服务器，返回值为作品id
        iid = self.clientSocket.sendWork(self.token, filePath, text)
        # 完成上传后，弹窗提示
        simpleMessageBox('提示', '已将作品上传至服务器，id为' + iid)
        # 刷新文件列表
        self.downLoadWork_myWork()

    # 登录结束后初始化，获取用户token和用户名
    def setUserInfo(self, token, account):
        self.token = token
        self.account = account
        # 用户账户标签显示
        self.accountLabel.setText(self.account)
        # 刷新文件列表栏
        self.downLoadWork_myWork()


def main():
    app = QtWidgets.QApplication(sys.argv)
    platformWin = PlatformWin()
    platformWin.setUserInfo("123", "123")

    platformWin.show()
    app.exec_()


if __name__ == '__main__':
    main()
