# -*- coding: utf-8 -*-
from nlp.item.ContentItem import *
from nlp.tool.UnicodeTool import *

class TokenItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None, count = 1) :
        # 调用父类初始化
        super().__init__(content, count)
        # 检查参数
        if content is not None :
            assert len(content) == 1

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "content" : self.content,
                "unicode" : ord(self.content),
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        # 检查参数
        assert ord(self.content) == value["unicode"]

    def dump(self):
        # 打印信息
        print("TokenItem.dump : show properties !")
        print(f"\tcount = {self.count}")
        print(f"\ttoken = \'{self.content}\'")
        print(f"\tunicode = {"0x%4X".format(ord(self.content))}")
        print(f"\tremark = \"{UnicodeTool.get_remark(self.content)}\"")