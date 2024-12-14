# -*- coding: utf-8 -*-
import numpy
import numba

from numba import jit
from numba import cuda

from widget.ProgressBar import *

from nlp.alg.Solution import *

# 归一化
@jit
def _normalized(matrix) :
    # 计算模长
    #norm = numpy.linalg.norm(matrix, axis = 1)
    # 兼容性写法
    norm = numpy.square(matrix)
    norm = numpy.sqrt(numpy.sum(norm, axis = 1))
    # 返回结果
    return (matrix.T * numpy.reciprocal(norm)).T

# 生成随机矩阵
@jit
def _init_random_matrix(size, dimension) :
    # 返回结果
    # 该初始化数据更有利于收敛
    return 1.0 - 2.0 * numpy.random.random((size, dimension))
    #return _normalized(1.0 - 2.0 * numpy.random.random((size, dimension)))

class JitSolution(Solution) :
    # 初始化
    def __init__(self, w2v) :
        # 调用父类初始化
        super().__init__(w2v)

    # 从Vector拷贝至ais和bjs矩阵
    def _copy_to(self, ais = None, bjs = None) :
        # 检查参数
        assert ais is not None
        assert bjs is not None
        # 进度条
        pb = ProgressBar(self._size)
        # 开始
        pb.begin(f"JitSolution.__copy_to : copy square[{self._size}] matrix !")
        # 循环处理
        for item in self._w2v.vectors() :
            # 进度条
            pb.increase()
            # 获得索引值
            index = item.index
            # 拷贝转换矩阵
            ais[index] = numpy.asarray(item.matrix[0])  # Ai
            bjs[index] = numpy.asarray(item.matrix[1])  # Bj
        # 结束
        pb.end(f"JitSolution.__copy_to : square[{self._size}] matrix copied !")

    # 从ais和bjs矩阵拷贝至Vector
    def _copy_from(self, ais = None, bjs = None) :
        # 检查参数
        assert ais is not None
        assert bjs is not None
        # 进度条
        pb = ProgressBar(self._size)
        # 开始
        pb.begin(f"JitSolution._copy_from : copy square[{self._size}] matrix !")
        # 循环处理
        for item in self._w2v.vectors() :
            # 进度条
            pb.increase()
            # 获得索引值
            index = item.index
            # 拷贝转换矩阵
            item.matrix[0] = ais[index].tolist() # Ai
            item.matrix[1] = bjs[index].tolist() # Bj
        # 结束
        pb.end(f"JitSolution._copy_from : square[{self._size}] matrix copied !")

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
            print(f"JitSolution._run : initialize ais !")
            # 创建矢量矩阵
            ais = numpy.zeros((self._size, self._dimension))
            # 打印信息
            print(f"JitSolution._run : initialize bjs !")
            # 创建矢量矩阵
            bjs = numpy.zeros((self._size, self._dimension))
            # 拷贝数据
            # 由存储对象拷贝至矢量组
            self._copy_to(ais, bjs)
        else :
            # 初始化ais和bjs
            # 打印信息
            print(f"JitSolution._run : initialize random ais !")
            # 生成ais
            ais = _init_random_matrix(self._size, self._dimension)
            # 打印信息
            print(f"JitSolution._run : initialize random bjs !")
            # 生成bjs
            bjs = _init_random_matrix(self._size, self._dimension)
        # 打印信息
        print(f"JitSolution._run : square[{self._size}] matrix initialized !")

        # 清理标记
        self._break_loop = False
        # 获得相关系数
        gammas = self._get_gammas()
        # 执行解方程过程
        result = self._solving(numpy.asarray(gammas), ais, bjs)
        # 检查结果
        if result > self._error :
            # 打印信息
            print(f"JitSolution._run : fail to solve !")
        else :
            # 打印信息
            print(f"JitSolution._run : successfully done !")

        # 将数据拷贝回至矢量组
        self._copy_from(ais, bjs)
        # 打印信息
        print(f"JitSolution._run : result[{self._size}] copied !")
