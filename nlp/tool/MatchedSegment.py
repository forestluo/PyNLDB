# -*- coding: utf-8 -*-

from nlp.corpus.CommonWord import *

class MatchedSegment :
    # 初始化
    # matched为正则表达式匹配结果
    def __init__(self, matched = None) :
        # 设置缺省值
        # 计数
        self.count = 0
        # 检查参数
        if matched is None:
            # 内容
            self.content = ""
            # 索引【开始，结束】
            # 长度 = 结束 - 开始
            self._index = [-1, -1]
        else :
            # 设置内容
            self.content = matched.group()
            # 设置长度
            self._index = [matched.start(), matched.end()]

    # 终止
    @property
    def end(self) :
        # 返回结果
        return self._index[1]

    @end.setter
    def end(self, value) :
        # 返回结果
        self._index[1] = value

    # 起始
    @property
    def start(self) :
        # 返回结果
        return self._index[0]

    @start.setter
    def start(self, value) :
        # 设置数值
        self._index[0] = value

    # 是否有效
    def is_valid(self) :
        # 检查数据
        # 不检查长度大于2的项目
        if len(self.content) > 2 :
            return True
        # 检查数据
        # 含有ASC字符的，基本都是正确的
        for char in self.content :
            if char.isascii() : return True
        # 检查数据
        # 序数词不检查
        if self.content[0] in ("每", "第") : return True
        # 检查数据
        if CommonWord.is_quantity(self.content) : return True
        # 返回结果
        # 其余的应按照中文处理
        return False if self.content[0] == "一" else True

    # 判断是否相等
    def __eq__(self, segment) :
        # 检查参数
        assert isinstance(segment, MatchedSegment)
        # 检查内容
        return self.content == segment.content

    # 是否为空
    @property
    def empty(self) :
        # 返回结果
        return len(self.content) == 0 or self.start >= self.end
