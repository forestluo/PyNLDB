# -*- coding: utf-8 -*-
import re

class SplitTool :
    # 次要分隔符
    # 对句子成分做次要划分（暂不处理）
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

    # 合并部分标点符号
    @staticmethod
    def __merge_combination__(segments) :
        # 索引
        index =  0
        # 结果集
        result = []
        # 合并部分标点符号
        while index < len(segments) - 1:
            # 获得一个字符
            char = segments[index][0]
            # 获得后续字符
            next_char = segments[index + 1][0]
            # 合并部分符合要求的标点符号
            if not SplitTool.__is_combinable__(char, next_char) :
                # 增加到结果集
                result.append(segments[index]); index += 1 # 额外增加索引
            else :
                # 保存合并后的结果
                result.append(char + next_char); index += 2 # 额外增加索引
        # 检查索引值
        if index < len(segments) : result.append(segments[index])
        # 返回结果
        return result

    # 合并分段数字
    @staticmethod
    def __merge_digits__(segments) :
        # 索引
        index =  0
        # 结果集
        result = []
        # 合并部分标点符号
        while index < len(segments) - 1:
            # 获得最后一个字符
            char = segments[index][-1]
            # 检查结果
            if not char.isdigit() :
                # 增加到结果集
                result.append(segments[index]); index += 1 # 额外增加索引
            else :
                # 计数器
                end = index + 1
                # 合并内容
                combination = ""
                # 循环处理
                while end < len(segments) - 1 :
                    # 检查数据
                    # 第一段需要是逗号标点
                    # 第二段的长度不能小于4
                    # 第二段的前三个字符必须是数字
                    if not segments[end] in ",，" \
                        or len(segments[end + 1]) < 4 \
                        or not segments[end + 1][1:4].isdigit() : break
                    # 合并内容
                    combination += "," + segments[end + 1][1:]; end += 2
                # 检查结果
                if end <= index + 1 :
                    # 增加到结果集
                    result.append(segments[index]); index += 1 # 额外增加索引
                else :
                    # 增加到结果集
                    result.append(segments[index] + combination); index = end
        # 检查索引值
        if index < len(segments) : result.append(segments[index])
        # 返回结果
        return result

    # 合并分段内容
    @staticmethod
    def combinate(segments) :
        # 检查参数
        assert isinstance(segments, list)
        # 内容
        content = ""
        # 循环处理
        for segment in segments :
            # 增加内容
            content += segment if segment[0] != '$' else segment[1:]
        # 返回结果
        return content

    # 将段落内容完全分解
    # 1）只接受正则处理后的段落内容
    # 2）将内容完全按照标点拆解
    # 3）合并有关内容引用的标点符号
    # 4）在文字内容前加上标识，以区别标点符号
    # 5）将分段数字表达与常规标点标识区别开
    @staticmethod
    def split(content) :
        # 检查参数
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
        # 返回合并结果
        return SplitTool.__merge_combination__(SplitTool.__merge_digits__(segments))
