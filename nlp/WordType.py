# -*- coding: utf-8 -*-

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