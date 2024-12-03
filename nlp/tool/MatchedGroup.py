# -*- coding: utf-8 -*-

from nlp.tool.MatchedSegment import *

class MatchedGroup :
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
        self._segments.append(MatchedSegment(matched))

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

    # 清理无效数据
    def clear_invalid(self) :
        # 重新组织数据
        self._segments = [item for item in self._segments if item.is_valid()]

    def dump(self) :
        # 打印信息
        print("MatchedGroup.dump : show segments !")
        for i in range(len(self._segments)) :
            # 获得段落
            segment = self._segments[i]
            # 打印信息
            print("\t", end = ""); print("segment[%d](%d,%d) = \"%s\"" % (i, segment.start, segment.end, segment.content))
