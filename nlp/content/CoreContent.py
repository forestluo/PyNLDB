# -*- coding: utf-8 -*-
from nlp.item.CoreItem import *
from nlp.item.ContentItem import *
from nlp.content.ContentGroup import *

class CoreContent(ContentGroup) :
    # 新对象
    def new_item(self, content = None, count = 1) :
        # 返回结果
        return CoreItem(content, count)

    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_item(CoreItem(content))

    def add_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 获得内容
        content = item.content
        # 检查结果
        if content in self :
            # 增加计数
            self[content].count += item.count; return
        # 检查类型
        if isinstance(item, CoreItem) :
            # 增加对象
            self[content] = item
        # 检查是否为中文
        # 如果是纯中文内容，则增加数据项
        elif item.is_chinese() :
            # 增加项目
            self[content] = self.new_item(content, item.count)

    # 增加项目
    # 用于traverse函数
    def count_item(self, item, need_split = True):
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
                # 循环处理
                for length in range(1, 1 + self.max_length) :
                    # 长度限定在当前长度
                    if i + length > len(content) : break
                    # 获得子字符串
                    value = content[i : i + length]
                    # 检查结果
                    if value in self : self[value].count += item.count

    def get_gamma(self, segments) :
        # 检查参数
        assert isinstance(segments, list)
        # Gamma数值
        gamma = 0.0
        # 内容
        content = ""
        # 循环处理
        for segment in segments :
            # 增加字符
            content += segment
            # 检查字典
            if segment not in self : return -1.0
            # 获得计数
            count = self[segment].count
            # 检查结果
            if count <= 0 : return -1.0
            # 计算结果
            gamma += 1.0 / float(count)
        # 计算总值
        if not content in self : return 0.0
        # 返回结果
        return gamma * float(self[content].count) / float(len(segments))

    # 更新相关系数
    def update_gammas(self) :
        # 获得总数
        total = len(self)

        # 指定长度
        length = 0
        # 循环处理
        while True :
            # 长度加一
            length += 1
            # 标志位
            flag = False
            # 打印信息
            print("CoreContent.update_gammas : try to process !")
            print(f"\tlength = {length}")
            # 进度条
            pb = ProgressBar(total)
            # 打印数据总数
            pb.begin()
            # 循环处理
            for item in self.values() :
                # 进度条
                pb.increase()
                # 检查长度
                if item.length != length : continue
                # 设置标志位
                flag = True
                # 复位数据
                item.gamma = 0.0
                item.pattern = None
                # 检查长度
                if item.length == 1 :
                    # 直接设定
                    item.gamma = 1.0
                    item.pattern = None
                else :
                    # 重置
                    item.gamma = 0.0
                    item.pattern = None
                    # 更新数值
                    item.update_gamma(self)
            # 结束
            pb.end()
            # 打印信息
            print(f"CoreContent.update_gammas : length({length}) processed !")
            # 检查标志位
            if not flag : break
