# -*- coding: utf-8 -*-

import traceback

from Content import *
from ContentTool import *
from QuantityTool import *
from SentenceTool import *

json_path = ".\\json\\"

# 数据项目
raw_items = []
# 生成对象
raw = RawContent()
# 加载数据
if raw.load(json_path + "raw.json") > 0 :
    # 获得所有项目
    raw_items = raw.get_items()
else :
    print("OperateData.random_quantity : fail to load file !")

def random_quantity() :
    # 清理输入项目
    user_input = ""
    # 循环处理
    while user_input.lower() != '0':
        # 获得随机数
        index = random.randint(0, len(raw_items))
        # 获得内容
        original = raw_items[index].content
        normalized = ContentTool.normalize_content(original)
        # 打印结果
        print("OperateData.random_quantity : normalized result !")
        print("\t", end = ""); print("original   =\"%s\"" % original)
        print("\t", end = ""); print("normalized =\"%s\"" % normalized)
        # 提取数量词
        group = QuantityTemplate.extract(normalized)
        # 检查结果
        if group is not None :
            # 打印信息
            group.dump()
        else :
            # 打印信息
            print("OperateData.random_quantity : no matched !")
        # 继续选择输入
        user_input = input("Enter '0' to exit : ")

def random_sentence() :
    # 清理输入项目
    user_input = ""
    # 循环处理
    while user_input.lower() != '0':
        # 获得随机数
        index = random.randint(0, len(raw_items))
        # 获得内容
        original = raw_items[index].content
        normalized = ContentTool.normalize_content(original)
        # 打印结果
        print("OperateData.random_sentence : normalized result !")
        print("\t", end = ""); print("original   =\"%s\"" % original)
        print("\t", end = ""); print("normalized =\"%s\"" % normalized)
        # 打散和标记
        segments = SentenceTool.split(normalized)
        # 打印结果
        print("OperateData.random_sentence : split result !")
        # 打印结果
        for segment in segments: print("\t%s" % segment)
        # 合并
        segments = SentenceTool.merge(segments)
        # 打印结果
        print("OperateData.random_sentence : merged result !")
        # 打印结果
        for segment in segments: print("\t%s" % segment)
        # 继续选择输入
        user_input = input("Enter '0' to exit : ")

def update_core_gammas() :
    # 生成对象
    cores = CoreContent()
    # 加载数据
    if cores.load(json_path + "cores.json") <= 0 :
        print("OperateData.update_core_gammas : fail to load file !")
    # 更新数据
    cores.update_gammas()
    # 保存数据
    cores.save(json_path + "cores.json")

def main() :
    # 选项
    options = \
        [
            "exit",
            "random quantity",
            "random sentence",
            "update core gammas",
            "get gamma by words",
        ]

    # 提示信息
    inputMessage = "Please pick an option :\n"
    # 打印选项
    for index, item in enumerate(options) :
        inputMessage += f"{index}) {item}\n"
    # 打印提示
    inputMessage += "Your choice : "

    # 循环处理
    while True :
        # 清理输入项目
        userInput = ""
        # 循环处理
        while userInput.lower() \
                not \
                in map(str, range(0, len(options))) :
            # 继续选择输入
            userInput = input(inputMessage)
        # 开始执行
        if userInput == '0' :
            # 打印信息
            print("OperateData.main : user exit !"); break
        elif userInput == '1' :
            # 随机选择一条内容，提取数量词
            random_quantity()
        elif userInput == '2' :
            # 随机选择一条内容，拆分成句子
            random_sentence()
        elif userInput == '3' :
            # 更新Gamma数值
            update_core_gammas()
        else :
            print("OperateData.main : unknown choice !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("OperateData.main :__main__ : ", str(e))
        print("OperateData.main :__main__ : unexpected exit !")