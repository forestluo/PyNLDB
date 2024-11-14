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
    # 初始化对象
    def __init__(self, content = None) :
        # 调用父类初始化函数
        super().__init__(content)
        # 半维度
        self.__half__ = 2
        # 全维度（偶数）
        self.__dimension__ = 4
        # 增量
        self.delta = [0.0] * self.__dimension__
        # 矢量
        self.vector = \
            [random.random() for i in range(self.__dimension__)]

    # 设置维度
    def initialize(self, dimension) :
        # 检查参数
        assert dimension >= 4
        assert dimension & 0x01 == 0
        # 设置参数
        self.__half__ = dimension // 2
        self.__dimension__ = dimension
        # 增量
        self.delta = [0.0] * dimension
        # 矢量
        self.vector = [random.random() for i in range(dimension)]
        # 返回结果
        return self

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
        # 设置矢量
        self.vector = value["vector"]
        # 检查长度
        #assert self.length == value["length"]
        # 设置正确的维度值
        dimension = len(self.vector)
        # 检查参数
        assert dimension >= 4
        assert dimension & 0x01 == 0
        # 设置参数
        self.__half__ = dimension // 2
        self.__dimension__ = dimension
        # 增量
        self.delta = [0.0] * dimension

    # 检查各个分量，应当大于一定数值
    def is_useless(self) :
        # 循环处理
        for v in self.vector :
            # 检查每个分量
            if math.fabs(v) < 1.0e-5 :
                return True
        # 返回结果
        return super().is_useless()

    # 随机矢量
    def random(self) :
        # 循环处理
        for i in range(self.__dimension__) :
            # 设置随机数值
            self.vector[i] = random.random()

    # 将误差值设置为零
    def zero(self) :
        # 设置初始值
        self.delta = [0.0] * self.__dimension__

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
        assert item1.__dimension__ == item2.__dimension__
        # 返回结果值
        return dot(item1.vector[: item1.__half__], item2.vector[: -item2.__half__])

    @staticmethod
    def delta(item1, item2, delta) :
        # 检查参数
        assert isinstance(item1, VectorItem)
        assert isinstance(item2, VectorItem)
        assert item1.__dimension__ == item2.__dimension__
        # 获得前置矢量
        v3 = item1.vector[: item1.__half__]
        # 获得后置矢量
        v4 = item2.vector[: -item2.__half__]
        # 计算数据
        value = dot(v3, v3) + dot(v4, v4)
        # 检查数值（防止除法溢出）
        if value < 1.0e-10 : value = 1.0
        # 求各个分量
        dv1 = kdot(delta / value, v4); dv1.extend([0.0] * (len(item1.vector) - item1.__half__))
        dv2 = [0.0] * (len(item2.vector) - item2.__half__); dv2.extend(kdot(delta / value, v3))
        # 返回结果
        return dv1, dv2

class VectorGroup(ContentGroup) :
    # 初始化
    def __init__(self, dimension) :
        # 调用父类初始化
        super().__init__()
        # 检查参数
        assert dimension >= 4
        assert dimension & 0x01 == 0
        # 设置维度
        self._dimension = dimension

    # 维度
    @property
    def dimension(self) :
        # 返回结果
        return self._dimension

    # 生成新的对象
    def new_item(self, content = None) :
        # 返回结果
        return VectorItem(content) \
            .initialize(self._dimension)

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
        self[content] = self.new_item(item.content); self[content].count = item.count

    # 随机赋值
    def random(self) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self)
        # 打印数据总数
        print("VectorGroup.random : try to process %d vector(s) !" % total)
        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 循环处理
        for item in self.values():
            # 清零
            item.random()
            # 计数器加1
            count = count + 1
            # 检查结果
            if count >= (percent + 1) * one_percent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end = "")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                sys.stdout.flush()
            # 打印数据总数
        print("")
        print("VectorGroup.random : %d vector(s) processed !" % total)

    # 清理增量
    def zero_delta(self) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self)
        # 打印数据总数
        print("VectorGroup.zero_delta : try to process %d vector(s) !" % total)
        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 循环处理
        for item in self.values():
            # 清零
            item.zero()
            # 计数器加1
            count = count + 1
            # 检查结果
            if count >= (percent + 1) * one_percent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end = "")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                sys.stdout.flush()
            # 打印数据总数
        print("")
        print("VectorGroup.zero_delta : %d vector(s) processed !" % total)

    def add_delta(self) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self)
        # 打印数据总数
        print("VectorGroup.add_delta : try to process %d vector(s) !" % total)
        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 循环处理
        for item in self.values() :
            # 加和
            item.vector = add(item.vector, item.delta)
            # 计数器加1
            count = count + 1
            # 检查结果
            if count >= (percent + 1) * one_percent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end = "")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                sys.stdout.flush()
            # 打印数据总数
        print("")
        print("VectorGroup.add_delta : %d vector(s) processed !" % total)

    # 重置无用的数据
    def reset_useless(self) :
        # 标志位
        flag = False
        # 计数器
        count = 0
        # 获得总数
        total = len(self._contents)
        # 打印数据总数
        print("VectorGroup.reset_useless : try to process %d row(s) !" % total)
        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 检查数据结果
        for item in self.vales() :
            # 检查参数
            if item.is_useless() :
                # 设置标志位，并重置数据
                flag = True; item.random()
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
        print("VectorGroup.reset_useless : %d row(s) processed !" % total)
        # 返回结果
        return flag

    def average_delta(self) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self)
        # 打印数据总数
        print("VectorGroup.average_delta : try to process %d vector(s) !" % total)
        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 循环处理
        for item in self.values():
            # 求均值
            item.delta = kdot(1.0 / float(total), item.delta)
            # 计数器加1
            count = count + 1
            # 检查结果
            if count >= (percent + 1) * one_percent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end = "")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                sys.stdout.flush()
            # 打印数据总数
        print("")
        print("VectorGroup.average_delta : %d vector(s) processed !" % total)

    def get_max_delta(self) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self)
        # 打印数据总数
        print("VectorGroup.get_max_delta : try to process %d vector(s) !" % total)
        # 最大误差值
        max_value = 0.0
        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 循环处理
        for item in self.values():
            # 获得模长
            value = norm(item.delta)
            # 检查数据
            if value > max_value : max_value = value
            # 计数器加1
            count = count + 1
            # 检查结果
            if count >= (percent + 1) * one_percent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end = "")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                sys.stdout.flush()
            # 打印数据总数
        print("")
        print("VectorGroup.get_max_delta : %d vector(s) processed !" % total)
        # 返回结果
        return max_value

    def get_max_dist(self) :
        # 获得所有项目
        items = [item for item in self.values()]

        # 计数器
        count = 0
        # 获得总数
        total = len(items)
        # 打印数据总数
        print("VectorGroup.add_delta : try to process %d vector(s) !" % total)
        # 最大误差值
        max_value = 0.0
        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 循环处理
        for i in range(len(items)) :
            # 循环处理
            for j in range(i + 1, len(items)) :
                # 获得距离
                value = dist(items[i].vector, items[j].vector)
                # 检查结果
                if value > max_value : max_value = value
                # 计数器加1
                count = count + 1
                # 检查结果
                if count >= (percent + 1) * one_percent:
                    # 增加百分之一
                    percent = percent + 1
                    # 打印进度条
                    print("\r", end = "")
                    print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                    sys.stdout.flush()
            # 打印数据总数
        print("")
        print("VectorGroup.get_max_dist : %d vector(s) processed !" % total)
        # 返回结果
        return max_value

class Word2Vector :
    # 初始化
    def __init__(self, dimension) :
        # 检查参数
        assert dimension >= 4
        assert dimension & 0x01 == 0
        # 生成对象
        self._words = WordContent()
        # 生成对象
        self._vectors = VectorGroup(dimension)

    # 保存数据
    def save(self, path) :
        # 保存数据
        self._vectors.save(path + "vectors.json")
        # 打印信息
        print("Word2Vector.save : vectors.json saved !")

    # 加载数据
    def load(self, path) :
        # 加载数据
        if self._vectors.load(path + "vectors.json") <= 0 :
            # 打印信息
            print("Word2Vector.save : fail to load vectors.json !")
        else :
            # 打印信息
            print("Word2Vector.save : vectors.json has been loaded !")

    # 加载数据
    def init(self, path) :
        # 清理
        self._words.clear()
        # 加载数据
        if self._words.load(path + "words1.json") <= 0 :
            # 打印信息
            print("Word2Vector.init : fail to load words1.json !")
            return False

        # 清理
        self._vectors.clear()
        # 生成数据
        # 自动设置元素的维度
        self._words.traverse(self._vectors.add_item)
        # 打印信息
        print("Word2Vector.init : all vectors initialized !")

        # 清理
        self._words.clear()
        # 加载数据
        if self._words.load(path + "words2.json") <= 0 :
            # 打印信息
            print("Word2Vector.init : fail to load words2.json !")
            return False
        # 返回结果
        return True

    def get_count(self, t) :
        # 检查结果
        if t in self._vectors :
            # 返回数据
            return self._vectors[t].count
        # 返回数据
        return -1

    def distance(self, t1, t2) :
        # 检查结果
        if t1 not in self._vectors : return -1.0
        # 获得数据
        item1 = self._vectors[t1]
        # 检查结果
        if t2 not in self._vectors :
            return -1.0
        # 获得数据
        item2 = self._vectors[t2]
        # 返回结果
        return dist(item1.vector, item2.vector)

    def dot_gamma(self, t1, t2) :
        # 检查结果
        if t1 not in self._vectors :
            return 0.0
        # 获得数据
        item1 = self._vectors[t1]
        # 检查结果
        if t2 not in self._vectors :
            return 0.0
        # 获得数据
        item2 = self._vectors[t2]
        # 返回结果
        return VectorItem.dot(item1, item2)

    def get_gamma(self, t1, t2) :
        # 检查结果
        if t1 not in self._vectors :
            return 0.0
        # 获得数据
        item1 = self._vectors[t1]
        # 检查结果
        if t2 not in self._vectors :
            return 0.0
        # 获得数据
        item2 = self._vectors[t2]
        # 检查结果
        if t1 + t2 not in self._words :
            return 0.0
        # 获得数据
        item = self._words[t1 + t2]
        # 检查结果
        if item1.count <= 0 \
            or item2.count <= 0 or item.count <= 0 :
            return 0.0
        # 计算相关系数
        return (0.5 * float(item.count) *
                 (1.0 / float(item1.count) + 1.0 / float(item2.count)))

    # 完成一次全量计算
    def _solving(self) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self._vectors) * len(self._vectors)
        # 打印数据总数
        print("Word2Vector._solving : try to process %d relation(s) !" % total)
        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 循环处理
        for t1 in self._vectors.values() :
            # 循环处理
            for t2 in self._vectors.values() :
                # 相关系数
                gamma = 0.0
                # 获得拼接内容
                content = t1.content + t2.content
                # 检查结果
                if content in self._words :
                    # 获得词频
                    frequency = self._words[content].count
                    # 检查结果
                    if t1.count > 0 and t2.count > 0 and frequency > 0 :
                        # 计算相关系数
                        gamma = (0.5 * float(frequency) *
                            (1.0 / float(t1.count) + 1.0 / float(t2.count)))
                # 检查相关系数
                assert gamma >= 0

                # 计算相关系数
                result = VectorItem.dot(t1, t2)
                # 获得误差
                delta = gamma - result
                # 检查误差
                if math.fabs(delta) > 1.0e-5 :
                    # 获得需要调整的误差分量
                    dv1, dv2 = VectorItem.delta(t1, t2, delta)
                    # 计算整体误差
                    t1.delta = add(t1.delta, dv1); t2.delta = add(t2.delta, dv2)

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
        print("Word2Vector._solving : %d relation(s) processed !" % total)

    # 完成一次全量计算
    def solving(self, max_loop = 20) :
        # 循环处理
        loop_count = 0
        # 循环处理
        while True :
            # 循环次数加一
            loop_count += 1
            # 检查结果
            if loop_count > max_loop :
                # 重置循环次数
                loop_count = 0
                # 重置所有的数据
                self._vectors.random()

            # 清理标志位
            flag = 0x00
            # 内层计数器
            count = 0
            # 内层循环
            while count < max_loop :
                # 增加计数
                count += 1
                # 清理所有误差分量
                self._vectors.zero_delta()
                # 进行一次全量计算
                self._solving()
                # 对误差求均值
                self._vectors.average_delta()
                # 获得最大误差数值
                max_delta = self._vectors.get_max_delta()
                # 打印信息
                print("Word2Vector.solving : max Δg(%f) in %d count(s) !" % (max_delta, loop_count))
                # 检查结果
                if max_delta > 1.0e-5 :
                    # 加和所有分量
                    self._vectors.add_delta(); continue
                # 设置标记位
                flag |= 0x01
                # 检查次数；设置标记位；中断循环
                if loop_count == 1 : flag |= 0x10; count = max_loop

            # 检查标志位
            if (flag & 0x01) != 0x01 :
                # 设置循环次数，要求重置数据
                loop_count = max_loop
            # 检查矢量间的距离是否在范围内
            elif self._vectors.get_max_dist() > 1.0e2 :
                # 打印信息
                print("Word2Vector.solving : distance is too large !")
            elif self._vectors.reset_useless() :
                # 打印信息
                print("Word2Vector.solving : too small vector component !")
            else:
                # 打印信息
                print("Word2Vector.solving : all vectors have been properly set !")
                return True

# 路径
json_path = ".\\json\\"
# 生成对象
w2v = Word2Vector(8)

def init_vectors() :
    # 加载数文件
    if not w2v.init(json_path) :
        # 打印信息
        print("Word2Vector.init_vectors : fail to load files !")
    else :
        # 打印信息
        print("Word2Vector.init_vectors : all files have been loaded !")

def load_vectors() :
    # 加载数文件
    if not w2v.load(json_path) :
        # 打印信息
        print("Word2Vector.load_vectors : fail to load file !")
    else :
        # 打印信息
        print("Word2Vector.load_vectors : vectors.json has been loaded !")

def save_vectors() :
    # 加载数文件
    w2v.save(json_path)
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
        # 获得第一个字符
        w1 = user_input[0]
        w2 = user_input[-1]
        # 获得相关系数
        gamma = w2v.get_gamma(w1, w2)
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
        print("f1 = %d" % w2v.get_count(w1))

        print("\t", end = "")
        print("w2 = \"%s\"" % w2)
        print("\t", end = "")
        print("f2 = %d" % w2v.get_count(w2))

        print("\t", end = "")
        print("word12 = \"%s\"" % user_input)
        print("\t", end = "")
        print("Gamma12 = %f" % gamma)
        print("\t", end = "")
        print("gamma12 = %f" % w2v.dot_gamma(w1, w2))
        print("\t", end = "")
        print("distance12 = %f" % w2v.distance(w1, w2))

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
            save_vectors()
        elif user_input == '4' :
            # 求解
            w2v.solving()
        elif user_input == '5' :
            # 手工检验
            verify_vectors()
        else :
            print("WordVector.main : unknown choice !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("VectorGroup.main :__main__ : ", str(e))
        print("VectorGroup.main :__main__ : unexpected exit !")