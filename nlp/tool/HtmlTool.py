# -*- coding: utf-8 -*-
import re

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
        assert isinstance(content, str)

        # 将&优先转换，避免后续重复叠加转换
        content = content.replace("&","&amp;")
        # 替换内容
        content = content.replace("<","&lt;")
        content = content.replace(">","&gt;")
        content = content.replace("'","&apos;")
        content = content.replace(" ","&nbsp;")
        content = content.replace("\"","&quot;")
        # 返回结果
        return content

    # Html反转义
    @staticmethod
    def unescape(content):
        # 检查参数
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

    # Html反转义
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
