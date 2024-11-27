# -*- coding: utf-8 -*-

import math
import cupy
import numpy
import numba
from numba import jit
from numba import cuda


# 归一化处理
#@jit (axis 选项不支持)
def get_normalized(matrix) :
    # 计算模长
    norm = numpy.linalg.norm(matrix, axis = 1)
    # 返回结果
    return (matrix.T * numpy.reciprocal(norm)).T

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#
# Jit加速函数
#
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# 生成随机数组
@jit
def get_random_matrix(n, dimension) :
    # 返回结果
    return 1.0 - 2.0 * \
    numpy.random.random((n, dimension))

@jit
def get_delta_matrix(gammas, ais, bjs) :
    # 返回结果
    return gammas - numpy.dot(ais, bjs.T)

@jit
def get_masked_delta(n, delta, positions) :
    # 生成掩码矩阵
    _mask = numpy.zeros((n, n))
    # 设置掩码矩阵
    for i in range(len(positions)) :
        # 已经在函数外完成转换
        row = positions[i][0]
        col = positions[i][1]
        # 设置掩码值
        _mask[row][col] = 1.0
    # 屏蔽其他数据
    return numpy.multiply(delta, _mask)

@jit
def get_next_step(n, ais, bjs, delta, positions) :
    # 生成掩码矩阵
    _mask = numpy.zeros((n, n))
    # 设置掩码矩阵
    for i in range(len(positions)):
        # 已经在函数外完成转换
        row = int(positions[i][0])
        col = int(positions[i][1])
        # 设置掩码值
        _mask[row][col] = 1.0
    # 屏蔽其他数据
    delta = numpy.multiply(delta, _mask)

    # 求各个分量的平方和（相当于模长的平方）
    _ais = numpy.sum(numpy.square(ais), axis = 1)
    # 与numba兼容的写法
    _ais = _ais.repeat(n).reshape((-1, n))

    # 求各个分量的平方和（相当于模长的平方）
    _bjs = numpy.sum(numpy.square(bjs), axis = 1)
    # 与numba兼容的写法
    _bjs = _bjs.repeat(n).reshape((-1, n)).T

    # 计算系数矩阵
    _w = numpy.multiply(delta, numpy.reciprocal(_bjs + _ais))
    # 计算误差分量
    _dai = numpy.dot(_w, bjs)
    _dbj = numpy.dot(_w.T, ais)
    # 返回结果
    return _dai, _dbj

# 获得掩码矩阵
@jit
def get_max_positions(n, delta, length) :
    # 检查参数
    if length < 0 : length = 0
    elif length >= n : length = n - 1
    # 位置记录
    positions = []
    # 获得误差的绝对值
    abs_delta = numpy.abs(delta)

    # 查找最大值的位置
    pos = numpy.argmax(abs_delta)
    # 获得索引
    row = pos // n
    col = pos - row * n
    max_delta = abs_delta[row][col]
    # 记录位置
    positions.append([row, col, max_delta])

    # 检查结果
    if max_delta > 1.0e-5 :
        # 循环处理
        for i in range(length) :
            # 查找最大值的位置
            pos = numpy.argmax(abs_delta)
            # 获得索引
            row = pos // n
            col = pos - row * n
            value = abs_delta[row][col]
            # 检查结果
            if value <= 1.0e-5 : break
            # 记录位置
            positions.append([row, col, value])
            # 划去该位置的行列数据
            abs_delta[row][:] = 0.0; abs_delta[:][col] = 0.0
    # 返回结果
    return positions

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#
# Cuda加速函数（内存属于不同区域）
#
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def cupy_normalized(matrix) :
    # 计算模长
    norm = cupy.linalg.norm(matrix, axis = 1)
    # 返回结果
    return (matrix.T * cupy.reciprocal(norm)).T

# 生成随机数组
def cupy_random_matrix(n, dimension) :
    # 返回结果
    return 1.0 - 2.0 * \
        cupy.random.random((n, dimension))

def cupy_delta_matrix(gammas, ais, bjs) :
    # 返回结果
    return gammas - cupy.dot(ais, bjs.T)

def cupy_next_step(n, ais, bjs, delta, positions) :
    # 生成掩码矩阵
    _mask = cupy.zeros((n, n))
    # 设置掩码矩阵
    for i in range(len(positions)):
        # 必须强制转整数
        # 否则矩阵值会不变！！！
        row = int(positions[i][0])
        col = int(positions[i][1])
        # 设置掩码值
        _mask[row][col] = 1.0
    # 屏蔽其他数据
    delta = cupy.multiply(delta, _mask)

    # 求各个分量的平方和（相当于模长的平方）
    _ais = cupy.sum(cupy.square(ais), axis = 1)
    # 与numba兼容的写法
    _ais = _ais.repeat(n).reshape((-1, n))

    # 求各个分量的平方和（相当于模长的平方）
    _bjs = cupy.sum(cupy.square(bjs), axis = 1)
    # 与numba兼容的写法
    _bjs = _bjs.repeat(n).reshape((-1, n)).T

    # 计算系数矩阵
    _w = cupy.multiply(delta, cupy.reciprocal(_bjs + _ais))
    # 计算误差分量
    _dai = cupy.dot(_w, bjs)
    _dbj = cupy.dot(_w.T, ais)
    # 返回结果
    return _dai, _dbj

def cupy_max_positions(n, delta, length) :
    # 检查参数
    if length < 0 : length = 0
    elif length >= n : length = n - 1
    # 位置记录
    positions = []
    # 获得误差的绝对值
    abs_delta = cupy.abs(delta)

    # 查找最大值的位置
    pos = cupy.argmax(abs_delta)
    # 获得索引
    row = pos // n
    col = pos - row * n
    max_delta = abs_delta[row][col]
    # 记录位置
    positions.append([row, col, max_delta])

    # 检查结果
    if max_delta > 1.0e-5 :
        # 循环处理
        for i in range(length) :
            # 查找最大值的位置
            pos = cupy.argmax(abs_delta)
            # 获得索引
            row = pos // n
            col = pos - row * n
            value = abs_delta[row][col]
            # 检查结果
            if value <= 1.0e-5 : break
            # 记录位置
            positions.append([row, col, value])
            # 划去该位置的行列数据
            abs_delta[row][:] = 0.0; abs_delta[:][col] = 0.0
    # 返回结果
    return positions