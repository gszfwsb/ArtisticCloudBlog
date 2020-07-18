import os
import shutil


class FileSystem:
    def __init__(self):
        # print(os.getcwd())
        # 原图片本地地址
        self.oriImgDirPath = os.path.abspath("../resources/ClientFile/OriginalImage")
        self.oriImgDirPath = self.oriImgDirPath.replace('\\', '/')
        # 风格图片本地地址
        self.styImgDirPath = os.path.abspath("../resources/ClientFile/StyleImage")
        self.styImgDirPath = self.styImgDirPath.replace('\\', '/')
        # 生成图片本地地址
        self.traImgDirPath = os.path.abspath("../resources/ClientFile/result")
        self.traImgDirPath = self.traImgDirPath.replace('\\', '/')
        # 图标本地地址
        self.iconPath = os.path.abspath("../resources/ClientFile/icon")
        self.iconPath = self.iconPath.replace('\\', '/')
        # 浏览图片本地地址
        self.browsePath = os.path.abspath("../resources/ClientFile/BrowseImage")
        self.browsePath = self.browsePath.replace('\\', '/')
        # 下载图片本地地址
        self.downloadPath = os.path.abspath("../resources/ClientFile/DownloadImage")
        self.downloadPath = self.downloadPath.replace('\\', '/')

    # 原图片和风格图片的路径，由指定格式生成图片名
    def getTraImgPath(self, oriImgPath, styImgPath):
        oriImgName = os.path.basename(oriImgPath)
        styImgName = os.path.basename(styImgPath)
        oriImgName, suffix1 = oriImgName.split('.', 1)
        styImgName, suffix2 = styImgName.split('.', 1)
        if suffix1 == 'gif':
            traImgName = oriImgName + '_' + styImgName + '.gif'
        else:
            traImgName = oriImgName + '_' + styImgName + '.png'
        traImgPath = self.traImgDirPath + '/' + traImgName
        return traImgPath

    # 获取路径中的纯文件名
    def getfileName(self, filePath):
        fileName = os.path.basename(filePath)
        return fileName

    # 获取目前路径下所有文件信息
    def getFileInfoList(self, dirPath):
        fileInfoList = []
        # 获取该目录内所有文件
        fileNameList = os.listdir(dirPath)
        for fileName in fileNameList:
            # 依次获取这些文件的信息并存储在列表中
            fileInfoList.append(self.getFileInfo(fileName, dirPath))
        # 返回文件信息列表
        return fileInfoList

    # 获取文件详细信息并返回字典
    def getFileInfo(self, fileName, dirPath):
        fileInfo = {}
        filePath = dirPath + '/' + fileName
        fileInfo['filePath'] = filePath
        if '.' in fileName:
            fileName, suffix = fileName.split('.', 1)
        else:
            print("格式错误：文件名无后缀")
            return
        # 获取文件名
        fileInfo['fileName'] = fileName
        # 获取文件后缀
        fileInfo['fileType'] = suffix
        # 返回文件信息字典
        return fileInfo

    # 另存为文件
    def fileSaveAs(self, oldFilePath, newFilePath):
        shutil.copyfile(oldFilePath, newFilePath)

    # 删除目录内所有文件
    def dirDelete(self, dirPath):
        # 获取该目录内所有文件
        fileNameList = os.listdir(dirPath)
        for fileName in fileNameList:
            try:
                # 依次获取这些文件的信息并存储在列表中
                os.remove(dirPath + '/' + fileName)
            except Exception as e:
                print(e)


    # 文件重命名
    def fileRename(self, oldFilePath, newName):
        oldFileName = os.path.basename(oldFilePath)
        oldFilePureName, suffix = oldFileName.split('.', 1)
        dirPath = os.path.dirname(oldFilePath)
        newFilePath = dirPath + '/' + newName + '.' + suffix
        os.rename(oldFilePath, newFilePath)

def main():
    fileSystem = FileSystem()
    fileInfoList = fileSystem.getFileInfoList(fileSystem.iconPath)
    for fileInfo in fileInfoList:
        print(fileInfo)

    # fileSystem.dirDelete(fileSystem.browsePath)


if __name__ == '__main__':
    main()