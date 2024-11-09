# -*- coding: utf-8 -*-

import sys
import json
import sqlite3
import traceback

from Content import *

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

        # 计数器
        count = 0
        # 获得总数
        total = self.total()
        # 打印数据总数
        print("SQLite3.traverse : try to process %d row(s) !" % total)

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
        print("SQLite3.traverse : %d row(s) processed !" % total)

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

        # 计数器
        count = 0
        # 获得总数
        total = self.total()
        # 打印数据总数
        print("SQLite3.save : try to save %d row(s) !" % total)
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
        print("SQLite3.save : %d row(s) saved !" % total)
        # 关闭文件
        json_file.close()
        # 打印信息
        print("SQLite3.save : file(\"%s\") closed !" % file_name)

class NLDB3Raw(SQLite3) :
    # 删除RawContent数据表
    def drop(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try:
            # 创建数据表
            sql = "DROP TABLE IF EXISTS raw;"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Raw.drop : normalized content dropped !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Raw.drop : ", str(e))
            print("NLDB3Raw.drop : unexpected exit !")

    # 生成RawContent数据表
    def create(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "CREATE TABLE IF NOT EXISTS raw " + \
                "(length integer default 0," + \
                "content text not null, source varchar(32));"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Raw.create_raw : normalized table created !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Raw.create : ", str(e))
            print("NLDB3Raw.create : unexpected exit !")

    def insert(self, item) :
        # 检查参数
        assert isinstance(item, RawItem)

        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "INSERT INTO raw(length, content, source) VALUES (?, ?, ?);"
            # 执行
            self._dbCursor.execute(sql, (item.length, item.content, item.source))
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Raw.insert : ", str(e))
            print("NLDB3Raw.insert : unexpected exit !")

class NLDB3Normalized(SQLite3) :
    # 删除RawContent数据表
    def drop(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try:
            # 创建数据表
            sql = "DROP TABLE IF EXISTS normalized;"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Normalized.drop : normalized table dropped !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Normalized.drop : ", str(e))
            print("NLDB3Normalized.drop : unexpected exit !")

    # 生成RawContent数据表
    def create(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "CREATE TABLE IF NOT EXISTS normalized " + \
                "(length integer default 0," + \
                "content text not null, source varchar(32));"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Normalized.create_raw : normalized table created !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Normalized.create : ", str(e))
            print("NLDB3Normalized.create : unexpected exit !")

    def insert(self, item) :
        # 检查参数
        assert isinstance(item, RawItem)

        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "INSERT INTO normalized(length, content, source) VALUES (?, ?, ?);"
            # 执行
            self._dbCursor.execute(sql, (item.length, item.content, item.source))
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Normalized.insert : ", str(e))
            print("NLDB3Normalized.insert : unexpected exit !")

class NLDB3Tokens(SQLite3) :
    # 删除RawContent数据表
    def drop(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try:
            # 创建数据表
            sql = "DROP TABLE IF EXISTS tokens;"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Tokens.drop : tokens table dropped !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Tokens.drop : ", str(e))
            print("NLDB3Tokens.drop : unexpected exit !")

    # 生成RawContent数据表
    def create(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "CREATE TABLE IF NOT EXISTS tokens " + \
                "(length integer default 0, count integer default 0," + \
                "content char(1) primary key not null, unicode integer default 0);"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Tokens.create : tokens table created !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Tokens.create : ", str(e))
            print("NLDB3Tokens.create : unexpected exit !")

    def insert(self, item) :
        # 检查参数
        assert isinstance(item, TokenItem)

        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "INSERT INTO tokens(length, count, content, unicode) VALUES (?, ?, ?, ?);"
            # 执行
            self._dbCursor.execute(sql, (item.length, item.count, item.content, ord(item.content)))
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Tokens.insert : ", str(e))
            print("NLDB3Tokens.insert : unexpected exit !")

class NLDB3Segments(SQLite3) :
    # 删除RawContent数据表
    def drop(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try:
            # 创建数据表
            sql = "DROP TABLE IF EXISTS segments;"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Segments.drop : segments content dropped !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Segments.drop : ", str(e))
            print("NLDB3Segments.drop : unexpected exit !")

    # 生成RawContent数据表
    def create(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "CREATE TABLE IF NOT EXISTS segments " + \
                "(length integer default 0, " + \
                "count integer default 0, content text not null);"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Segments.create : segments table created !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Segments.create : ", str(e))
            print("NLDB3Segments.create : unexpected exit !")

    def insert(self, item) :
        # 检查参数
        assert isinstance(item, SegmentItem)

        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "INSERT INTO segments(length, count, content) VALUES (?, ?, ?);"
            # 执行
            self._dbCursor.execute(sql, (item.length, item.count, item.content))
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Segments.insert : ", str(e))
            print("NLDB3Segments.insert : unexpected exit !")

class NLDB3Sentences(SQLite3) :
    # 删除RawContent数据表
    def drop(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try:
            # 创建数据表
            sql = "DROP TABLE IF EXISTS sentences;"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Sentences.drop : sentences content dropped !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Sentences.drop : ", str(e))
            print("NLDB3Sentences.drop : unexpected exit !")

    # 生成RawContent数据表
    def create(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "CREATE TABLE IF NOT EXISTS sentences " + \
                "(length integer default 0, " + \
                "count integer default 0, content text not null);"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Sentences.create : sentences table created !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Sentences.create : ", str(e))
            print("NLDB3Sentences.create : unexpected exit !")

    def insert(self, item) :
        # 检查参数
        assert isinstance(item, SentenceItem)

        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "INSERT INTO sentences(length, count, content) VALUES (?, ?, ?);"
            # 执行
            self._dbCursor.execute(sql, (item.length, item.count, item.content))
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Sentences.insert : ", str(e))
            print("NLDB3Sentences.insert : unexpected exit !")

class NLDB3Dictionary(SQLite3) :
    # 删除RawContent数据表
    def drop(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try:
            # 创建数据表
            sql = "DROP TABLE IF EXISTS dictionary;"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Dictionary.drop : dictionary content dropped !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Dictionary.drop : ", str(e))
            print("NLDB3Dictionary.drop : unexpected exit !")

    # 生成RawContent数据表
    def create(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "CREATE TABLE IF NOT EXISTS dictionary " + \
                "(length integer default 0, " + \
                "count integer default 0, content text not null);"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Dictionary.create : dictionary table created !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Dictionary.create : ", str(e))
            print("NLDB3Dictionary.create : unexpected exit !")

    def insert(self, item) :
        # 检查参数
        assert isinstance(item, DictionaryItem)

        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "INSERT INTO dictionary(length, count, content) VALUES (?, ?, ?);"
            # 执行
            self._dbCursor.execute(sql, (item.length, item.count, item.content))
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Dictionary.insert : ", str(e))
            print("NLDB3Dictionary.insert : unexpected exit !")

class NLDB3Words(SQLite3) :
    # 删除RawContent数据表
    def drop(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try:
            # 创建数据表
            sql = "DROP TABLE IF EXISTS words;"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Words.drop : words content dropped !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Words.drop : ", str(e))
            print("NLDB3Words.drop : unexpected exit !")

    # 生成RawContent数据表
    def create(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "CREATE TABLE IF NOT EXISTS words " + \
                "(length integer default 0, " + \
                "count integer default 0, content text not null);"
            # 执行
            self._dbCursor.execute(sql)
            # 打印提示信息
            print("NLDB3Words.create : words table created !")
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Words.create : ", str(e))
            print("NLDB3Words.create : unexpected exit !")

    def insert(self, item) :
        # 检查参数
        assert isinstance(item, WordItem)

        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 创建数据表
            sql = "INSERT INTO words(length, count, content) VALUES (?, ?, ?);"
            # 执行
            self._dbCursor.execute(sql, (item.length, item.count, item.content))
        except Exception as e:
            traceback.print_exc()
            print("NLDB3Words.insert : ", str(e))
            print("NLDB3Words.insert : unexpected exit !")
