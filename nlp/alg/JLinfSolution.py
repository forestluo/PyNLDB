# -*- coding: utf-8 -*-
import time
import numpy
import numba

from numba import jit

from nlp.alg.JitSolution import *

# 获得最大误差
@jit
def _get_major_delta(delta) :
    # 返回结果
    return numpy.sum(numpy.square(delta))

@jit
def _get_minor_delta(delta) :
    # 返回结果
    return numpy.sum(numpy.abs(delta))

# 获得误差矩阵
@jit
def _get_delta_matrix(gammas, ais, bjs) :
    # 返回结果
    # return gammas[0] - numpy.dot(ais, bjs.T)
    return numpy.multiply(gammas[1], gammas[0] - numpy.dot(ais, bjs.T))

@jit
def _get_next_step(size, ais, bjs, delta, positions) :
    # 生成掩码矩阵
    _mask = numpy.zeros((size, size))
    # 设置掩码矩阵
    for i in range(len(positions)):
        # 必须强制转整数
        # 否则矩阵值会不变！！！
        row = int(positions[i][0])
        col = int(positions[i][1])
        # 设置掩码值
        _mask[row][col] = 1.0
    # 屏蔽其他数据
    delta = numpy.multiply(delta, _mask)

    # 求各个分量的平方和（相当于模长的平方）
    _ais = numpy.sum(numpy.square(ais), axis = 1)
    # 与numba兼容的写法
    _ais = _ais.repeat(size).reshape((-1, size))

    # 求各个分量的平方和（相当于模长的平方）
    _bjs = numpy.sum(numpy.square(bjs), axis = 1)
    # 与numba兼容的写法
    _bjs = _bjs.repeat(size).reshape((-1, size)).T

    # 计算系数矩阵
    _w = numpy.multiply(delta, numpy.reciprocal(_bjs + _ais))
    # 计算误差分量
    _dai = numpy.dot(_w, bjs)
    _dbj = numpy.dot(_w.T, ais)
    # 返回结果
    return _dai, _dbj

@jit
def _get_max_positions(size, delta, length, error) :
    # 检查参数
    if length < 0 : length = 0
    elif length >= size : length = size - 1
    # 位置记录
    positions = []
    # 获得误差的绝对值
    abs_delta = numpy.abs(delta)

    # 查找最大值的位置
    pos = numpy.argmax(abs_delta)
    # 获得索引
    row = pos // size
    col = pos - row * size
    max_delta = abs_delta[row][col]
    # 记录位置
    positions.append([row, col, max_delta])

    # 检查结果
    if max_delta > error :
        # 循环处理
        for i in range(length) :
            # 查找最大值的位置
            pos = numpy.argmax(abs_delta)
            # 获得索引
            row = pos // size
            col = pos - row * size
            value = abs_delta[row][col]
            # 检查结果
            if value <= error : break
            # 记录位置
            positions.append([row, col, value])
            # 划去该位置的行列数据
            abs_delta[row][:] = 0.0; abs_delta[:][col] = 0.0
    # 返回结果
    return positions

class JLinfSolution(JitSolution) :
    # 解算方法
    def _solving(self, gammas, ais, bjs) :
        # 调用父类函数
        super()._solving(gammas, ais, bjs)
        # 打印信息
        print(f"JLinfSolution._solving : algorithm(\"L∞\") !")

        # 搜索长度
        length = 0
        # 循环计数
        i = 0; j = 0
        # 最大行和范数
        last_delta = numpy.inf
        # 循环直至误差符合要求，或者收敛至最小误差
        while i < self._max_loop :
            # 检查标志位
            if self._break_loop : break

            # 计数器加一
            i += 1; j += 1
            # 开始计时
            start = time.perf_counter()

            # 获得计算值
            delta = _get_delta_matrix(gammas, ais, bjs)
            # 获得一系列误差最大值位置记录
            positions = _get_max_positions(self._size, delta, length, self._error)
            # 检查参数
            assert len(positions) >= 1
            # 先获得最大误差值
            max_delta = positions[0][2]
            # 检查参数
            # numba会强制类型，数组均为浮点型，因此需要强制转换为整数类型
            positions = numpy.array(positions).astype(numpy.int32)
            # 转换后再取值
            row = int(positions[0][0])
            col = int(positions[0][1])
            # 检查结果
            if max_delta <= self._error :
                # 设置数值，并中断循环
                last_delta = max_delta; break
            # 临时记录
            _last_delta = last_delta
            # 检查结果
            if last_delta < max_delta :
                # 呈上升趋势
                length = 0
            else :
                # 呈下降趋势
                i = 0; length += 1
                # 保存上次误差
                last_delta = max_delta
                # 检查结果
                if length > self._size // 4 : length = self._size // 4
            # 通过误差计算步长，并移至下一个步骤
            _dai, _dbj = _get_next_step(self._size, ais, bjs, delta, positions)
            # 注意：分成两个步骤计算
            ais += _dai; bjs += _dbj

            # 计时结束
            end = time.perf_counter()
            # 间隔打印
            if numpy.remainder(j, self._max_loop) == 0 :
                # 获得时间
                timespan = int((end - start) * 1000)
                # 打印信息
                print(f"JLinfSolution._solving : show result !")
                print(f"\tloop[{j},{i},{length}] = {timespan} ms")
                print(f"\tMax(|Δγᵢⱼ|) = ({row},{col},{max_delta})")
                if j > 1 : print(f"\tΔMax(|Δγᵢⱼ|) = {_last_delta - max_delta}")
                print(f"\t\tΣ(|Δγᵢⱼ|) = {_get_minor_delta(delta)}")
                print(f"\t\tΣ(|Δγᵢⱼ|²) = {_get_major_delta(delta)}")
        # 返回结果
        return last_delta