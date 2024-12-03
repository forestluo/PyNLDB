# -*- coding: utf-8 -*-

class ChineseTool :

    @staticmethod
    def is_chinese(content) :
        # 检查参数
        assert isinstance(content, str)
        # 循环处理
        for char in content :
            if not 0x4E00 <= ord(char) <= 0x9FA5 : return False
        # 返回结果
        return True

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
        new_content = ""
        # 循环处理
        for char in content :
            # 获得Unicode
            unicode = ord(char)
            # 特殊处理
            if unicode == 12288 :
                new_content += ' '
            elif unicode < 65281 :
                new_content += char
            elif unicode > 65374 :
                new_content += char
            else :
                new_content += chr(unicode - 65248)
        # 返回结果
        return new_content
