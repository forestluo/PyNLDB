# -*- coding: utf-8 -*-

from nldb.sqlite.SQContent import *

class SQRaw(SQContent) :
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
            {"length" : item.length, "content" : item.content, "source" : item.source})
