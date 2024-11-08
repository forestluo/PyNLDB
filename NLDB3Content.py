# -*- coding: utf-8 -*-

import sys
import json
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
        exist_flag = False
        # 设置SQL语句
        db_sql = "SELECT * FROM SYSDATABASES WHERE name='nldb3'"
        # 执行SQL
        self._dbCursor.execute(db_sql)
        # 查看结果集
        while True:
            # 获得一条记录
            data = self._dbCursor.fetchone()
            # 检查返回结果
            if data is None : break
            # 设置标记位
            exist_flag = True

        # 使用nldb3
        self._dbCursor.execute("USE NLDB3")

        # 打印数据记录
        if exist_flag:
            # 打印提示信息
            print("NLDB3.open : database(\"nldb3\") exists !")
        else:
            # 打印提示信息
            print("NLDB3.open : database(\"nldb3\") does not exist !")
        # 返回结果
        return exist_flag

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

    def _total(self, sql) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None
        assert isinstance(sql, str)

        # 执行语句
        self._dbCursor.execute(sql)
        # 获得返回数据
        data = self._dbCursor.fetchone()
        # 检查数据结果
        assert data is not None
        # 返回数据结果
        return data["count"]

    def _random(self, table_name) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None
        assert isinstance(table_name, str)

        # 设置SQL语句
        db_sql = "SELECT TOP 1 content FROM " + table_name + " ORDER BY NEWID()"
        # 执行语句
        self._dbCursor.execute(db_sql)
        # 获得返回数据
        data = self._dbCursor.fetchone()
        # 打印数据总数
        print("NLDB3Raw.random : 1 row processed !")
        # 返回结果
        return data

    def _traverse(self, sql, function) :
        # 检查数据库链接及游标
        assert isinstance(sql, str)
        assert self._dbConn is not None
        assert self._dbCursor is not None

        # 计数器
        count = 0
        # 获得总数
        total = self.total()
        # 打印数据总数
        print("NLDB3.traverse : try to process %d row(s) !" % total)

        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 执行语句
        self._dbCursor.execute(sql)
        # 获得返回数据
        data = self._dbCursor.fetchone()
        # 检查数据结果
        while data :
            # 计数器加1
            count = count + 1
            # 检查函数
            if function is not None: function(data)
            # 检查结果
            if count >= (percent + 1) * one_percent :
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end = "")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end = "")
                sys.stdout.flush()
            # 取得下一行数据
            data = self._dbCursor.fetchone()
        # 打印数据总数
        print("")
        print("NLDB3.traverse : %d row(s) processed !" % total)

    def _save(self, sql, file_name) :
        # 检查文件名
        assert isinstance(file_name, str)
        # 打开文件
        json_file = open(file_name, "w", encoding = "utf-8")
        # 打印信息
        print("NLDB3.save : file(\"%s\") opened !" % file_name)
        # 检查文件
        assert json_file is not None

        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        # 计数器
        count = 0
        # 获得总数
        total = self.total()
        # 打印数据总数
        print("NLDB3.save : try to save %d row(s) !" % total)
        # 将总数写入文件
        json_file.write(str(total))
        json_file.write("\n")

        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 执行语句
        self._dbCursor.execute(sql)
        # 获得返回数据
        data = self._dbCursor.fetchone()
        # 检查数据结果
        while data:
            # 计数器加1
            count = count + 1
            # 写入文件
            json_file.write(json.dumps(data, ensure_ascii = False))
            json_file.write("\n")
            # 检查结果
            if count >= (percent + 1) * one_percent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end = "")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end = "")
                sys.stdout.flush()
            # 取得下一行数据
            data = self._dbCursor.fetchone()
        # 打印数据总数
        print("")
        print("NLDB3.save : %d row(s) saved !" % total)
        # 关闭文件
        json_file.close()
        # 打印信息
        print("NLDB3.save : file(\"%s\") closed !" % file_name)

class NLDB3Raw (NLDB3) :
    # 数据表名
    _tableName = "RawContent"

    def random(self) :
        # 返回结果
        return self._random(NLDB3Raw._tableName)

    def total(self) :
        # 返回数据结果
        return self._total("SELECT COUNT(*) AS count FROM " + NLDB3Raw._tableName)

    def save(self, file_name) :
        # 调用父类函数
        self._save("SELECT length, content, count, source FROM " + NLDB3Raw._tableName, file_name)

    def traverse(self, function) :
        # 调用父类函数
        self._traverse("SELECT length, content, count, source FROM " + NLDB3Raw._tableName, function)

class NLDB3Dictionary(NLDB3) :
    # 数据表名
    _tableName = "DictionaryContent"

    def random(self) :
        # 返回结果
        return self._random(NLDB3Dictionary._tableName)

    def total(self):
        # 返回数据结果
        return self._total("SELECT COUNT(*) AS count FROM " + NLDB3Dictionary._tableName)

    def save(self, file_name):
        # 调用父类函数
        self._save("SELECT length, content, count, source, remark FROM " + NLDB3Dictionary._tableName, file_name)

    def traverse(self, function):
        # 调用父类函数
        self._traverse("SELECT length, content, count, source, remark FROM " + NLDB3Dictionary._tableName, function)
