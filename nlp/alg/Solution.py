# -*- coding: utf-8 -*-
import traceback

from threading import Thread

from widget.ProgressBar import *

class Solution(Thread) :
    # 初始化
    def __init__(self, w2v) :
        # 调用父类初始化
        super().__init__()
        # 主动中断循环
        self._break_loop = False
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

    def __new_gamma(self) :
        # 创建矢量矩阵
        # 只有这样定义二维数组才能防止“粘连”
        # 即，数组按行或者按列形成了完全绑定关系
        return [[[0.0
            for _ in range(self._size)]
            for _ in range(self._size)] for _ in range(2)]

    # 获得标准数据
    def _get_gammas(self) :
        # 重建索引
        self._w2v.index_vectors()
        # 结束
        print(f"Solution._get_gammas : finished reindexing vectors !")

        # 创建矩阵
        gammas = self.__new_gamma()
        # 进度条
        pb = ProgressBar(self._w2v.wsize)
        # 开始
        pb.begin(f"Solution._get_gammas : building matrix !")
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
            if v1 is None : continue

            # 获得单词
            c2 = c[-1]
            # 检查数据
            v2 = self._w2v.vector(c2)
            # 检查结果
            if v2 is None : continue

            # 设置数值
            gammas[0][v1.index][v2.index] = item.gamma
            # 检查结果
            if item.gamma > self._error : \
                    gammas[1][v1.index][v2.index] = 1.0
        # 结束
        pb.end(f"Solution._get_gammas : finished building matrix !")
        # 返回结果
        return gammas

    # 打印信息
    def dump(self) :
        # 打印信息
        print(f"Solution.dump : dump properties !")
        print(f"\terror = {self._error}")
        print(f"\tmax_loop = {self._max_loop}")
        print(f"\tvsize = {self._w2v.vsize}")
        print(f"\twsize = {self._w2v.wsize}")
        print(f"\tdimension = {self._w2v.dimension}")
        print(f"\tmin_count = {self._w2v.min_count}")
        print(f"\tcopy_data = {self._w2v.copy_data}")

    def start(self) :
        # 启动线程
        if not self.is_alive() :
            # 启动线程
            super().start()
            # 打印信息
            print(f"Solution.start : thread startup !")
        else :
            # 打印信息
            print(f"Solution.start : fail to startup thread !")

    def stop(self) :
        # 检查参数
        if self.is_alive() :
            # 设置标记
            self._break_loop = True
            # 打印信息
            print(f"Solution.stop : flag was set !")
            # 等待结束
            self.wait()
            # 打印信息
            print(f"Solution.stop : finish waiting !")
        else :
            # 打印信息
            print(f"Solution.stop : thread already stopped !")

    # 等待线程结束
    def wait(self) :
        # 尝试
        try :
            # 检查线程
            if self.is_alive() :
                # 等待线程结束
                self.join()
                # 设置标记
                self._break_loop = False
                # 打印信息
                print(f"Solution.wait : thread stopped !")
            else :
                # 打印信息
                print(f"Solution.wait : thread not running !")
        except Exception as e:
            traceback.print_exc()
            print("Solution.run : ", str(e))
            print("Solution.run : unexpected exit !")

    # 执行函数
    def _run(self) :
        # 设置标记
        self._break_loop = True
        # 打印信息
        print(f"Solution._run : do nothing !")

    # 执行函数
    def run(self) :
        # 异常处理
        try :
            # 打印信息
            print(f"Solution.run : thread is running !")
            # 调用函数
            self._run()
            # 打印信息
            print(f"Solution.run : thread finished running !")
        except Exception as e :
            traceback.print_exc()
            print("Solution.run : ", str(e))
            print("Solution.run : unexpected exit !")
        # 设置标记
        self._break_loop = False
        # 打印信息
        print(f"Solution.run : thread has been stopped !")
