# -*- coding: utf-8 -*-

import os
import sys
import json
import math
import traceback

from Content import *

# 求模长
def norm(v) :
    # 距离
    value = 0.0
    # 循环处理
    for p in v:
        # 求值，并加和
        value += p * p
    # 返回结果
    return math.sqrt(value)

# 求距离
def dist(v1, v2) :
    # 返回结果
    return norm(sub(v1, v2))

# 常数乘以矢量
def kdot(k, v) :
    # 返回结果
    return [k * p for p in v]

def add(v1, v2) :
    # 返回结果
    return [p + q for p, q in zip(v1, v2)]

def sub(v1, v2) :
    # 返回结果
    return [p - q for p, q in zip(v1, v2)]

def dot(v1, v2) :
    # 初始值
    value = 0.0
    # 同时遍历两个对象
    for p, q in zip(v1, v2) : value += p * q
    # 返回结果
    return value

class VectorItem(ContentItem) :
    # 维度
    # 半维度
    __half__ = 512
    # 全维度（偶数）
    __dimension__ = 1024

    # 初始化对象
    def __init__(self, content = None) :
        # 调用父类初始化函数
        super().__init__(content)
        # 备份
        self._backup = [0.0] * VectorItem.__dimension__
        # 矢量
        self.vector = \
            [random.random() for i in range(VectorItem.__dimension__)]

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "content" : self.content,
                "vector" : self.vector,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        self.vector = value["vector"]
        # 检查数据
        assert len(self.vector) >= 4
        assert len(self.vector) & 0x01 == 0
        # 检查维度一致性
        if len(self.vector) != VectorItem.__dimension__ :
            # 设置正确的维度值
            VectorItem.__dimension__ = len(self.vector)
            VectorItem.__half__ = VectorItem.__dimension__ / 2
        #assert self.length == value["length"]

    # 检查各个分量，应当大于一定数值
    def is_useless(self) :
        # 循环处理
        for v in self.vector :
            # 检查每个分量
            if math.fabs(v) < 1.0e-5 :
                return True
        # 返回结果
        return super().is_useless()

    # 复位
    def random(self) :
        # 循环处理
        for i in range(len(self.vector)) :
            # 设置随机数值
            self.vector[i] = random.random()

    # 求取原值与当前值之间的误差
    @property
    def error(self) :
        # 返回结果
        return dist(self.vector, self._backup)

    # 误差是否在容忍范围内
    def is_intolerable(self) :
        # 返回结果
        return dist(self.vector, self._backup) > 1.0e-5

    # 保留原值
    def backup(self) :
        # 拷贝当前矢量
        self._backup = [item for item in self.vector]

    def dump(self):
        # 打印信息
        print("VectorItem.dump : show properties !")
        print("\t", end = ""); print("length = %d" % self.length)
        print("\t", end = ""); print("count = %d" % self.count)
        print("\t", end = ""); print("content = \"%s\"" % self.content)
        print("\t[", end = "")
        for i in range(len(self.vector)) :
            print("%f" % self.vector[i], end = "")
            if i < len(self.vector) - 1 : print(" ", end = "")
        print("]")

    # 求相关系数
    @staticmethod
    def dot(item1, item2) :
        # 检查参数
        assert isinstance(item1, VectorItem)
        assert isinstance(item2, VectorItem)
        # 返回结果值
        return dot(item1.vector[ : VectorItem.__half__],
                   item2.vector[ : -VectorItem.__half__])

    @staticmethod
    def delta(item1, item2, delta) :
        # 检查参数
        assert isinstance(item1, VectorItem)
        assert isinstance(item2, VectorItem)
        # 获得前置矢量
        v3 = item1.vector[ : VectorItem.__half__]
        # 获得后置矢量
        v4 = item2.vector[ : -VectorItem.__half__]
        # 计算数据
        value = dot(v3, v3) + dot(v4, v4)
        # 检查数值（防止除法溢出）
        if value < 1.0e-10 : value = 1.0
        # 求各个分量
        dv1 = kdot(delta / value, v4); dv1.extend([0.0] * (len(item1.vector) - VectorItem.__half__))
        dv2 = [0.0] * (len(item2.vector) - VectorItem.__half__); dv2.extend(kdot(delta / value, v3))
        # 返回结果
        return dv1, dv2

class VectorGroup(ContentGroup) :
    # 最大循环次数
    __max_loop__ = 20

    # 生成新的对象
    def new_item(self, content = None) :
        # 返回结果
        return VectorItem(content)

    # 增加项目
    # 用于traverse函数调用
    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_content(ContentItem(content))

    # 增加项目
    # 用于traverse函数调用
    def add_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 获得内容
        content = item.content
        # 检查字典
        if content in self:
            # 增加计数
            self[content].count += item.count; return
        # 增加项目
        self[content] = VectorItem(item.content); self[content].count = item.count

    # 计算相关系数
    def get_gamma(self, w1, w2) :
        # 检查第一个词
        if w1 not in self : return -1.0
        # 查询第一个词的词频
        f1 = self[w1].count
        # 检查第二个词
        if w2 not in self : return -1.0
        # 查询第二个词的词频
        f2 = self[w2].count
        # 合成词
        w = w1 + w2
        # 查询合成词的词频
        f = self[w].count if w in self else 0.0
        # 返回结果
        return 0.5 * float(f) * (1.0 / float(f1) + 1.0 / float(f2))

    # 迭代计算
    def solving(self, w1, w2) :
        # 检查参数
        assert len(w1) >= 1 and len(w2) >= 1
        # 计算相关系数
        gamma = \
            self.get_gamma(w1, w2)
        # 检查结果
        if gamma <= 0 : return False

        # 循环次数
        loop_count = 0
        # 循环处理
        while True :
            # 清理标志位
            flag = 0x00
            # 循环次数加一
            loop_count += 1
            # 检查结果
            if loop_count > VectorGroup.__max_loop__ :
                # 重置循环次数
                loop_count = 0
                # 重新随机赋值
                self[w1].random(); self[w2].random()

            # 误差值
            delta = 0
            # 内部计数
            count = 0
            # 结果
            result = 0.0
            # 保留原值
            self[w1].backup(); self[w2].backup()
            # 循环处理
            while count < VectorGroup.__max_loop__ :
                # 计数器加一
                count += 1
                # 求相关系数（点积）
                result = VectorItem.dot(self[w1], self[w2])
                # 获得误差
                delta = gamma - result
                # 检查误差
                if math.fabs(delta) < 1.0e-5 :
                    # 设置标记位
                    flag |= 0x01
                    # 检查次数，并设置标记位
                    if count == 1 : flag |= 0x10; break
                    # 打印信息
                    #print("VectorGroup.solve : Δg(%f) in %d count(s) !" % (math.fabs(delta), count));
                # 获得需要调整的误差分量
                dv1, dv2 = VectorItem.delta(self[w1], self[w2], delta)
                # 设置新的迭代数据
                self[w1].vector = add(self[w1].vector, dv1)
                self[w2].vector = add(self[w2].vector, dv2)
            # 检查标志位
            if (flag & 0x01) != 0x01 :
                # 设置循环次数，要求重置数据
                loop_count = VectorGroup.__max_loop__
                # 打印信息
                #print("VectorGroup.solve : Δg(%f) failed in %d count(s) !" % (math.fabs(delta), count))
            # 检查误差距离是否在范围内
            elif dist(self[w1].vector, self[w2].vector) > 1.0e2 : continue
                # 打印信息
                #print("VectorGroup.solve : distance is too large !")
            elif self[w1].is_useless() or self[w2].is_useless() : continue
                # 打印信息
                #print("VectorGroup.solve : too small vector component !")
            elif self[w1].is_intolerable() or self[w2].is_intolerable() : continue
                # 打印信息
                #print("VectorGroup.solve : margin of error is intolerable !")
            else :
                # 打印信息
                #print("VectorGroup.solve : show results !")
                #print("\t", end = ""); print("Γ(12) = %f (G12 = %f, Δ12 = %f) !" % (result, gamma, delta))
                return True

    # 迭代计算
    def solving_all(self) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self._contents)
        # 打印数据总数
        print("VectorGroup.solving_all : try to process %d row(s) !" % total)

        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 检查数据结果
        for item in self._contents.values() :
            # 检查长度
            if item.length == 2 :
                # 获得第一个字符
                w1 = item.content[0]
                # 获得第二个字符
                w2 = item.content[-1]
                # 检查
                if w1 in self or w2 in self :
                    # 解矢量
                    self.solving(w1, w2)
                else :
                    # 删除当前数据
                    del vectors[item.content]
            # 计数器加1
            count = count + 1
            # 检查结果
            if count >= (percent + 1) * one_percent :
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end = "")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end = "")
                sys.stdout.flush()
        # 打印数据总数
        print("")
        print("VectorGroup.solving_all : %d row(s) processed !" % total)

# 路径
json_path = ".\\json\\"
# 生成对象
vectors = VectorGroup()

def init_vectors() :
    # 清理内容
    vectors.clear()
    print("VectorGroup.init_vectors : vectors cleared !")

    # 生成对象
    words = WordContent()
    # 加载数据
    if words.load(json_path + "words1.json") <= 0 :
        print("VectorGroup.init_vectors : fail to load file !")
        return
    # 增加内容
    words.traverse(vectors.add_item)
    # 加载数据
    if words.load(json_path + "words2.json") <= 0:
        print("VectorGroup.init_vectors : fail to load file !")
        return
    # 增加内容
    words.traverse(vectors.add_item)

    # 清理数据
    words.clear()
    # 清理无效内容
    vectors.clear_invalid()
    print("VectorGroup.init_vectors : words cleared !")

def load_vectors() :
    # 清理内容
    vectors.clear()
    print("VectorGroup.load_vectors : vectors cleared !")

    # 加载数据
    if vectors.load(json_path + "vectors.json") <= 0 :
        print("VectorGroup.load_vectors : fail to load file !")
        return

    # 清理无效内容
    vectors.clear_invalid()
    print("VectorGroup.load_vectors : invalid vectors cleared !")

def verify_vectors() :
    # 检查数据
    if len(vectors) <= 0 :
        # 打印信息
        print("VectorGroup.verify_vectors : no vectors !")
        return

    # 清理输入项目
    user_input = ""
    # 循环处理
    while user_input.lower() != '0' :
        # 继续选择输入
        user_input = input("Enter '0' to exit : ")
        # 检查长度
        if len(user_input) != 2 : continue
        # 获得第一个字符
        w1 = user_input[0]
        w2 = user_input[-1]
        # 获得相关系数
        gamma = vectors.get_gamma(w1, w2)
        # 检查结果
        if gamma <= 0.0 :
            # 打印信息
            print("WordVector.verify_vectors : invalid input !")
            continue
        # 打印信息
        print("WordVector.verify_vectors : show results !")

        print("\t", end = "")
        print("w1 = \"%s\"" % w1)
        print("\t", end = "")
        print("f1 = %f" % vectors[w1].count)
        print("\t", end = "")
        print("e1 = %f" % vectors[w1].error)

        print("\t", end = "")
        print("w2 = \"%s\"" % w2)
        print("\t", end = "")
        print("f2 = %f" % vectors[w2].count)
        print("\t", end = "")
        print("e2 = %f" % vectors[w2].error)

        print("\t", end = "")
        print("word12 = \"%s\"" % user_input)
        print("\t", end = "")
        print("Gamma12 = %f" % gamma)
        print("\t", end = "")
        print("gamma12 = %f" % dot(vectors[w1].vector, vectors[w2].vector))
        print("\t", end = "")
        print("distance12 = %f" % dist(vectors[w1].vector, vectors[w2].vector))

def main() :

    # 选项
    options = \
        [
            "exit",
            "init vectors",
            "load vectors",
            "save vectors",
            "solving all",
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
            print("WordVector.main : user exit !"); break
        elif user_input == '1' :
            # 初始化
            init_vectors()
        elif user_input == '2' :
            # 加载
            load_vectors()
        elif user_input == '3' :
            # 保存
            vectors.save(json_path + "vectors.json")
        elif user_input == '4' :
            # 求解
            vectors.solving_all()
        elif user_input == '5' :
            # 手工检验
            verify_vectors()
        else :
            print("WordVector.main : unknown choice !")

    # 清理无用内容
    vectors.clear_useless()
    # 保存数据
    vectors.save(json_path + "vectors.json")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("VectorGroup.main :__main__ : ", str(e))
        print("VectorGroup.main :__main__ : unexpected exit !")