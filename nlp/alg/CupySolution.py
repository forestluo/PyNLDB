# -*- coding: utf-8 -*-
import cupy
import numpy

from widget.ProgressBar import *

from nlp.alg.Solution import *

# 归一化
def _normalized(matrix) :
    # 计算模长
    norm = cupy.linalg.norm(matrix, axis = 1)
    # 返回结果
    return (matrix.T * cupy.reciprocal(norm)).T

# 生成随机矩阵
def _init_random_matrix(size, dimension) :
    # 返回结果
    # 该初始化数据更有利于收敛
    return 1.0 - 2.0 * cupy.random.random((size, dimension))
    #return _normalized(1.0 - 2.0 * cupy.random.random((size, dimension)))

class CupySolution(Solution) :
    # 初始化
    def __init__(self, w2v) :
        # 调用父类初始化
        super().__init__(w2v)

    # 从Vector拷贝至ais和bjs矩阵
    def __copy_to(self, ais, bjs) :
        # 进度条
        pb = ProgressBar(self._size)
        # 开始
        pb.begin(f"CupySolution.__copy_to : copy matrix[{self._size}] !")
        # 循环处理
        for item in self._w2v.vectors() :
            # 进度条
            pb.increase()
            # 获得索引值
            index = item.index
            # 拷贝转换矩阵
            ais[index] = cupy.asarray(item.matrix[0])  # Ai
            bjs[index] = cupy.asarray(item.matrix[1])  # Bj
        # 结束
        pb.end(f"CupySolution.__copy_to : matrix[{self._size}] copied !")

    # 从ais和bjs矩阵拷贝至Vector
    def __copy_from(self, ais, bjs) :
        # 进度条
        pb = ProgressBar(self._size)
        # 开始
        pb.begin(f"CupySolution.__copy_from : copy matrix[{self._size}] !")
        # 循环处理
        for item in self._w2v.vectors() :
            # 进度条
            pb.increase()
            # 获得索引值
            index = item.index
            # 拷贝转换矩阵
            item.matrix[0] = cupy.asnumpy(ais[index]).tolist() # Ai
            item.matrix[1] = cupy.asnumpy(bjs[index]).tolist() # Bj
        # 结束
        pb.end(f"CupySolution.__copy_from : matrix[{self._size}] copied !")

    # 必须重载
    def _solving(self, gammas, ais, bjs) :
        # 打印信息
        self.dump()
        # 返回结果
        return 0.0

    # 执行函数
    def _run(self) :
        # 矩阵尺寸
        self._size = self._w2v.vsize
        # 矩阵维度
        self._dimension = self._w2v.dimension
        # 检查标记位
        if self._w2v.copy_data :
            # 打印信息
            print(f"CupySolution._run : initialize ais !")
            # 创建矢量矩阵
            ais = cupy.zeros((self._size, self._dimension))
            # 打印信息
            print(f"CupySolution._run : initialize bjs !")
            # 创建矢量矩阵
            bjs = cupy.zeros((self._size, self._dimension))
            # 拷贝数据
            # 由存储对象拷贝至矢量组
            self.__copy_to(ais, bjs)
        else :
            # 初始化ais和bjs
            # 打印信息
            print(f"CupySolution._run : initialize random ais !")
            # 生成ais
            ais = _init_random_matrix(self._size, self._dimension)
            # 打印信息
            print(f"CupySolution._run : initialize random bjs !")
            # 生成bjs
            bjs = _init_random_matrix(self._size, self._dimension)
        # 打印信息
        print(f"CupySolution._run : square[{self._size}] matrix initialized !")

        # 清理标记
        self._break_loop = False
        # 获得相关系数
        gammas = self._get_gammas()
        # 执行解方程过程
        result = self._solving(cupy.asarray(gammas), ais, bjs)
        # 检查结果
        if result > self._error :
            # 打印信息
            print(f"CupySolution._run : fail to solve !")
        else :
            # 打印信息
            print(f"CupySolution._run : successfully done !")

        # 将数据拷贝回至矢量组
        self.__copy_from(ais, bjs)
        # 打印信息
        print(f"CupySolution._run : result[{self._size}] copied !")
