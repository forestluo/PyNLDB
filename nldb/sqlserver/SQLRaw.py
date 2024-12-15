# -*- coding: utf-8 -*-

from nldb.sqlserver.SQLServer import *

class SQLRaw(SQLServer) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化
        super().__init__("RawContent")

    def save(self, file_name) :
        # 获得总数
        total = self.total_count()
        # 调用父类函数
        self._save(total,
            f"SELECT length, content, source FROM {self.table_name}", file_name)

    def traverse(self, function, parameter = None) :
        # 获得总数
        total = self.total_count()
        # 调用父类函数
        self._traverse(total,
            f"SELECT length, content, source FROM {self.table_name}", function, parameter)
