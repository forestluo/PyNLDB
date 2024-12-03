# -*- coding: utf-8 -*-
from nlp.item.ContentItem import *
from nlp.item.SentenceItem import *
from nlp.content.ContentGroup import *
from nlp.tool.SentenceTemplate import *

class SentenceContent(ContentGroup) :
    # 新对象
    def new_item(self, content = None, count = 1, source = None) :
        # 返回结果
        return SentenceItem(content, count, source)

    def add_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 检查单词
        content = item.content
        # 检查结果
        if content in self:
            # 增加计数器
            self[content].count += item.count; return
        # 检查类型
        if isinstance(item, SentenceItem) :
            # 增加对象
            self[content] = item
        else :
            # 增加项目
            self[content] = self.new_item(content, item.count)

    # 提取句子
    # 用于traverse函数
    def add_extracted(self, item, parameter = None) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 提取句子
        sentences = SentenceTemplate.extract(item.content)
        # 检查结果
        if len(sentences) <= 0 : return
        # 循环处理f
        for sentence in sentences :
            # 检查数据是否存在
            if sentence in self :
                # 计数器增加
                self[sentence].count += item.count
            else :
                # 加入字典
                self[sentence] = self.new_item(sentence, item.count, item.source)
