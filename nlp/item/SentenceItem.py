# -*- coding: utf-8 -*-
from nlp.item.ContentItem import *

class SentenceItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None, count = 1, source = None) :
        # 设置参数
        self.source = source
        # 调用父类初始化函数
        super().__init__(content, count)

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "source" : self.source,
                "content" : self.content,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        # 检查参数
        if "source" in value :
            self.source = value["source"]
        #assert self.length == value["length"]

    # 打印信息
    def dump(self):
        # 打印信息
        print("SentenceItem.dump : show properties !")
        print(f"\tcount = {self.count}")
        print(f"\tlength = {self.length}")
        print(f"\tsource = \"{self.source}\"")
        print(f"\tcontent = \"{self.content}\"")
