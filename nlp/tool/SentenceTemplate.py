# -*- coding: utf-8 -*-
import re

from nlp.tool.ContentTool import *
from nlp.tool.SentenceTool import *

class SentenceTemplate :
    # 所有模板（静态）
    _templates = []

    # 将规则进行预编译
    def __init__(self, rules) :
        # 检查参数
        assert isinstance(rules, list)
        # 原始规则记录在第一项
        self.rules = rules
        # 设置匹配模板
        # 必须使用空对象初始化
        # 否则后续len函数判断长度会失误
        self.patterns = \
            [re.compile("^\\$")] * len(rules)
        # 循环处理
        for i in range(0, len(rules)) :
            # 检查参数
            assert isinstance(rules[i], str)
            # 检查起始符
            if rules[i][0] != '$' :
                # 设置匹配模式
                self.patterns[i] = re.compile(rules[i])

    # 是否匹配
    def __is_matched__(self, segments) :
        # 检查参数
        assert isinstance(segments, list)
        # 检查参数
        # 模板的长度比分段数量多，则肯定无法匹配
        if len(self.patterns) > len(segments) : return False
        # 循环处理
        for i in range(0, len(self.patterns)) :
            # 检查参数
            assert isinstance(segments[i], str)
            assert self.patterns[i] is not None
            # 匹配
            matched = self.patterns[i].match(segments[i])
            # 检查结果
            if not matched or matched.start() != 0 : return False
        # 返回结果
        return True

    @staticmethod
    def clear() :
        # 清除所有模板
        SentenceTemplate._templates.clear()

    @staticmethod
    def append(rules) :
        # 增加模板
        SentenceTemplate._templates.append(SentenceTemplate(rules))

    # 提取句子
    @staticmethod
    def extract(content) :
        # 正则化内容
        content = ContentTool.normalize_content(content)
        # 打散和标记
        segments = SentenceTool.split(content)
        # 合并
        segments = SentenceTool.merge(segments)
        # 提取
        return SentenceTemplate._extract_(segments)

    # 提取句子
    @staticmethod
    def _extract_(segments) :
        # 句子
        sentences = []
        # 循环处理
        # 模板最小长度为2
        # 无标点的短标题，基本会被直接抛弃
        while len(segments) > 1 :
            # 提取句子
            sentence = SentenceTemplate.__extract__(segments)
            # 检查结果
            # 删除开头不能匹配的项目，并继续尝试匹配
            if sentence is None :
                # 跳过该段落
                del segments[0 : 1]
            # 添加句子
            else : sentences.append(sentence)
        # 返回结果
        return sentences

    # 提取句子
    # 注意：已经匹配的部分会被删除
    # 输入参数是已经处理过的分段内容
    @staticmethod
    def __extract__(segments) :
        # 循环处理
        # 匹配过程遵循最大匹配法原则：即优先匹配最长的部分。
        for template in SentenceTemplate._templates :
            # 检查结果
            if not template.__is_matched__(segments) : continue

            # 句子内容
            sentence = ""
            # 获得长度
            length = len(template.patterns)
            # 组织内容
            for i in range(0, length) :
                # 检查内容
                if segments[i][0] != '$':
                    # 添加内容
                    sentence += segments[i]
                else :
                    # 添加实际内容
                    sentence += segments[i][1:]
            # 删除头部内容，并返回结果
            del segments[0 : length]; return sentence
        # 返回结果
        return None

    # 加载顺序遵从最大匹配法原则
    @staticmethod
    def set_default() :
        # 符号嵌套
        SentenceTemplate.append(["“$", "$a", "(，|：|。|；|？|！)+‘$", "$b", "(。|；|？|！)*’$", "$c", "(。|？|！|…)+”$"])

        SentenceTemplate.append(["“$", "$a", "(，|：|。|；|？|！|…)*”$", "$b", "(，|：)?“$", "$c", "(。|？|！|…)+”$"])
        SentenceTemplate.append(["‘$", "$a", "(，|：|。|；|？|！|…)*’$", "$b", "(，|：)?‘$", "$c", "(。|？|！|…)+’$"])
        SentenceTemplate.append(["「$", "$a", "(，|：|。|；|？|！|…)*」$", "$b", "(，|：)?“$", "$c", "(。|？|！|…)+”$"])
        SentenceTemplate.append(["『$", "$a", "(，|：|。|；|？|！|…)*』$", "$b", "(，|：)?‘$", "$c", "(。|？|！|…)+’$"])
        SentenceTemplate.append(["〝$", "$a", "(，|：|。|；|？|！|…)*〞$", "$b", "(，|：)?“$", "$c", "(。|？|！|…)+”$"])
        SentenceTemplate.append(["【$", "$a", "(，|：|。|；|？|！|…)*】$", "$b", "(，|：)?‘$", "$c", "(。|？|！|…)+’$"])

        SentenceTemplate.append(["$a", "(，|：)?“$", "$b", "(，|；|…)*”$", "$c", "(。|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?‘$", "$b", "(，|；|…)*’$", "$c", "(。|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?「$", "$b", "(，|；|…)*」$", "$c", "(。|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?『$", "$b", "(，|；|…)*』$", "$c", "(。|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?〝$", "$b", "(，|；|…)*〞$", "$c", "(。|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?【$", "$b", "(，|；|…)*】$", "$c", "(。|？|！|…)+$"])

        SentenceTemplate.append(["“$", "$a", "(，|：|。|；|？|！)+‘$", "$b", "(。|；|？|！|…)*’”$"])
        SentenceTemplate.append(["“‘$", "$a", "(，|：|。|；|？|！|…)*’$", "$b", "(。|；|？|！|…)+”$"])

        SentenceTemplate.append(["“$", "$a", "(，|：|。|；|？|！|…)*”$", "$b", "(。|？|！|…)+$"])
        SentenceTemplate.append(["‘$", "$a", "(，|：|。|；|？|！|…)*’$", "$b", "(。|？|！|…)+$"])

        SentenceTemplate.append(["$a", "(，|：)?“$", "$b", "(。|？|！|…)?”$"])
        SentenceTemplate.append(["$a", "(，|：)?‘$", "$b", "(。|？|！|…)?’$"])
        SentenceTemplate.append(["$a", "(，|：)?「$", "$b", "(。|？|！|…)?」$"])
        SentenceTemplate.append(["$a", "(，|：)?『$", "$b", "(。|？|！|…)?』$"])
        SentenceTemplate.append(["$a", "(，|：)?〝$", "$b", "(。|？|！|…)?〞$"])
        SentenceTemplate.append(["$a", "(，|：)?【$", "$b", "(。|？|！|…)?】$"])

        # 常见符号
        SentenceTemplate.append(["$a", "(：)$", "$b", "(。|；|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?“$", "$b", "(。|；|？|！|…)*”$"])
        SentenceTemplate.append(["$a", "(，|：)?‘$", "$b", "(。|；|？|！|…)*’$"])
        SentenceTemplate.append(["$a", "(，|：)?（$", "$b", "(。|；|？|！|…)*）$"])
        SentenceTemplate.append(["$a", "(，|：)?「$", "$b", "(。|；|？|！|…)*」$"])
        SentenceTemplate.append(["$a", "(，|：)?『$", "$b", "(。|；|？|！|…)*』$"])
        SentenceTemplate.append(["$a", "(，|：)?〝$", "$b", "(。|；|？|！|…)*〞$"])

        SentenceTemplate.append(["$a", "(，|：)?《$", "$b", "》(。|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?【$", "$b", "】(。|？|！|…)+$"])

        # 符号嵌套
        SentenceTemplate.append(["“‘$", "$a", "(，|：|。|；|？|！|…)*’”$"])
        SentenceTemplate.append(["“（$", "$a", "(，|：|。|；|？|！|…)*）”$"])

        # 常见符号
        SentenceTemplate.append(["“$", "$a", "(，|：|。|；|？|！|…)*”$"])
        SentenceTemplate.append(["‘$", "$a", "(，|：|。|；|？|！|…)*’$"])
        SentenceTemplate.append(["（$", "$a", "(，|：|。|；|？|！|…)*）$"])
        SentenceTemplate.append(["《$", "$a", "(，|：|。|；|？|！|…)*》$"])
        SentenceTemplate.append(["【$", "$a", "(，|：|。|；|？|！|…)*】$"])
        # 比较少见
        SentenceTemplate.append(["「$", "$a", "(，|：|。|；|？|！|…)*」$"])
        SentenceTemplate.append(["『$", "$a", "(，|：|。|；|？|！|…)*』$"])
        SentenceTemplate.append(["〖$", "$a", "(，|：|。|；|？|！|…)*〗$"])
        SentenceTemplate.append(["〝$", "$a", "(，|：|。|；|？|！|…)*〞$"])

        # 最简单的句子
        SentenceTemplate.append(["$a", "(。|；|？|！|…)+$"])

# 加载缺省模板
SentenceTemplate.set_default()
# 打印信息
print("SentenceTemplate.SentenceTemplate : default templates were set !")
