# -*- coding: utf-8 -*-
import cupy
import time

from nlp.alg.CupySolution import *

# 获得最大误差
def _get_major_delta(delta) :
    # 返回结果
    return cupy.sum(cupy.square(delta))

def _get_minor_delta(delta) :
    # 返回结果
    return cupy.sum(cupy.abs(delta))

# 获得误差
def _get_delta_matrix(gammas, ais, bjs) :
    # 返回结果
    # return gammas[0] - cupy.dot(ais, bjs.T)
    return cupy.multiply(gammas[1], gammas[0] - cupy.dot(ais, bjs.T))

# 获得步长
def _get_next_step(multiple, step, delta, ais, bjs) :
    return cupy.dot(cupy.multiply(2.0 * step * multiple, delta), bjs), \
        cupy.dot(cupy.multiply(2.0 * step * multiple, delta).T, ais)

# 获得最大误差
def _get_max_position(size, delta) :
    # 获得误差的绝对值
    abs_delta = cupy.abs(delta)
    # 查找最大值的位置
    pos = cupy.argmax(abs_delta)
    # 获得索引
    row = pos // size
    col = pos - row * size
    max_delta = abs_delta[row][col]
    # 返回结果
    return row, col, max_delta

class CL2Solution(CupySolution) :
    # 解算方法
    def _solving(self, gammas, ais, bjs) :
        # 调用父类函数
        super()._solving(gammas, ais, bjs)
        # 打印信息
        print(f"CL2Solution._solving : algorithm(\"L2\") !")

        # 循环计数
        i = 0; j = 0
        # 步长倍数
        multiple = 1
        # 步长
        step = self._error
        # 最大行和范数
        last_delta = cupy.inf
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
            # 获得最大值
            max_delta = _get_major_delta(delta)
            # 检查结果
            if max_delta <= self._error :
                # 设置数值，并中断循环
                last_delta = max_delta; break
            # 临时记录
            _last_delta = last_delta
            # 检查结果
            if last_delta < max_delta :
                # 呈上升趋势
                multiple = 1
            else :
                # 呈下降趋势
                i = 0
                # 乘数加一
                multiple += 1
                # 保存上次误差
                last_delta = max_delta
                # 检查结果
                if multiple > self._size : multiple = self._size
            # 通过误差计算步长，并移至下一个步骤
            _dai, _dbj = _get_next_step(multiple, step, delta, ais, bjs)
            # 注意：分成两个步骤计算
            ais += _dai; bjs += _dbj

            # 计时结束
            end = time.perf_counter()
            # 间隔打印
            if cupy.remainder(j, self._max_loop) == 0 :
                # 获得时间
                timespan = int((end - start) * 1000)
                # 打印信息
                print(f"CL2Solution._solving : show result !")
                print(f"\tloop[{j},{i},{multiple}] = {timespan} ms")
                print(f"\tΣ(|Δγᵢⱼ|²)  = {max_delta}")
                if j > 1 : print(f"\t∇Σ(|Δγᵢⱼ|²) = {_last_delta - max_delta}")
                print(f"\t\tΣ|Δγᵢⱼ| = {_get_minor_delta(delta)}")
                # 获得一系列误差最大值位置记录
                row, col, max_delta = _get_max_position(self._size, delta)
                print(f"\t\tMax(|Δγᵢⱼ|) = ({row},{col},{max_delta})")
        # 返回结果
        return last_delta
