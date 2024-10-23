# -*- coding: utf-8 -*-

import re

from NLDB3Raw import *
from SentenceTool import *

class ChineseTool :

    @staticmethod
    def wide_convert(content):
        # 检查参数
        assert content is not None
        assert isinstance(content, str)

        # 新内容
        newContent = ""
        # 循环处理
        for char in content :
            # 获得Unicode
            unicode = ord(char)
            # 特殊处理
            if unicode == 32 :
                newContent += chr(12288)
            elif unicode < 33 :
                newContent += char
            elif unicode > 126 :
                newContent += char
            else :
                newContent += chr(unicode + 65248)
        # 返回结果
        return newContent

    @staticmethod
    def narrow_convert(content):
        # 检查参数
        assert content is not None
        assert isinstance(content, str)

        # 新内容
        newContent = ""
        # 循环处理
        for char in content :
            # 获得Unicode
            unicode = ord(char)
            # 特殊处理
            if unicode == 12288 :
                newContent += ' '
            elif unicode < 65281 :
                newContent += char
            elif unicode > 65374 :
                newContent += char
            else :
                newContent += chr(unicode - 65248)
        # 返回结果
        return newContent

class HtmlTool :
    # 错误
    _errors = ['o', 'O', 'l']
    # 模式
    _patterns = \
        [
            re.compile("&#[0-9|oOl]{1,5};"),
            re.compile("&#[x|X]([0-9|a-fA-FoOl]{1,4});")
        ]
    # 反转义
    _escapes = \
        {
            "&amp;" : "\x26",
            "&quot;": "\x22",
            "&nbsp;" : "\xa0",
            "&shy;" : "\xad",
            "&Agrave;" : "\xc0",
            "&agrave;" : "\xe0",
            "&Aacute;" : "\xc1",
            "&aacute;" : "\xe1",
            "&Acirc;" : "\xc2",
            "&acirc;" : "\xe2",
            "&Atilde;" : "\xc3",
            "&atilde;" : "\xe3",
            "&Auml;" : "\xc4",
            "&auml;" : "\xe4",
            "&Aring;" : "\xc5",
            "&aring;" : "\xe5",
            "&AElig;" : "\xc6",
            "&aelig;" : "\xe6",
            "&Ccedil;" : "\xc7",
            "&ccedil;" : "\xe7",
            "&Egrave;" : "\xc8",
            "&egrave;" : "\xe8",
            "&Eacute;" : "\xc9",
            "&eacute;" : "\xe9",
            "&Ecirc;" : "\xca",
            "&ecirc;" : "\xea",
            "&Euml;" : "\xcb",
            "&euml;" : "\xeb",
            "&Igrave;" : "\xcc",
            "&igrave;" : "\xec",
            "&Iacute;" : "\xcd",
            "&iacute;" : "\xed",
            "&Icirc;" : "\xce",
            "&icirc;" : "\xee",
            "&Iuml;" : "\xcf",
            "&iuml;" : "\xef",
            "&ETH;" : "\xd0",
            "&eth;" : "\xf0",
            "&Ntilde;" : "\xd1",
            "&ntilde;" : "\xf1",
            "&Ograve;" : "\xd2",
            "&ograve;" : "\xf2",
            "&Oacute;" : "\xd3",
            "&oacute;" : "\xf3",
            "&Ocirc;" : "\xd4",
            "&ocirc;" : "\xf4",
            "&Otilde;" : "\xd5",
            "&otilde;" : "\xf5",
            "&Ouml;" : "\xd6",
            "&ouml;" : "\xf6",
            "&Oslash;" : "\xd8",
            "&oslash;" : "\xf8",
            "&Ugrave;" : "\xd9",
            "&ugrave;" : "\xf9",
            "&Uacute;" : "\xda",
            "&uacute;" : "\xfa",
            "&Ucirc;" : "\xdb",
            "&ucirc;" : "\xfb",
            "&Uuml;" : "\xdc",
            "&uuml;" : "\xfc",
            "&Yacute;" : "\xdd",
            "&yacute;" : "\xfd",
            "&THORN;" : "\xde",
            "&thorn;" : "\xfe",
            "&szlig;" : "\xdf",
            "&yuml;" : "\xff",
            "&iexcl;" : "\xa1",
            "&cent;" : "\xa2",
            "&pound;" : "\xa3",
            "&curren;" : "\xa4",
            "&yen;" : "\xa5",
            "&brvbar;" : "\xa6",
            "&sect;" : "\xa7",
            "&die;" : "\xa8",
            "&copy;" : "\xa9",
            "&laquo;" : "\xab",
            "&reg;" : "\xae",
            "&macron;" : "\xaf",
            "&deg;" : "\xb0",
            "&plusmn;" : "\xb1",
            "&sup2;" : "\xb2",
            "&sup3;" : "\xb3",
            "&acute;" : "\xb4",
            "&micro;" : "\xb5",
            "&para;" : "\xb6",
            "&middot;" : "\xb7",
            "&cedil;" : "\xb8",
            "&supl;" : "\xb9",
            "&raquo;" : "\xbb",
            "&frac14;" : "\xbc",
            "&frac12;" : "\xbd",
            "&frac34;" : "\xbe",
            "&iquest;" : "\xbf",
            "&times;" : "\xd7",
            "&divide;" : "\xf7",
            "&ldquo;" : "\x201c",
            "&rdquo;" : "\x201d"
        }

    @staticmethod
    def escape(content) :
        # 检查参数
        assert content is not None
        assert isinstance(content, str)

        # 将&优先转换，避免后续重复叠加转换
        content = content.replace("&", "&amp;")

        # 替换内容
        content = content.replace("<", "&lt;")
        content = content.replace(">", "&gt;")
        content = content.replace("'", "&apos;")
        content = content.replace(" ", "&nbsp;")
        content = content.replace("\"", "&quot;")

        # 返回结果
        return content

    # XML反转义
    @staticmethod
    def unescape(content):
        # 检查参数
        assert content is not None
        assert isinstance(content, str)
        # 循环处理
        while True:
            # 获得长度
            length = len(content)
            # 反转义XML
            content = HtmlTool.__unescape(content)
            # 检查结果
            if len(content) >= length: break
        # 返回结果
        return content

    # XML反转义
    @staticmethod
    def __unescape(content) :
        # 需要转义的内容
        escapes = {}
        # 检索匹配项目
        matched = HtmlTool._patterns[0].findall(content)
        # 检查结果
        if matched is not None :
            # 循环处理
            for item in matched :
                # 截取
                number = item[2 : (len(item) - 1)]
                # 检查结果
                if len(number) <= 0 :
                    # 将结果加入字典
                    if not item in escapes : escapes[item] = ''
                else :
                    # 替换
                    number = number.replace("l", "1")
                    number = number.replace("o", "0")
                    number = number.replace("O", "0")
                    # 转换
                    value = int(number)
                    # 将结果加入字典
                    if not value in escapes : escapes[item] = chr(value)

        # 检索匹配项目
        matched = HtmlTool._patterns[1].findall(content)
        # 检查结果
        if matched is not None :
            # 循环处理
            for item in matched :
                # 截取
                number = item[3 : (len(item) - 1)]
                # 检查结果
                if len(number) <= 0 :
                    # 将结果加入字典
                    if not item in escapes : escapes[item] = ''
                else :
                    # 替换
                    number = number.replace("l", "1")
                    number = number.replace("o", "0")
                    number = number.replace("O", "0")
                    # 转换
                    value = int(number)
                    # 将结果加入字典
                    if not value in escapes : escapes[item] = chr(value)

        # 替换掉所有转义内容
        for key in escapes.keys() : content = content.replace(key, escapes[key])
        for key in HtmlTool._escapes.keys(): content = content.replace(key, HtmlTool._escapes[key])
        # 返回结果
        return content

class ClearTool :
    # 预编译
    _compiled = re.compile("([\x00-\x1F]|\x7F|\u1680|\u180E|[\u2000-\u200D]|[\u2028-\u2029]|\u202F|[\u205F-\u2060]|\u3000|[\uD7B0-\uF8FF]|\uFEFF|[\uFFF0-\uFFFF])+")

    # 清理空格
    @staticmethod
    def clear_blank(content) :
        # 检查参数
        assert content is not None
        assert isinstance(content, str)
        # 返回结果
        return re.sub("\\s", "", content)
    
    # 清理不可见字符
    @staticmethod
    def clear_invisible(content):
        # 检查参数
        assert content is not None
        assert isinstance(content, str)
        # 返回结果
        return ClearTool._compiled.sub(" ", content)

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
    def normalize_item(item) :
        # 检查参数
        assert item is not None
        # 返回结果
        item.content = ContentTool.normalize_content(item.content)

    @staticmethod
    def normalize_dict(data) :
        # 检查参数
        assert data is not None
        # 返回结果
        data["content"] = ContentTool.normalize_content(data["content"])

    # 正则化
    @staticmethod
    def normalize_content(content) :
        # 检查参数
        assert content is not None
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
        # 检查参数
        assert content is not None
        assert isinstance(content, str)
        # 新内容
        newContent = ""
        # 循环处理
        for char in content :
            # 检查内容
            if not char in ContentTool._punctuations.keys() :
                # 按照原字符处理
                newContent += char
            else :
                # 转换标点符号至全角
                newContent += ContentTool._punctuations[char]
        # 返回结果
        return newContent

    @staticmethod
    def __filter_content(content) :
        # 检查参数
        assert content is not None
        assert isinstance(content, str)
        # 循环处理
        while True:
            # 标志位
            matched = False
            # 循环处理
            for (compiled, replaced) in ContentTool._rules.items():
                # 过滤替换
                newContent = compiled.sub(replaced, content)
                # 比较前后结果
                if newContent != content:
                    # 设置标记位
                    matched = True
                    # 设置返回内容
                    content = newContent
            # 检查标记位
            if not matched: break
        # 返回结果
        return content

    # 微调内容
    # 仅针对对话内容中的引号调整
    @staticmethod
    def __adjust(content):
        # 检查参数
        assert content is not None
        assert isinstance(content, str)
        # 调整内容
        content = ContentTool.__adjust__(content, '\"')
        # 调整内容
        content = ContentTool.__adjust__(content, '\'')
        # 返回结果
        return content

    # 微调内容
    @staticmethod
    def __adjust__(content, value):
        # 匹配模式
        matched = re.search("([:：])(\\s)*%s".format(value), content)
        # 检查结果
        if matched is None: return content

        # 声明标志位
        flag = True
        # 字符串
        newContent = ""
        # 获得索引
        index = matched.span()[1]
        # 循环处理
        while index >= 0:
            # 检查字符
            if content[index] != value:
                # 增加字符
                newContent += content[index]
            else:
                # 反转标志位
                flag = not flag
                # 增加字符
                newContent += '“' if flag else '”'
            # 索引减一
            index -= 1

        # 反转
        newContent = newContent[::-1]

        # 初始变量
        flag = False
        # 获得索引
        index = matched.span()[1] + 1
        # 循环处理
        while index < len(newContent):
            # 检查字符
            if content[index] != value:
                # 增加字符
                newContent += content[index]
            else:
                # 反转标志位
                flag = not flag
                # 增加字符
                newContent += '“' if flag else '”'
            # 索引减一
            index += 1

        # 返回结果
        return newContent

def main():

    # 建立数据库链接
    raw = NLDB3Raw()
    # 打开数据库链接
    raw.open()
    # 随机抽取一条记录
    data = raw.random()
    # 处理数据
    content = ContentTool.normalize_content(data["content"])
    # 关闭数据库链接
    raw.close()

    # 打印结果
    print("ContentTool.main : compare data !")
    print("\toriginal   =\"%s\"" % data["content"])
    print("\tnormalized =\"%s\"" % content)

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("ContentTool.main :__main__ : ", str(e))
        print("ContentTool.main :__main__ : unexpected exit !")