# -*- coding: utf-8 -*-
import json

from nlp.tool.HashTool import *
from nlp.tool.ChineseTool import *

class ContentItem :
    # 初始化对象
    def __init__(self, content = None, count = 1) :
        # 设置来源
        self.count = count
        # 设置内容
        self.content = content

    # 复位
    def reset(self) :
        # 复位数据
        self.count = 0

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "content" : self.content,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        # 检查数据
        #assert self.length == value["length"]

    @property
    def length(self) :
        # 检查参数
        assert isinstance(self.content, str)
        # 返回结果
        return len(self.content)

    @property
    def sha256(self) :
        # 检查参数
        assert isinstance(self.content, str)
        # 返回结果
        return HashTool.sha256(self.content)

    # 无用
    def is_useless(self):
        # 返回结果
        return self.count <= 0

    # 检查有效性
    def is_valid(self, max_length = -1) :
        # 检查参数
        if max_length <= 0 :
            # 返回结果
            return 1 <= len(self.content)
        # 返回结果
        return 1 <= len(self.content) <= max_length

    # 非常用
    def is_rare(self):
        # 返回结果
        return UnicodeTool.is_rare(self.content)

    # 中文
    def is_chinese(self) :
        # 返回结果
        return ChineseTool.is_chinese(self.content)

    def dump(self):
        # 打印信息
        print("ContentItem.dump : show properties !")
        print("\t", end = ""); print("length = %d" % self.length)
        print("\t", end = ""); print("count = %d" % self.count)
        print("\t", end = ""); print("content = \"%s\"" % self.content)
        print("\t", end = ""); print("sha256 = 0x%s" % self.sha256.hexdigest())
