# -*- coding: utf-8 -*-

import traceback

from NLDB3Raw import *
from ContentTool import *

class SplitTool :
    # 次要分隔符
    # 对句子成分做次要划分
    _minors = \
    [
        '、', '·', '—', '～'
    ]
    # 主要分隔符
    # 对句子成分做主要划分
    _majors = \
    [
        '，', '。', '；', '：', '？', '！', '…'
    ]
    # 成对分隔符
    # 与引用、释义或对话有关
    _pairs = \
    [
        # 全角符号
        '“', '”', '（', '）', '《', '》',
        '‘', '’', '【', '】', '〈', '〉',
        '「', '」', '『', '』', '〔', '〕',
        '〖', '〗', '〝', '〞', '﹙', '﹚',
        '﹛', '﹜', '﹝', '﹞', '﹤', '﹥',
        # 半角字符对应的全角符号
        '［', '］', '｛', '｝'
    ]
    # 分隔模式
    # 对半角英文字符或者分隔符予以忽视
    # 对规范后的文本以全角标点为基准进行处理
    _split_pattern = re.compile("([" + ''.join(_majors) + ''.join(_pairs) + "])")

    @staticmethod
    def _is_major_(content) :
        # 返回结果
        return content in SplitTool._majors

    @staticmethod
    def _is_pair_end_(content) :
        # 返回结果
        return content in "”）》’】〉」』〕〗〞﹚﹜﹞﹥］｝"

    @staticmethod
    def _is_pair_start_(content) :
        # 返回结果
        return content in "“（《‘【〈「『〔〖〝﹙﹛﹝﹤［｛"

    @staticmethod
    def _is_splitter_(content) :
        # 返回结果
        # 忽略其他标点符号
        return content in SplitTool._majors or content in SplitTool._pairs

    # 检查是否为非终结符
    @staticmethod
    def _is_not_end_(content) :
        # 循环处理
        for char in content :
            if not char in ['，', '：'] : return False
        # 返回结果
        return True

    # 检查是否为终结符
    @staticmethod
    def _is_end_(content) :
        # 循环处理
        for char in content :
            if not char in ['。', '；', '？', '！', '…'] : return False
        # 返回结果
        return True

    # 检查是否为左引号（用于对话内容）
    @staticmethod
    def _is_left_quote_(content) :
        # 循环处理
        for char in content :
            if not char in ['“', '‘', '「', '『', '〝'] : return False
        # 返回结果
        return True

    # 检查是否为右引号（用于对话内容）
    @staticmethod
    def _is_right_quote_(content) :
        # 循环处理
        for char in content :
            if not char in ['”', '’', '」', '』', '〞'] : return False
        # 返回结果
        return True

    @staticmethod
    def __split__(content) :
        # 返回结果
        return list(filter(None, SplitTool._split_pattern.split(content)))

    @staticmethod
    def __is_combinable__(char, nextChar) :
        # 返回结果
        return SplitTool._is_major_(char) and SplitTool._is_right_quote_(nextChar) \
                or SplitTool._is_not_end_(char) and SplitTool._is_left_quote_(nextChar)

    # 将段落内容完全分解
    # 1) 只接受正则处理后的段落内容
    # 2）将内容完全按照标点拆解
    # 3）合并有关内容引用的标点符号
    # 4）在文字内容前加上标识，以区别标点符号
    @staticmethod
    def split(content) :
        # 检查参数
        assert content is not None
        assert isinstance(content, str)

        # 获得经标点分段的结果
        segments = SplitTool.__split__(content)

        # 增加标识
        for i in range(0, len(segments)) :
            # 增加内容标识前缀（‘$’符号并不属于分隔符，因此可以完全区别开）
            if not SplitTool._is_splitter_(segments[i][0]) : segments[i] = '$' + segments[i]
        # 微调数据
        for i in range(1, len(segments)) :
            # 前面有标点符号的情况下，可认为省略号属于内容
            if segments[i][0] == '…' and segments[i - 1][0] != '$' : segments[i] = '$' + segments[i]

        # 索引
        index =  0
        # 结果集
        result = []
        # 合并部分标点符号
        while index < len(segments) - 1:
            # 获得一个字符
            char = segments[index][0]
            # 获得后续字符
            nextChar = segments[index + 1][0]
            # 合并部分符合要求的标点符号
            if not SplitTool.__is_combinable__(char, nextChar) :
                # 增加到结果集
                result.append(segments[index]); index += 1 # 额外增加索引
            else :
                # 保存合并后的结果
                result.append(char + nextChar); index += 2 # 额外增加索引
        # 检查索引值
        if index < len(segments) : result.append(segments[index])
        # 返回结果
        return result

class SentenceTool(SplitTool) :
    # 合并内容
    # 将分解后带有标记的内容进行合并
    @staticmethod
    def merge(segments) :
        # 检查参数
        assert segments is not None
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

def main():

    # 建立数据库链接
    raw = NLDB3Raw()
    # 打开数据库链接
    raw.open()
    # 随机抽取一条记录
    data = raw.random()
    #data["content"] = "“我们上哪儿吃饭？”她问。"
    #data["content"] = "“是啊，这地儿一丢，国内的油价还得涨。”陆臻感觉很新奇，他倒是没顾上想这么远。"
    # 处理数据
    content = ContentTool.normalize_content(data["content"])
    # 关闭数据库链接
    raw.close()

    # 打印结果
    print("SentenceTool.main : normalized result !")
    print("\toriginal   =\"%s\"" % data["content"])
    print("\tnormalized =\"%s\"" % content)

    # 打散和标记
    segments = SentenceTool.split(content)
    # 打印结果
    print("SentenceTool.main : split result !")
    # 打印结果
    for segment in segments : print("\t%s" % segment)

    # 合并
    segments = SentenceTool.merge(segments)
    # 打印结果
    print("SentenceTool.main : merged result !")
    # 打印结果
    for segment in segments : print("\t%s" % segment)

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("SentenceTool.main :__main__ : ", str(e))
        print("SentenceTool.main :__main__ : unexpected exit !")

