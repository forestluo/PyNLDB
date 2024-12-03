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
