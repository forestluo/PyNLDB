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

    # 更新Gamma数值
    def update_gamma(self, cores) :
        # 检查参数
        assert cores is not None
        # 长度小于1，则返回空
        if self.length < 1 : return
        # 长度为1，则设置gamma为1.0
        if self.length == 1 : self.gamma = 1.0; return
        # 已更新过的内容，则不再更新
        if self.gamma > 0 and self.pattern is not None : return

        # 结果
        gammas = {}
        # 循环处理
        for i in range(1, len(self.content)) :
            # 获得gamma数值
            gamma = cores.get_gamma([self.content[0:i], self.content[i:]])
            # 检查结果
            if gamma <= 0 : continue
            # 移动分隔符
            gammas[self.content[0:i] + '|' + self.content[i:]] = gamma
        # 循环处理
        for i in range(1, len(self.content)) :
            for j in range(i + 1, len(self.content)) :
                # 部分
                gamma = cores.get_gamma([self.content[0:i], self.content[i:j], self.content[j:]])
                # 检查结果
                if gamma <= 0 : continue
                # 移动分隔符
                gammas[self.content[0:i] + '|' + self.content[i:j] + '|' + self.content[j:]] = gamma
        # 循环处理
        for i in range(1, len(self.content)) :
            for j in range(i + 1, len(self.content)) :
                for k in range(j + 1, len(self.content)) :
                    # 部分
                    gamma = cores.get_gamma([self.content[0:i], self.content[i:j], self.content[j:k], self.content[k:]])
                    # 检查结果
                    if gamma <= 0 : continue
                    # 移动分隔符
                    gammas[self.content[0:i] + '|' + self.content[i:j] + '|' + self.content[j:k] + '|' + self.content[k:]] = gamma
        # 排序
        self.gamma = 0.0
        # 循环处理
        # 选择Gamma值最大的一组数据
        for (key, value) in gammas.items() :
            # 检查结果
            if value > self.gamma : self.gamma = value; self.pattern = key
