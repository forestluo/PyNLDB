# -*- coding: utf-8 -*-
import numpy

from widget.ProgressBar import *

from nlp.alg.Solution import *

# 归一化
def _normalized(matrix) :
    # 计算模长
    norm = numpy.linalg.norm(matrix, axis = 1)
    # 返回结果
    return (matrix.T * numpy.reciprocal(norm)).T

# 生成随机矩阵
def _init_random_matrix(size, dimension) :
    # 返回结果
    # 该初始化结果更有利于收敛
    return 1.0 - 2.0 * numpy.random.random((size, dimension))
    #return _normalized(1.0 - 2.0 * numpy.random.random((size, dimension)))

class NumpySolution(Solution) :
    # 初始化
    def __init__(self, w2v) :
        # 调用父类初始化
        super().__init__()
        # 设置对象
        self._w2v = w2v
        # 误差
        self._error = 1.0e-5
        # 循环次数
        self._max_loop = 100
        # 矩阵尺寸
        self._size = w2v.vsize
        # 矩阵维度
        self._dimension = w2v.dimension

    # 获得标准数据
    def __get_gammas(self) :
        # 重建索引
        self._w2v.index_vectors()
        # 结束
        print(f"NumpySolution.__get_gammas : finished reindexing vectors !")

        # 生成数据
        gammas = numpy.zeros((2, self._size, self._size))
        # 进度条
        pb = ProgressBar(self._w2v.wsize)
        # 开始
        pb.begin(f"NumpySolution.__get_gammas : building matrix !")
        # 初始化相关系数
        for item in self._w2v.words() :
            # 进度条
            pb.increase()

            # 获得内容
            f = item.count
            c = item.content
            # 检查数据
            assert len(c) == 2
            # 检查数值
            if f <= 0 : continue

            # 获得单词
            c1 = c[:1]
            # 检查数据
            v1 = self._w2v.vector(c1)
            # 检查结果
            if v1 is None :
                continue
            # 获得索引值
            else : i = v1.index

            # 获得单词
            c2 = c[-1]
            # 检查数据
            v2 = self._w2v.vector(c2)
            # 检查结果
            if v2 is None :
                continue
            # 获得索引值
            else : j = v2.index

            # 设置数值
            gammas[0][i][j] = item.gamma
            # 检查结果
            if item.gamma >= self._error : gammas[1][i][j] = 1.0
        # 结束
        pb.end(f"NumpySolution.__get_gammas : finished building matrix !")
        # 返回结果
        return gammas

    # 从Vector拷贝至ais和bjs矩阵
    def __copy_to(self, ais, bjs) :
        # 进度条
        pb = ProgressBar(self._size)
        # 开始
        pb.begin(f"NumpySolution.__copy_to : copy matrix[{self._size}] !")
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
        pb.end(f"NumpySolution.__copy_to : matrix[{self._size}] copied !")

    # 从ais和bjs矩阵拷贝至Vector
    def __copy_from(self, ais, bjs) :
        # 进度条
        pb = ProgressBar(self._size)
        # 开始
        pb.begin(f"NumpySolution.__copy_from : copy matrix[{self._size}] !")
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
        pb.end(f"NumpySolution.__copy_from : matrix[{self._size}] copied !")

    # 必须重载
    def _solving(self, gammas, ais, bjs) :
        # 打印信息
        print("NumpySolution._solving : dump properties !")
        print(f"\terror = {self._error}")
        print(f"\tmax_loop = {self._max_loop}")
        print(f"\tvsize = {self._w2v.vsize}")
        print(f"\twsize = {self._w2v.wsize}")
        print(f"\tdimension = {self._w2v.dimension}")
        print(f"\tmin_count = {self._w2v.min_count}")
        print(f"\tcopy_data = {self._w2v.copy_data}")
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
            print(f"NumpySolution._run : initialize ais !")
            # 创建矢量矩阵
            ais = numpy.zeros((self._size, self._dimension))
            # 打印信息
            print(f"NumpySolution._run : initialize bjs !")
            # 创建矢量矩阵
            bjs = numpy.zeros((self._size, self._dimension))
            # 拷贝数据
            # 由存储对象拷贝至矢量组
            self.__copy_to(ais, bjs)
        else :
            # 初始化ais和bjs
            # 打印信息
            print(f"NumpySolution._run : initialize random ais !")
            # 生成ais
            ais = _init_random_matrix(self._size, self._dimension)
            # 打印信息
            print(f"NumpySolution._run : initialize random bjs !")
            # 生成bjs
            bjs = _init_random_matrix(self._size, self._dimension)
        # 打印信息
        print(f"NumpySolution._run : matrix[{self._size}] initialized !")

        # 清理标记
        self._break_loop = False
        # 获得相关系数矩阵
        gammas = self.__get_gammas()
        # 执行解方程过程
        result = self._solving(gammas, ais, bjs)
        # 检查结果
        if result > self._error :
            # 打印信息
            print(f"NumpySolution._run : fail to solve !")
        else :
            # 打印信息
            print(f"NumpySolution._run : successfully done !")

        # 将数据拷贝回至矢量组
        self.__copy_from(ais, bjs)
        # 打印信息
        print(f"NumpySolution._run : result[{self._size}] copied !")
