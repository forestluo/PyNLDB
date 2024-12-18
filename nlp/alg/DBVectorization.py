# -*- coding: utf-8 -*-
import math

from nlp.alg.WordVector import *
from nlp.alg.SQVectorization import *
from nlp.content.WordContent import *

class DBVectorization(WordVector) :
    # 初始化
    def __init__(self, dimension, table) :
        # 数据库链接
        self.__table = table
        # 调用父类初始化
        super().__init__(dimension)
        # 开启数据库连接
        if not self.__table.open() :
            # 打印信息
            print(f"DBVectorization.__init__ : "
                f"fail to open table({self.table_name}) !")
        else :
            # 打印信息
            print(f"DBVectorization.__init__ : "
                  f"table({self.table_name}) opened !")

    # 析构
    def __del__(self) :
        # 调用父类函数
        super().__del__()
        # 关闭数据库连接
        self.__table.close()
        # 打印信息
        print(f"DBVectorization.__del__ : "
            f"table({self.table_name}) has been closed !")

    # 获得表名
    @property
    def table_name(self) :
        # 返回结果
        return self.__table.table_name

    @property
    def wsize(self) :
        # 兼容性写法
        return math.inf

    # 获得计数
    def get_count(self, key) :
        # 返回结果
        return self.__table.get_count(key)

    # 获得相关系数
    # 速度慢，但能兼容多数内容
    def get_gammas(self, error) :
        # 重建索引
        self.index_vectors()
        # 结束
        print(f"DBVectorization.get_gammas : finished reindexing vectors !")

        # 创建矩阵
        gammas = self._new_gamma()
        # 进度条
        pb = ProgressBar(self.vsize * self.vsize)
        # 开始
        pb.begin(f"DBVectorization.get_gammas : building matrix !")
        # 初始化相关系数
        for v1 in self.vectors() :
            # 检查项目
            if v1.count <= 0 :
                # 增加计数
                pb.increase(self.vsize)
                continue
            # 循环处理
            for v2 in self.vectors() :
                # 进度条
                pb.increase()
                # 检查项目
                if v2.count <= 0 : continue

                # 获得计数
                count = self.get_count(v1.content + v2.content)
                # 检查数值
                if count <= 0 : continue

                # 计算数值
                gamma = 0.5 * float(count) * \
                    (1.0 / float(v1.count) + 1.0 / float(v2.count))
                # 设置数值
                gammas[0][v1.index][v2.index] = gamma
                # 检查结果
                if gamma > error : gammas[1][v1.index][v2.index] = 1.0
        # 结束
        pb.end(f"DBVectorization.get_gammas : finished building matrix !")
        # 返回结果
        return gammas

    # 保存数据
    def save_gammas(self, file_name) :
        # 重建索引
        self.index_vectors()
        # 结束
        print(f"DBVectorization.save_gammas : finished reindexing vectors !")

        # 新建
        words = WordContent()
        # 进度条
        pb = ProgressBar(self.vsize * self.vsize)
        # 开始
        pb.begin(f"DBVectorization.save_gammas : building matrix !")
        # 初始化相关系数
        for v1 in self.vectors() :
            # 检查项目
            if v1.count <= 0 : continue
            # 循环处理
            for v2 in self.vectors() :
                # 检查项目
                if v2.count <= 0 : continue

                # 获得内容
                content = \
                    v1.content + v2.content
                # 获得计数
                count = self.get_count(content)
                # 检查数值
                if count <= 0 : continue

                # 进度条
                pb.increase()
                # 计算数值
                gamma = 0.5 * float(count) * \
                        (1.0 / float(v1.count) + 1.0 / float(v2.count))
                # 检查结果
                if content not in words :
                    # 新建项目
                    item = words.new_item(content, count)
                    # 计算数值
                    item.gamma = gamma
                    # 增加项目
                    words.add_item(item)
                else :
                    # 获得项目
                    item = words[content]
                    # 检查数值
                    if item.gamma < gamma : item.gamma = gamma
        # 结束
        pb.end(f"DBVectorization.save_gammas : finished building matrix !")
        # 保存
        words.save(file_name)
        # 结束
        print(f"DBVectorization.save_gammas : file({file_name}) was saved !")

# 测试代码
def main() :

    # 生成对象
    sqv = SQVectorization(32)

    # 选项
    # 加载数据
    if sqv.load_vectors("..\\..\\json\\vectors.json", False) <= 0 :
        # 打印信息
        print("DBVectorization.main : fail to load vectors.json !")
        return
    """
    # 加载数据
    if sqv.load_vectors("..\\..\\json\\cores.json", False) <= 0 :
        # 打印信息
        print("DBVectorization.main : fail to load cores.json !")
        return
    """
    # 打印信息
    print("DBVectorization.main : successfully loaded !")
    # 获得求解器
    solution = sqv.get_solution("cupy.l2")
    # 检查结果
    if solution is None :
        # 打印信息
        print("DBVectorization.main : fail to get solution !")
        return
    # 启动
    solution.start()
    # 打印信息
    print("DBVectorization.main : successfully start solving !")
    # 等待输入
    input()
    # 结束线程
    solution.stop()
    # 打印信息
    print("DBVectorization.main : successfully stopped solving !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("DBVectorization.main :__main__ : ", str(e))
        print("DBVectorization.main :__main__ : unexpected exit !")