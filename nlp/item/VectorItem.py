# -*- coding: utf-8 -*-
import math
import random

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
        # 矩阵
        # 只有这样定义二维数组才能防止数的粘连
        # 即，数组中有数值之间形成了完全绑定关系
        self.__matrix = [[]] * 2
        self.__matrix[0] = [1.0] * dimension
        self.__matrix[1] = [1.0] * dimension

    @property
    def norm(self) :
        # 模长
        norm = 0.0
        # 循环处理
        for k in range(len(self.__matrix[0])) :
            norm += math.pow(self.__matrix[0][k], 2.0)
        for k in range(len(self.__matrix[1])) :
            norm += math.pow(self.__matrix[1][k], 2.0)
        # 返回结果
        return math.sqrt(norm)

    @property
    def sqa(self) :
        # 模长
        value = 0.0
        # 循环处理
        for k in range(len(self.__matrix[0])) :
            value += math.pow(self.__matrix[0][k], 2.0)
        # 返回结果
        return value

    @property
    def sqb(self) :
        # 模长
        value = 0.0
        # 循环处理
        for k in range(len(self.__matrix[1])) :
            value += math.pow(self.__matrix[1][k], 2.0)
        # 返回结果
        return value

    @property
    def matrix(self) :
        # 返回结果
        return self.__matrix

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "content" : self.content,
                "index" : self.index,
                "matrix" : self.__matrix,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.index = value["index"]
        self.count = value["count"]
        self.content = value["content"]
        self.__matrix = value["matrix"]
        # 检查长度
        #assert self.length == value["length"]

    def random(self) :
        # 循环处理
        for k in range(len(self.__matrix[0])) :
            # 初始化随机值
            self.__matrix[0][k] = \
                1.0 - 2.0 * random.random()
        for k in range(len(self.__matrix[1])) :
            self.__matrix[1][k] = \
                1.0 - 2.0 * random.random()

    def normalize(self) :
        # 获得模长
        scale = 1.0 / self.norm
        # 循环处理
        for k in range(len(self.__matrix[0])) :
            self.__matrix[0][k] *= scale
        for k in range(len(self.__matrix[1])) :
            self.__matrix[1][k] *= scale

    def dump(self, dump_matrix = True):
        # 打印信息
        print("VectorItem.dump : show properties !")
        print(f"\tindex = {self.index}")
        print(f"\tcount = {self.count}")
        print(f"\tlength = {self.length}")
        print(f"\tcontent = \"{self.content}\"")
        if dump_matrix : print("matrix : "); print(self.__matrix)

    @staticmethod
    def get_gamma(v1, v2, dimension) :
        # 检查参数
        assert len(v1.__matrix[0]) == dimension
        assert len(v2.__matrix[1]) == dimension
        # 结果
        result = 0.0
        # 循环处理
        for k in range(dimension) :
            # 求点积
            result += v1.__matrix[0][k] * v2.__matrix[1][k] # Ai·Bj
        # 返回结果
        return result