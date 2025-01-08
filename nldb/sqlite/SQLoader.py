# -*- coding: utf-8 -*-
import sqlite3

def main() :
    # 建立数据库链接
    print(f"SQLoader.main : open db file !")
    dbConn = \
        sqlite3.connect(
            "..\\..\\db\\nldb3.db",
            check_same_thread = False)
    # 内存数据库
    print(f"SQLoader.main : open memory file !")
    memConn = \
        sqlite3.connect(
            ":memory:",
            check_same_thread = False)
    #加载数据
    print(f"SQLoader.main : load db file into memory !")
    dbConn.backup(memConn)
    # 关闭连接
    print(f"SQLoader.main : close db file !")
    dbConn.close()
    # 查找
    print(f"SQLoader.main : create cursor of memory file !")
    dbCursor = memConn.cursor()
    # 执行
    dbCursor.execute("SELECT * FROM words WHERE content = ? LIMIT 1", "吖宝")
    # 获得返回数据
    data = dbCursor.fetchone()
    # 关闭
    print(f"SQLoader.main : close cursor of memory file !")
    dbCursor.close()
    # 关闭连接
    print(f"SQLoader.main : close memory file !")
    memConn.close()
    # 打印
    print(data)

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("SQLoader.main :__main__ : ", str(e))
        print("SQLoader.main :__main__ : unexpected exit !")
