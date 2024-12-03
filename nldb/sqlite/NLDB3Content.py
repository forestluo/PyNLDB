# -*- coding: utf-8 -*-

from nldb.sqlite.SQLite3 import *

class NLDB3Content(SQLite3) :
    # 初始化函数
    def __init__(self, table_name) :
        # 调用父类初始化
        super().__init__()
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