# 界面相关
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

# 文件处理
import os
import shutil
from PIL import Image
from enum import Enum


class ImageFormat(Enum):
    png = 0
    gif = 1
    other = 2


class LookResult(QWidget):
    closeSignal = pyqtSignal()

    def __init__(self, filename: str):
        super(LookResult, self).__init__()
        self.__filename: str = filename
        self.__initStatus: bool = False
        self.__screenSize: tuple
        self.__imageSize: tuple
        self.__imageFormat: ImageFormat
        self.__maxSize: tuple = (1600, 900)
        self.__zoomSize: QSize
        self.__pixmap: QPixmap
        self.__setup_ui()

    def __setup_ui(self):
        if os.path.exists(self.__filename) is True:
            self.setWindowTitle(os.path.basename(self.__filename))
            self.__get_image_property()
            self.__calculate_max_size()
            self.__init_image()
        else:
            QMessageBox.warning(self, "打开文件失败", "找不到文件！", QMessageBox.Yes)

    def get_init_status(self):
        return self.__initStatus

    def __get_image_property(self):
        try:
            with Image.open(self.__filename) as image:
                self.__imageSize = image.size
                self.__imageFormat = self.__convert_format_to_enum(image.format)
        except OSError:
            self.__imageSize = (0, 0)
            self.__imageFormat = ImageFormat.other

    def __calculate_max_size(self, scaling_percentage: float = 0.3):
        width = int(self.__imageSize[0] * scaling_percentage)
        height = int(self.__imageSize[1] * scaling_percentage)
        self.__maxSize = (width, height)

    def __init_image(self):
        if self.__imageFormat is not ImageFormat.other:
            if self.__imageFormat is ImageFormat.png:
                self.__preview_png()
            else:
                self.__preview_gif()
            self.__move_to_center()
            self.__set_layout()
            self.show()
            self.__initStatus = True
        else:
            QMessageBox.warning(self, "查看失败", "不支持的文件格式！", QMessageBox.Yes)

    def __preview_png(self):
        self.__zoom_static_image()
        self.setFixedSize(self.__zoomSize)
        self.__set_png()

    def __preview_gif(self):
        self.__calculate_zoom_size()
        self.setFixedSize(self.__zoomSize)
        self.__set_gif()

    def __move_to_center(self):
        self.__get_screen_size()
        self.move((self.__screenSize[0] - self.__zoomSize.width()) // 2,
                  (self.__screenSize[1] - self.__zoomSize.height()) // 2)

    def __get_screen_size(self):
        desktopWidget = QApplication.desktop()
        screenRect = desktopWidget.screenGeometry()
        self.__screenSize = (screenRect.width(), screenRect.height())

    @staticmethod
    def __convert_format_to_enum(format_string: str):
        format_string = format_string.lower()
        if format_string == 'png':
            return ImageFormat.png
        if format_string == 'gif':
            return ImageFormat.gif
        return ImageFormat.other

    def __zoom_static_image(self):
        image = QImage(self.__filename)
        self.__calculate_zoom_size()
        self.__pixmap = QPixmap.fromImage(image.scaled(self.__zoomSize, Qt.IgnoreAspectRatio))

    def __calculate_zoom_size(self):
        if self.__imageSize[0] > self.__maxSize[0]:
            height = int(self.__imageSize[1] * (self.__maxSize[0] / self.__imageSize[0]))
            self.__zoomSize = QSize(self.__maxSize[0], height)
        elif self.__imageSize[1] > self.__maxSize[1]:
            width = int(self.__imageSize[0] * (self.__maxSize[1] / self.__imageSize[1]))
            self.__zoomSize = QSize(width, self.__maxSize[1])
        else:
            self.__zoomSize = QSize(*self.__imageSize)

    def __set_png(self):
        self.__imageLabel = QLabel()
        self.__imageLabel.resize(self.__zoomSize.width(), self.__zoomSize.height())
        self.__imageLabel.setPixmap(self.__pixmap)

    def __set_gif(self):
        self.__imageLabel = QLabel()
        movie = QMovie(self.__filename)
        movie.setScaledSize(self.__zoomSize)
        self.__imageLabel.setMovie(movie)
        movie.start()

    def __set_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.__imageLabel)
        # 设置布局占用窗口的范围为铺满窗口
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def __download_image(self):
        whereToStorage = QFileDialog.getSaveFileName(
            self, "请选择保存路径", "", "图片文件 (*.{})".format(self.__imageFormat.name))
        if whereToStorage[0] is not "":
            shutil.copyfile(self.__filename, whereToStorage[0])

    def mouseReleaseEvent(self, mouse_event: QMouseEvent):
        if mouse_event.button() == Qt.RightButton:
            self.__download_image()

    def closeEvent(self, a0: QCloseEvent):
        self.closeSignal.emit()


if __name__ == "__main__":
    class Test:
        def __init__(self):
            self.__isLookingResult = False
            self.__lookResult = None

        def look_result(self, file_location: str):
            if self.__isLookingResult is False:
                self.__isLookingResult = True
                self.__lookResult = LookResult(file_location)
                if self.__lookResult.get_init_status() is True:
                    self.__lookResult.closeSignal.connect(self.__change_look_result_status)
                else:
                    self.__change_look_result_status()
            else:
                QMessageBox.information(None, "提示", "请先关闭当前查看窗口！\n然后重试！", QMessageBox.Yes)
                # 跳转到当前正在预览的窗口，方便用户关闭
                self.__lookResult.setWindowState(Qt.WindowActive)

        def __change_look_result_status(self):
            self.__isLookingResult = False


    app = QApplication(sys.argv)
    test = Test()
    # test.look_result(r"../resources/ClientFile/OriginalImage/gym.jpg")
    test.look_result(r"../resources/ClientFile/result/a.gif")
    test.look_result(r"../resources/ClientFile/result/gym_muse.png")
    sys.exit(app.exec_())
