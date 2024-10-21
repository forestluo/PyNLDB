# -*- coding: utf-8 -*-

import sys
import json
import traceback

from NLDB3 import NLDB3

class NLDB3Raw (NLDB3) :
    # 数据表名
    _tableName = "RawContent"

    def total(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        # 设置SQL语句
        dbSQL = "SELECT COUNT(*) as count FROM " + self._tableName
        # 执行语句
        self._dbCursor.execute(dbSQL)
        # 获得返回数据
        dataResult = self._dbCursor.fetchone()
        # 检查数据结果
        assert dataResult is not None
        # 返回数据结果
        return dataResult["count"]

    def random(self) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        # 设置SQL语句
        dbSQL = "SELECT TOP 1 source,content FROM " + self._tableName + " ORDER BY NEWID()"
        # 执行语句
        self._dbCursor.execute(dbSQL)
        # 获得返回数据
        dataResult = self._dbCursor.fetchone()
        # 打印数据总数
        print("NLDB3Raw.random : 1 row processed !")
        # 返回结果
        return dataResult

    def traverse(self, function) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        # 计数器
        count = 0
        # 获得总数
        total = self.total()
        # 打印数据总数
        print("NLDB3Raw.traverse : try to process %d row(s) !" % total)

        # 百分之一
        percent = 0
        onePercent = total / 100.0
        # 设置SQL语句
        dbSQL = "SELECT * FROM " + self._tableName
        # 执行语句
        self._dbCursor.execute(dbSQL)
        # 获得返回数据
        dataResult = self._dbCursor.fetchone()
        # 检查数据结果
        while dataResult :
            # 计数器加1
            count = count + 1
            # 检查函数
            if function is not None:
                # 调用函数处理数据
                function(dataResult)
            # 检查结果
            if count >= (percent + 1) * onePercent :
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end = "")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end = "")
                sys.stdout.flush()
            # 取得下一行数据
            dataResult = self._dbCursor.fetchone()
        # 打印数据总数
        print("")
        print("NLDB3Raw.traverse : %d row(s) processed !" % total)

    def save(self, fileName):
        # 检查文件名
        if fileName is None:
            fileName = "raw.json"
        # 打开文件
        jsonFile = open(fileName, "w", encoding = "utf-8")
        # 打印信息
        print("NLDB3Raw.save : file(\"%s\") opened !" % fileName)
        # 检查文件
        assert jsonFile is not None

        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        # 计数器
        count = 0
        # 获得总数
        total = self.total()
        # 打印数据总数
        print("NLDB3Raw.save : try to save %d row(s) !" % total)
        # 将总数写入文件
        jsonFile.write(str(total))
        jsonFile.write("\n")

        # 百分之一
        percent = 0
        onePercent = total / 100.0
        # 设置SQL语句
        dbSQL = "SELECT source,content FROM " + self._tableName
        # 执行语句
        self._dbCursor.execute(dbSQL)
        # 获得返回数据
        dataResult = self._dbCursor.fetchone()
        # 检查数据结果
        while dataResult:
            # 计数器加1
            count = count + 1
            # 写入文件
            jsonFile.write(json.dumps(dataResult, ensure_ascii = False))
            jsonFile.write("\n")
            # 检查结果
            if count >= (percent + 1) * onePercent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end="")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                sys.stdout.flush()
            # 取得下一行数据
            dataResult = self._dbCursor.fetchone()
        # 打印数据总数
        print("")
        print("NLDB3Raw.save : %d row(s) saved !" % total)
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("NLDB3Raw.save : file(\"%s\") closed !" % fileName)

def main() :
    # 建立数据库链接
    rawContent = NLDB3Raw()
    # 尝试开启数据库
    assert rawContent.open()
    # 打印数据总数
    print("NLDB3Raw.main : %d row(s) !" % rawContent.total())
    # 格式化输出
    rawContent.save("raw.json")
    # 关闭数据库链接
    rawContent.close()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        print("NLDB3Raw.main :__main__ : ", str(e))
        print("NLDB3Raw.main :__main__ : unexpected exit !")
