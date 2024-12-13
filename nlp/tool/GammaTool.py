# -*- coding: utf-8 -*-

from widget.ProgressBar import *

from nlp.item.CoreItem import *
from nlp.item.ContentItem import *
from nlp.content.CoreContent import *
from nlp.content.ContentGroup import *

class GammaTool :

    # 获得相关系数值
    # 分词方式已经指定
    @staticmethod
    def get_gamma(contents, segments) :
        # Gamma数值
        gamma = 0.0
        # 内容
        content = ""
        # 循环处理
        for segment in segments :
            # 增加字符
            content += segment
            # 检查字典
            if segment not in contents : return -1.0
            # 获得计数
            count = contents[segment].count
            # 检查结果
            if count <= 0 : return -1.0
            # 计算结果
            gamma += 1.0 / float(count)
        # 计算总值
        if not content in contents : return 0.0
        # 返回结果
        return gamma * float(contents[content].count) / float(len(segments))

    # 最大相关系数值
    # 分词方式未指定，最多四段
    @staticmethod
    def get_max_gamma(contents, segment) :
        # 获得长度
        length = len(segment)
        # 长度小于1，则返回空
        if length <= 1 : return -1.0

        # 结果
        max_gamma = 0.0
        # 循环处理
        for i in range(1, length) :
            # 获得gamma数值
            gamma = GammaTool.get_gamma(contents,
                    [segment[0:i], segment[i:]])
            # 检查结果
            if gamma <= 0.0 : continue
            # 移动分隔符
            if gamma > max_gamma : max_gamma = gamma
        # 循环处理
        for i in range(1, length) :
            for j in range(i + 1, length) :
                # 部分
                gamma = GammaTool.get_gamma(contents,
                    [segment[0:i], segment[i:j], segment[j:]])
                # 检查结果
                if gamma <= 0 : continue
                # 移动分隔符
                if gamma > max_gamma : max_gamma = gamma
        # 循环处理
        for i in range(1, length) :
            for j in range(i + 1, length) :
                for k in range(j + 1, length) :
                    # 部分
                    gamma = GammaTool.get_gamma(contents,
                    [segment[0:i], segment[i:j], segment[j:k], segment[k:]])
                    # 检查结果
                    if gamma <= 0 : continue
                    # 移动分隔符
                    if gamma > max_gamma : max_gamma = gamma
        # 返回结果
        return max_gamma

    @staticmethod
    def update_gammas(contents) :
        # 获得总数
        total = len(contents)
        # 检查参数
        assert total > 0
        # 检查参数
        assert isinstance(contents, CoreContent)

        # 指定长度
        length = 0
        # 循环处理
        while True :
            # 长度加一
            length += 1
            # 标志位
            flag = False
            # 打印信息
            print("GammaTool.update_gammas : try to process !")
            print(f"\tlength = {length}")
            # 进度条
            pb = ProgressBar(total)
            # 打印数据总数
            pb.begin()
            # 循环处理
            for item in contents.values() :
                # 进度条
                pb.increase()
                # 检查长度
                if item.length != length : continue
                # 设置标志位
                flag = True
                # 复位数据
                item.pattern = None
                # 检查长度
                if item.length == 1 :
                    # 直接设定
                    item.gamma = 1.0
                else :
                    # 重置
                    item.gamma = 0.0
                    # 更新数值
                    GammaTool.update_gamma(contents, item)
            # 结束
            pb.end()
            # 打印信息
            print(f"GammaTool.update_gammas : length({length}) processed !")
            # 检查标志位
            if not flag : break

    @staticmethod
    def update_gamma(contents, item) :
        # 检查参数
        assert isinstance(item, CoreItem)
        assert isinstance(contents, ContentGroup)
        # 长度小于1，则返回空
        if item.length < 1 : return
        # 长度为1，则设置gamma为1.0
        if item.length == 1 : item.gamma = 1.0; return
        # 已更新过的内容，则不再更新
        if item.gamma > 0 and item.pattern is not None : return

        # 结果
        gammas = {}
        # 循环处理
        for i in range(1, len(item.content)) :
            # 获得gamma数值
            gamma = GammaTool.get_gamma(contents,
            [item.content[0:i], item.content[i:]])
            # 检查结果
            if gamma <= 0 : continue
            # 移动分隔符
            gammas[item.content[0:i] + '|' + item.content[i:]] = gamma
        # 循环处理
        for i in range(1, len(item.content)) :
            for j in range(i + 1, len(item.content)) :
                # 部分
                gamma = GammaTool.get_gamma(contents,
                [item.content[0:i], item.content[i:j], item.content[j:]])
                # 检查结果
                if gamma <= 0 : continue
                # 移动分隔符
                gammas[item.content[0:i] + '|' + item.content[i:j] + '|' + item.content[j:]] = gamma
        # 循环处理
        for i in range(1, len(item.content)) :
            for j in range(i + 1, len(item.content)) :
                for k in range(j + 1, len(item.content)) :
                    # 部分
                    gamma = GammaTool.get_gamma(contents,
                    [item.content[0:i], item.content[i:j], item.content[j:k], item.content[k:]])
                    # 检查结果
                    if gamma <= 0 : continue
                    # 移动分隔符
                    gammas[item.content[0:i] + '|' + item.content[i:j] + '|' + item.content[j:k] + '|' + item.content[k:]] = gamma
        # 排序
        item.gamma = 0.0
        # 循环处理
        # 选择Gamma值最大的一组数据
        for (key, value) in gammas.items() :
            # 检查结果
            if value > item.gamma : item.gamma = value; item.pattern = key
