# -*- coding: utf-8 -*-
import cupy
import numpy

from nlp.item.ContentItem import *

class VectorItem(ContentItem) :
    # 初始化对象
    def __init__(self, dimension, content = None, count = 1) :
        # 调用父类初始化函数
        super().__init__(content, count)
        # 检查参数
        assert dimension >= 2
        # 索引
        self.index = -1
        # 增量
        self.__delta = numpy.zeros((2, dimension))
        # 矩阵
        self.__matrix = numpy.zeros((2, dimension))

    @property
    def delta(self) :
        # 返回结果
        return self.__delta

    @property
    def matrix(self) :
        # 返回结果
        return self.__matrix

    # 是否无用
    def is_useless(self) :
        # 调用父类函数
        if super().is_useless() :
            # 返回结果
            return True
        # 获得矩阵最大值
        value = self.__matrix.max()
        # 检查结果
        return not (1.0e-5 < value < 10)

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "content" : self.content,
                "index" : self.index,
                "matrix" : self.__matrix.tolist(),
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.index = value["index"]
        self.count = value["count"]
        self.content = value["content"]
        # 检查长度
        #assert self.length == value["length"]
        # 设置举着
        self.__matrix = numpy.array(value["matrix"])

    def dump(self, dump_matrix = True, dump_delta = True):
        # 打印信息
        print("VectorItem.dump : show properties !")
        print(f"\tindex = {self.index}")
        print(f"\tcount = {self.count}")
        print(f"\tlength = {self.length}")
        print(f"\tcontent = \"{self.content}\"")
        if dump_matrix : print("matrix : "); print(self.__matrix)
        if dump_delta :   print("delta : ");  print(self.__delta)

    # 遍历函数
    # 重新计算无效的数据
    @staticmethod
    def reset_useless(t, p = None) :
        # 检查数据
        if not t.is_useless() : return
        # 设置初始值
        t.__delta = \
            numpy.zeros(t.__delta.shape)
        # 设置矩阵
        t.__matrix = 1 - 2 * \
            numpy.random.random(t.__matrix.shape)

    # 求单位向量
    @staticmethod
    def normalize(t, p = None) :
        # 计算结果
        t.__matrix = \
            get_normalized(t.__matrix)

    # 遍历函数
    # 缩放误差
    @staticmethod
    def mul_delta(t, value) :
        # 矩阵加和
        t.__delta = \
            numpy.dot(value, t.__delta)

    # 遍历函数
    # 加和误差
    @staticmethod
    def add_delta(t, delta = None) :
        # 检查参数
        if delta is not None :
            # 矩阵加和
            t.__matrix += delta
        else :
            # 矩阵加和
            t.__matrix += t.__delta

    # 遍历函数
    # 寻找行和范数
    @staticmethod
    def max_delta(t, max_delta) :
        # 返回结果
        # 1: 列和范数
        # inf : 行和范数
        value = numpy.linalg.\
            norm(t.__delta, numpy.inf)
        # 检查结果
        if value > max_delta[0] : max_delta[0] = value

    # 遍历函数
    # 初始化误差矩阵
    # 将误差值设置为零
    @staticmethod
    def init_delta(t, delta = None) :
        # 检查参数
        if delta is not None :
            # 设置矩阵
            # 数组分别赋值
            t.__delta[0] = delta[0][t.index] # dAi
            t.__delta[1] = delta[1][t.index] # dBi
        else :
            # 设置初始值
            t.__delta = numpy.zeros(t.__delta.shape)

    # 遍历函数
    # 初始化矢量矩阵
    # 给矩阵赋予随机数值
    @staticmethod
    def init_matrix(t, matrix = None) :
        # 检查参数
        if matrix is None :
            # 设置矩阵
            t.__matrix = 1 - 2 * \
                numpy.random.random(t.__matrix.shape)
            return
        # 检查类型
        if isinstance(matrix[0], numpy.ndarray) :
            t.__matrix[0] = matrix[0][t.index] # Ai
        elif isinstance(matrix[0], cupy.ndarray) :
            t.__matrix[0] = cupy.asnumpy(matrix[0][t.index]) # Ai
        else :
            # 数值拷贝
            for k in range(matrix[0].shape[1]) :
                t.__matrix[0][k] = matrix[0][t.index][k]  # Ai
        # 检查类型
        if isinstance(matrix[1], numpy.ndarray) :
            t.__matrix[1] = matrix[1][t.index] # Bj
        elif isinstance(matrix[1], cupy.ndarray) :
            t.__matrix[1] = cupy.asnumpy(matrix[1][t.index]) # Bj
        else :
            # 数值拷贝
            for k in range(matrix[1].shape[1]) :
                t.__matrix[1][k] = matrix[1][t.index][k]  # Bj

    # 求相关系数
    # 按照公式正常处置
    @staticmethod
    def cal_gamma(t1, t2) :
        # Ti = (Ai, Bi)'
        # Tj = (Aj, Bj)'
        # G = [1, 0].(Ti.Tj').[0, 1]'
        # 获得矩阵（2x2）
        # Ti * Tj = Ti.Tj' = (Ai, Bi)'.(Aj, Bj)
        # | Ai.Aj Ai.Bj |
        # | Bi.Aj Bi.Bj |
        result = numpy.matmul(t1.__matrix, t2.__matrix.T)
        # 正常处置
        result = numpy.matmul(numpy.array([[1, 0]]), result)
        result = numpy.matmul(result, numpy.array([[0, 1]]).T)
        # 返回结果
        return result[0][0]

    # 按照公式正常处置
    @staticmethod
    def cal_delta(t1, t2, delta) :
        # Ti = (Ai, Bi)'
        # Tj = (Aj, Bj)'
        # 计算模长
        _Bj = numpy.dot(t2.__matrix[1], t2.__matrix[1]) # |Bj| * |Bj|
        _Ai = numpy.dot(t1.__matrix[0], t1.__matrix[0]) # |Ai| * |Ai|
        # 计算数据
        value = delta / (_Bj + _Ai)
        # 计算delta
        # | 0, value | | Aj |   | 0    , 0 | | Ai |
        # | 0    , 0 |.| Bj | , | value, 0 |.| Bi |
        return numpy.matmul(numpy.array([[value, 0],[0, 0]]), t2.__matrix), \
                    numpy.matmul(numpy.array([[0, 0],[0, value]]), t1.__matrix)
