# -*- coding: utf-8 -*-

import sys

class ParallelBar :
    # 初始化
    def __init__(self) :
        # 内容条
        self.__bars = []
        # 标志位
        self.__new_bars = True

    # 打印
    def print(self, bars) :
        # 检查参数
        assert isinstance(bars, list)
        # 内容条
        self.__bars = bars
        # 检查参数
        if self.__new_bars :
            # 设置参数
            self.__new_bars = False
        else :
            # 打印多行
            for i in range(len(self.__bars)) :
                # 这一行的作用是在打印完一行之后回退到上一行，所以有几个\n就要加几行
                # 如果想在循环玩之后保留最后输出的内容，就要在最后一次循环的时候不运行这行
                sys.stdout.write(u'\u001b[1A')
        # 打印多行
        for i in range(len(self.__bars)) :
            # 检查参数
            if i > 0 :
                # 最后一行加\n主要是为了保持循环结束后光标在行首
                sys.stdout.write(self.__bars[i] + '\n')
            else :
                # '\u001b[1000D\u001b[2K'的作用是把这一行清空
                sys.stdout.write(u'\u001b[1000D\u001b[2K' + self.__bars[i] + '\n')
        # 刷新
        sys.stdout.flush()

class ProgressBar :
    # 初始化
    def __init__(self, total = 0) :
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
        # 检查参数
        assert total >= 0
        # 增加数值
        self.__count += value

    def increase(self, count = 1) :
        # 计数器加1
        self.__count += count
        self.update()

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
        print("")
        # 检查参数
        if isinstance(line, str) : print(line)

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

class IndexCounter :
    # 初始化
    def __init__(self) :
        # 记录
        self.__counter = {}

    # 清理
    def clear(self) :
        # 清理数据
        self.__counter.clear()

    # 记录位置
    def count(self, index, values) :
        # 检查参数
        assert isinstance(values, list)
        assert len(values) == 3
        # 检查数据
        if index in \
            self.__counter.keys() :
            # 增加计数
            self.__counter[index][0] += 1
        # 设置初始值
        else : self.__counter[index] = values

    def remove_max(self) :
        # 获得索引
        index = self.max_index()
        # 移除相关项目
        self.__counter.pop(index, None)

    def max_index(self) :
        # 检查长度
        if len(self.__counter) <= 0:
            return -1
        # 获得最大值
        return max(self.__counter,
            key = lambda k : self.__counter[k][0])

    def max_value(self) :
        # 获得索引
        index = self.max_index()
        # 返回结果
        return self.__counter[index] \
            if index >= 0 else None

    def max_count(self) :
        # 获得索引
        value = self.max_value()
        # 返回结果
        return value[0] \
            if value is not None else -1

    def max_position(self, n) :
        # 检查参数
        assert n > 0
        # 获得索引
        index = self.max_index()
        # 检查结果
        if index < 0 : return -1, -1
        # 获得行数
        row = index // n
        # 获得列数
        col = index - row * n
        # 返回结果
        return row, col

