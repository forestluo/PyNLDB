# -*- coding: utf-8 -*-
import re

from nlp.tool.SplitTool import *

class SentenceTool(SplitTool) :
    # 合并内容
    # 将分解后带有标记的内容进行合并
    @staticmethod
    def merge(segments) :
        # 检查参数
        assert isinstance(segments, list)
        # 循环处理
        while True :
            # 获得数量
            count = len(segments)
            # 合并内容
            segments = SentenceTool._merge_(segments)
            # 检查结果
            if len(segments) >= count : break
        # 返回结果
        return segments

    @staticmethod
    def _merge_(segments) :
        # 合并内容
        # 将形如：
        # $a ... $b
        # 两段进行直接合并
        segments = SentenceTool._merge_content_(segments)
        # 合并引用
        # 将形如：
        # ，（ ... $a ... ）。
        # 三段进行直接合并
        segments = SentenceTool._merge_quotation_(segments)
        # 合并分段
        # 将形如：
        # $a ... , ... $b
        # 三段进行直接合并
        segments = SentenceTool._merge_segment_(segments)
        # 合并子内容
        # 将形如：
        # （ ... $a ... 。 ... $b
        # 后三段内容进行合并
        segments = SentenceTool._merge_compound_(segments)
        # 返回结果
        return segments

    # 将相邻的文字内容进行合并
    @staticmethod
    def _merge_content_(segments) :
        # 循环处理
        while True :
            # 获得数量
            count = len(segments)
            # 合并内容
            segments = SentenceTool.__merge_content__(segments)
            # 检查结果
            if len(segments) >= count : break
        # 返回结果
        return segments

    @staticmethod
    def __merge_content__(segments) :
        # 索引
        index =  0
        # 结果集
        result = []
        # 合并部分标点符号
        while index < len(segments) - 1:
            # 合并部分符合要求的标点符号
            if segments[index][0] != '$' or \
                    segments[index + 1][0] != '$' :
                # 增加到结果集
                result.append(segments[index]); index += 1 # 额外增加索引
            else :
                # 保存合并后的结果
                result.append(segments[index] + segments[index + 1][1:]); index += 2 # 额外增加索引
        # 检查索引值
        while index < len(segments) : result.append(segments[index]); index += 1
        # 返回结果
        return result

    # 将相邻的文字内容进行合并
    @staticmethod
    def _merge_quotation_(segments) :
        # 循环处理
        while True :
            # 获得数量
            count = len(segments)
            # 合并内容
            segments = SentenceTool.__merge_quotation__(segments)
            # 检查结果
            if len(segments) >= count : break
        # 返回结果
        return segments

    @staticmethod
    def __merge_quotation__(segments) :
        # 索引
        index =  0
        # 结果集
        result = []
        # 合并部分标点符号
        while index < len(segments) - 2:
            # 合并部分符合要求的标点符号
            # 匹配形如：
            # ，（ ... $a ... ）。
            # 因此首段必须是标点符号；中段必须是文字内容；末端也必须是标点符号
            if segments[index][0] == '$' \
                or segments[index + 1][0] != '$' \
                or segments[index + 2][0] == '$' \
                or not SplitTool._is_pair_start_(segments[index][-1]) \
                or not SplitTool._is_pair_end_(segments[index + 2][0]) :
                # 增加到结果集
                result.append(segments[index]); index += 1 # 额外增加索引
            else :
                # 保存合并后的结果
                result.append('$' + segments[index] + segments[index + 1][1:] + segments[index + 2]); index += 3 # 额外增加索引
        # 检查索引值
        while index < len(segments) : result.append(segments[index]); index += 1
        # 返回结果
        return result

    # 将相邻的文字内容进行合并
    @staticmethod
    def _merge_segment_(segments) :
        # 循环处理
        while True :
            # 获得数量
            count = len(segments)
            # 合并内容
            segments = SentenceTool.__merge_segment__(segments)
            # 检查结果
            if len(segments) >= count : break
        # 返回结果
        return segments

    @staticmethod
    def __merge_segment__(segments) :
        # 索引
        index =  0
        # 结果集
        result = []
        # 合并部分标点符号
        while index < len(segments) - 2:
            # 合并部分符合要求的标点符号
            # 匹配形如：
            # $a ... , ... $b
            # 因此首段必须是文字内容；中段必须是非终结标点；末端也必须是文字内容
            if segments[index][0] != '$' \
                or segments[index + 1][0] == '$' \
                or segments[index + 2][0] != '$' \
                or not SplitTool._is_not_end_(segments[index + 1]) :
                # 增加到结果集
                result.append(segments[index]); index += 1 # 额外增加索引
            else :
                # 保存合并后的结果
                result.append(segments[index] + segments[index + 1] + segments[index + 2][1:]); index += 3 # 额外增加索引
        # 检查索引值
        while index < len(segments) : result.append(segments[index]); index += 1
        # 返回结果
        return result

    # 将引用的部分进行合并
    @staticmethod
    def _merge_compound_(segments) :
        # 循环处理
        while True :
            # 获得数量
            count = len(segments)
            # 合并内容
            segments = SentenceTool.__merge_compound__(segments)
            # 检查结果
            if len(segments) >= count : break
        # 返回结果
        return segments

    @staticmethod
    def __merge_compound__(segments) :
        # 索引
        index =  1
        # 结果集
        result = [segments[0]]
        # 合并部分标点符号
        while index < len(segments) - 2:
            # 合并部分符合要求的标点符号
            # 匹配形如：
            # （ ... $a ... 。 ... $b
            # 因此前置有引用标记；首段必须是文字内容；中段必须是终结标点；末端也必须是文字内容
            if segments[index][0] != '$' \
                or segments[index + 1][0] == '$' \
                or segments[index + 2][0] != '$' \
                or not SplitTool._is_end_(segments[index + 1]) \
                or not SplitTool._is_left_quote_(segments[index - 1][-1]) :
                # 增加到结果集
                result.append(segments[index]); index += 1 # 额外增加索引
            else :
                # 保存合并后的结果
                result.append(segments[index] + segments[index + 1] + segments[index + 2][1:]); index += 3 # 额外增加索引
        # 检查索引值
        while index < len(segments) : result.append(segments[index]); index += 1
        # 返回结果
        return result
