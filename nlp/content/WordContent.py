# -*- coding: utf-8 -*-
from nlp.item.WordItem import *
from nlp.item.ContentItem import *
from nlp.content.ContentGroup import *

class WordContent(ContentGroup) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 当前长度
        self.limit_length = 1

    # 新对象
    def new_item(self, content = None, count = 1) :
        # 返回结果
        return WordItem(content, count)

    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_item(WordItem(content))

    def add_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 检查单词
        word = item.content
        # 检查结果
        if word in self:
            # 增加计数器
            self[word].count += item.count; return
        # 检查类型
        if isinstance(item, WordItem) :
            # 增加对象
            self[word] = item
        # 检查是否为中文
        # 如果是纯中文内容，则增加数据项
        elif item.is_chinese() :
            # 增加项目
            self[word] = self.new_item(word, item.count)

    def add_splitted(self, item, need_split = True) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 生成内容
        segments = ['$' + item.content]
        # 检查标志位
        if need_split :
            # 拆分内容
            segments = SplitTool.split(item.content)
        # 循环处理
        for segment in segments :
            # 检查结果
            if segment[0] != '$' : continue
            # 获得内容
            content = segment[1 : ]
            # 循环处理
            for i in range(len(content)) :
                # 长度限定在当前长度
                if i + self.limit_length > len(content) : break
                # 获得单词
                word = content[i : i + self.limit_length]
                # 检查结果
                if word in self :
                    # 增加计数器
                    self[word].count += item.count
                # 检查是否为中文
                # 如果是纯中文内容，则增加数据项
                elif item.is_chinese() :
                    # 增加项目
                    self[word] = self.new_item(word, item.count)

    # 初始化相关系数
    def init_gammas(self) :
        # 总数
        total = len(self)
        # 进度条
        pb = ProgressBar(total)
        # 开始
        pb.begin(f"WordContent.init_gammas : init gammas[{total}] !")
        # 初始化相关系数
        for item in self.values() :
            # 进度条
            pb.increase()
            # 获得内容
            f = item.count
            c = item.content
            # 检查数值
            if f <= 0 :
                item.gamma = 0.0; continue

            # 检查数据
            assert len(c) == 2

            # 获得单词
            c1 = c[:1]
            # 检查数据
            if c1 not in self :
                # 设置为无效值
                item.gamma = 0.0; continue
            # 获得频次
            f1 = self[c1].count
            # 检查数据
            if f1 <= 0 :
                item.gamma = 0.0; continue

            # 获得单词
            c2 = c[-1]
            # 检查数据
            if c2 not in self :
                # 设置为无效值
                item.gamma = 0.0; continue
            # 获得频次
            f2 = self[c2].count
            # 检查数据
            if f2 <= 0 :
                item.gamma = 0.0; continue

            # 计算相关系数
            item.gamma = 0.5 * float(f) \
                * (1.0 / float(f1) + 1.0 / float(f2))
