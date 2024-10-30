# -*- coding: utf-8 -*-

import os
import ast
import random
import traceback

from BPNetwork import *
from WordContent import *
from DictionaryContent import *

# 数据文件
json_path = ".\\json\\"

# 误差
error = 0.001
# 隐藏层数量
hidden_count = 12
# 学习率
learning_rate = 0.008

# 词汇
words = WordContent()
# 字典
dictionary = DictionaryContent()

def load_data() :
    # 加载words1.json
    words.load(json_path + "words1.json")
    # 加载words2.json
    words.load(json_path + "words2.json")
    # 记载dictionary.json
    dictionary.load(json_path + "dictionary.json")

def verify_neuron(content) :
    assert isinstance(content, str)
    assert len(content) == 2
    assert ChineseTool.is_chinese(content)

    # 输入项
    inputs = []
    # 循环处理
    for i in range(3):
        # 获得一个随机字符
        token = content[i] \
            if i < 2 else content
        # 检查数据
        # 获得统计次数
        if token in words:
            inputs.append(words[token])
        else :
            inputs.append(WordItem(token))
    # 打印信息
    print("DataTraining.verify_neuron : print result !")
    print("\terror = %f" % error)
    print("\thidden_count = %d" % hidden_count)
    print("\tlearning_rate = %f" % learning_rate)
    # 生成神经元
    neuron = Neuron()
    # 加载数据
    neuron.load("neuron.json")
    # 设置输入
    neuron.inputs = WordCoach.transform(inputs)
    # 向前传播
    neuron.forward()
    # 获得结果
    outputs = neuron.outputs
    # 打印结果
    print("\tresult = " + str(outputs))

def random_training() :
    # 打印信息
    print("DataTraining.random_training : print result !")
    print("\terror = %f" % error)
    print("\thidden_count = %d" % hidden_count)
    print("\tlearning_rate = %f" % learning_rate)
    # 创建神经元
    neuron = WordCoach.get_neuron(hidden_count, learning_rate)

    # 训练次数
    count = 0
    total = 100000
    # 百分之一
    percent = 0
    onePercent = total / 100.0

    # 训练次数
    training_count = 0
    # 正向
    positive_count = 0
    # 循环处理
    while count < total:
        # 输入项
        inputs = []
        # 循环处理
        for i in range(3):
            # 获得一个随机字符
            token = ChineseTool.randchr() \
                if i < 2 else inputs[0].word + inputs[1].word
            # 检查数据
            # 获得统计次数
            if token in words:
                inputs.append(words[token])
            else:
                inputs.append(WordItem(token))

        # 输出值
        output = 0.0
        # 检查字典
        if inputs[2].word in dictionary : output = 1.0; positive_count += 1

        # 训练神经元
        training_count += WordCoach.training(neuron, inputs, output, error)

        # 计数器加一
        count += 1
        # 检查结果
        if count >= (percent + 1) * onePercent:
            # 增加百分之一
            percent = percent + 1
            # 打印进度条
            print("\r", end="")
            print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
            sys.stdout.flush()

    print("")
    print("DataTraining.random_training : average training count !")
    print("\tpositive_count = %d" % positive_count)
    print("\taverage_training_count = %f" % (training_count / float(total)))
    # 显示数据
    neuron.save("neuron.json")

def dictionary_training() :
    # 打印信息
    print("DataTraining.dictionary_training : print result !")
    print("\terror = %f" % error)
    print("\thidden_count = %d" % hidden_count)
    print("\tlearning_rate = %f" % learning_rate)
    # 创建神经元
    neuron = WordCoach.get_neuron(hidden_count, learning_rate)

    # 获得项目
    items = dictionary.get_items(2)

    # 训练次数
    count = 0
    total = len(items)
    # 百分之一
    percent = 0
    onePercent = total / 100.0

    # 训练次数
    training_count = 0
    # 循环处理
    for item in items :
        # 输入项
        inputs = []
        # 循环处理
        for i in range(3):
            # 获得一个随机字符
            token = item.content[i] \
                if i < 2 else item.content
            # 获得统计次数
            if token in words:
                inputs.append(words[token])
            else:
                inputs.append(WordItem(token))

        # 输出值
        output = 0.0
        # 检查字典
        if inputs[2].word in dictionary : output = 1.0;

        # 训练神经元
        training_count += WordCoach.training(neuron, inputs, output, error)

        # 计数器加一
        count += 1
        # 检查结果
        if count >= (percent + 1) * onePercent:
            # 增加百分之一
            percent = percent + 1
            # 打印进度条
            print("\r", end="")
            print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
            sys.stdout.flush()

    print("")
    print("DataTraining.random_training : average training count !")
    print("\taverage_training_count = %f" % (training_count / float(total)))
    # 显示数据
    neuron.save("neuron.json")

def main() :

    # 选项
    options = \
        [
            "exit",
            "hidden count [4 - 20]",
            "error [0.1 - 0.000001]",
            "training rate [0.000001 - 1.0]",
            "random training",
            "dictionary training",
            "verify training result",
        ]

    # 提示信息
    inputMessage = "Please pick an option :\n"
    # 打印选项
    for index, item in enumerate(options) :
        inputMessage += f"{index}) {item}\n"
    # 打印提示
    inputMessage += "Your choice : "

    # 加载数据
    load_data()

    # 循环处理
    while True :
        # 清理输入项目
        userInput = ""
        # 循环处理
        while userInput.lower() \
                not in map(str, range(0, len(options))) :
            # 继续选择输入
            userInput = input(inputMessage)
        # 开始执行
        if userInput == '0' :
            # 打印信息
            print("DataTraining.main : user exit !"); break
        elif userInput == '1' :
            # 获得隐藏层数量
            userInput = input(options[1] + " : ")
            # 获得数值
            global hidden_count
            hidden_count = int(ast.literal_eval(userInput))
        elif userInput == '2':
            # 获得误差
            userInput = input(options[2] + " : ")
            # 获得数值
            global error
            error = ast.literal_eval(userInput)
        elif userInput == '3':
            # 获得学习率
            userInput = input(options[3] + " : ")
            # 获得数值
            global learning_rate
            learning_rate = ast.literal_eval(userInput)
        elif userInput == '4':
            # 集中训练一次
            random_training()
        elif userInput == '5':
            # 集中训练一次
            dictionary_training()
        elif userInput == '6':
            # 获得词汇
            userInput = input(options[6] + " : ")
            # 检查输入
            if len(userInput) == 2 \
                    and ChineseTool.is_chinese(userInput) : verify_neuron(userInput)
        else :
            print("DataTraining.main : unknown choice !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("DataTraining.main :__main__ : ", str(e))
        print("DataTraining.main :__main__ : unexpected exit !")