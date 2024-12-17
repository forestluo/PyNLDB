# -*- coding: utf-8 -*-

class SimpleElement :
    # 初始化
    def __init__(self, value = None) :
        # 设置参数
        self.__value = value

    def __del__(self) :
        # 清理
        self.__value = None

    def clear(self) :
        # 清理
        self.__value = None

    @property
    def value(self) :
        # 返回结果
        return self.__value

    @value.setter
    def value(self, value) :
        # 设置参数
        self.__value = value

    @property
    def is_empty(self) :
        # 返回结果
        return self.__value is None

    def set(self, value = None) :
        # 设置数值
        self.__value = value