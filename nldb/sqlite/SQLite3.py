# -*- coding: utf-8 -*-
import sqlite3

from nldb.SimpleDB import *

class SQLite3(SimpleDB) :
    # 初始化
    def __init__(self, table_name) :
        # 调用父类初始化
        super().__init__()
        # 设置数据表名
        self.__table_name = table_name

    @property
    def table_name(self) :
        # 返回结果
        return self.__table_name

    # 必须被重载
    def _new_conn(self) :
        # 建立数据库链接
        self._dbConn = \
            sqlite3.connect("..\\..\\db\\nldb3.db")
        # 修改返回方式
        def dict_factory(cursor, row) :
            result = {}
            for index, column in \
                enumerate(cursor.description) :
                result[column[0]] = row[index]
            return result
        # 设置数据
        self._dbConn.row_factory = dict_factory

    def _insert_table(self, table_name, parameters) :
        # 检查数据
        assert isinstance(table_name, str)
        assert isinstance(parameters, dict)

        # SQL语句
        values = []
        suffix = ")"
        prefix = f"("
        for key, value in parameters.values() :
            # 增加数据
            values.append(value)
            # 拼接语句
            suffix = ", ?" + suffix
            prefix = prefix + key + ", "
        # SQL语句
        suffix = "(" + suffix[3:]
        prefix = prefix[:-2] + ")"
        # 返回结果
        return self._execute(f"INSERT INTO {table_name} {prefix} VALUES {suffix}", tuple(values))

    # 删除数据表
    def drop_table(self) :
        # 返回结果
        return self._drop_table(self.__table_name)

    def total_count(self) :
        # 返回结果
        return self._total_count(self.table_name)

    # 随机选取一行
    def random(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None
        assert isinstance(self.table_name, str)

        # 执行语句
        self._dbCursor.execute(f"SELECT content FROM {self.table_name} ORDER BY RAND() LIMIT 1")
        # 获得返回数据
        return self._dbCursor.fetchone()







