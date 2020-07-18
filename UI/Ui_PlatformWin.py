from PyQt5 import QtCore, QtGui, QtWidgets
import BLL.FileSystem

class Ui_PlatformWin(object):
    def setupUi(self, MainWindow):
        # 初始路径
        self.fileSystem = BLL.FileSystem.FileSystem()
        iconPath = self.fileSystem.iconPath

        # 主窗口
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        # 设置窗口背景颜色为白色
        pe = QtGui.QPalette()
        pe.setColor(pe.Background, QtGui.QColor(255, 255, 255))
        self.centralwidget.window().setPalette(pe)

        # 主窗口布局
        gLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        # 用户窗口初始化（主窗口布局左侧）
        userWidget = QtWidgets.QWidget(self.centralwidget)
        userWidget.setMaximumWidth(250)
        gLayout.addWidget(userWidget)
        # 用户头像
        avatarLabel = QtWidgets.QLabel(userWidget)
        path = iconPath + '/' + "user.png"
        img = QtGui.QImage(path)
        # 设置最大长宽
        maxSize = QtCore.QSize(80, 80)
        # 按比例放缩（最大长宽通过传入的QSize限制）
        avatarImg = QtGui.QPixmap.fromImage(img.scaled(maxSize, QtCore.Qt.KeepAspectRatio,
                                                     QtCore.Qt.SmoothTransformation))
        avatarLabel.setPixmap(avatarImg)

        # 头像居中
        avatarLabel.setAlignment(QtCore.Qt.AlignCenter)


        # 账户标签
        self.accountLabel = QtWidgets.QLabel(userWidget)
        self.accountLabel.setFont(QtGui.QFont("微软雅黑", 12, QtGui.QFont.Bold))
        # 标签居中
        self.accountLabel.setAlignment(QtCore.Qt.AlignCenter)

        # 统一设置按钮格式
        userWidget.setStyleSheet("""QPushButton{
                                            color:white;
                                            background-color:rgb(14 , 150 , 254);
                                            border-radius:5px;
                                            font: 微软雅黑 bold 12px;
                                            min-width: 220px;
                                            min-height: 30px;

                                            }
                                            """)

        # 浏览热门图片
        self.browseButton = QtWidgets.QPushButton(userWidget)
        self.browseButton.setText("浏览热门作品")
        self.browseButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 查看我的作品
        self.myWorkButton = QtWidgets.QPushButton(userWidget)
        self.myWorkButton.setText("查看我的作品")
        self.myWorkButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 查看指定作品
        self.downLoadButton = QtWidgets.QPushButton(userWidget)
        self.downLoadButton.setText("查看指定作品")
        self.downLoadButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 生成迁移图片
        self.transferButton = QtWidgets.QPushButton(userWidget)
        self.transferButton.setText("生成迁移图片")
        self.transferButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 上传本地作品
        self.upLoadButton = QtWidgets.QPushButton(userWidget)
        self.upLoadButton.setText("上传本地作品")
        self.upLoadButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


        # 列表栏（主窗口布局左下）
        self.listWidget = QtWidgets.QListWidget(userWidget)
        self.listWidget.setResizeMode(QtWidgets.QListView.Adjust)
        # 设置列表栏的滚动条
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget.verticalScrollBar().setSingleStep(20)
        # 设置列表固定宽度
        self.listWidget.setMinimumSize(230, 500)
        self.listWidget.setMaximumSize(230, 500)
        # 用户窗口布局
        userWidgetLayout = QtWidgets.QVBoxLayout(userWidget)
        userWidgetLayout.addWidget(avatarLabel)
        userWidgetLayout.addWidget(self.accountLabel)

        userWidgetLayout.addWidget(self.browseButton, 1, QtCore.Qt.AlignCenter)
        userWidgetLayout.addWidget(self.myWorkButton, 1, QtCore.Qt.AlignCenter)
        userWidgetLayout.addWidget(self.downLoadButton, 1, QtCore.Qt.AlignCenter)
        userWidgetLayout.addWidget(self.upLoadButton, 1, QtCore.Qt.AlignCenter)
        userWidgetLayout.addWidget(self.transferButton, 1, QtCore.Qt.AlignCenter)



        userWidgetLayout.addWidget(self.listWidget)
        self.pageWidget = QtWidgets.QWidget(self.centralwidget)
        # 布局
        pageWidgetLayout = QtWidgets.QVBoxLayout(self.pageWidget)
        # 标题框
        self.titleEdit = QtWidgets.QLabel(self.pageWidget)
        self.titleEdit.setMinimumHeight(50)
        self.titleEdit.setMaximumHeight(50)
        self.titleEdit.setFont(QtGui.QFont("微软雅黑", 20, QtGui.QFont.Bold))
        self.titleEdit.setAlignment(QtCore.Qt.AlignCenter)
        # 标题框背景透明
        self.titleEdit.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        # 文本编辑窗口初始化（主窗口布局右侧）
        imgWidget = QtWidgets.QWidget(self.pageWidget)
        # 文本编辑窗口内部布局
        textWidgetLayout = QtWidgets.QVBoxLayout(imgWidget)


        # 图片显示标签
        self.imgLabel = QtWidgets.QLabel(imgWidget)
        self.imgLabel.setText("未选择图片")
        self.imgLabel.setMinimumSize(500, 500)
        self.imgLabel.setAlignment(QtCore.Qt.AlignCenter)

        # 文字显示标签
        self.textLabel = QtWidgets.QLabel(imgWidget)
        self.textLabel.setText("")
        self.textLabel.setMinimumSize(500, 50)
        self.textLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.textLabel.setFont(QtGui.QFont("微软雅黑", 14, QtGui.QFont.Bold))

        # 点赞按钮
        self.starButton = QtWidgets.QPushButton(imgWidget)
        path = iconPath + '/' + "star.png"
        self.starButton.setStyleSheet("QPushButton{border-image: url(%s)}" % path)
        self.starButton.setFixedSize(80, 80)
        self.starButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 评论按钮
        self.commentButton = QtWidgets.QPushButton(imgWidget)
        path = iconPath + '/' + "comment.png"
        self.commentButton.setStyleSheet("QPushButton{border-image: url(%s)}" % path)
        self.commentButton.setFixedSize(80, 80)
        self.commentButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 导出按钮
        self.saveAsButton = QtWidgets.QPushButton(imgWidget)
        path = iconPath + '/' + "saveAs.png"
        self.saveAsButton.setStyleSheet("QPushButton{border-image: url(%s)}" % path)
        self.saveAsButton.setFixedSize(80, 80)
        self.saveAsButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 删除按钮
        self.deleteButton = QtWidgets.QPushButton(imgWidget)
        path = iconPath + '/' + "delete.png"
        self.deleteButton.setStyleSheet("QPushButton{border-image: url(%s)}" % path)
        self.deleteButton.setFixedSize(80, 80)
        self.deleteButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 按钮窗口
        buttonWidget = QtWidgets.QWidget(imgWidget)
        buttonWidgetLayout = QtWidgets.QHBoxLayout(buttonWidget)
        buttonWidgetLayout.addWidget(self.starButton, QtCore.Qt.AlignCenter)
        buttonWidgetLayout.addWidget(self.commentButton, QtCore.Qt.AlignCenter)
        buttonWidgetLayout.addWidget(self.saveAsButton, QtCore.Qt.AlignCenter)
        buttonWidgetLayout.addWidget(self.deleteButton, QtCore.Qt.AlignCenter)


        # 文本编辑框添加进文本编辑窗口的内部布局（下方）
        textWidgetLayout.addWidget(self.imgLabel)
        textWidgetLayout.addWidget(self.textLabel)
        textWidgetLayout.addWidget(buttonWidget)


        pageWidgetLayout.addWidget(self.titleEdit)
        pageWidgetLayout.addWidget(imgWidget)
        # 文本编辑窗口添加进主窗口布局（右侧）
        gLayout.addWidget(self.pageWidget)





