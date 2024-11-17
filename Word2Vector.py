# -*- coding: utf-8 -*-

import math
import numpy

from Content import *

class VectorItem(ContentItem) :
    # 初始化对象
    def __init__(self, dimension, content = None) :
        # 调用父类初始化函数
        super().__init__(content)
        # 检查参数
        assert dimension >= 2
        # 索引
        self.index = -1
        # 增量
        self.__delta = numpy.zeros((2, dimension))
        # 矩阵
        self.__matrix = numpy.zeros((2, dimension))

    # 是否无用
    def is_useless(self) :
        # 调用父类函数
        if super().is_useless() :
            # 返回结果
            return True
        # 获得矩阵最大值
        value = self.__matrix.max()
        # 检查结果
        return not (1.0e-5 < value < 10)

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "content" : self.content,
                "matrix" : self.__matrix.tolist(),
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        # 检查长度
        #assert self.length == value["length"]
        # 设置举着
        self.__matrix = numpy.array(value["matrix"])
        # 设置误差
        self.__delta = numpy.zeros(self.__matrix.shape)

    def dump(self):
        # 打印信息
        print("VectorItem.dump : show properties !")
        print("\t", end = ""); print("length = %d" % self.length)
        print("\t", end = ""); print("count = %d" % self.count)
        print("\t", end = ""); print("content = \"%s\"" % self.content)
        print("matrix : ")
        print(self.__matrix)

    # 遍历函数
    # 初始化索引
    @staticmethod
    def set_index(t, value) :
        # 设置初始值
        t.index = value

    # 遍历函数
    # 相当于矩阵无穷范数
    @staticmethod
    def max_delta(t, p) :
        # 获得数据
        value = t.__delta.max()
        # 检查数据
        if value > p[0] : p[0] = value

    # 遍历函数
    # 相当于矩阵无穷范数
    @staticmethod
    def max_matrix(t, p) :
        # 获得数据
        value = t.__matrix.max()
        # 检查数据
        if value > p[0] : p[0] = value

    # 遍历函数
    @staticmethod
    def min_matrix(t, p) :
        # 获得数据
        value = t.__matrix.min()
        # 检查数据
        if value < p[0] : p[0] = value

    # 遍历函数
    # 初始化误差矩阵
    # 将误差值设置为零
    @staticmethod
    def init_delta(t, p = None) :
        # 设置初始值
        t.__delta = \
            numpy.zeros(t.__delta.shape)

    # 遍历函数
    # 加和误差
    @staticmethod
    def add_delta(t, p = None) :
        # 矩阵加和
        t.__matrix += t.__delta

    # 遍历函数
    # 缩放误差
    @staticmethod
    def mul_delta(t, value) :
        # 矩阵加和
        t.__delta = \
            numpy.dot(value, t.__delta)

    @staticmethod
    def norm_delta(t, p) :
        # 返回结果
        # 1: 列和范数
        # inf : 行和范数
        value = numpy.linalg.\
            norm(t.__delta, numpy.inf)
        # 检查结果
        if value > p[0] : p[0] = value

    # 遍历函数
    # 初始化矢量矩阵
    # 给矩阵赋予随机数值
    @staticmethod
    def init_matrix(t, p = None) :
        # 设置矩阵
        t.__matrix = \
            numpy.random.random(t.__matrix.shape)

    # 遍历函数
    # 重新计算无效的数据
    @staticmethod
    def reset_useless(t, p = None) :
        # 检查数据
        if not t.is_useless() : return
        # 设置初始值
        t.__delta = \
            numpy.zeros(t.__delta.shape)
        # 设置矩阵
        t.__matrix = \
            numpy.random.random(t.__matrix.shape)

    # 快速处置数据
    @staticmethod
    def solving(t1, t2, gamma) :
        # 拷贝原始矩阵
        matrix1 = t1.__matrix.copy()
        matrix2 = t2.__matrix.copy()
        # 获得相关系数误差（快捷处置）
        delta = gamma - \
            numpy.dot(matrix1[0], matrix2[1]) # Ai.Bj
        # 计算模长
        _Bj = numpy.dot(matrix2[1], matrix2[1])
        _Ai = numpy.dot(matrix1[0], matrix1[0])
        # 计算数据
        value = delta / (_Bj + _Ai)
        # 计算分量（快捷处置）加和误差分量
        t1.__delta[0] += numpy.dot(value, matrix2[1])
        t2.__delta[1] += numpy.dot(value, matrix1[0])
        # 返回结果
        return numpy.abs(delta)

    """
    # 求相关系数
    # 按照公式正常处置
    @staticmethod
    def dot(t1, t2) :
        # Ti = (Ai, Bi)'
        # Tj = (Aj, Bj)'
        # G = [1, 0].(Ti.Tj').[0, 1]'
        # 获得矩阵（2x2）
        # Ti * Tj = Ti.Tj' = (Ai, Bi)'.(Aj, Bj)
        # | Ai.Aj Ai.Bj |
        # | Bi.Aj Bi.Bj |
        result = numpy.matmul(t1.__matrix, t2.__matrix.T)
        # 正常处置
        result = numpy.matmul(numpy.array([[1, 0]]), result)
        result = numpy.matmul(result, numpy.array([[0, 1]]).T)
        # 返回结果
        return result[0][0]
    """

    """
    # 按照公式正常处置
    @staticmethod
    def delta(t1, t2, delta) :
        # Ti = (Ai, Bi)'
        # Tj = (Aj, Bj)'
        # 计算模长
        _Bj = numpy.dot(t2.__matrix[1], t2.__matrix[1]) # |Bj| * |Bj|
        _Ai = numpy.dot(t1.__matrix[0], t1.__matrix[0]) # |Ai| * |Ai|
        # 计算数据
        value = delta / (_Bj + _Ai)
        # 计算delta
        # | 0, value | | Aj |   | 0    , 0 | | Ai |
        # | 0    , 0 |.| Bj | , | value, 0 |.| Bi |
        return numpy.matmul(numpy.array([[value, 0],[0, 0]]), t2.__matrix), \
                    numpy.matmul(numpy.array([[0, 0],[0, value]]), t1.__matrix)
    """

class VectorGroup(ContentGroup) :
    # 初始化
    def __init__(self, dimension) :
        # 调用父类初始化
        super().__init__()
        # 检查参数
        assert dimension >= 2
        # 设置维度
        self._dimension = dimension
        # 设置词汇组
        self._words = WordContent()

    # 清理
    def clear(self) :
        # 调用父类函数
        super().clear()
        # 清理词汇
        self._words.clear()

    # 维度
    @property
    def dimension(self) :
        # 返回结果
        return self._dimension

    # 获得词汇描述
    def get_word(self, value) :
        # 检查数据
        if value in self._words :
            # 返回结果
            return self._words[value]
        # 返回结果
        return None

    # 增加词汇
    def add_word(self, content, count) :
        # 生成词汇
        item = WordItem(content)
        # 增加词汇
        self._words[content] = item
        # 设置词频
        self._words[content].count = count

    # 生成新的对象
    def new_item(self, content = None) :
        # 返回结果
        return VectorItem(self._dimension, content)

    # 增加项目
    # 用于traverse函数调用
    def add_item(self, item, parameter = None) :
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

    # 加载数据
    def init(self, path) :
        # 清理
        self.clear()
        # 加载数据
        if self._words.load(path + "words1.json") <= 0 :
            # 打印信息
            print("VectorGroup.init : fail to load words1.json !")
            return False
        # 生成数据
        # 自动设置元素的维度
        self._words.traverse(self.add_item)
        # 打印信息
        print("VectorGroup.init : all vectors added !")
        # 清理
        self._words.clear()
        # 加载数据
        if self._words.load(path + "words2.json") <= 0 :
            # 打印信息
            print("VectorGroup.init : fail to load words2.json !")
            return False
        # 打印信息
        print("VectorGroup.init : all vectors initialized !")
        # 返回结果
        return True

    # 初始化相关系数
    def init_gammas(self) :
        # 清理索引
        self._traverse(VectorItem.set_index, 0)
        # 打印信息
        print("VectorGroup.init : index of all words initialized !")
        # 初始化相关系数
        self._init_gammas()
        # 打印信息
        print("VectorGroup.init : gammas of all words initialized !")
        # 交叉检查，清理无用的矢量
        self._contents = \
            {key : item for (key, item)
             in self._contents.items() if item.index > 0}
        # 打印信息
        print("VectorGroup.init : %d row(s) left !" % len(self))
        print("VectorGroup.init : useless vectors have been removed !")

    # 初始化相关系数
    def _init_gammas(self) :
        # 初始化相关系数
        for item in self._words.values() :
            # 获得内容
            f = item.count
            c = item.content
            # 检查数值
            if f <= 0 :
                item.gamma = 0.0; continue

            # 检查数据
            assert len(c) == 2

            # 获得单词
            c1 = c[:1]
            # 检查数据
            if c1 not in self :
                # 设置为无效值
                item.gamma = 0.0; continue
            # 获得频次
            f1 = self[c1].count
            # 检查数据
            if f1 <= 0 :
                item.gamma = 0.0; continue

            # 获得单词
            c2 = c[-1]
            # 检查数据
            if c2 not in self :
                # 设置为无效值
                item.gamma = 0.0; continue
            # 获得频次
            f2 = self[c2].count
            # 检查数据
            if f2 <= 0 :
                item.gamma = 0.0; continue

            # 设置标记位
            self[c1].index |= 0x01
            self[c2].index |= 0x02
            # 计算相关系数
            item.gamma = 0.5 * float(f) \
                * (1.0 / float(f1) + 1.0 / float(f2))

    # 完成一次全量计算
    def solving(self, max_loop = 20, error = 1.0e-5) :
        # 检查参数
        assert 0 < error < 1.0
        # 总数
        count = len(self)
        # 检查内容
        if count < 2 :
            print("VectorGroup.solving : insufficient vectors !")
            return
        # 求倒数
        value = 1.0 / float(count)

        # 初始化相关系数
        self.init_gammas()
        # 初始化矩阵
        self._traverse(VectorItem.init_matrix)

        # 循环计数
        i = 0; j = 0
        # 最大行和范数
        last_delta = 1.0e5
        # 循环直至误差符合要求，或者收敛至最小误差
        while i < max_loop :
            # 计数器加一
            i += 1; j += 1
            # 设置初始误差矩阵
            self._traverse(VectorItem.init_delta)
            # 进行一次全量计算，累积误差数值
            delta = self._solving()
            # 打印信息
            print("")
            print("VectorGroup.solving : ΔG[%d] = %f !" % (j, delta))
            # 检查结果
            if last_delta > delta :
                # 呈下降趋势
                i = 0; last_delta = delta
            # 检查结果
            if delta > error :
                # 求平均值
                self._traverse(VectorItem.mul_delta, value)
                # 进行加和计算
                self._traverse(VectorItem.add_delta)
                # 重置无效的数据
                self._traverse(VectorItem.reset_useless)
            else :
                # 最大行和范数
                max_norm = [0]
                # 获得误差矩阵的最大行和范数
                self._traverse(VectorItem.norm_delta, max_norm)
                # 打印结果
                print("VectorGroup.solving : norm[%d] = %f !" % (j, max_norm[0])); break
        # 返回结果
        return last_delta

    # 完成一次全量计算
    def _solving(self) :
        # 获得总数
        total = len(self) * len(self)
        # 进度条
        pb = ProgressBar(total)
        # 打印信息
        pb.begin()
        #pb.begin(f"Word2Vector._solving : try to process {total} relation(s) !")

        # 最大误差
        max_delta = 0.0
        # 循环处理
        for t1 in self.values():
            # 获得内容
            c1 = t1.content
            # 循环处理
            for t2 in self.values() :
                # 获得内容
                c2 = t2.content

                # 相关系数
                gamma = 0.0
                # 获得拼接内容
                c = c1 + c2
                # 检查数据
                if c in self._words :
                    # 设置相关系数
                    gamma = self._words[c].gamma

                # 进度条
                pb.increase()
                # 计算数值
                delta = \
                    VectorItem.solving(t1, t2, gamma)
                # 检查结果
                if delta > max_delta : max_delta = delta

        # 打印数据总数
        pb.end()
        #pb.end(f"Word2Vector._solving : {total} relations(s) processed !")
        # 返回结果
        return max_delta

# 路径
json_path = ".\\json\\"
# 生成对象
vectors = VectorGroup(8)

def init_vectors() :
    # 加载数文件
    if not vectors.init(json_path) :
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
        else :
            # 打印信息
            print("Word2Vector.verify_vectors : invalid input !")
            continue
        # 打印信息
        print("Word2Vector.verify_vectors : show results !")

        w1 = user_input[:1]
        print("\t", end = "")
        print("w1 = \"%s\"" % w1)
        print("\t", end = "")
        if w1 not in vectors :
            print("f1 = -1.0")
        else :
            print("f1 = %d" % vectors[w1].count)

        w2 = user_input[:-1]
        print("\t", end = "")
        print("w2 = \"%s\"" % w2)
        print("\t", end = "")
        if w2 not in vectors :
            print("f2 = -1.0")
        else :
            print("f2 = %d" % vectors[w2].count)

        print("\t", end = "")
        print("word12 = \"%s\"" % user_input)
        print("\t", end = "")
        print("Gamma12 = %f" % gamma)
        print("\t", end = "")
        print("gamma12 = %f" % VectorItem.dot(vectors[w1], vectors[w2]))

def calculation_example():
    # 生成对象
    vectors = VectorGroup(2)

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

    # 求解
    if vectors.solving() > 1.0e-5 :
        print("Word2Vector.calculation_example : fail to solve !")
    else :
        print("Word2Vector.calculation_example : successfully done !")


def main() :

    # 计算加速器
    accelerator = None

    # 选项
    options = \
        [
            "exit",
            "init vectors",
            "load vectors",
            "save vectors",
            "solving vectors",
            "verify vectors",
            "initialize gammas",
            "calculation example",
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
            vectors.solving(10)
        elif user_input == '5' :
            # 验证
            verify_vectors()
        elif user_input == '6' :
            # 求解
            vectors.init_gammas()
        elif user_input == '7' :
            # 计算例子
            calculation_example()
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