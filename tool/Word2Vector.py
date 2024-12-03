# -*- coding: utf-8 -*-

from nlp.alg.VectorContent import *

# 路径
json_path = "..\\json\\"
# 生成对象
vectors = VectorContent(256)

def init_vectors() :
    # 加载数文件
    if not vectors.init_data(json_path) :
        # 打印信息
        print("Word2Vector.init_vectors : fail to load files !")
    else :
        # 打印信息
        print("Word2Vector.init_vectors : all files have been loaded !")

def load_vectors() :
    # 加载数文件
    if not vectors.load(json_path + "vectors.json") :
        # 打印信息
        print("Word2Vector.load_vectors : fail to load file !")
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
            vectors[w1].dump()
        else :
            print(f"\tw1 = \"{w1}\"")
            print(f"\tf1 = ...invalid word...")

        w2 = user_input[-1]
        # 检查结果
        if w2 in vectors :
            vectors[w2].dump()
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

def normal_solving() :
    # 检查参数
    if len(vectors) <= 0 :
        # 打印信息
        print("Word2Vector.normal_solving : insufficient vectors !")
        return

    # 计数器
    i = 0
    while True :
        # 计数器加一
        i += 1
        # 求解
        max_delta = vectors.solving()
        # 检查结果
        if max_delta > 1.0e-5 :
            # 打印信息
            print("Word2Vector.normal_solving : fail to solve !")
        else :
            print("Word2Vector.normal_solving : successfully done !"); break

def fast_solving() :
    # 检查参数
    if len(vectors) <= 0 :
        # 打印信息
        print("Word2Vector.fast_solving : insufficient vectors !")
        return

    # 计数器
    i = 0
    # 循环处理
    while True :
        # 计数器加一
        i += 1
        # 求解
        max_delta = vectors.fast_solving()
        # 检查结果
        if max_delta > 1.0e-5 :
            # 打印信息
            print("Word2Vector.fast_solving : fail to solve !")
        else :
            print("Word2Vector.fast_solving : successfully done !"); break

def gradient_solving() :
    # 检查参数
    if len(vectors) <= 0 :
        # 打印信息
        print("Word2Vector.gradient_solving : insufficient vectors !")
        return

    # 计数器
    i = 0
    while True :
        # 计数器加一
        i += 1
        # 求解
        max_delta = vectors.gradient_solving()
        # 检查结果
        if max_delta > 1.0e-5 :
            # 打印信息
            print("Word2Vector.gradient_solving : fail to solve !")
        else :
            print("Word2Vector.gradient_solving : successfully done !"); break

def fast_calculation_example():
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

    # 打印数据
    for item in vectors.values() : item.dump(dump_delta = False)
    # 设置标记位
    vectors.init_matrix = True
    # 求解
    if vectors.fast_solving() > 1.0e-5 :
        print("Word2Vector.fast_calculation_example : fail to solve !")
    else :
        print("Word2Vector.fast_calculation_example : successfully done !")
    # 打印数据
    for item in vectors.values() : item.dump(dump_delta = False)

def normal_calculation_example():
    # 生成对象
    vectors.clear()

    # 生成对象
    v1 = vectors.new_item("运")
    v1.count = 937002
    vectors.add_item(v1)

    # 生成对象
    v2 = vectors.new_item("动")
    v2.count = 2363927
    vectors.add_item(v2)

    vectors.add_word("运运", 343)
    vectors.add_word("动动", 1753)
    vectors.add_word("运动", 175908)
    vectors.add_word("动运", 1122)

    # 打印数据
    for item in vectors.values() : item.dump(dump_delta = False)
    # 设置标记位
    vectors.init_matrix = True
    # 求解
    if vectors.solving() > 1.0e-5 :
        print("Word2Vector.normal_calculation_example : fail to solve !")
    else :
        print("Word2Vector.normal_calculation_example : successfully done !")
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
            "fast solving vectors",
            "normal solving vectors",
            "gradient solving vectors",
            "verify vectors",
            "fast calculation example",
            "normal calculation example",
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
            fast_solving()
        elif user_input == '5' :
            # 求解
            normal_solving()
        elif user_input == '6' :
            # 梯度下降法
            gradient_solving()
        elif user_input == '7' :
            # 验证
            verify_vectors()
        elif user_input == '8' :
            # 计算例子
            fast_calculation_example()
        elif user_input == '9' :
            # 计算例子
            normal_calculation_example()
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