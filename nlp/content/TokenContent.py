# -*- coding: utf-8 -*-
from nlp.item.TokenItem import *
from nlp.item.ContentItem import *
from nlp.content.ContentGroup import *

class TokenContent(ContentGroup) :
    # 生成新的对象
    def new_item(self, content = None, count = 1) :
        # 返回结果
        return TokenItem(content, count)

    # 增加项目
    # 用于traverse函数调用
    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_item(ContentItem(content))

    def add_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 获得内容
        content = item.content
        # 检查类型
        if content in self :
            # 增加计数器
            self[token].count += item.count; return
        # 检查类型
        if isinstance(item, TokenItem) :
            # 增加对象
            self[content] = item
        else :
            # 增加项目
            self[content] = self.new_item(item.content, item.count)

    # 增加项目
    # 用于traverse函数调用
    def add_splitted(self, item, parameter = None) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 扫描结果
        for token in item.content :
            # 检查字典
            if token in self :
                # 增加计数器
                self[token].count += item.count
            else :
                # 增加字典内容
                self[token] = self.new_item(token, item.count)
