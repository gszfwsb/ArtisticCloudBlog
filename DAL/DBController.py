import sqlite3
import time
import uuid
import os


class DBController:
    def __init__(self):
        path = "..\\DAL\\MyDb.db"
        path = os.path.abspath(path)
        path = path.replace('\\', '/')
        self.__connect = sqlite3.connect(path)

    # 根据作品id获取该作品的评论信息
    def getCommentInfo(self, iid):
        self.cursor = self.__connect.cursor()
        sql = 'SELECT * FROM COMMENT WHERE IID = ?'
        self.cursor.execute(sql, (iid,))
        result = self.cursor.fetchall()
        if not result:
            print("无评论信息")
            return ''
        else:
            commentList = []
            for row in result:
                # 先搜索单个评论的信息建立字典
                comment = {}
                comment['content'] = row[3]
                comment['time'] = row[4]
                # 根据uid找到account
                uid = row[2]
                sql = 'SELECT account FROM USR WHERE uid = ?'
                self.cursor.execute(sql, (uid,))
                result = self.cursor.fetchone()
                if not result:
                    print("数据库错误：未找到用户 UID=", uid)
                    return ''
                else:
                    account = result[0]
                comment['account'] = account
                # 字典建立完毕，加入到列表中
                commentList.append(comment)
            return commentList

    # 评论
    def comment(self, token, iid, content):
        self.cursor = self.__connect.cursor()
        # 根据token获取uid
        result = self.getUSRByToken(token)
        # 查找失败，则返回
        if not result:
            print("未找到用户id！")
            return ''
        else:
            uid = result[0]
        # 获取当前时间
        localTime = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(time.time()))
        # 插入评论表
        # 寻找最大CID
        self.cursor.execute('SELECT max(CID) FROM COMMENT')
        result = self.cursor.fetchone()[0]
        if result is None:
            cid = 0
        else:
            cid = result + 1
        # 开始插入
        self.cursor.execute('INSERT INTO COMMENT(CID, IID, UID, Content, Time)'
                            'VALUES (?,?,?,?,?)',
                            (cid, iid, uid, content, localTime))
        self.__connect.commit()
        self.__connect.close()
        return cid

    # 点赞
    def star(self, token, iid):
        self.cursor = self.__connect.cursor()
        # 根据token获取uid
        result = self.getUSRByToken(token)
        # 查找失败，则返回
        if not result:
            print("未找到用户id！")
            return ''
        else:
            uid = result[0]

        # 根据uid查询点赞表
        sql = 'SELECT * FROM STAR WHERE uid = ? and iid = ?'
        self.cursor.execute(sql, (uid, iid))
        result = self.cursor.fetchone()
        # 该用户点过赞
        if result:
            print("该用户已经对该作品点过赞了")
            return ''

        # 该用户未点过赞，插入点赞表，并增加点赞数
        sql = 'SELECT * FROM STAR WHERE uid = ?'
        self.cursor.execute(sql, (uid,))
        self.cursor.execute('INSERT INTO STAR(IID, UID) '
                            'VALUES (?, ?)',
                            (iid, uid))

        self.cursor.execute('UPDATE WORK SET StarNum = StarNum + 1 Where IID = ?', (iid,))

        sql = 'SELECT StarNum FROM WORK WHERE IID = ?'
        self.cursor.execute(sql, (iid,))
        result = self.cursor.fetchone()[0]

        self.__connect.commit()
        self.__connect.close()
        return result

    # 获取最高点赞数的前N个作品id（若不足N个则只显示当前存在的）
    def getHotWork(self, N):
        self.cursor = self.__connect.cursor()
        # 根据starNum获得iid列表

        sql = 'select IID from WORK order by StarNum desc'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        iidList = []
        i = 0
        for row in result:
            if i >= N:
                break
            iidList.append(row[0])
            i = i + 1

        return iidList

    # 根据token获取指定用户的所有作品id
    def getUserWork(self, token):
        self.cursor = self.__connect.cursor()
        # 根据token获取uid
        result = self.getUSRByToken(token)
        # 查找失败，则返回
        if not result:
            print("未找到用户id！")
            return ''
        else:
            uid = result[0]

        # 根据uid获得iid列表
        iidList = []
        sql = 'SELECT IID FROM WORK WHERE UID = ?'
        self.cursor.execute(sql, (uid,))
        result = self.cursor.fetchall()
        if not result:
            print("IID查找失败")
            return ''
        else:
            for row in result:
                iidList.append(row[0])
        return iidList

    # 根据iid获取作品有关信息
    def getWorkInfo(self, iid):
        # [图片ID、图片名、路径、账户、点赞数、配文、[评论群]]
        self.cursor = self.__connect.cursor()
        iid = int(iid)
        # 根据IID获取UID
        sql = 'SELECT UID, Name, Path, StarNum, Text FROM WORK WHERE IID = ?'
        self.cursor.execute(sql, (iid,))
        result = self.cursor.fetchone()
        if not result:
            print("UID查找失败")
            return ''
        else:
            uid = result[0]
            name = result[1]
            path = result[2]
            starNum = result[3]
            text = result[4]

        # 根据IID获取account
        sql = 'SELECT Account FROM USR WHERE UID = ?'
        self.cursor.execute(sql, (uid,))
        result = self.cursor.fetchone()
        if not result:
            print("用户名查找失败")
            return ''
        else:
            account = result[0]

        fileInfo = {}
        fileInfo['filePath'] = path
        fileName = os.path.basename(fileInfo['filePath'])
        if '.' in fileName:
            fileName, suffix = fileName.split('.', 1)
        else:
            print("格式错误：需要发送的文件名无后缀")
            return ''
        fileInfo['fileName'] = name
        fileInfo['fileType'] = suffix
        fileInfo['iid'] = str(iid)
        fileInfo['account'] = account
        fileInfo['starNum'] = str(starNum)
        fileInfo['text'] = text

        # 获取评论群信息
        commentList = self.getCommentInfo(iid)
        fileInfo['comment'] = commentList

        print("数据库 getWorkInfo: ", fileInfo)

        return fileInfo

    # 插入新的作品
    def insertWork(self, token, name, path, text):
        self.cursor = self.__connect.cursor()
        # 根据token获取用户信息
        result = self.getUSRByToken(token)
        # 查找失败，则返回
        if not result:
            print("未找到用户ID！")
            return ''
        else:
            UID = result[0]

        # 获取最新的IID
        self.cursor.execute('SELECT max(IID) FROM WORK')
        result = self.cursor.fetchone()[0]
        print("插入新的作品 IID ", result)
        if result is None:
            IID = 0
        else:
            IID = result + 1

        # 开始插入
        self.cursor.execute('INSERT INTO WORK(IID, UID, Name, Path, StarNum, Text)'
                            'VALUES (?,?,?,?,?,?)',
                            (IID, UID, name, path, 0, text))

        self.__connect.commit()
        self.__connect.close()
        return IID

    # 根据account获取密保问题
    def getSecurityQes(self, account):
        self.cursor = self.__connect.cursor()
        # 根据账户获取密保问题答案
        self.cursor.execute('SELECT SecurityQes FROM USR WHERE Account = ?', (account,))
        result = self.cursor.fetchone()
        print("result", result)
        # 用户不存在
        if not result:
            return ''
        # 用户存在，返回密保问题
        result = result[0]
        return result

    # 忘记密码
    def forgotPassword(self, account, password, answer):
        self.cursor = self.__connect.cursor()
        # 根据账户获取密保问题答案
        self.cursor.execute('SELECT SecurityAns FROM USR WHERE Account = ?', (account,))
        result = self.cursor.fetchone()
        # 答案错误
        if not result:
            return ''
        # 答案正确
        result = result[0]
        if result == answer:
            self.cursor.execute('''
                UPDATE USR SET Password = ?
                WHERE Account = ?
                ''', (password, account))
            print("数据库 忘记密码，新密码：", password)
            self.__connect.commit()
            self.__connect.close()
            return password

    # 注册
    def register(self, account, password, securityQes, securityAns):
        self.cursor = self.__connect.cursor()
        self.cursor.execute('SELECT * FROM USR WHERE Account = ?', (account,))
        result = self.cursor.fetchone()
        # 用户名已存在，返回
        if result:
            return ''
        # 用户名不存在，注册
        # 寻找最大UID
        self.cursor.execute('SELECT max(UID) FROM USR')
        result = self.cursor.fetchone()[0]
        if result is None:
            UID = 0
        else:
            UID = result + 1
        # 生成token
        userInfo = account + ' ' + password
        token = str(uuid.uuid3(uuid.NAMESPACE_OID, userInfo))
        print("register: account=", account, ", token=", token)
        self.cursor.execute('INSERT INTO USR(UID,Account,Password,SecurityQes,SecurityAns,Token) '
                            'VALUES (?,?,?,?,?,?)',
                            (UID, account, password, securityQes, securityAns, token))
        self.__connect.commit()
        self.__connect.close()
        return UID

    # 登录
    def login(self, account, password):
        self.cursor = self.__connect.cursor()
        sql = 'SELECT Password FROM USR WHERE Account = ?'
        self.cursor.execute(sql, (account,))
        result = self.cursor.fetchone()
        # 账号不存在
        if not result:
            return ''
        # 密码错误
        else:
            result = result[0]
            if result != password:
                return ''
        # 登录成功
        # 根据account找到token
        sql = 'SELECT Token FROM USR WHERE Account = ?'
        self.cursor.execute(sql, (account,))
        result = self.cursor.fetchone()[0]
        # 返回token
        return result

    # 根据token找到用户表的一行
    def getUSRByToken(self, token):
        self.cursor = self.__connect.cursor()
        sql = 'SELECT * FROM USR WHERE Token = ?'
        self.cursor.execute(sql, (token,))
        result = self.cursor.fetchone()
        if not result:
            return ''
        else:
            return result

    # 创建用户表USR（UID，用户名Account，密码Password，密保问题SecurityQes，密保答案SecurityAns，令牌token）
    def create_USR(self):
        self.cursor = self.__connect.cursor()
        sql = '''CREATE TABLE USR
              (UID int primary key,
              Account varchar(30) unique,
              Password varchar(30) NOT NULL,
              SecurityQes varchar(50) NOT NULL,
              SecurityAns varchar(50) NOT NULL,
              Token varchar(100) NOT NULL);'''
        self.cursor.execute(sql)
        self.__connect.commit()
        self.__connect.close()

    # 创建作品表WORK（作品IID，上传者UID，名称Name，路径Path，点赞数StarNum，配文Text）
    def create_WORK(self):
        self.cursor = self.__connect.cursor()
        sql = '''CREATE TABLE WORK
                  (IID int primary key, 
                  UID int references USR(UID),
                  Name varchar(50) not null,
                  Path varchar(200) not null,
                  StarNum int not null,
                  Text varchar(100)
                  );'''
        self.cursor.execute(sql)
        self.__connect.commit()
        self.__connect.close()

    # 创建点赞表STAR（被点赞的作品IID，点赞者UID）（省略了联合主键的声明，只写了外键）
    def create_STAR(self):
        self.cursor = self.__connect.cursor()
        sql = '''CREATE TABLE STAR
                      (IID int references WORK(IID), 
                      UID int references USR(UID)
                      );'''
        self.cursor.execute(sql)
        self.__connect.commit()
        self.__connect.close()

    # 创建评论表COMMENT（评论CID，被评论的作品IID，评论者UID，评论内容Content，评论时间Time）
    def create_COMMENT(self):
        self.cursor = self.__connect.cursor()
        sql = '''CREATE TABLE COMMENT
                          (CID int primary key, 
                          IID int references WORK(IID) not null,
                          UID int references USR(UID) not null,
                          Content varchar(100) not null,
                          Time varchar(50) not null
                          );'''
        self.cursor.execute(sql)
        self.__connect.commit()
        self.__connect.close()

    # 打印目前所有作品信息
    def print_WORK(self):
        self.cursor = self.__connect.cursor()
        sql = 'SELECT * FROM WORK'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print("WORK:")
        print(result)

    # 打印目前所有用户信息
    def print_USR(self):
        self.cursor = self.__connect.cursor()
        sql = 'SELECT * FROM USR'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print("USR:")
        print(result)

    # 打印目前所有点赞信息
    def print_STAR(self):
        self.cursor = self.__connect.cursor()
        sql = 'SELECT * FROM STAR'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print("STAR:")
        print(result)

    # 打印目前所有评论信息
    def print_COMMENT(self):
        self.cursor = self.__connect.cursor()
        sql = 'SELECT * FROM COMMENT'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print("COMMENT:")
        print(result)

    # 删除用户表中所有行
    def delete_USR(self):
        self.cursor = self.__connect.cursor()
        sql = 'DELETE FROM USR'
        self.cursor.execute(sql)
        self.__connect.commit()
        self.__connect.close()

    # 删除作品表中所有行
    def delete_WORK(self):
        self.cursor = self.__connect.cursor()
        sql = 'DELETE FROM WORK'
        self.cursor.execute(sql)
        self.__connect.commit()
        self.__connect.close()

    # 删除点赞表中所有行
    def delete_STAR(self):
        self.cursor = self.__connect.cursor()
        sql = 'DELETE FROM STAR'
        self.cursor.execute(sql)
        self.__connect.commit()
        self.__connect.close()

    # 删除评论表中所有行
    def delete_COMMENT(self):
        self.cursor = self.__connect.cursor()
        sql = 'DELETE FROM COMMENT'
        self.cursor.execute(sql)
        self.__connect.commit()
        self.__connect.close()

    # 根据iid删除单个作品
    def deleteWork(self, token, iid):
        self.cursor = self.__connect.cursor()
        # 根据token获取用户信息
        result = self.getUSRByToken(token)
        # 查找失败，则返回
        if not result:
            print("未找到用户ID")
            return ''
        else:
            uid = result[0]

        # 根据iid查询对应作品表的作者uid，对比是否一致，不一致则不能删除
        sql = 'SELECT UID FROM WORK WHERE IID = ?'
        self.cursor.execute(sql, (iid,))
        result = self.cursor.fetchone()
        # 查找失败，则返回
        if not result:
            print("未找到用户ID")
            return ''
        # 不一致，返回
        if uid != result[0]:
            print("不是自己的作品，没有权限删除")
            return ''
        # 一致，删除
        sql = 'DELETE FROM WORK WHERE IID = ?'
        self.cursor.execute(sql, (iid,))
        # 还要删除这个作品的点赞表和评论表
        sql = 'DELETE FROM STAR WHERE IID = ?'
        self.cursor.execute(sql, (iid,))
        sql = 'DELETE FROM COMMENT WHERE IID = ?'
        self.cursor.execute(sql, (iid,))

        self.__connect.commit()
        self.__connect.close()
        return iid

    # 测试
    def test(self):
        self.cursor = self.__connect.cursor()

        token = "796ae392-55dd-30cd-be61-6f15e2477771"
        sql = 'SELECT * FROM USR WHERE Token = ?'
        self.cursor.execute(sql, (token,))
        result = self.cursor.fetchone()
        print("fetch1: ", result)

        token = "796ae392-55dd-30cd-be61-6f15e247777"
        sql = 'SELECT * FROM USR WHERE Token = ?'
        self.cursor.execute(sql, (token,))
        result = self.cursor.fetchone()
        print("fetch2: ", result)

        token = "796ae392-55dd-30cd-be61-6f15e2477771"
        sql = 'SELECT UID FROM USR WHERE Token = ?'
        self.cursor.execute(sql, (token,))
        result = self.cursor.fetchone()
        print("fetch3: ", result)

        token = "796ae392-55dd-30cd-be61-6f15e247777"
        sql = 'SELECT UID FROM USR WHERE Token = ?'
        self.cursor.execute(sql, (token,))
        result = self.cursor.fetchone()
        print("fetch4: ", result)

        sql = 'SELECT MAX(UID) FROM USR'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        print("fetch5: ", result)

        sql = 'SELECT MAX(UID) FROM USR Where UID > 10'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        print("fetch6: ", result)

def main():
    dbc = DBController()

    # dbc.register('456', 'abc', '你的家乡缩写是？', 'WH')
    # dbc.print_WORK()
    # result = dbc.getUSRByToken("796ae392-55dd-30cd-be61-6f15e2477771")
    # print(result)
    # result = dbc.forgotPassword("123", "abc", "DWQ")

    # dbc.delete_STAR()
    # dbc.star("796ae392-55dd-30cd-be61-6f15e2477771", 0)
    # dbc.print_STAR()

    # dbc.comment("796ae392-55dd-30cd-be61-6f15e2477771", 0, "不行哦")
    # dbc.print_COMMENT()
    # print(dbc.getCommentInfo(0))
    # dbc.select_USR()

    # dbc.deleteWork("796ae392-55dd-30cd-be61-6f15e2477771", 0)
    # dbc.print_WORK()





if __name__ == '__main__':
    main()

    







