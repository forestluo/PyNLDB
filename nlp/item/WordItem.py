# -*- coding: utf-8 -*-
from nlp.item.ContentItem import *

class WordItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None, count = 1) :
        # 设置相关系数
        # 主要用于临时计算
        self.gamma = -1.0
        # 调用父类初始化函数
        super().__init__(content, count)

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "content" : self.content,
                "gamma" : self.gamma,
            }

    @json.setter
    def json(self, value) :
        self.count = value["count"]
        self.content = value["content"]
        if "gamma" in value :
            self.gamma = value["gamma"]
        #assert self.length == value["length"]

    def dump(self) :
        # 打印信息
        print("WordItem.dump : show properties !")
        print(f"\tlength = {self.length}")
        print(f"\tcount = {self.count}")
        print(f"\tcontent = \"{self.content}\"")
        print(f"\tgamma = {self.gamma}")
