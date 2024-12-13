# -*- coding: utf-8 -*-
import random
import threading

from nlp.tool.GammaTool import *
from nlp.tool.SegmentTool import *
from nlp.content.WordContent import *

# 路径
json_path = "..\\json\\"
# 生成对象
cores = CoreContent()
# 加载基础数据
def load_cores() :
    # 清理
    cores.clear()
    # 加载数文件
    if cores.load(json_path + "cores.json") <= 0 :
        # 打印信息
        print("SegmentExample.load_cores : fail to load file !")
        return False
    else :
        # 打印信息
        print("SegmentExample.load_cores : cores.json has been loaded !")
    # 更新相关系数
    GammaTool.update_gammas(cores)
    # 打印信息
    print("SegmentExample.load_cores : gammas has been updated !")
    # 保存文件
    cores.save(json_path + "cores.json")
    # 打印信息
    print("SegmentExample.load_cores : gammas has been saved !")
    # 返回结果
    return True

def main() :
    # 加载数据
    if not load_cores() : return
    # 循环处理
    while True :
        # 等待输入
        user_input = input("Enter '0' to exit : ")
        # 开始执行
        if user_input == '0' :
            # 打印信息
            print("SegmentExample.main : user exit !"); break
        # 检查长度
        if len(user_input) < 2 : continue

        # 打印信息
        print("SegmentExample.main : max match(l2r) !")
        # 从左至右，最大匹配法
        segments = SegmentTool.l2r(cores, user_input)
        # 获得相关系数值
        gamma = GammaTool.get_gamma(cores, segments)
        # 打印信息
        print(f"\tgamma = {gamma}")
        # 打印数据
        for index, segment in enumerate(segments) :
            # 获得对应词汇
            word = cores[segment]
            # 打印数据
            print(f"\t[{index}](\"{segment}\" : {word.count}) = (\"{word.pattern}\", {word.gamma})")

        # 打印信息
        print("SegmentExample.main : max match(r2l) !")
        # 从左至右，最大匹配法
        segments = SegmentTool.r2l(cores, user_input)
        # 获得相关系数值
        gamma = GammaTool.get_gamma(cores, segments)
        # 打印信息
        print(f"\tgamma = {gamma}")
        # 打印数据
        for index, segment in enumerate(segments) :
            # 获得对应词汇
            word = cores[segment]
            # 打印数据
            print(f"\t[{index}](\"{segment}\" : {word.count}) = (\"{word.pattern}\", {word.gamma})")

        # 打印信息
        print("SegmentExample.main : max match(mid) !")
        # 获得长度
        length = len(user_input)
        # 获得随机索引值
        index = random.randint(0, length - 1)
        # 打印信息
        print(f"\tindex = {index}")
        # 中分最大匹配法
        segments = SegmentTool.mid(cores, user_input, index)
        # 获得相关系数值
        gamma = GammaTool.get_gamma(cores, segments)
        # 打印信息
        print(f"\tgamma = {gamma}")
        # 打印数据
        for index, segment in enumerate(segments) :
            # 获得对应词汇
            word = cores[segment]
            # 打印数据
            print(f"\t[{index}](\"{segment}\" : {word.count}) = (\"{word.pattern}\", {word.gamma})")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("SegmentExample.main :__main__ : ", str(e))
        print("SegmentExample.main :__main__ : unexpected exit !")