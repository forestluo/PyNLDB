# -*- coding: utf-8 -*-

from nlp.alg.DBVectorization import *
from nldb.sqlserver.SQLCounter import *

class SQLVectorization(DBVectorization) :
    # 初始化
    def __init__(self, dimension) :
        # 调用父类初始化
        super().__init__(dimension, SQLCounter())

def main() :
    # 新建
    sqlvz = SQLVectorization(2)
    # 获得计数
    count = sqlvz.get_count("运动")
    # 打印信息
    print(f"SQLVectorization.main : count = {count}")

    # 加载测试数据
    if sqlvz.load_vectors("..\\..\\json\\vectors.json") > 0 :
        # 保存相关系数矩阵
        sqlvz.save_gammas("..\\..\\json\\gammas.json")
    else :
        # 打印信息
        print(f"SQLVectorization.main : fail to load file !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("SQLVectorization.main :__main__ : ", str(e))
        print("SQLVectorization.main :__main__ : unexpected exit !")