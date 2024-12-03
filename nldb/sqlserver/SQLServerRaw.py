# -*- coding: utf-8 -*-

from nldb.sqlserver.SQLServer import *

class SQLServerRaw (SQLServer) :
    # 数据表名
    _tableName = "RawContent"

    def random(self) :
        # 返回结果
        return self._random(SQLServerRaw._tableName)

    def total(self) :
        # 返回数据结果
        return self._total("SELECT COUNT(*) AS count FROM " + SQLServerRaw._tableName)

    def save(self, file_name) :
        # 调用父类函数
        self._save("SELECT length, content, source FROM " + SQLServerRaw._tableName, file_name)

    def traverse(self, function, parameter = None) :
        # 调用父类函数
        self._traverse("SELECT length, content, source FROM " + SQLServerRaw._tableName, function, parameter)
