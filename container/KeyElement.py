# -*- coding: utf-8 -*-

from container.SimpleElement import *

class KeyElement(SimpleElement) :
    # 初始化
    def __init__(self, key = None, value = None) :
        # 设置参数
        self.__key = key
        # 调用父类初始化函数
        super().__init__(value)

    def __del__(self) :
        # 调用父类
        super().__del__()
        # 清理
        self.__key = None

    def clear(self) :
        # 调用父类函数
        super().clear()
        # 清理
        self.__key = None

    @property
    def key(self) :
        # 返回结果
        return self.__key

    @key.setter
    def key(self, key) :
        # 设置参数
        self.__key = key

    @property
    def is_none(self) :
        # 返回结果
        return self.__key is None

    def set(self, key = None, value = None) :
        # 设置数值
        self.__key = key
        # 调用父类函数
        super().set(value)
