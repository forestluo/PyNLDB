# -*- coding: utf-8 -*-

import time

from nlp.item.VectorItem import *
from nlp.content.ContentGroup import *

class VectorContent(ContentGroup) :
    # 初始化
    def __init__(self, dimension) :
        # 调用父类初始化
        super().__init__()
        # 检查参数
        assert dimension >= 2
        # 设置维度
        self._dimension = dimension

    # 维度
    @property
    def dimension(self) :
        # 返回结果
        return self._dimension

    # 设置维度
    @dimension.setter
    def dimension(self, dimension) :
        # 检查参数
        assert dimension >= 2
        # 设置维度
        self._dimension = dimension

    # 生成新的对象
    def new_item(self, content = None, count = 1) :
        # 返回结果
        return VectorItem(self._dimension, content, count)

    # 增加项目
    # 用于traverse函数调用
    def add_item(self, item, parameter = None) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 获得内容
        content = item.content
        # 检查字典
        if content in self:
            # 增加计数
            self[content].count += item.count; return
        # 检查类型
        if isinstance(item, VectorItem) :
            # 增加项目
            self[content] = item
        else :
            # 增加项目
            self[content] = self.new_item(item.content, item.count)
