from PyQt5 import QtCore, QtGui, QtWidgets
import BLL.FileSystem

# 主界面的控件声明类，不含操作函数
class Ui_MainWin(object):
    def setupUi(self, MainWindow):
        # 主窗口
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # 设置窗口背景颜色为白色
        pe = QtGui.QPalette()
        pe.setColor(pe.Background, QtGui.QColor(255, 255, 255))
        self.centralwidget.window().setPalette(pe)

        # 文件操作类初始化
        self.fileSystem = BLL.FileSystem.FileSystem()
        iconPath = self.fileSystem.iconPath

        # 主窗口布局
        gLayout = QtWidgets.QHBoxLayout(self.centralwidget)

        # 页面窗口（可看作当前的主窗口）
        self.pageWidget = QtWidgets.QWidget(self.centralwidget)
        pageWidgetLayout = QtWidgets.QVBoxLayout(self.pageWidget)

        # 工具窗口
        toolWidget = QtWidgets.QWidget(self.pageWidget)
        # 工具窗口背景颜色
        toolWidget.setStyleSheet('background-color: rgb(255, 255, 255)')
        # 工具窗口固定高度
        toolWidget.setFixedHeight(80)

        # 标题标签
        self.avatarLabel = QtWidgets.QLabel(toolWidget)
        self.avatarLabel.setText("Style Transferer")
        self.avatarLabel.setFont(QtGui.QFont("微软雅黑", 24, QtGui.QFont.Bold))
        self.avatarLabel.setAlignment(QtCore.Qt.AlignCenter)


        # 工具窗口布局
        toolWidgetLayout = QtWidgets.QHBoxLayout(toolWidget)
        # 用户头像标签添加进工具窗口的内部布局
        toolWidgetLayout.addWidget(self.avatarLabel)


        # 工具窗口添加进页面窗口的内部布局（顶部）
        pageWidgetLayout.addWidget(toolWidget)


        # 图片名称窗口
        imgNameWidget = QtWidgets.QWidget(self.pageWidget)

        # 原图片名称框
        self.oriImgNameLabel = QtWidgets.QLabel(imgNameWidget)

        # 固定高度
        self.oriImgNameLabel.setFixedHeight(60)
        # 初始文本
        self.oriImgNameLabel.setText("Content")
        # 设置字体
        self.oriImgNameLabel.setFont(QtGui.QFont("微软雅黑", 20, QtGui.QFont.Bold))
        # 居中显示
        self.oriImgNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        # 设置原图片名称框背景透明
        # self.oriImgNameLabel.setStyleSheet("background:transparent;border-width:0;border-style:outset")

        # 风格图片名称框
        self.styImgNameLabel = QtWidgets.QLabel(self.pageWidget)
        # 固定高度
        self.styImgNameLabel.setFixedHeight(60)
        # 初始文本
        self.styImgNameLabel.setText("Style")
        # 设置字体
        self.styImgNameLabel.setFont(QtGui.QFont("微软雅黑", 20, QtGui.QFont.Bold))
        # 居中显示
        self.styImgNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        # 设置原图片名称框背景透明
        # self.styImgNameLabel.setStyleSheet("background:transparent;border-width:0;border-style:outset")

        # 图片名称窗口的内部布局
        imgNameWidgetLayout = QtWidgets.QHBoxLayout(imgNameWidget)
        imgNameWidgetLayout.addWidget(self.oriImgNameLabel)
        imgNameWidgetLayout.addWidget(self.styImgNameLabel)

        # 原图片名称框添加进页面窗口的内部布局（上方）
        pageWidgetLayout.addWidget(imgNameWidget)


        # 图片窗口
        imgWidget = QtWidgets.QWidget(self.pageWidget)
        # 固定高度
        imgWidget.setFixedHeight(300)

        # 获取图片
        path = iconPath + '/' + "defaultOriImg.png"
        img = QtGui.QImage(path)
        # 设置最大长宽
        maxSize = QtCore.QSize(100, 100)
        # 按比例放缩（最大长宽通过传入的QSize限制）
        oriImg = QtGui.QPixmap.fromImage(img.scaled(maxSize, QtCore.Qt.KeepAspectRatio,
                                                    QtCore.Qt.SmoothTransformation))
        # 原图片标签
        self.oriImgLabel = ClickedLabel(MainWindow)
        # 鼠标移上去显示为手型
        self.oriImgLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # 设置标签边框
        self.oriImgLabel.setStyleSheet(
            """background:transparent;
            border-radius:10px;
            border-width:3;
            border-style: solid;
            border-color: black;
            """)
        # 阴影效果（相对距离、阴影颜色、阴影模糊度）
        shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        shadow_effect.setOffset(0, 0)
        shadow_effect.setColor(QtCore.Qt.red)
        shadow_effect.setBlurRadius(10)
        self.oriImgLabel.setGraphicsEffect(shadow_effect)
        # 设置标签中的图片
        self.oriImgLabel.setPixmap(oriImg)
        # 标签居中
        self.oriImgLabel.setAlignment(QtCore.Qt.AlignCenter)
        # 获取图片
        path = iconPath + '/' + "defaultStyImg.png"
        img = QtGui.QImage(path)
        # 设置最大长宽
        maxSize = QtCore.QSize(100, 100)
        # 按比例放缩（最大长宽通过传入的QSize限制）
        triImg = QtGui.QPixmap.fromImage(img.scaled(maxSize, QtCore.Qt.KeepAspectRatio,
                                                    QtCore.Qt.SmoothTransformation))

        # 风格图片标签
        self.styImgLabel = ClickedLabel(MainWindow)
        # 鼠标移上去显示为手型
        self.styImgLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # 设置标签边框
        self.styImgLabel.setStyleSheet(
            """background:transparent;
            border-radius:10px;
            border-width:3;
            border-style: solid;
            border-color: black;
            """)
        # 阴影效果（相对距离、阴影颜色、阴影模糊度）
        shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        shadow_effect.setOffset(0, 0)
        shadow_effect.setColor(QtGui.QColor(26, 128, 230))
        shadow_effect.setBlurRadius(10)
        self.styImgLabel.setGraphicsEffect(shadow_effect)

        # 设置标签中的图片
        self.styImgLabel.setPixmap(triImg)
        self.styImgLabel.setAlignment(QtCore.Qt.AlignCenter)
        # 图片窗口的内部布局
        imgWidgetLayout = QtWidgets.QHBoxLayout(imgWidget)
        # 原图片和风格图片添加进图片窗口的内部布局
        imgWidgetLayout.addWidget(self.oriImgLabel)
        imgWidgetLayout.addWidget(self.styImgLabel)

        # 图片窗口添加进页面窗口的内部布局（中间）
        pageWidgetLayout.addWidget(imgWidget)


        # 图片按钮窗口
        imgButtonWidget = QtWidgets.QWidget(self.pageWidget)

        # 开始迁移按钮
        self.transferButton = QtWidgets.QPushButton(imgButtonWidget)

        self.transferButton.setText("Submit")
        self.transferButton.setStyleSheet("""
                            color:white;
                            background-color:rgb(14 , 150 , 254);
                            border-radius:10px;
                            """)
        self.transferButton.setFont(QtGui.QFont("微软雅黑", 18, QtGui.QFont.Bold))
        self.transferButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.transferButton.setFixedSize(200, 50)

        # 图片按钮窗口布局
        imgButtonWidgetLayout = QtWidgets.QHBoxLayout(imgButtonWidget)
        imgButtonWidgetLayout.addWidget(self.transferButton, QtCore.Qt.AlignCenter)

        # 图片按钮窗口添加进页面窗口
        pageWidgetLayout.addWidget(imgButtonWidget)


        # 风格窗口
        styleWidget = QtWidgets.QWidget(self.pageWidget)

        # 风格图片列表栏（页面窗口下方）
        self.styImgListWidget = QtWidgets.QListWidget(self.pageWidget)
        self.styImgListWidget.setResizeMode(QtWidgets.QListView.Adjust)
        # 设置列表栏的滚动条为横向
        self.styImgListWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.styImgListWidget.horizontalScrollBar().setSingleStep(20)
        # 隐藏横向滚动条
        self.styImgListWidget.setFlow(QtWidgets.QListView.LeftToRight)
        self.styImgListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # 设置列表项可拖拽
        self.styImgListWidget.setDragDropMode(QtWidgets.QListWidget.InternalMove)
        # 设置列表固定宽度
        self.styImgListWidget.setFixedSize(805, 200)

        # 左右按钮
        self.leftButton = QtWidgets.QPushButton(styleWidget)
        path = iconPath + '/' + "left.png"
        self.leftButton.setStyleSheet("QPushButton{border-image: url(%s)}" % path)
        self.leftButton.setFixedSize(100, 100)
        self.leftButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.rightButton = QtWidgets.QPushButton(styleWidget)
        path = iconPath + '/' + "right.png"
        self.rightButton.setStyleSheet("QPushButton{border-image: url(%s)}" % path)
        self.rightButton.setFixedSize(100, 100)
        self.rightButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # 风格窗口内部布局
        styleWidgetLayout = QtWidgets.QHBoxLayout(styleWidget)
        styleWidgetLayout.addWidget(self.leftButton)
        styleWidgetLayout.addWidget(self.styImgListWidget)
        styleWidgetLayout.addWidget(self.rightButton)

        # 风格窗口添加进页面窗口的内部布局（下方）
        pageWidgetLayout.addWidget(styleWidget)

        # 页面窗口添加进主窗口布局（目前占满）
        gLayout.addWidget(self.pageWidget)


# 自定义标签类（可点击标签）
class ClickedLabel(QtWidgets.QLabel):
    # 自定义单击信号
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ClickedLabel, self).__init__(parent)

    def mouseReleaseEvent(self, e):
        self.clicked.emit()
