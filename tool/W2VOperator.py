# -*- coding: utf-8 -*-
import threading

from nlp.alg.Word2Vector import *

# 路径
json_path = "..\\json\\"
# 生成对象
w2v = Word2Vector(32)

def auto_initialize() :
    # 加载数文件
    if not w2v.initialize(json_path) :
        # 打印信息
        print("W2VOperator.auto_initialize : fail to load files !")
    else :
        # 打印信息
        print("W2VOperator.auto_initialize : all files have been loaded !")

def load_example() :
    # 加载例程数据
    w2v.load_example()
    # 打印信息
    print("W2VOperator.load_example : example was loaded !")

def load_words() :
    # 加载数文件
    if w2v.load_words(json_path + "words2.json") <= 0 :
        # 打印信息
        print("W2VOperator.load_words : fail to load file !")
        return
    else :
        # 打印信息
        print("W2VOperator.load_words : words2.json has been loaded !")

def load_cores() :
    # 加载数文件
    if w2v.load_words(json_path + "cores.json") <= 0 :
        # 打印信息
        print("W2VOperator.load_cores : fail to load file !")
        return
    else :
        # 打印信息
        print("W2VOperator.load_cores : cores.json has been loaded !")

def load_dictionary() :
    # 加载数文件
    if w2v.load_words(json_path + "dictionary.json") <= 0 :
        # 打印信息
        print("W2VOperator.load_dictionary : fail to load file !")
        return
    else :
        # 打印信息
        print("W2VOperator.load_dictionary : dictionary.json has been loaded !")

def save_vectors() :
    # 加载数文件
    w2v.save(json_path + "vectors.json")
    # 打印信息
    print("W2VOperator.save_vectors : vectors.json has been saved !")

def load_vectors() :
    # 加载数文件
    if w2v.load_vectors(json_path + "vectors.json") <= 0 :
        # 打印信息
        print("W2VOperator.load_vectors : fail to load file !")
        return
    else :
        # 打印信息
        print("W2VOperator.load_vectors : vectors.json has been loaded !")

def solving_vectors() :
    # 解算方法
    solution = None
    # 循环处理
    while True :
        # 继续选择输入
        user_input = \
            input("Enter '0' to exit : ")
        # 打印
        print("")
        # 小写
        user_input = \
            user_input.lower()
        # 检查输入结果
        if user_input == '0' :
            # 检查方法
            if solution is not None \
                and solution.is_alive() :
                # 停止
                solution.stop()
                # 设置标记
                w2v.copy_data = True
                # 打印信息
                print("Word2Vector.solving_vectors : thread has been stopped !")
            return
        else :
            # 检查参数
            if solution is not None \
                and solution.is_alive() :
                # 打印信息
                print("W2VOperator.solving_vectors : thread is alive !")
                continue
            # 检查状态
            if solution is None \
                or not solution.is_alive() :
                # 获得求解器
                solution = w2v.get_solution(user_input)
                # 检查结果
                if solution is None :
                    # 打印信息
                    print("W2VOperator.solving_vectors : fail to get solution !")
                else :
                    # 启动
                    solution.start()
                    # 打印信息
                    print("W2VOperator.solving_vectors : successfully start solving !")

def verify_vectors() :
    # 清理输入项目
    user_input = ""
    # 循环处理
    while user_input.lower() != '0' :
        # 继续选择输入
        user_input = input("Enter '0' to exit : ")
        # 检查长度
        if len(user_input) != 2 : continue
        # 检查数据
        gamma = 0.0
        # 获得词汇描述
        word = w2v.word(user_input)
        # 检查结构
        if word is not None :
            # 设置相关系数
            gamma = word.gamma

        w1 = user_input[:1]
        # 获得矢量
        v1 = w2v.vector(w1)
        # 检查结果
        if v1 is not None :
            v1.dump(dump_matrix = False)
        else :
            print(f"\tw1 = \"{w1}\"")
            print(f"\tf1 = ...invalid word...")

        w2 = user_input[-1]
        # 获得矢量
        v2 = w2v.vector(w2)
        # 检查结果
        if v2 is not None :
            v2.dump(dump_matrix = False)
        else :
            print(f"\tw2 = \"{w2}\"")
            print(f"\tf2 = ...invalid word...")

        # 检查结果
        if word is not None :
            # 打印数据
            word.dump()
        else :
            # 打印信息
            print("W2VOperator.verify_vectors : invalid input !")

        # 打印信息
        print("W2VOperator.verify_vectors : show results !")
        print(f"\tGamma12 (from words) = {gamma}")
        if v1 is not None and v2 is not None :
            print(f"\tGamma12 (from vector calculation) ="
                  f"{VectorItem.get_gamma(v1, v2, w2v.dimension)}")

def main() :
    # 选项
    options = \
        [
            "exit",
            "load words",
            "load cores",
            "load example",
            "load dictionary",
            "load vectors",
            "save vectors",
            "auto initialize",
            "solving vectors",
            "verify vectors",
        ]

    # 提示信息
    input_message = "Please pick an option :\n"
    # 打印选项
    for index, item in enumerate(options) :
        input_message += f"{index}) {item}\n"
    # 打印提示
    input_message += "Your choice : "

    # 循环处理
    while True :
        # 清理输入项目
        user_input = ""
        # 循环处理
        while user_input.lower() \
                not in map(str, range(0, len(options))) :
            # 继续选择输入
            user_input = input(input_message)
        # 开始执行
        if user_input == '0' :
            # 打印信息
            print("W2VOperator.main : user exit !"); break
        elif user_input == '1' :
            # 加载
            load_words()
        elif user_input == '2' :
            # 加载
            load_cores()
        elif user_input == '3' :
            # 加载
            load_example()
        elif user_input == '4' :
            # 加载
            load_dictionary()
        elif user_input == '5' :
            # 加载
            load_vectors()
        elif user_input == '6' :
            # 保存
            save_vectors()
        elif user_input == '7' :
            # 初始化
            auto_initialize()
        elif user_input == '8':
            # 迭代计算
            solving_vectors()
        elif user_input == '9':
            # 验算
            verify_vectors()
        else :
            print("W2VOperator.main : unknown choice !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("W2VOperator.main :__main__ : ", str(e))
        print("W2VOperator.main :__main__ : unexpected exit !")