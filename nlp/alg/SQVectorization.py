# -*- coding: utf-8 -*-

from nldb.sqlite.SQWords import *
from nlp.alg.DBVectorization import *

class SQVectorization(DBVectorization) :
    # 初始化
    def __init__(self, dimension) :
        # 调用父类初始化
        super().__init__(dimension, SQWords())

def main() :
    # 新建
    sqvz = SQVectorization(2)
    # 获得计数
    count = sqvz.get_count("运动")
    # 打印信息
    print(f"SQVectorization.main : count = {count}")

    # 加载测试数据
    if sqvz.load_vectors("..\\..\\json\\vectors.json") > 0 :
        # 保存相关系数矩阵
        sqvz.save_gammas("..\\..\\json\\gammas.json")
    else :
        # 打印信息
        print(f"SQVectorization.main : fail to load file !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("SQVectorization.main :__main__ : ", str(e))
        print("SQVectorization.main :__main__ : unexpected exit !")
