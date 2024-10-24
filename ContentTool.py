# -*- coding: utf-8 -*-

import re

from NLDB3Raw import *
from SentenceTool import *

class UnicodeTool :

    @staticmethod
    def is_rare(content) :
        # 检查参数
        assert isinstance(content, str)
        # 循环处理
        for char in content :
            if not 0 <= ord(char) < 65536 : return True
        # 返回结果
        return False

    @staticmethod
    def get_remark(token):
        # 检查参数
        assert isinstance(token, str)
        # 获得Unicode值
        unicode = ord(token)
        # 检查结果
        if unicode <= 0x007F : return "C0控制符及基本拉丁文"
        if unicode <= 0x00FF : return "C1控制符及拉丁文补充-1"
        if unicode <= 0x017F : return "拉丁文扩展-A"
        if unicode <= 0x024F : return "拉丁文扩展-B"
        if unicode <= 0x02AF : return "国际音标扩展"
        if unicode <= 0x02FF : return "空白修饰字母"
        if unicode <= 0x036F : return "结合用读音符号"
        if unicode <= 0x03FF : return "希腊文及科普特文"
        if unicode <= 0x04FF : return "西里尔字母"
        if unicode <= 0x052F : return "西里尔字母补充"
        if unicode <= 0x058F : return "亚美尼亚语"
        if unicode <= 0x05FF : return "希伯来文"
        if unicode <= 0x06FF : return "阿拉伯文"
        if unicode <= 0x074F : return "叙利亚文"
        if unicode <= 0x077F : return "阿拉伯文补充"
        if unicode <= 0x07BF : return "马尔代夫语"
        if unicode <= 0x07FF : return "西非书面語言"
        if unicode <= 0x085F : return "阿维斯塔语及巴列维语"
        if unicode <= 0x087F : return "Mandaic"
        if unicode <= 0x08AF : return "撒马利亚语"
        if unicode <= 0x097F : return "天城文书"
        if unicode <= 0x09FF : return "孟加拉语"
        if unicode <= 0x0A7F : return "锡克教文"
        if unicode <= 0x0AFF : return "古吉拉特文"
        if unicode <= 0x0B7F : return "奥里亚文"
        if unicode <= 0x0BFF : return "泰米尔文"
        if unicode <= 0x0C7F : return "泰卢固文"
        if unicode <= 0x0CFF : return "卡纳达文"
        if unicode <= 0x0D7F : return "德拉维族语"
        if unicode <= 0x0DFF : return "僧伽罗语"
        if unicode <= 0x0E7F : return "泰文"
        if unicode <= 0x0EFF : return "老挝文"
        if unicode <= 0x0FFF : return "藏文"
        if unicode <= 0x109F : return "缅甸语"
        if unicode <= 0x10FF : return "格鲁吉亚语"
        if unicode <= 0x11FF : return "朝鲜文"
        if unicode <= 0x137F : return "埃塞俄比亚语"
        if unicode <= 0x139F : return "埃塞俄比亚语补充"
        if unicode <= 0x13FF : return "切罗基语"
        if unicode <= 0x167F : return "统一加拿大土著语音节"
        if unicode <= 0x169F : return "欧甘字母"
        if unicode <= 0x16FF : return "如尼文"
        if unicode <= 0x171F : return "塔加拉语"
        if unicode <= 0x173F : return "Hanunóo"
        if unicode <= 0x175F : return "Buhid"
        if unicode <= 0x177F : return "Tagbanwa"
        if unicode <= 0x17FF : return "高棉语"
        if unicode <= 0x18AF : return "蒙古文"
        if unicode <= 0x18FF : return "Cham"
        if unicode <= 0x194F : return "Limbu"
        if unicode <= 0x197F : return "德宏泰语"
        if unicode <= 0x19DF : return "新傣仂语"
        if unicode <= 0x19FF : return "高棉语记号"
        if unicode <= 0x1A1F : return "Buginese"
        if unicode <= 0x1A5F : return "Batak"
        if unicode <= 0x1AEF : return "Lanna"
        if unicode <= 0x1B7F : return "巴厘语"
        if unicode <= 0x1BB0 : return "巽他语"
        if unicode <= 0x1BFF : return "Pahawh Hmong"
        if unicode <= 0x1C4F : return "雷布查语"
        if unicode <= 0x1C7F : return "Ol Chiki"
        if unicode <= 0x1CDF : return "曼尼普尔语"
        if unicode <= 0x1D7F : return "语音学扩展"
        if unicode <= 0x1DBF : return "语音学扩展补充"
        if unicode <= 0x1DFF : return "结合用读音符号补充"
        if unicode <= 0x1EFF : return "拉丁文扩充附加"
        if unicode <= 0x1FFF : return "希腊语扩充"
        if unicode <= 0x206F : return "常用标点"
        if unicode <= 0x209F : return "上标及下标"
        # 货币符号
        if unicode <= 0x20CF : return "货币符号"
        if unicode <= 0x20FF : return "组合用记号"
        if unicode <= 0x214F : return "字母式符号"
        if unicode <= 0x218F : return "数字形式"
        if unicode <= 0x21FF : return "箭头"
        if unicode <= 0x22FF : return "数学运算符"
        if unicode <= 0x23FF : return "杂项工业符号"
        if unicode <= 0x243F : return "控制图片"
        if unicode <= 0x245F : return "光学识别符"
        if unicode <= 0x24FF : return "封闭式字母数字"
        if unicode <= 0x257F : return "制表符"
        if unicode <= 0x259F : return "方块元素"
        if unicode <= 0x25FF : return "几何图形"
        if unicode <= 0x26FF : return "杂项符号"
        if unicode <= 0x27BF : return "印刷符号"
        if unicode <= 0x27EF : return "杂项数学符号-A"
        if unicode <= 0x27FF : return "追加箭头-A"
        if unicode <= 0x28FF : return "盲文点字模型"
        if unicode <= 0x297F : return "追加箭头-B"
        if unicode <= 0x29FF : return "杂项数学符号-B"
        if unicode <= 0x2AFF : return "追加数学运算符"
        if unicode <= 0x2BFF : return "杂项符号和箭头"
        if unicode <= 0x2C5F : return "格拉哥里字母"
        if unicode <= 0x2C7F : return "拉丁文扩展-C"
        if unicode <= 0x2CFF : return "古埃及语"
        if unicode <= 0x2D2F : return "格鲁吉亚语补充"
        if unicode <= 0x2D7F : return "提非纳文"
        if unicode <= 0x2DDF : return "埃塞俄比亚语扩展"
        if unicode <= 0x2E7F : return "追加标点"
        if unicode <= 0x2EFF : return "CJK 部首补充"
        if unicode <= 0x2FDF : return "康熙字典部首"
        if unicode <= 0x2FFF : return "表意文字描述符"
        if unicode <= 0x303F : return "CJK 符号和标点"
        if unicode <= 0x309F : return "日文平假名"
        if unicode <= 0x30FF : return "日文片假名"
        if unicode <= 0x312F : return "注音字母"
        if unicode <= 0x318F : return "朝鲜文兼容字母"
        if unicode <= 0x319F : return "象形字注释标志"
        if unicode <= 0x31BF : return "注音字母扩展"
        if unicode <= 0x31EF : return "CJK 笔画"
        if unicode <= 0x31FF : return "日文片假名语音扩展"
        if unicode <= 0x32FF : return "封闭式 CJK 文字和月份"
        if unicode <= 0x33FF : return "CJK 兼容"
        if unicode <= 0x4DBF : return "CJK 统一表意符号扩展 A"
        if unicode <= 0x4DFF : return "易经六十四卦符号"
        # 基础汉字
        if unicode <= 0x9FBF : return "CJK 统一表意符号"
        if unicode <= 0xA48F : return "彝文音节"
        if unicode <= 0xA4CF : return "彝文字根"
        if unicode <= 0xA61F : return "Vai"
        if unicode <= 0xA6FF : return "统一加拿大土著语音节补充"
        if unicode <= 0xA71F : return "声调修饰字母"
        if unicode <= 0xA7FF : return "拉丁文扩展-D"
        if unicode <= 0xA82F : return "Syloti Nagri"
        if unicode <= 0xA87F : return "八思巴字"
        if unicode <= 0xA8DF : return "Saurashtra"
        if unicode <= 0xA97F : return "爪哇语"
        if unicode <= 0xA9DF : return "Chakma"
        if unicode <= 0xAA3F : return "Varang Kshiti"
        if unicode <= 0xAA6F : return "Sorang Sompeng"
        if unicode <= 0xAADF : return "Newari"
        if unicode <= 0xAB5F : return "越南傣语"
        if unicode <= 0xABA0 : return "Kayah Li"
        if unicode <= 0xD7AF : return "朝鲜文音节"
        # 不可见字符
        if unicode <= 0xDBFF : return "High-half zone of UTF-16"
        # 不可见字符
        if unicode <= 0xDFFF : return "Low-half zone of UTF-16"
        if unicode <= 0xF8FF : return "自行使用区域"
        if unicode <= 0xFAFF : return "CJK 兼容象形文字"
        if unicode <= 0xFB4F : return "字母表達形式"
        if unicode <= 0xFDFF : return "阿拉伯表達形式A"
        if unicode <= 0xFE0F : return "变量选择符"
        if unicode <= 0xFE1F : return "竖排形式"
        if unicode <= 0xFE2F : return "组合用半符号"
        if unicode <= 0xFE4F : return "CJK 兼容形式"
        if unicode <= 0xFE6F : return "小型变体形式"
        if unicode <= 0xFEFF : return "阿拉伯表達形式B"
        if unicode <= 0xFFEF : return "半型及全型形式"
        # 不可见字符
        if unicode <= 0xFFFF : return "特殊"
        # 返回结果
        return None

class ChineseTool :

    @staticmethod
    def wide_convert(content):
        # 检查参数
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
        assert isinstance(content, str)

        # 将&优先转换，避免后续重复叠加转换
        content = content.replace( __old = "&", __new = "&amp;")

        # 替换内容
        content = content.replace(__old = "<", __new = "&lt;")
        content = content.replace(__old = ">", __new = "&gt;")
        content = content.replace(__old = "'", __new = "&apos;")
        content = content.replace(__old = " ", __new = "&nbsp;")
        content = content.replace(__old = "\"", __new = "&quot;")

        # 返回结果
        return content

    # XML反转义
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
                    number = number.replace(__old = "l", __new = "1")
                    number = number.replace(__old = "o", __new = "0")
                    number = number.replace(__old = "O", __new = "0")
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
        assert isinstance(content, str)
        # 返回结果
        return re.sub("\\s", "", content)
    
    # 清理不可见字符
    @staticmethod
    def clear_invisible(content):
        # 检查参数
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
        newContent = ""
        # 获得索引
        index = matched.end()
        # 循环处理
        while index >= 0:
            # 检查字符
            if content[index] != value :
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
        index = matched.end() + 1
        # 循环处理
        while index < len(newContent) :
            # 检查字符
            if content[index] != value :
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