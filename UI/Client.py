import sys
import UI.TransferWin
import UI.LoginWin
import UI.PlatformWin
from PyQt5 import QtWidgets


def main():
    app = QtWidgets.QApplication(sys.argv)
    # 平台界面初始化
    platformWin = UI.PlatformWin.PlatformWin()
    # 工作界面初始化
    mainWin = UI.TransferWin.TransferWin()
    # 登录界面初始化
    logWin = UI.LoginWin.LoginWin()
    # 登录界面关闭后，显示平台界面
    logWin.setMainWin(platformWin)
    # 平台界面把工作界面作为一个子界面打开
    platformWin.setMainWin(mainWin)
    # 显示登录界面
    logWin.show()
    # 跳过登录快速启动，实际运行时需要注释掉
    # logWin.quickStart()
    app.exec_()


if __name__ == '__main__':
    main()
