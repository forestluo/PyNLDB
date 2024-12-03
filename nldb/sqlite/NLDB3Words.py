# -*- coding: utf-8 -*-

from nldb.sqlite.NLDB3Content import *

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
