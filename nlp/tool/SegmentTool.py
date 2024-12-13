# -*- coding: utf-8 -*-

from nlp.item.ContentItem import *
from nlp.content.ContentGroup import *

class SegmentTool :

    # 最大匹配法（从左至右）
    @staticmethod
    def l2r(contents, content) :
        # 获得长度
        length = len(content)
        assert length > 0
        # 检查参数
        assert isinstance(content, str)
        assert isinstance(contents, ContentGroup)
        # 计数器
        i = 0
        # 结果集
        segments = []
        # 循环处理
        while i < length :
            # 标志位
            flag = False
            # 计数器
            j = length
            # 循环处理
            while j > i :
                # 获得内容
                segment = content[i : j]
                # 计数器减一
                j -= 1
                # 查询数据
                if segment in contents :
                    # 设置标志位
                    flag = True
                    # 增加长度
                    i += len(segment)
                    # 增加元素
                    segments.append(segment); break
            # 检查标记位
            if not flag :
                segments.append(content[i : i + 1]); i += 1
        # 返回结果
        return segments

    # 最大匹配法（从右至左）
    @staticmethod
    def r2l(contents, content) :
        # 获得长度
        length = len(content)
        assert length > 0
        # 检查参数
        assert isinstance(content, str)
        assert isinstance(contents, ContentGroup)
        # 计数器
        i = length
        # 结果集
        segments = []
        # 循环处理
        while i > 0 :
            # 标志位
            flag = False
            # 计数器
            j = 0
            # 循环处理
            while j < i :
                # 获得内容
                segment = content[j : i]
                # 计数器加一
                j += 1
                # 查询数据
                if segment in contents :
                    # 设置标志位
                    flag = True
                    # 增加长度
                    i -= len(segment)
                    # 增加元素
                    segments.append(segment); break
            # 检查标记位
            if not flag :
                segments.append(content[i - 1 : i]); i -= 1
        # 返回结果
        return segments[::-1]

    # 最大分解法（中分）
    @staticmethod
    def mid(contents, content, index) :
        # 获得长度
        length = len(content)
        assert length > 0
        # 检查参数
        assert 0 <= index < length
        assert isinstance(content, str)
        # 左侧内容
        left = content[0 : index]
        # 右侧内容
        right = content[index : ]
        # 检查左侧内容
        if len(left) <= 0 :
            # 返回右侧部分
            return SegmentTool.l2r(contents, content)
        if len(right) <= 0 :
            # 返回左侧部分
            return SegmentTool.r2l(contents, content)
        # 返回结果
        return SegmentTool.r2l(contents, left) + SegmentTool.l2r(contents, right)
