# -*- coding: utf-8 -*-
from nlp.tool.SplitTool import *
from nlp.item.ContentItem import *
from nlp.item.SegmentItem import *
from nlp.content.ContentGroup import *

class SegmentContent(ContentGroup) :
    # 新对象
    def new_item(self, content = None, count = 1, source = None) :
        # 返回结果
        return SegmentItem(content, count, source)

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
        # 检查结果
        if content in self:
            # 获得元素
            element = self[content]
            # 增加计数
            element.count += item.count
            # 检查来源
            if isinstance(item.source, str) :
                # 增加来源
                element.add_source(item.source)
        # 增加项目
        elif isinstance(item, SegmentItem) : self[content] = item
        else :
            # 增加项目
            self[content] = self.new_item(content, item.count, item.source)

    def add_splitted(self, item, parameter = None) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 拆分内容
        segments = SplitTool.split(item.content)
        # 循环处理
        for segment in segments :
            # 检查结果
            if segment[0] != '$' : continue
            # 获得内容
            content = segment[1 : ]
            # 检查结果
            if content in self :
                # 获得元素
                element = self[content]
                # 增加计数
                element.count += item.count
                # 检查来源
                if isinstance(item.source, str) : element.add_source(item.source)
            else :
                # 增加项目
                self[content] = self.new_item(content)
                # 设置参数
                self[content].source = item.source; self[content].count = item.count
