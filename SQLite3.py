# -*- coding: utf-8 -*-

import sys
import json
import sqlite3
import traceback

from Content import *
from CommonTool import *

db_path = ".\\db\\"

def dict_factory(cursor, row) :
    d = {}
    for idx, col in enumerate(cursor.description) :
        d[col[0]] = row[idx]
    return d

class SQLite3 :
    # 数据库链接
    _dbConn = None
    # 数据库游标
    _dbCursor = None

    # 建立数据库链接
    def open(self) :
        try:
            # 打开数据库链接
            print("SQLite3.open : try to open database !")
            # 建立数据库链接
            self._dbConn = sqlite3.connect(db_path + "nldb3.db")
            # 设置数据
            self._dbConn.row_factory = dict_factory
            # 创建游标对象，并设置返回数据类型的字符为字典
            print("SQLite3.open : try to create cursor !")
            self._dbCursor = self._dbConn.cursor()
            # 打印提示信息
            print("SQLite3.open : database(\"nldb3\") exists !")
            # 返回结果
            return True
        except Exception as e:
            traceback.print_exc()
            print("SQLite3.close : ", str(e))
            print("SQLite3.close : unexpected exit !")
        # 返回结果
        return False

    # 关闭数据库链接
    def close(self) :
        # 检查数据库游标
        if self._dbCursor is not None:
            try:
                # 关闭数据游标
                self._dbCursor.close()
                # 打印提示信息
                print("SQLite3.close : cursor was closed !")
            except Exception as e:
                traceback.print_exc()
                print("SQLite3.close : ", str(e))
                print("SQLite3.close : unexpected exit !")

        # 检查数据库链接
        if self._dbConn is not None:
            try:
                # 提交
                self._dbConn.commit()
                # 关闭数据库链接
                self._dbConn.close()
                # 打印提示信息
                print("SQLite3.close : connection was closed !")
            except Exception as e:
                traceback.print_exc()
                print("SQLite3.close : ", str(e))
                print("SQLite3.close : unexpected exit !")

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

    def _traverse(self, sql, function) :
        # 检查数据库链接及游标
        assert isinstance(sql, str)
        assert self._dbConn is not None
        assert self._dbCursor is not None

        # 获得总数
        total = self.total()
        # 进度条
        pb = ProgressBar(total)
        # 打印数据总数
        pb.begin(f"SQLite3.traverse : try to process {total} row(s) !")

        # 执行语句
        self._dbCursor.execute(sql)
        # 获得返回数据
        data = self._dbCursor.fetchone()
        # 检查数据结果
        while data :
            # 计数器加1
            pb.increase()
            # 检查函数
            if function is not None: function(data)
            # 取得下一行数据
            data = self._dbCursor.fetchone()
        # 打印数据总数
        pb.end(f"SQLite3.traverse : {total} row(s) processed !")

    def _save(self, sql, file_name) :
        # 检查文件名
        assert isinstance(file_name, str)
        # 打开文件
        json_file = open(file_name, "w", encoding = "utf-8")
        # 打印信息
        print("SQLite3.save : file(\"%s\") opened !" % file_name)
        # 检查文件
        assert json_file is not None

        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        # 获得总数
        total = self.total()
        # 进度条
        pb = ProgressBar(total)
        # 打印数据总数
        pb.begin(f"SQLite3.save : try to save {total} row(s) !")
        # 将总数写入文件
        json_file.write(str(total))
        json_file.write("\n")
        # 执行语句
        self._dbCursor.execute(sql)
        # 获得返回数据
        data = self._dbCursor.fetchone()
        # 检查数据结果
        while data:
            # 计数器加1
            pb.increase()
            # 写入文件
            json_file.write(json.dumps(data, ensure_ascii = False))
            json_file.write("\n")
            # 取得下一行数据
            data = self._dbCursor.fetchone()
        # 打印信息
        pb.end(f"SQLite3.save : {total} row(s) saved !")
        # 关闭文件
        json_file.close()
        # 打印信息
        print("SQLite3.save : file(\"%s\") closed !" % file_name)

    def _execute(self, sql, parameters = None, commit = False) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 检查参数
            if parameters is None :
                # 执行
                self._dbCursor.execute(sql)
            # 执行
            else : self._dbCursor.execute(sql, parameters)
            # 提交
            if commit : self._dbConn.commit()
            # 返回结果
            return True
        except Exception as e:
            traceback.print_exc()
            print("SQLite3._execute : ", str(e))
            print("SQLite3._execute : unexpected exit !")
        # 返回结果
        return False

    def _drop_table(self, table_name) :
        # 检查数据
        assert isinstance(table_name, str)
        # 返回结果
        return self._execute("DROP TABLE IF EXISTS {};".format(table_name), commit = True)

    def _insert_table(self, table_name, sql, parameters) :
        # 检查数据
        assert isinstance(table_name, str)
        # 返回结果
        return self._execute("INSERT INTO {} ".format(table_name) + sql, parameters)

    # 生成数据表
    def _create_table(self, table_name, rows) :
        # 检查数据
        assert isinstance(rows, list)
        assert isinstance(table_name, str)
        # 返回结果
        return self._execute("CREATE TABLE IF NOT EXISTS {} (".format(table_name) + ",".join(rows) + ");", commit = True)

class NLDB3Content(SQLite3) :
    # 初始化函数
    def __init__(self, table_name) :
        # 检查参数
        assert isinstance(table_name, str)
        # 设置数据表名
        self._table_name = table_name

    # 数据表名
    @property
    def table_name(self) :
        # 返回结果
        return self._table_name

    # 删除Content数据表
    def drop_table(self):
        # 返回结果
        return self._drop_table(self._table_name)

    # 生成RawContent数据表
    def create_table(self):
        # 返回结果
        return self._create_table(self._table_name,
        ["length integer default 0",
            "count integer default 0", "content text not null"])

    def insert_table(self, item):
        # 检查参数
        assert isinstance(item, ContentItem)
        # 返回结果
        return self._insert_table(self._table_name,
        "(length, count, content) VALUES (?, ?, ?)",(item.length, item.count, item.content))

class NLDB3Raw(NLDB3Content) :
    # 初始化函数
    def __init__(self) :
        # 调用父类函数
        super().__init__("raw")

    # 生成RawContent数据表
    def create_table(self) :
        # 返回结果
        return self._create_table(self._table_name,
            ["length integer default 0",
            "content text not null", "source varchar(32)"])

    def insert_table(self, item) :
        # 检查参数
        assert isinstance(item, RawItem)
        # 返回结果
        return self._insert_table(self._table_name,
        "(length, content, source) VALUES (?, ?, ?)",
        (item.length, item.content, item.source))

class NLDB3Tokens(NLDB3Content) :
    # 初始化函数
    def __init__(self) :
        # 调用父类函数
        super().__init__("tokens")

    # 生成TokenContent数据表
    def create_table(self) :
        # 返回结果
        return self._create_table(self._table_name,
        ["length integer default 0", "count integer default 0",
            "content char(1) primary key not null", "unicode integer default 0"])

    def insert_table(self, item) :
        # 检查参数
        assert isinstance(item, TokenItem)
        # 返回结果
        return self._insert_table(self._table_name,
        "(length, count, content, unicode) VALUES (?, ?, ?, ?)",
        (item.length, item.count, item.content, ord(item.content)))

class NLDB3Segments(NLDB3Content) :
    # 初始化函数
    def __init__(self) :
        # 调用父类函数
        super().__init__("segments")

class NLDB3Sentences(NLDB3Content) :
    # 初始化函数
    def __init__(self):
        # 调用父类函数
        super().__init__("sentences")

class NLDB3Dictionary(NLDB3Content) :
    # 初始化函数
    def __init__(self):
        # 调用父类函数
        super().__init__("dictionary")

    # 生成DictionaryContent数据表
    def create_table(self) :
        # 返回结果
        return self._create_table(self._table_name,
        ["length integer default 0", "count integer default 0",
            "content varchar(64) primary key not null"])

class NLDB3Words(NLDB3Content) :
    # 初始化函数
    def __init__(self):
        # 调用父类函数
        super().__init__("words")

    # 生成WordContent数据表
    def create_table(self) :
        # 返回结果
        return self._create_table(self._table_name,
        ["length integer default 0", "count integer default 0",
            "content varchar(8) primary key not null"])
