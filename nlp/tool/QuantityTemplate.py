# -*- coding: utf-8 -*-
import re

from nlp.WordType import *
from nlp.tool.QuantityTool import *
from nlp.tool.MatchedGroup import *
from nlp.tool.MatchedSegment import *

class QuantityTemplate(QuantityTool) :
    # 匹配模板
    _patterns = []
    # 数量词模板
    _templates = \
    [
        "\\d+", # 编号

        "\\d+$v", # 单位符号
        "\\d+$u", # 单位名称
        "\\d+$q", # 量词
        "\\d+$y", # 货币名称

        ",\\d{3}",
        "\\d+[至|比]",
        "[￥|＄]\\d+",

        "$c+$u", # 单位名称
        "$c+$q", # 量词
        "$c+$y", # 货币名称

        "[\\.|+|\\-|*|/|<|=|#|＋|－|×|÷]+[A-Za-z\\d]+",
        "[A-Za-z\\d]+[\\.|~|'|\"|:|+|\\-|*|/|>|=|#|：|～|＋|－|×|÷]+",

        "[十|百|千|万|亿][多|余]?[十|百|千|万|亿]?$c{1,2}",
        "$c{1,2}[十|百|千|万|亿][多|余]?[个|十|百|千|万|亿]?($u|$q|$y)?",

        "\\d+[十|百|千|万|亿][多|余]?[个|十|百|千|万|亿]?($u|$q|$y)?",
        # 序数
        "每$u",
        "第$c", # 序数
        "第\\d+", # 序数
        # 百分数
        "$c+分之",
        "[百]?分之$c+",
        "[\\d+|$c+]个百分点", # 百分点
        # 时间
        #"[上|中|下]午",
        "(\\d+|$c+)个(月|小时)",
        "(\\d+|$c+)(周|年|季度|刻钟)",
        "([\\?|\\d+]\\s[-|—|~|～|－]\\s[\\?|\\d+][年]?)"
    ]

    @staticmethod
    def _extract_(content) :
        # 匹配的段落集合
        group = MatchedGroup()
        # 循环处理
        for pattern in QuantityTemplate._patterns :
            # 匹配
            matched = pattern.finditer(content)
            # 检查结果
            for match in matched : group.add_matched(match)
        # 返回结果
        return None if group.empty else group

    @staticmethod
    def extract(content) :
        # 检查参数
        assert isinstance(content, str)

        # 获得所有匹配的段落集合
        group = QuantityTemplate._extract_(content)
        # 检查结果
        if group is None : return None

        # 索引
        index = 0
        # 新集合
        new_group = MatchedGroup()
        # 循环处理
        while index < len(content) :
            # 获得当前字符
            value = group.get_char(index)
            # 检查结果
            if value is None : index += 1; continue

            # 生成新的段落
            segment = MatchedSegment()
            # 设置索引
            segment.start = index
            # 设置内容
            segment.content = value
            # 设置类型
            segment.remark = WordType.quantity

            # 循环处理
            for j in range(index + 1, len(content)) :
                # 设置结束标记
                segment.end = j
                # 获得当前字符
                value = group.get_char(j)
                # 检查结果
                if value is None : break
                # 增加内容
                segment.content += value
            # 检查结果
            if not segment.empty :
                # 增加段落
                new_group.add_segment(segment)
            # 检查索引
            if index + 1 < len(content) :
                # 设置索引
                index = segment.end + 1
            # 已经是结尾
            else : segment.end = index + 1
        # 清理无效数据
        new_group.clear_invalid()
        # 检查结果
        return None if new_group.empty else new_group

    @staticmethod
    def set_default() :
        # 获得预编译模板
        QuantityTemplate._patterns = \
            [re.compile(QuantityTool._get_rule_(template)) for template in QuantityTemplate._templates]

# 设置缺省提取模板
QuantityTemplate.set_default()
# 打印信息
print("QuantityTemplate.QuantityTemplate : default templates were set !")
