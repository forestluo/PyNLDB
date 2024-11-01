# -*- coding: utf-8 -*-

import traceback

from Content import *
from ContentTool import *
from NLDB3Content import *

json_path = ".\\json\\"

def update_gammas_13() :
    # 加载数据
    words = WordContent()
    # 加载words1.json
    words.load(json_path + "words1.json")
    # 加载words2.json
    words.load(json_path + "words2.json")
    # 更新Gamma数值
    words.update_gammas()
    # 加载words3.json
    words.load(json_path + "words3.json")
    # 更新Gamma数值
    words.update_gammas()
    # 保存文件
    words.save(json_path + "words13.json")

def update_gammas_18() :
    # 加载数据
    words = WordContent()
    # 加载words1.json
    words.load(json_path + "words13.json")
    # 加载words4.json
    words.load(json_path + "words4.json")
    # 更新Gamma数值
    words.update_gammas()
    # 加载words5.json
    words.load(json_path + "words5.json")
    # 更新Gamma数值
    words.update_gammas()
    # 加载words6.json
    words.load(json_path + "words6.json")
    # 更新Gamma数值
    words.update_gammas()
    # 加载words7.json
    words.load(json_path + "words7.json")
    # 更新Gamma数值
    words.update_gammas()
    # 加载words7.json
    words.load(json_path + "words8.json")
    # 更新Gamma数值
    words.update_gammas()
    # 保存文件
    words.save(json_path + "words18.json")

def random_quantity() :
    # 建立数据库链接
    raw = NLDB3Raw()
    # 打开数据库链接
    raw.open()
    # 随机抽取一条记录
    data = raw.random()
    # 关闭数据库链接
    raw.close()
    # 处理数据
    content = ContentTool.normalize_content(data["content"])
    # 打印结果
    print("OperateData.random_quantity : normalized result !")
    print("\toriginal   =\"%s\"" % data["content"])
    print("\tnormalized =\"%s\"" % content)

    # 提取数量词
    group = QuantityTemplate.extract(content)
    # 检查结果
    if group is not None :
        # 打印信息
        group.dump()
    else :
        # 打印信息
        print("OperateData.random_quantity : no matched !")

def random_sentence() :
    # 建立数据库链接
    raw = NLDB3Raw()
    # 打开数据库链接
    raw.open()
    # 随机抽取一条记录
    data = raw.random()
    # 关闭数据库链接
    raw.close()
    # 处理数据
    content = ContentTool.normalize_content(data["content"])
    # 打印结果
    print("OperateData.random_sentence : normalized result !")
    print("\toriginal   =\"%s\"" % data["content"])
    print("\tnormalized =\"%s\"" % content)

    # 打散和标记
    segments = SentenceTool.split(content)
    # 打印结果
    print("OperateData.random_sentence : split result !")
    # 打印结果
    for segment in segments : print("\t%s" % segment)

    # 合并
    segments = SentenceTool.merge(segments)
    # 打印结果
    print("OperateData.random_sentence : merged result !")
    # 打印结果
    for segment in segments : print("\t%s" % segment)

def main() :

    # 选项
    options = \
        [
            "exit",
            "random quantity",
            "random sentence",
            "update gammas words[1 - 3]",
            "update gammas words[1 - 8]",
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
            update_gammas_13()
        elif userInput == '4':
            # 更新Gamma数值
            update_gammas_18()
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