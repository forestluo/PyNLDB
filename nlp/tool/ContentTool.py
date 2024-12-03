# -*- coding: utf-8 -*-
import re

from nlp.tool.HtmlTool import *
from nlp.tool.ClearTool import *
from nlp.tool.SplitTool import *
from nlp.tool.ChineseTool import *

class ContentTool :
    # 需要转全角的标点
    _punctuations = \
        {
            ',' : '，',
            '\u2236' : '：',
            ':' : '：',
            ';' : '；',
            '?' : '？',
            '!' : '！',
            '〝' : '“',
            '〞' : '”',
            '「' : '“',
            '」' : '”',
            '『' : '“',
            '』' : '”',
            #'(' : '（',
            #')' : '）',
            #'[' : '［',
            #']' : '］',
            #'{' : '\uff5b',
            #'}' : '\uff5d',
        }

    # 所有过滤规则
    _rules = \
        {
            re.compile("(\\u0020)\\s") : " ",

            re.compile("('){2,}") : "'",
            re.compile("(`){2,}") : "`",
            re.compile("(<){2,}") : "<",
            re.compile("(>){2,}") : ">",
            re.compile("(-){2,}") : "—",
            re.compile("(、){2,}") : "、",
            re.compile("(～){2,}") : "～",
            re.compile("(—){2,}") : "—",

            re.compile("(…){2,}") : "…",
            re.compile("(\\.){3,}") : "…",

            re.compile("，(，|：|\\s)*，") : "，",
            re.compile("，(，|：|\\s)*：") : "：",
            re.compile("，(，|：|\\s)*。") : "。",
            re.compile("，(，|：|\\s)*；") : "；",
            re.compile("，(，|：|\\s)*？") : "？",
            re.compile("，(，|：|\\s)*！") : "！",

            re.compile("：(，|：|\\s)*，") : "：",
            re.compile("：(，|：|\\s)*：") : "：",
            re.compile("：(，|：|\\s)*。") : "。",
            re.compile("：(，|：|\\s)*；") : "；",
            re.compile("：(，|：|\\s)*？") : "？",
            re.compile("：(，|：|\\s)*！") : "！",

            re.compile("。(，|：|。|；|？|！|\\s)+") : "。",
            re.compile("；(，|：|。|；|？|！|\\s)+") : "；",
            re.compile("？(，|：|。|；|？|！|\\s)+") : "？",
            re.compile("！(，|：|。|；|？|！|\\s)+") : "！",

            re.compile("<(br|hr|input)((\\s|\\.)*)/>") : " ",
            re.compile("<(img|doc|url|input)((\\s|\\.)*)>") : " ",
            re.compile("<[a-zA-Z]+\\s*[^>]*>(.*?)</[a-zA-Z]+>") : "$1",

            re.compile("\\s([<>【】〈〉“”‘’《》()（）［］｛｝…～—、？！；。：，])") : "\\1",
            re.compile("([<>【】〈〉“”‘’《》()（）［］｛｝…～—、？！；。：，])\\s") : "\\1",
        }

    @staticmethod
    def normalize_item(item, parameter = None) :
        # 检查参数
        assert item is not None
        # 返回结果
        item.content = ContentTool.normalize_content(item.content)

    @staticmethod
    def normalize_data(data, parameter = None) :
        # 检查参数
        assert data is not None
        # 返回结果
        data["content"] = ContentTool.normalize_content(data["content"])

    # 正则化
    @staticmethod
    def normalize_content(content, parameter = None) :
        # 检查参数
        assert isinstance(content, str)
        # 微调数据
        content = ContentTool.__adjust(content)
        # 正则化内容
        content = ContentTool.__normalize(content)
        # 过滤内容
        content = ContentTool.__filter_content(content)
        # 半角转全角
        content = ChineseTool.wide_convert(content)
        # 过滤内容
        content = ContentTool.__filter_content(content)
        # 全角转半角
        content = ChineseTool.narrow_convert(content)
        # 部分标点符号转全角
        content = ContentTool.__wide_punctuation(content)
        # 拆分内容
        return SplitTool.combinate(SplitTool.split(content))

    # 正则化
    @staticmethod
    def __normalize(content) :
        # 循环处理
        while True:
            # 长度
            length = len(content)
            # 全角转换成半角
            content = ChineseTool.narrow_convert(content)
            # 清理不可见字符
            content = ClearTool.clear_invisible(content)
            # Html反转义
            content = HtmlTool.unescape(content)
            # 检查结果
            if len(content) >= length : break
        # 返回结果
        return content

    # 标点符号转全角
    @staticmethod
    def __wide_punctuation(content) :
        # 新内容
        new_content = ""
        # 循环处理
        for char in content :
            # 检查内容
            if not char in ContentTool._punctuations.keys() :
                # 按照原字符处理
                new_content += char
            else :
                # 转换标点符号至全角
                new_content += ContentTool._punctuations[char]
        # 返回结果
        return new_content

    @staticmethod
    def __filter_content(content) :
        # 循环处理
        while True:
            # 标志位
            matched = False
            # 循环处理
            for (compiled, replaced) in ContentTool._rules.items():
                # 过滤替换
                new_content = compiled.sub(replaced, content)
                # 比较前后结果
                if new_content != content:
                    # 设置标记位
                    matched = True
                    # 设置返回内容
                    content = new_content
            # 检查标记位
            if not matched: break
        # 返回结果
        return content

    # 微调内容
    @staticmethod
    def __adjust(content) :
        # 调整内容
        content = ContentTool.__adjust__(content, "\"")
        # 调整内容
        content = ContentTool.__adjust__(content, "\'")
        # 返回结果
        return content

    # 微调内容
    @staticmethod
    def __adjust__(content, value) :
        # 匹配模式
        matched = re.search("([:：])(\\s)*%s".format(value), content)
        # 检查结果
        if matched is None: return content

        # 声明标志位
        flag = True
        # 字符串
        new_content = ""
        # 获得索引
        index = matched.end()
        # 循环处理
        while index >= 0:
            # 检查字符
            if content[index] != value :
                # 增加字符
                new_content += content[index]
            else:
                # 反转标志位
                flag = not flag
                # 增加字符
                new_content += '“' if flag else '”'
            # 索引减一
            index -= 1

        # 反转
        new_content = new_content[::-1]

        # 初始变量
        flag = False
        # 获得索引
        index = matched.end() + 1
        # 循环处理
        while index < len(new_content) :
            # 检查字符
            if content[index] != value :
                # 增加字符
                new_content += content[index]
            else:
                # 反转标志位
                flag = not flag
                # 增加字符
                new_content += '“' if flag else '”'
            # 索引减一
            index += 1

        # 返回结果
        return new_content
