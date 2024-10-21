# -*- coding: utf-8 -*-

import pymssql
import traceback

class NLDB3:

    # 数据库服务器
    server = "localhost"
    # 数据库登录用户名
    user = "sa"
    # 数据库登录密码
    password = "forest_luo"

    # 数据库链接
    _dbConn = None
    # 数据库游标
    _dbCursor = None

    # 建立数据库链接
    def open(self):
        # 打开数据库链接
        print("NLDB3.open : try to open database !")
        # 建立数据库链接
        self._dbConn = pymssql.connect(self.server, self.user, self.password)
        # 设置立即操作
        self._dbConn.autocommit(True)

        # 创建游标对象，并设置返回数据类型的字符为字典
        print("NLDB3.open : try to create cursor !")
        self._dbCursor = self._dbConn.cursor(as_dict = True)

        # 标记位
        existFlag = False
        # 设置SQL语句
        dbSQL = "SELECT * FROM SYSDATABASES WHERE name='nldb3'"
        # 执行SQL
        self._dbCursor.execute(dbSQL)
        # 查看结果集
        while True:
            # 获得一条记录
            dataResult = self._dbCursor.fetchone()
            # 检查返回结果
            if dataResult is None:
                break
            # 设置标记位
            existFlag = True

        # 使用nldb3
        self._dbCursor.execute("USE NLDB3")

        # 打印数据记录
        if existFlag:
            # 打印提示信息
            print("NLDB3.open : database(\"nldb3\") exists !")
        else:
            # 打印提示信息
            print("NLDB3.open : database(\"nldb3\") does not exist !")
        # 返回结果
        return existFlag

    # 关闭数据库链接
    def close(self):
        # 检查数据库游标
        if self._dbCursor is not None:
            try:
                # 关闭数据游标
                self._dbCursor.close()
                # 打印提示信息
                print("NLDB3.close : cursor was closed !")
            except Exception as e:
                traceback.print_exc()
                print("NLDB3.close : ", str(e))
                print("NLDB3.close : unexpected exit !")

        # 检查数据库链接
        if self._dbConn is not None:
            try:
                # 关闭数据库链接
                self._dbConn.close()
                # 打印提示信息
                print("NLDB3.close : connection was closed !")
            except Exception as e:
                traceback.print_exc()
                print("NLDB3.close : ", str(e))
                print("NLDB3.close : unexpected exit !")

def main():

    # 建立数据库链接
    nldb3 = NLDB3()
    # 尝试开启数据库
    existFlag = nldb3.open()
    # 关闭数据库链接
    nldb3.close()

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("NLDB3.main :__main__ : ", str(e))
        print("NLDB3.main :__main__ : unexpected exit !")