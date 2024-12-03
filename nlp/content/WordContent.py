# -*- coding: utf-8 -*-
from nlp.item.WordItem import *
from nlp.item.ContentItem import *
from nlp.content.ContentGroup import *

class WordContent(ContentGroup) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 当前长度
        self.limit_length = 1

    # 新对象
    def new_item(self, content = None, count = 1) :
        # 返回结果
        return WordItem(content, count)

    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_item(WordItem(content))

    def add_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 检查单词
        word = item.content
        # 检查结果
        if word in self:
            # 增加计数器
            self[word].count += item.count; return
        # 检查类型
        if isinstance(item, WordItem) :
            # 增加对象
            self[word] = item
        # 检查是否为中文
        # 如果是纯中文内容，则增加数据项
        elif item.is_chinese() :
            # 增加项目
            self[word] = self.new_item(word, item.count)

    def add_splitted(self, item, need_split = True) :
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
                # 长度限定在当前长度
                if i + self.limit_length > len(content) : break
                # 获得单词
                word = content[i : i + self.limit_length]
                # 检查结果
                if word in self :
                    # 增加计数器
                    self[word].count += item.count
                # 检查是否为中文
                # 如果是纯中文内容，则增加数据项
                elif item.is_chinese() :
                    # 增加项目
                    self[word] = self.new_item(word, item.count)
