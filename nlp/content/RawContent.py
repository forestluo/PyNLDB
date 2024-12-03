# -*- coding: utf-8 -*-
from nlp.item.RawItem import *
from nlp.item.ContentItem import *
from nlp.content.ContentGroup import *

class RawContent(ContentGroup) :
    # 生成新的对象
    def new_item(self, content = None, count = 1, source = None) :
        # 返回结果
        return RawItem(content, count, source)

    # 增加项目
    def add_content(self, content):
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_content(ContentItem(content))

    # 增加项目
    # 用于traverse函数调用
    def add_data(self, data, parameter = None) :
        # 生成新对象
        self.add_item(self.new_item(data["content"], 1, data["source"]), parameter)

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
        if isinstance(item, RawItem) :
            # 增加对象
            self[content] = item
        else :
            # 增加项目
            self[content] = self.new_item(item.content, item.count)
