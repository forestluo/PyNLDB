# -*- coding: utf-8 -*-

import sys

class ProgressBar :
    # 初始化
    def __init__(self, total) :
        # 检查参数
        assert total >= 0
        # 设置计数
        self.__count = 0
        # 设置百分数
        self.__percent = 0
        # 设置参数
        self.__total = total

    @property
    def count(self) :
        # 返回结果
        return self.__count

    @count.setter
    def count(self, value) :
        # 增加数值
        self.__count += value

    def increase(self) :
        # 计数器加1
        self.__count += 1; self.update()

    def begin(self, line = None) :
        # 检查参数
        if isinstance(line, str) : print(line)
        # 打印进度条
        print("\r", end = "")
        print("Progress({0}%) : total {1} step(s)" \
            .format(self.__percent, self.__total), end = "")
        sys.stdout.flush()

    def end(self, line = None) :
        # 设置进度
        self.__percent = 100
        """
        # 打印进度条
        print("\r", end = "")
        print("Progress({0}%) : total {1} step(s)" \
              .format(self.__percent, self.__total), end = "")
        sys.stdout.flush()
        """
        # 检查参数
        if isinstance(line, str) : print(""); print(line)

    def update(self) :
        # 检查结果
        if self.__count >= (self.__percent + 1) * 0.01 * self.__total :
            # 计算当前百分比
            self.__percent = int(self.__count * 100.0 / self.__total)
            # 打印进度条
            print("\r", end = "")
            print("Progress({}%) :" \
                .format(self.__percent), "▓" * (self.__percent * 3 // 5), end = "")
            sys.stdout.flush()

