# -*- coding: utf-8 -*-
import re

class ClearTool :
    # 预编译
    _compiled = re.compile(
        "([\x00-\x1F]|\x7F|\u1680|\u180E|[\u2000-\u200D]|[\u2028-\u2029]|\u202F|[\u205F-\u2060]|\u3000|[\uD7B0-\uF8FF]|\uFEFF|[\uFFF0-\uFFFF])+")

    # 清理空格
    @staticmethod
    def clear_blank(content) :
        # 检查参数
        assert isinstance(content, str)
        # 返回结果
        return re.sub("\\s", "", content)

    # 清理不可见字符
    @staticmethod
    def clear_invisible(content) :
        # 检查参数
        assert isinstance(content, str)
        # 返回结果
        return ClearTool._compiled.sub(" ", content)
