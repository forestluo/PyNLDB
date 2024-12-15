# -*- coding: utf-8 -*-

from nldb.sqlite.SQContent import *

class SQWords(SQContent) :
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

    def get_count(self, key) :
        # 检查数据库链接及游标
        assert isinstance(key, str)

        # 执行语句
        self._execute(
            f"SELECT count FROM "
            f"{self.table_name} WHERE content = ? LIMIT 1", tuple([key]))
        # 获得返回数据
        data = self._dbCursor.fetchone()
        # 返回结果
        return data["count"] if data is not None else -1

def main() :
    # 新建
    counter = SQWords()
    # 打开连接
    if not counter.open() :
        # 打印信息
        print(f"SQWords.main : fail to open connection !")
        return
    # 获得计数
    count = counter.get_count("吖宝")
    # 打印信息
    print(f"SQWords.main : count = {count}")
    # 关闭连接
    counter.close()
    # 打印信息
    print(f"SQWords.main : connection successfully closed !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("SQWords.main :__main__ : ", str(e))
        print("SQWords.main :__main__ : unexpected exit !")
