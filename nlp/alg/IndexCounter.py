# -*- coding: utf-8 -*-

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