# -*- coding: utf-8 -*-
import traceback

from nldb.sqlserver.SQLServer import *

class SQLCounter(SQLServer) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化
        super().__init__("CounterContent")

    def get_count(self, key) :
        # 检查数据库链接及游标
        assert isinstance(key, str)

        # 执行语句
        self._execute(
            f"SELECT TOP 1 count FROM "
            f"{self.table_name} WHERE content = %s", tuple([key]))
        # 获得返回数据
        data = self._dbCursor.fetchone()
        # 返回结果
        return data["count"] if data is not None else -1

    def save(self, file_name) :
        # 获得总数
        total = self.total_count()
        # 调用父类函数
        self._save(total,
            f"SELECT content, count FROM {self.table_name}", file_name)

    def traverse(self, function, parameter = None) :
        # 获得总数
        total = self.total_count()
        # 调用父类函数
        self._traverse(total,
            f"SELECT content, count FROM {self.table_name}", function, parameter)

def main() :
    # 新建
    counter = SQLCounter()
    # 打开连接
    if not counter.open() :
        # 打印信息
        print(f"SQLCounter.main : fail to open connection !")
        return
    # 获得计数
    count = counter.get_count("运动")
    # 打印信息
    print(f"SQLCounter.main : count = {count}")
    # 关闭连接
    counter.close()
    # 打印信息
    print(f"SQLCounter.main : connection successfully closed !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("SQLCounter.main :__main__ : ", str(e))
        print("SQLCounter.main :__main__ : unexpected exit !")
