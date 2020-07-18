import BLL.ClientSocket
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog, commentList):
        Dialog.resize(530, 600)
        vLayout = QtWidgets.QVBoxLayout(Dialog)

        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 530, 674))
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget.verticalScrollBar().setSingleStep(20)

        for comment in commentList:
            self.initJudge(comment['account'], comment['time'], comment['content'])
        commentWidget = QtWidgets.QWidget()
        hLayout = QtWidgets.QHBoxLayout(commentWidget)

        # 用来显示评论输入
        self.le_judge = QtWidgets.QTextEdit()
        self.le_judge.setMaximumHeight(60)
        self.le_judge.setGeometry(QtCore.QRect(10, 270, 93, 28))
        self.le_judge.setPlaceholderText("发表我的看法")
        hLayout.addWidget(self.le_judge)

        # 用来显示评论按钮
        self.pb_judge = QtWidgets.QPushButton()
        self.pb_judge.setGeometry(QtCore.QRect(130, 270, 93, 28))
        self.pb_judge.setText('评论')
        self.pb_judge.setMaximumWidth(60)
        hLayout.addWidget(self.pb_judge)
        hLayout.setContentsMargins(0, 0, 0, 0)

        # 总布局
        vLayout.addWidget(self.listWidget, 5)
        vLayout.addWidget(commentWidget, 1)
        vLayout.setContentsMargins(5, 5, 5, 5)

    # 初始化列表项
    def initJudge(self, account, time, comment):
        item = customQListWidgetItem(account, time, comment)
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, item.widget)


# 自定义的item 继承自QListWidgetItem
class customQListWidgetItem(QListWidgetItem):
    def __init__(self, name, time, comment):
        super().__init__()

        # 自定义item中的widget 用来显示自定义的内容
        self.widget = QWidget()

        # 用来显示用户名
        nameLabel = QtWidgets.QLabel()
        nameLabel.setText(name)
        nameLabel.setFixedSize(450, 50)
        nameLabel.setFont(QtGui.QFont("微软雅黑", 14, QtGui.QFont.Bold))

        # 用来显示评论
        commentLabel = QtWidgets.QTextBrowser()
        # 设置评论框背景透明
        commentLabel.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        commentLabel.setText(comment)

        # 用来显示时间
        timeLabel = QtWidgets.QLabel()
        timeLabel.setText(time)
        layout_main = QVBoxLayout()  # 总体纵向布局
        layout_main.addWidget(nameLabel)
        layout_main.addWidget(commentLabel)
        layout_middle = QVBoxLayout()    # 中间布局
        layout_middle.addWidget(timeLabel)
        layout_main.addLayout(layout_middle)
        # # 设置widget的布局
        self.widget.setLayout(layout_main)
        # 设置自定义的QListWidgetItem的sizeHint，不然无法显示
        self.setSizeHint(QtCore.QSize(450, 200))


# 实际界面类
class CommentDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, token, iid, commentList):
        super(CommentDialog, self).__init__()
        self.token = token
        self.iid = iid
        self.commentList = commentList
        # 窗口组件初始化
        self.setupUi(self, self.commentList)
        # 设置窗口名称
        self.setWindowTitle("评论界面")
        # 激活评论功能
        self.pb_judge.clicked.connect(self.comment)

    # 评论
    def comment(self):
        # 弹出窗口，获取用户输入的评论内容
        content = self.le_judge.toPlainText()
        # 若用户未输入，则返回
        if not content:
            return
        # 调用客户端的评论函数发送评论
        clientSocket = BLL.ClientSocket.ClientSocket()
        response = clientSocket.comment(self.token, self.iid, content)
        # 评论成功
        if response:
            messageBox = QMessageBox()
            messageBox.setWindowTitle('提示')
            messageBox.setText('评论成功')
            messageBox.setStandardButtons(QMessageBox.Yes)
            buttonY = messageBox.button(QMessageBox.Yes)
            buttonY.setText('确定')
            messageBox.exec_()
            self.close()
        else:
            messageBox = QMessageBox()
            messageBox.setWindowTitle('提示')
            messageBox.setText('删除失败')
            messageBox.setStandardButtons(QMessageBox.Yes)
            buttonY = messageBox.button(QMessageBox.Yes)
            buttonY.setText('确定')
            messageBox.exec_()
