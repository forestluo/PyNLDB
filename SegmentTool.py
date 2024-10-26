# -*- coding: utf-8 -*-

import re

from enum import Enum

# 词类
class WordType(Enum) :
    # 特殊
    idiom = "习惯用语"
    # 实词
    noun = "名词"
    verb = "动词"
    pronoun = "代词"
    numeral = "数词"
    locative = "方位词"
    quantity = "数量词"
    adjective = "形容词"
    quantifier = "量词"
    # 虚词
    adverb = "副词"
    padding = "衬词"
    auxiliary = "助词"
    preposition = "介词"
    conjunction = "连词"
    exclamation = "感叹词"
    onomatopoeia = "拟声词"

class ContentSegment :
    # 初始化
    # matched为正则表达式匹配结果
    def __init__(self, matched = None) :
        # 设置缺省值
        # 计数
        self.count = 0
        # 备注
        self.remark = None
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

    # 判断是否相等
    def __eq__(self, segment) :
        # 检查参数
        assert isinstance(segment, ContentSegment)
        # 检查内容
        return self.remark == segment.remark \
                and self.content == segment.content

    # 是否为空
    @property
    def empty(self):
        # 返回结果
        return len(self.content) == 0 or self.start >= self.end

class SegmentGroup :
    # 初始化
    def __init__(self) :
        # 初始化为私有对象
        # 否则会被认为是静态对象
        self._segments = []

    # 检查是否为空
    @property
    def empty(self) :
        # 返回结果
        return len(self._segments) == 0

    # 增加段落
    def add_segment(self, segment) :
        # 增加项目
        self._segments.append(segment)

    # 增加匹配项目
    def add_matched(self, matched) :
        # 增加项目
        self._segments.append(ContentSegment(matched))

    # 找到可以匹配的字符
    # index为基于整个匹配字符串的索引
    def get_char(self, index) :
        # 查找匹配的段落
        segment = self._get_segment_(index)
        # 检查结果
        if segment is None : return None
        # 检查参数
        assert index < segment.end
        assert index >= segment.start
        # 返回结果
        return segment.content[index - segment.start]

    # 通过索引查找可以匹配的段落
    # index为基于整个匹配字符串的索引
    def _get_segment_(self, index):
        # 循环处理
        for segment in self._segments:
            # 检查索引位置
            if segment.start <= index < segment.end : return segment
        # 返回空
        return None

    def dump(self) :
        # 打印信息
        print("SegmentGroup.dump : show segments !")
        for i in range(0, len(self._segments)) :
            # 获得段落
            segment = self._segments[i]
            # 打印信息
            print("\tsegment[%d](%d,%d) = \"%s\"" % (i, segment.start, segment.end, segment.content))
