# -*- coding: utf-8 -*-

from nldb.sqlite.SQLite3 import *

class SQContent(SQLite3) :
    # 初始化函数
    def __init__(self, table_name) :
        # 调用父类初始化
        super().__init__(table_name)
        # 检查参数
        assert isinstance(table_name, str)

    # 生成RawContent数据表
    def create_table(self):
        # 返回结果
        return self._create_table(self.table_name,
        ["length integer default 0",
            "count integer default 0", "content text not null"])

    def insert_table(self, item):
        # 检查参数
        assert isinstance(item, ContentItem)
        # 返回结果
        return self._insert_table(self.table_name,
            {"length" : item.length, "count" : item.count, "content" : item.content})