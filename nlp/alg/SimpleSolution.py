# -*- coding: utf-8 -*-
import math
import random

from widget.ProgressBar import *

from nlp.alg.Solution import *
from nlp.item.VectorItem import *

class SimpleSolution(Solution) :
    # 初始化
    def __init__(self, vz) :
        # 调用父类初始化
        super().__init__(vz)

    # 新建误差矩阵
    def __new_delta(self) :
        # 创建矢量矩阵
        # 只有这样定义二维数组才能防止“粘连”
        # 即，数组中有数值之间形成了完全绑定关系
        return [[[0.0
            for _ in range(self._dimension)]
            for _ in range(2)] for _ in range(self._size)]

    def _solving(self) :
        # 打印信息
        self.dump()
        # 重新建立索引
        self._vz.index_vectors()
        # 打印信息
        print(f"SimpleSolution._solving : index of vectors rebuilt !")

        # 循环计数
        i = 0; j = 0
        # 最大行和范数
        last_delta = math.inf
        # 循环处理
        while i < self._max_loop :
            # 检查标记
            if self._break_loop : break

            # 获得误差矩阵
            delta = self.__new_delta()
            # 计数器加一
            i += 1; j += 1
            # 运算结果
            max_delta = self.__solving(delta)
            # 打印信息
            print(f"SimpleSolution._solving : ΔGamma[{i},{j}] = {max_delta} !")
            # 检查结果
            if j == 1 :
                # 设置误差
                last_delta = max_delta
            # 检查趋势
            elif last_delta > max_delta :
                # 呈下降趋势
                i = 0; last_delta = max_delta
            # 检查结果
            if max_delta <= self._error : break
            # 比例
            scale = 1.0 / float(self._size)
            # 求均值
            for index in range(self._size) :
                for k in range(self._dimension) :
                    # 求平均值
                    delta[index][0][k] *= scale
                    delta[index][1][k] *= scale
            # 叠加结果
            for v in self._vz.vectors() :
                for k in range(self._dimension) :
                    v.matrix[0][k] += delta[v.index][0][k]
                    v.matrix[1][k] += delta[v.index][1][k]
        # 返回结果
        return last_delta

    # 必须重载
    def __solving(self, delta) :
        # 进度条
        pb = ProgressBar(self._vz.wsize)
        # 开始
        #pb.begin(f"SimpleSolution._solving : begin processing !")
        # 最大误差
        max_delta = 0.0
        # 循环处理
        for w in self._vz.words() :
            # 检查标志位
            if self._break_loop : break

            # 增加计数
            pb.increase()
            # 检查参数
            assert w.length == 2

            # 获得前置
            c1 = w.content[:1]
            # 查询矢量
            v1 = self._vz.vector(c1) # Ai
            # 检查结果
            if v1 is None : continue

            # 获得后置
            c2 = w.content[-1]
            # 查询矢量
            v2 = self._vz.vector(c2) # Bj
            # 检查结果
            if v2 is None : continue

            # 数值
            _delta = w.gamma - \
                VectorItem.get_gamma(v1, v2, self._dimension) # Ai·Bj
            # 绝对值
            abs_delta = math.fabs(_delta)
            # 检查结果
            if abs_delta > max_delta :
                # 设置误差记录
                max_delta = abs_delta
            # 计算数据
            # value = Δγ / (Ai² + Bj²)
            value = _delta / (v1.sqa + v2.sqb)
            # 循环处理
            for k in range(self._dimension) :
                # 计算分量（快捷处置）加和误差分量
                # ΔAi = value·Bj
                delta[v1.index][0][k] += value * v2.matrix[1][k] # Bj
                # 计算分量（快捷处置）加和误差分量
                # ΔBj = value·Ai
                delta[v2.index][1][k] += value * v1.matrix[0][k] # Ai
        # 打印信息
        pb.end()
        #pb.end(f"SimpleSolution._solving : {total} relations(s) processed !")
        # 返回结果
        return max_delta

    # 执行函数
    def _run(self) :
        # 矩阵尺寸
        self._size = self._vz.vsize
        # 矩阵维度
        self._dimension = self._vz.dimension
        # 检查标记位
        if not self._vz.copy_data :
            # 打印信息
            print(f"SimpleSolution._run : initialize matrix !")
            # 进度条
            pb = ProgressBar(self._size)
            # 开始
            pb.begin(f"SimpleSolution._run : set random values !")
            # 循环
            for v in self._vz.vectors() :
                # 进度条
                pb.increase()
                # 随机赋值
                v.random()
                # 不要进行归一化处理
                # 否则，迭代发散的可能性很高
            # 结束
            pb.end(f"SimpleSolution._run : random values were set !")
        # 打印信息
        print(f"SimpleSolution._run : matrix[{self._size}] initialized !")

        # 清理标记
        self._break_loop = False
        # 执行解方程过程
        result = self._solving()
        # 检查结果
        if result > self._error :
            # 打印信息
            print(f"SimpleSolution._run : fail to solve !")
        else :
            # 打印信息
            print(f"SimpleSolution._run : successfully done !")
