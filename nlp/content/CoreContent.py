# -*- coding: utf-8 -*-
from nlp.item.CoreItem import *
from nlp.item.ContentItem import *
from nlp.content.ContentGroup import *

class CoreContent(ContentGroup) :
    # 新对象
    def new_item(self, content = None, count = 1) :
        # 返回结果
        return CoreItem(content, count)

    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_item(CoreItem(content))

    def add_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 获得内容
        content = item.content
        # 检查结果
        if content in self :
            # 增加计数
            self[content].count += item.count; return
        # 检查类型
        if isinstance(item, CoreItem) :
            # 增加对象
            self[content] = item
        # 检查是否为中文
        # 如果是纯中文内容，则增加数据项
        elif item.is_chinese() :
            # 增加项目
            self[content] = self.new_item(content, item.count)

    # 增加项目
    # 用于traverse函数
    def count_item(self, item, need_split = True):
        # 检查参数
        assert isinstance(item, ContentItem)
        # 生成内容
        segments = ['$' + item.content]
        # 检查标志位
        if need_split :
            # 拆分内容
            segments = SplitTool.split(item.content)
        # 循环处理
        for segment in segments :
            # 检查结果
            if segment[0] != '$' : continue
            # 获得内容
            content = segment[1 : ]
            # 循环处理
            for i in range(len(content)) :
                # 循环处理
                for length in range(1, 1 + self.max_length) :
                    # 长度限定在当前长度
                    if i + length > len(content) : break
                    # 获得子字符串
                    value = content[i : i + length]
                    # 检查结果
                    if value in self : self[value].count += item.count
