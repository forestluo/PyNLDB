# -*- coding: utf-8 -*-
import threading

from nlp.alg.VectorContent import *

# 路径
json_path = "..\\json\\"
# 生成对象
vectors = VectorContent(128)

def init_vectors() :
    # 加载数文件
    if not vectors.init_data(json_path) :
        # 打印信息
        print("Word2Vector.init_vectors : fail to load files !")
    else :
        # 打印信息
        print("Word2Vector.init_vectors : all files have been loaded !")

def load_vectors() :
    # 清理
    vectors.clear()
    # 加载数文件
    if vectors.load(json_path + "vectors.json") <= 0 :
        # 打印信息
        print("Word2Vector.load_vectors : fail to load file !")
        return
    else :
        # 打印信息
        print("Word2Vector.load_vectors : vectors.json has been loaded !")
    # 清理
    vectors.clear_words()
    # 加载数文件
    if vectors.load_words(json_path + "words2.json") <= 0 :
        # 打印信息
        print("Word2Vector.load_vectors : fail to load file !")
        return
    else :
        # 打印信息
        print("Word2Vector.load_vectors : vectors.json has been loaded !")

def save_vectors() :
    # 加载数文件
    vectors.save(json_path + "vectors.json")
    # 打印信息
    print("Word2Vector.save_vectors : vectors.json has been saved !")

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
        word = vectors.get_word(user_input)
        # 检查结构
        if word is not None :
            # 设置相关系数
            gamma = word.gamma

        w1 = user_input[0]
        # 检查结果
        if w1 in vectors :
            vectors[w1].dump(dump_delta = False)
        else :
            print(f"\tw1 = \"{w1}\"")
            print(f"\tf1 = ...invalid word...")

        w2 = user_input[-1]
        # 检查结果
        if w2 in vectors :
            vectors[w2].dump(dump_delta = False)
        else :
            print(f"\tw2 = \"{w2}\"")
            print(f"\tf2 = ...invalid word...")

        # 检查结果
        if word is not None :
            # 打印数据
            word.dump()
        else :
            # 打印信息
            print("Word2Vector.verify_vectors : invalid input !")

        # 打印信息
        print("Word2Vector.verify_vectors : show results !")
        print(f"\tGamma12 (from words) = {gamma}")
        if w1 in vectors and w2 in vectors :
            print(f"\tGamma12 (from vector calculation) = {VectorItem.cal_gamma(vectors[w1], vectors[w2])}")

def _solving(name, algorithm = 0) :
    # 求解
    max_delta = vectors.solving(algorithm)
    # 检查结果
    if max_delta > 1.0e-5 :
        # 打印信息
        print(f"Word2Vector._solving(\"{name}\") : fail to solve !")
    else :
        print(f"Word2Vector._solving(\"{name}\") : successfully done !")
    # 保存数据
    vectors.save(json_path + "vectors.json")

def solving(algorithm = 0) :
    # 检查参数
    if len(vectors) <= 0 :
        # 打印信息
        print("Word2Vector.solving : insufficient vectors !")
        return

    # 名称
    # 检查参数
    if algorithm == 1 : name = "L₁"
    elif algorithm == 2 : name = "L₂"
    elif algorithm >= 3 : name = "L∞"
    else : name = "classic"

    # 生成线程
    thread = threading.Thread(target = _solving, args = (name, algorithm))
    # 启动线程
    thread.start()
    # 继续选择输入
    while True :
        # 等待输入
        user_input = input("Enter '0' to exit : ")
        # 检查结果
        if user_input == '0' :
            vectors.break_loop = True; break
    # 等待线程停止
    thread.join()
    # 清理标记
    vectors.break_loop = False
    # 打印信息
    print("Word2Vector.solving : thread stopped !")

def calculation_example(algorithm = 0):
    # 生成对象
    vectors.clear()

    # 生成对象
    v1 = vectors.new_item("运", 937002)
    vectors.add_item(v1)

    # 生成对象
    v2 = vectors.new_item("动", 2363927)
    vectors.add_item(v2)

    vectors.add_word("运运", 343)
    vectors.add_word("动动", 1753)
    vectors.add_word("运动", 175908)
    vectors.add_word("动运", 1122)

    # 名称
    # 检查参数
    if algorithm == 1 : name = "L₁"
    elif algorithm == 2 : name = "L₂"
    elif algorithm >= 3 : name = "L∞"
    else : name = "classic"

    # 打印数据
    for item in vectors.values() : item.dump(dump_delta = False)
    # 设置标记位
    vectors.init_matrix = True
    # 求解
    if vectors.solving(algorithm) > 1.0e-5 :
        print(f"Word2Vector.calculation_example(\"{name}\") : fail to solve !")
    else :
        print(f"Word2Vector.calculation_example(\"{name}\") : successfully done !")
    # 打印数据
    for item in vectors.values() : item.dump(dump_delta = False)

def main() :
    # 选项
    options = \
        [
            "exit",
            "init vectors",
            "load vectors",
            "save vectors",
            "L₁ solving vectors",
            "L₂ solving vectors",
            "L∞ solving vectors",
            "verify vectors",
            "L₁ calculation example",
            "L₂ calculation example",
            "L∞ calculation example",
            "classic calculation example",
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
            print("Word2Vector.main : user exit !"); break
        elif user_input == '1' :
            # 初始化
            init_vectors()
        elif user_input == '2' :
            # 加载
            load_vectors()
        elif user_input == '3' :
            # 保存
            save_vectors()
        elif user_input == '4' :
            # 求解
            solving(1)
        elif user_input == '5' :
            # 求解
            solving(2)
        elif user_input == '6' :
            # 梯度下降法
            solving(3)
        elif user_input == '7' :
            # 验证
            verify_vectors()
        elif user_input == '8' :
            # 计算例子
            calculation_example(1)
        elif user_input == '9' :
            # 计算例子
            calculation_example(2)
        elif user_input == '10':
            # 计算例子
            calculation_example(3)
        elif user_input == '11':
            # 计算例子
            calculation_example(0)
        else :
            print("Word2Vector.main : unknown choice !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("Word2Vector.main :__main__ : ", str(e))
        print("Word2Vector.main :__main__ : unexpected exit !")