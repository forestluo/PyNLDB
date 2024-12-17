# -*- coding: utf-8 -*-

from container.KeyElement import *

class HashElement(KeyElement) :
    # 最大子节点数
    _max_subnode = 256

    # 初始化
    def __init__(self, size, key = None, value = None) :
        # 调用父类初始化函数
        super().__init__(key, value)
        # 检查参数
        assert 0 < size <= \
            HashElement._max_subnode\
        # 创建子节点
        self.__subnodes = [None] * size

    def __len__(self) :
        # 返回结果
        return len(self.__subnodes)

    def __getitem__(self, index) :
        # 返回结果
        return self.__subnodes[index]

    def __setitem__(self, index, value) :
        # 设置数值
        self.__subnodes[index] = value

    def __del__(self) :
        # 调用父类函数
        super().__del__()
        # 循环处理
        for subnode in self.__subnodes :
            # 检查参数
            if subnode is not None : del subnode
        # 删除所有
        del self.__subnodes; self.__subnodes = None

    def clear(self, clear_subnodes = False) :
        # 调用父类函数
        super().clear()
        # 清理
        if clear_subnodes :
            # 清理数据
            self.__subnodes = [None] * len(self._subnodes)

    @property
    def has_child(self) :
        # 返回结果
        return any(item is not None for item in self.__subnodes)