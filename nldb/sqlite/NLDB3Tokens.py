# -*- coding: utf-8 -*-

from nldb.sqlite.NLDB3Content import *

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
