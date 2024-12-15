# -*- coding: utf-8 -*-

import json
import pymssql

from nldb.SimpleDB import *
from widget.ProgressBar import *

class SQLServer(SimpleDB) :
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
        self._dbConn = pymssql.connect(
            "localhost", "sa", "forest_luo")
        # 设置立即操作
        self._dbConn.autocommit(True)

    # 新建游标
    def _new_cursor(self) :
        # 创建游标对象
        self._dbCursor = self._dbConn.cursor(as_dict = True)

    # 建立数据库链接
    def open(self) :
        # 调用父类函数
        if not super().open() : return False

        try :
            # 使用nldb3
            self._dbCursor.execute("USE nldb3")
            # 返回结果
            return True
        except Exception as e:
            traceback.print_exc()
            print("SQLServer.open : ", str(e))
            print("SQLServer.open : unexpected exit !")
        # 返回结果
        return False

    # 删除数据表
    def drop_table(self) :
        # 返回结果
        return self._drop_table(self.table_name)

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
        self._dbCursor.execute(f"SELECT TOP 1 content FROM {self.table_name} ORDER BY NEWID()")
        # 获得返回数据
        return self._dbCursor.fetchone()