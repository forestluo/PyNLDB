# -*- coding: utf-8 -*-
import re
import threading

from nlp.alg.NL1Solution import *
from nlp.alg.NL2Solution import *
from nlp.alg.NLinfSolution import *

from nlp.alg.JL1Solution import *
from nlp.alg.JL2Solution import *
from nlp.alg.JLinfSolution import *

from nlp.alg.CL1Solution import *
from nlp.alg.CL2Solution import *
from nlp.alg.CLinfSolution import *

from nlp.alg.SimpleSolution import *

from nlp.item.WordItem import *
from nlp.item.VectorItem import *
from nlp.content.CoreContent import *
from nlp.content.WordContent import *
from nlp.content.VectorContent import *

class Word2Vector :
    # 初始化
    def __init__(self, dimension) :
        # 检查参数
        assert dimension >= 2
        # 最小记录次数
        self.min_count = 512
        # 拷贝数据
        self.copy_data = False
        # 设置词汇组
        self._words = WordContent()
        # 设置是两组
        self._vectors = VectorContent(dimension)

    # 维度
    @property
    def dimension(self) :
        # 返回结果
        return self._vectors.dimension

    @property
    def wsize(self) :
        return len(self._words)

    @property
    def vsize(self) :
        return len(self._vectors)

    def words(self) :
        # 返回结果
        return self._words.values()

    def vectors(self) :
        # 返回结果
        return self._vectors.values()

    # 获得词汇
    def word(self, key) :
        # 检查参数
        if key in self._words :
            # 返回结果
            return self._words[key]
        # 返回结果
        return None

    # 获得词汇
    def vector(self, key) :
        # 检查参数
        if key in self._vectors :
            # 返回结果
            return self._vectors[key]
        # 返回结果
        return None

    # 初始化
    def initialize(self, path) :
        # 加载数文件
        if not self.__load_words(path):
            # 打印信息
            print(f"Word2Vector.initialize : fail to load words !")
            return False
        # 设置标记
        self.copy_data = False
        # 打印信息
        print(f"Word2Vector.initialize : words have been loaded !")
        # 初始化相关系数
        # 需要使用索引作为临时标记位
        self.__init_gammas()
        # 打印信息
        print(f"Word2Vector.initialize : gammas initialized !")
        # 清理无效数据
        self.__clear_invalid()
        # 打印信息
        print(f"Word2Vector.initialize : invalid data cleared !")
        # 重建索引
        self.index_vectors()
        # 打印信息
        print(f"Word2Vector.initialize : index of vectors rebuilt !")
        # 返回结果
        return True

    # 重建索引
    def index_vectors(self) :
        # 进度条
        pb = ProgressBar(self.vsize)
        # 开始
        pb.begin(f"Word2Vector.index_vectors : reindex vectors !")
        # 初始化索引值
        for index, v in enumerate(self.vectors()) :
            # 进度条
            pb.increase()
            # 设置索引
            v.index = index
        # 结束
        pb.end(f"Word2Vector.index_vectors : {self.vsize} vector(s) indexed !")

    # 加载数据
    def __load_words(self, path) :
        # 清理
        self._words.clear()
        # 检查文件是否存在
        if os.path.isfile(path + "words1.json") :
            # 加载数据
            if self._words.load(path + "words1.json") <= 0 :
                # 打印信息
                print("Word2Vector.__load_words : fail to load words1.json !")
                return False
        # 清理数据
        self._vectors.clear()
        # 生成数据
        # 自动设置元素的维度
        self._words.traverse(self._vectors.add_item)
        # 打印信息
        print("Word2Vector.__load_words : all vectors added !")
        # 清理
        self._words.clear()
        # 检查文件是否存在
        if os.path.isfile(path + "words2.json") :
            # 加载数据
            if self._words.load(path + "words2.json") <= 0 :
                # 打印信息
                print("Word2Vector.__load_words : fail to load words2.json !")
                return False
        # 打印信息
        print("Word2Vector.__load_words : all vectors initialized !")
        # 返回结果
        return True

    # 初始化相关系数
    def __init_gammas(self) :
        # 索引清零
        # 临时做为标记位使用
        for v in self.vectors() : v.index = 0
        # 总数
        total = self.wsize
        # 进度条
        pb = ProgressBar(total)
        # 开始
        pb.begin(f"Word2Vector.__init_gammas : init gammas[{total}] !")
        # 初始化相关系数
        for item in self.words() :
            # 进度条
            pb.increase()
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
            if c1 not in self._vectors :
                # 设置为无效值
                item.gamma = 0.0; continue
            # 获得频次
            f1 = self._vectors[c1].count
            # 检查数据
            if f1 <= 0 :
                item.gamma = 0.0; continue

            # 获得单词
            c2 = c[-1]
            # 检查数据
            if c2 not in self._vectors :
                # 设置为无效值
                item.gamma = 0.0; continue
            # 获得频次
            f2 = self._vectors[c2].count
            # 检查数据
            if f2 <= 0 :
                item.gamma = 0.0; continue

            # 设置标记位
            self._vectors[c1].index |= 0x01
            self._vectors[c2].index |= 0x02
            # 计算相关系数
            item.gamma = 0.5 * float(f) \
                * (1.0 / float(f1) + 1.0 / float(f2))
        # 结束
        pb.end()

    # 清理无效数据
    def __clear_invalid(self) :
        # 清理无效数据
        # 进度条
        pb = ProgressBar(self.vsize)
        # 开始
        pb.begin(f"Word2Vector.__clear_invalid : clear invalid vectors !")
        # 创建对象
        removed = WordContent()
        # 循环处理
        for item in self.vectors() :
            # 进度条
            pb.increase()
            # 检查计数
            # 至少需要的记录次数
            if item.index == 0 \
                or item.count < self.min_count : removed.add_item(item)
        # 结束
        pb.end()

        # 进度条
        pb = ProgressBar(self.wsize)
        # 开始
        pb.begin(f"Word2Vector.__clear_invalid : clear invalid words !")
        # 清理词汇
        for item in self.words() :
            # 进度条
            pb.increase()
            # 获得词汇
            content = item.content
            # 逐个检查单词
            for c in content :
                # 如果发现有字符在被删除要求中
                # 获得字符不在矢量组之中
                # 将无效词汇数据加入删除队列中
                if c in removed \
                    or c not in self._vectors : removed.add_item(item)
        # 结束
        pb.end()

        # 进度条
        pb = ProgressBar(len(removed))
        # 开始
        pb.begin(f"Word2Vector.__clear_invalid : remove all items !")
        # 清理词汇
        for item in removed.values() :
            # 进度条
            pb.increase()
            # 删除
            if item.content in self._words : self._words.remove(item.content)
            if item.content in self._vectors : self._vectors.remove(item.content)
        # 结束
        pb.end()
        # 打印信息
        print(f"Word2Vector.__clear_invalid : {self.wsize} word(s) left !")
        print(f"Word2Vector.__clear_invalid : {self.vsize} vector(s) left !")
        print(f"Word2Vector.__clear_invalid : total {len(removed)} item(s) removed !")

    # 加载数据
    def load_words(self, file_name) :
        # 创建
        words = WordContent()
        # 再调用父类加载数据
        result = words.load(file_name)
        # 检查结果
        if result <= 0 :
            # 打印信息
            print(f"Word2Vector.load_words : loading({file_name}) failed !")
            return result
        # 进度条
        pb = ProgressBar(len(words))
        # 开始
        pb.begin()
        # 新建
        self._words = WordContent()
        # 循环处理
        for item in words.values() :
            # 进度条
            pb.increase()
            # 只处理长度为2的数据
            if item.length != 2 : continue
            # 加入到词汇中
            self._words.add_item(item)
        # 结束
        pb.end()
        # 打印信息
        print(f"Word2Vector.load_words : total {self.wsize} item(s) loaded !")
        # 初始化相关系数
        self.__init_gammas()
        # 打印信息
        print(f"Word2Vector.load_words : gammas initialized !")
        # 清理无效数据
        self.__clear_invalid()
        # 打印信息
        print(f"Word2Vector.load_words : invalid data cleared !")
        # 重建索引
        self.index_vectors()
        # 打印信息
        print(f"Word2Vector.load_words : index of vectors rebuilt !")
        # 返回结果
        return result

    # 保存数据
    def save_vectors(self, file_name) :
        # 保存文件
        self._vectors.save(file_name)
        # 打印信息
        print(f"Word2Vector.save_vectors : file was saved !")

    # 加载数据
    def load_vectors(self, file_name) :
        # 清理
        vectors = VectorContent(self.dimension)
        # 加载矢量数据
        result = vectors.load(file_name)
        # 检查结果
        if result <= 0 : return result
        # 打印信息
        print(f"Word2Vector.load_vectors : file was loaded !")
        # 进度条
        pb = ProgressBar(len(vectors))
        # 开始
        pb.begin(f"Word2Vector.load_vectors : checking dimension of vectors !")
        # 维度
        dimension = -1
        # 循环处理
        for v in vectors.values() :
            # 进度条
            pb.increase()
            # 获得矩阵
            size = (len(v.matrix[0]) +
                len(v.matrix[1])) // 2
            # 检查数据
            if size != dimension :
                # 检查参数
                if dimension < 0 :
                    dimension = size
                # 检查维度
                elif size != dimension :
                    # 打印信息
                    print(f"Word2Vector.load_vectors : incorrect dimension{size} !")
                    return -1
        # 结束
        pb.end()
        # 检查维度
        if dimension < 2 :
            # 打印信息
            print(f"Word2Vector.load_vectors : incorrect dimension{dimension} !")
            return -1
        # 设置矢量
        self._vectors = vectors
        # 打印信息
        print(f"Word2Vector.load_words : vectors were set !")
        # 重建索引
        self.index_vectors()
        # 打印信息
        print(f"Word2Vector.load_words : index of vectors rebuilt !")
        # 设置维度
        self._vectors.dimension = dimension
        # 打印信息
        print(f"Word2Vector.load_vectors : vectors(dimension = {dimension}) loaded !")
        # 返回结果
        return result

    # 取得求解器
    def get_solution(self, method = "classic") :
        # 检查参数
        assert isinstance(method, str)
        # 变成小写
        method = method.lower()
        # 匹配
        if re.match("^classic|((numpy|jit|cupy).(l1|l2|linf))$", method) :
            # 检查模块名
            if method.startswith("jit") :
                # 检查算法名
                if method.endswith("l1") : return JL1Solution(self)
                elif method.endswith("l2") : return JL2Solution(self)
                elif method.endswith("linf") : return JLinfSolution(self)
            elif method.startswith("cupy") :
                # 检查算法名
                if method.endswith("l1") : return CL1Solution(self)
                elif method.endswith("l2") : return CL2Solution(self)
                elif method.endswith("linf") : return CLinfSolution(self)
            elif method.startswith("numpy") :
                # 检查算法名
                if method.endswith("l1") : return NL1Solution(self)
                elif method.endswith("l2") : return NL2Solution(self)
                elif method.endswith("linf") : return NLinfSolution(self)
            elif method.startswith("classic") : return SimpleSolution(self)
        # 打印信息
        print(f"Word2Vector.get_solution : unrecognized method(\"{method}\") !")
        # 返回结果
        return None

    # 加载测试数据
    def load_example(self) :
        # 清理数据
        self._words.clear()
        self._vectors.clear()
        # 设置标记
        self.copy_data = False
        # 生成对象
        self._vectors.add_item(
            self._vectors.new_item("运", 937002))
        # 生成对象
        self._vectors.add_item(
            self._vectors.new_item("动", 2363927))
        # 生成对象
        self._words.add_item(
            self._words.new_item("运运", 343))
        self._words.add_item(
            self._words.new_item("动动", 1753))
        self._words.add_item(
            self._words.new_item("运动", 175908))
        self._words.add_item(
            self._words.new_item("动运", 1122))
        # 初始化相关系数
        self.__init_gammas()
        # 打印信息
        print(f"Word2Vector.load_example : gammas initialized !")
        # 重建索引
        self.index_vectors()
        # 打印信息
        print(f"Word2Vector.load_example : index of vectors rebuilt !")

def main() :

    # 生成对象
    w2v = Word2Vector(32)
    # 加载例程
    #w2v.load_example()
    """
    # 初始化
    if not w2v.initialize("..\\..\\json\\") :
        # 打印信息
        print("Word2Vector.main : fail to initialize !")
        return
    # 打印信息
    print("Word2Vector.main : successfully initialized !")
    """
    # 加载数据
    if w2v.load_vectors("..\\..\\json\\vectors.json") <= 0 :
        # 打印信息
        print("Word2Vector.main : fail to load vectors.json !")
        return
    # 加载数据
    if w2v.load_words("..\\..\\json\\cores.json") <= 0 :
        # 打印信息
        print("Word2Vector.main : fail to load cores.json !")
        return
    # 打印信息
    print("Word2Vector.main : successfully loaded !")
    # 获得求解器
    solution = w2v.get_solution("cupy.l2")
    # 检查结果
    if solution is None :
        # 打印信息
        print("Word2Vector.main : fail to get solution !")
        return
    # 启动
    solution.start()
    # 打印信息
    print("Word2Vector.main : successfully start solving !")
    # 等待输入
    input()
    # 结束线程
    solution.stop()
    # 打印信息
    print("Word2Vector.main : successfully stopped solving !")

    # 打印数据
    #for v in w2v.vectors() : v.dump()

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("Word2Vector.main :__main__ : ", str(e))
        print("Word2Vector.main :__main__ : unexpected exit !")