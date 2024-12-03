# -*- coding: utf-8 -*-
from nlp.item.ContentItem import *

class DictionaryItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None, count = 1) :
        # 来源与注释
        # source : remark
        self.sources = {}
        # 调用父类初始化函数
        super().__init__(content, count)

    # 是否为其来源
    def has_source(self, source) :
        # 检查参数
        assert isinstance(source, str)
        # 返回结果
        return source in self.sources.keys()

    # 增加来源
    def add_source(self, source, remark) :
        # 检查参数
        assert isinstance(source, str)
        # 检查数据
        if source not in self.sources.keys() : self.sources[source] = remark

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "content" : self.content,
                "sources" : self.sources,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        # 检查参数
        if "sources" in value :
            self.sources = value["sources"]
        #assert self.length == value["length"]

    # 打印信息
    def dump(self):
        # 打印信息
        print("DictionaryItem.dump : show properties !")
        print(f"\tlength = {self.length}")
        print(f"\tcount = {self.count}")
        print(f"\tcontent = \"{self.content}\"")
        print(f"\tsources = {str(self.sources)}")
