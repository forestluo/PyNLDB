# -*- coding: utf-8 -*-
import traceback

class SimpleDB :
    # 初始化
    def __init__(self) :
        # 设置参数
        self._dbConn = None
        # 设置参数
        self._dbCursor = None

    # 必须被重载
    def _new_conn(self) :
        # 设置连接
        self._dbConn = None
        # 打印提示信息
        print("SimpleDB._new_conn : nothing to do !")

    # 新建游标
    def _new_cursor(self) :
        # 创建游标对象
        self._dbCursor = self._dbConn.cursor()

    # 建立数据库链接
    def open(self) :
        try :
            # 设置参数
            self._new_conn()
            # 检查数据库连接
            assert self._dbConn is not None
            # 设置参数
            self._new_cursor()
            # 检查数据游标
            assert self._dbCursor is not None
            # 返回结果
            return True
        except Exception as e:
            traceback.print_exc()
            print("SimpleDB.open : ", str(e))
            print("SimpleDB.open : unexpected exit !")
        # 返回结果
        return False

    # 关闭数据库链接
    def close(self) :
        # 检查数据库游标
        if self._dbCursor is not None :
            try:
                # 关闭数据游标
                self._dbCursor.close()
            except Exception as e:
                traceback.print_exc()
                print("SimpleDB.close : ", str(e))
                print("SimpleDB.close : unexpected exit !")
        # 检查数据库链接
        if self._dbConn is not None :
            try :
                # 关闭数据库链接
                self._dbConn.close()
            except Exception as e:
                traceback.print_exc()
                print("SimpleDB.close : ", str(e))
                print("SimpleDB.close : unexpected exit !")

    def _execute(self, sql, parameters = None, commit = False) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        try :
            # 检查参数
            if parameters is None :
                # 执行
                self._dbCursor.execute(sql)
            else :
                # 执行
                self._dbCursor.execute(sql, parameters)
            # 提交
            if commit : self._dbConn.commit()
            # 返回结果
            return True
        except Exception as e:
            traceback.print_exc()
            print("SimpleDB._execute : ", str(e))
            print("SimpleDB._execute : unexpected exit !")
        # 返回结果
        return False

    def _drop_table(self, table_name) :
        # 检查数据
        assert isinstance(table_name, str)
        # 返回结果
        return self._execute(f"DROP TABLE IF EXISTS {table_name};")

    # 生成数据表
    def _create_table(self, table_name, rows) :
        # 检查数据
        assert isinstance(rows, list)
        assert isinstance(table_name, str)
        # 返回结果
        return self._execute(f"CREATE TABLE IF NOT EXISTS {table_name} (" + ",".join(rows) + ");")

    def _total_count(self, table_name) :
        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None
        assert isinstance(table_name, str)

        # 执行语句
        self._dbCursor.execute(f"SELECT COUNT(*) AS total FROM {table_name}")
        # 获得返回数据
        data = self._dbCursor.fetchone()
        # 返回数据结果
        return data["total"] if data is not None else -1

    def _traverse(self, total, sql, function, parameter = None) :
        # 检查数据库链接及游标
        assert isinstance(sql, str)
        assert self._dbConn is not None
        assert self._dbCursor is not None

        # 进度条
        pb = ProgressBar(total)
        # 打印数据总数
        pb.begin(f"SimpleDB._traverse : try to process {total} row(s) !")
        # 执行语句
        self._dbCursor.execute(sql)
        # 获得返回数据
        data = self._dbCursor.fetchone()
        # 检查数据结果
        while data :
            # 进度条
            pb.increase()
            # 检查函数
            if function is not None: function(data, parameter)
            # 取得下一行数据
            data = self._dbCursor.fetchone()
        # 打印数据总数
        pb.end(f"SimpleDB._traverse : {total} row(s) processed !")

    def _save(self, total, sql, file_name) :
        # 检查文件名
        assert isinstance(file_name, str)
        # 打开文件
        json_file = open(file_name, "w", encoding = "utf-8")
        # 打印信息
        print("SimpleDB._save : file(\"%s\") opened !" % file_name)
        # 检查文件
        assert json_file is not None

        # 检查数据库链接及游标
        assert self._dbConn is not None
        assert self._dbCursor is not None

        # 进度条
        pb = ProgressBar(total)
        # 打印数据总数
        pb.begin(f"SimpleDB._save : try to save {total} row(s) !")
        # 将总数写入文件
        json_file.write(str(total))
        json_file.write("\n")
        # 执行语句
        self._dbCursor.execute(sql)
        # 获得返回数据
        data = self._dbCursor.fetchone()
        # 检查数据结果
        while data:
            # 计数器加1
            pb.increase()
            # 写入文件
            json_file.write(json.dumps(data, ensure_ascii = False))
            json_file.write("\n")
            # 取得下一行数据
            data = self._dbCursor.fetchone()
        # 打印信息
        pb.end(f"SimpleDB._save : {total} row(s) saved !")
        # 关闭文件
        json_file.close()
        # 打印信息
        print("SimpleDB._save : file(\"%s\") closed !" % file_name)
