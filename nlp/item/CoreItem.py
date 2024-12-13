# -*- coding: utf-8 -*-
from nlp.item.ContentItem import *

class CoreItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None, count = 1) :
        # 只选取最大gamma值的分解模式
        # 设置最大值
        self.gamma = 0.0
        # 设置分解模式
        self.pattern = None
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
                "pattern" : self.pattern,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        # 检查数据
        if "gamma" in value :
            self.gamma = value["gamma"]
        if "pattern" in value :
            self.pattern = value["pattern"]
        # 检查参数
        #assert self.length == value["length"]

    def is_valid(self, max_length = -1) :
        # 返回结果
        if self.count <= 1 : return False
        if self.length <= 0 : return False
        if self.gamma < 0.00001 : return False
        if self.length > 1 and self.pattern is None : return False
        if self.length == 1 and self.pattern is not None : return False
        # 返回结果
        return Ture if max_length <= 0 else self.length <= max_length

    def dump(self):
        # 打印信息
        print("WordItem.dump : show properties !")
        print("\t", end = ""); print("length = %d" % self.length)
        print("\t", end = ""); print("count = %d" % self.count)
        print("\t", end = ""); print("content = \"%s\"" % self.content)
        print("\t", end = ""); print("gamma = %f" % self.gamma)
        print("\t", end = ""); print("pattern =\"%s\"" % self.pattern)
        print("\t", end = ""); print("sha256 = 0x%s" % self.sha256.hexdigest())
