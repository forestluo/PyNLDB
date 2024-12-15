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

from nlp.alg.WordVector import *
from nlp.alg.SimpleSolution import *

from nlp.item.WordItem import *
from nlp.item.VectorItem import *
from nlp.content.CoreContent import *
from nlp.content.WordContent import *
from nlp.content.VectorContent import *

class WordVectorization(WordVector) :
    # 初始化
    def __init__(self, dimension) :
        # 调用父类初始化
        super().__init__(dimension)
        # 设置词汇组
        self._words = WordContent()

    # 析构
    def __del__(self) :
        # 调用父类函数
        super().__del__()
        # 清除
        self._words.clear()
        # 删除
        del self._words

    @property
    def wsize(self) :
        # 返回结果
        return len(self._words)

    def clear(self) :
        # 调用父类函数
        super().clear()
        # 清理
        self._words.clear()

    def words(self) :
        # 返回结果
        return self._words.values()

    # 获得词汇
    def word(self, key) :
        # 检查参数
        if key in self._words :
            # 返回结果
            return self._words[key]
        # 返回结果
        return None

    # 获得标准数据
    def get_gammas(self, error) :
        # 重建索引
        self.index_vectors()
        # 结束
        print(f"WordVectorization.get_gammas : finished reindexing vectors !")

        # 创建矩阵
        gammas = self._new_gamma()
        # 进度条
        pb = ProgressBar(self.wsize)
        # 开始
        pb.begin(f"WordVectorization.get_gammas : building matrix !")
        # 初始化相关系数
        for item in self.words() :
            # 进度条
            pb.increase()

            # 获得内容
            f = item.count
            c = item.content
            # 检查数据
            assert len(c) == 2
            # 检查数值
            if f <= 0 : continue

            # 获得单词
            c1 = c[:1]
            # 检查数据
            v1 = self.vector(c1)
            # 检查结果
            if v1 is None : continue

            # 获得单词
            c2 = c[-1]
            # 检查数据
            v2 = self.vector(c2)
            # 检查结果
            if v2 is None : continue

            # 设置数值
            gammas[0][v1.index][v2.index] = item.gamma
            # 检查结果
            if item.gamma > error : \
                    gammas[1][v1.index][v2.index] = 1.0
        # 结束
        pb.end(f"WordVectorization.get_gammas : finished building matrix !")
        # 返回结果
        return gammas

    # 初始化
    def initialize(self, path) :
        # 加载数文件
        if not self.__load_words(path):
            # 打印信息
            print(f"WordVectorization.initialize : fail to load words !")
            return False
        # 设置标记
        self.copy_data = False
        # 打印信息
        print(f"WordVectorization.initialize : words have been loaded !")
        # 初始化相关系数
        # 需要使用索引作为临时标记位
        self.__init_gammas()
        # 打印信息
        print(f"WordVectorization.initialize : gammas initialized !")
        # 清理无效数据
        self.__clear_invalid()
        # 打印信息
        print(f"WordVectorization.initialize : invalid data cleared !")
        # 重建索引
        self.index_vectors()
        # 打印信息
        print(f"WordVectorization.initialize : index of vectors rebuilt !")
        # 返回结果
        return True

    # 加载数据
    def __load_words(self, path) :
        # 清理
        self._words.clear()
        # 检查文件是否存在
        if os.path.isfile(path + "words1.json") :
            # 加载数据
            if self._words.load(path + "words1.json") <= 0 :
                # 打印信息
                print("WordVectorization.__load_words : fail to load words1.json !")
                return False
        # 清理数据
        self._vectors.clear()
        # 生成数据
        # 自动设置元素的维度
        self._words.traverse(self._vectors.add_item)
        # 打印信息
        print("WordVectorization.__load_words : all vectors added !")
        # 清理
        self._words.clear()
        # 检查文件是否存在
        if os.path.isfile(path + "words2.json") :
            # 加载数据
            if self._words.load(path + "words2.json") <= 0 :
                # 打印信息
                print("WordVectorization.__load_words : fail to load words2.json !")
                return False
        # 打印信息
        print("WordVectorization.__load_words : all vectors initialized !")
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
        pb.begin(f"WordVectorization.__init_gammas : init gammas[{total}] !")
        # 初始化相关系数
        for item in self.words() :
            # 进度条
            pb.increase()
            # 获得频次
            c = item.content
            # 检查数值
            if item.count <= 0 :
                item.gamma = 0.0; continue

            # 检查数据
            assert len(c) == 2

            # 获得单词
            c1 = c[:1]
            # 获得矢量
            v1 = self.vector(c1)
            # 检查数据
            if v1 is None :
                item.gamma = 0.0; continue
            # 检查数据
            if v1.count <= 0 :
                item.gamma = 0.0; continue

            # 获得单词
            c2 = c[-1]
            # 获得矢量
            v2 = self.vector(c2)
            # 检查数据
            if v2 is None :
                # 设置为无效值
                item.gamma = 0.0; continue
            # 检查数据
            if v2.count <= 0 :
                item.gamma = 0.0; continue

            # 设置标记位
            v1.index |= 0x01
            # 设置标记位
            v2.index |= 0x02
            # 计算相关系数
            item.gamma = 0.5 * float(item.count) \
                * (1.0 / float(v1.count) + 1.0 / float(v2.count))
        # 结束
        pb.end()

    # 清理无效数据
    def __clear_invalid(self) :
        # 清理无效数据
        # 进度条
        pb = ProgressBar(self.vsize)
        # 开始
        pb.begin(f"WordVectorization.__clear_invalid : clear invalid vectors !")
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
        pb.begin(f"WordVectorization.__clear_invalid : clear invalid words !")
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
        pb.begin(f"WordVectorization.__clear_invalid : remove all items !")
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
        print(f"WordVectorization.__clear_invalid : {self.wsize} word(s) left !")
        print(f"WordVectorization.__clear_invalid : {self.vsize} vector(s) left !")
        print(f"WordVectorization.__clear_invalid : total {len(removed)} item(s) removed !")

    # 加载数据
    def load_words(self, file_name) :
        # 创建
        words = WordContent()
        # 再调用父类加载数据
        result = words.load(file_name)
        # 检查结果
        if result <= 0 :
            # 打印信息
            print(f"WordVectorization.load_words : loading({file_name}) failed !")
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
        print(f"WordVectorization.load_words : total {self.wsize} item(s) loaded !")
        # 初始化相关系数
        self.__init_gammas()
        # 打印信息
        print(f"WordVectorization.load_words : gammas initialized !")
        # 清理无效数据
        self.__clear_invalid()
        # 打印信息
        print(f"WordVectorization.load_words : invalid data cleared !")
        # 重建索引
        self.index_vectors()
        # 打印信息
        print(f"WordVectorization.load_words : index of vectors rebuilt !")
        # 返回结果
        return result

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
        print(f"WordVectorization.load_example : gammas initialized !")
        # 重建索引
        self.index_vectors()
        # 打印信息
        print(f"WordVectorization.load_example : index of vectors rebuilt !")

# 测试代码
def main() :

    # 生成对象
    wv = WordVectorization(32)

    # 选项
    options = 2
    # 检查选项
    if options == 0 :
        # 加载例程
        wv.load_example()
    elif options == 1 :
        # 初始化
        if not wv.initialize("..\\..\\json\\") :
            # 打印信息
            print("WordVectorization.main : fail to initialize !")
            return
        # 打印信息
        print("WordVectorization.main : successfully initialized !")
    elif options == 2 :
        # 加载数据
        if wv.load_vectors("..\\..\\json\\vectors.json") <= 0 :
            # 打印信息
            print("WordVectorization.main : fail to load vectors.json !")
            return
        # 加载数据
        if wv.load_words("..\\..\\json\\cores.json") <= 0 :
            # 打印信息
            print("WordVectorization.main : fail to load cores.json !")
            return
    else :
        # 打印信息
        print(f"WordVectorization.main : unknown options({options}) !")
        return

    # 打印信息
    print("WordVectorization.main : successfully loaded !")
    # 获得求解器
    solution = wv.get_solution("cupy.l2")
    # 检查结果
    if solution is None :
        # 打印信息
        print("WordVectorization.main : fail to get solution !")
        return
    # 启动
    solution.start()
    # 打印信息
    print("WordVectorization.main : successfully start solving !")
    # 等待输入
    input()
    # 结束线程
    solution.stop()
    # 打印信息
    print("WordVectorization.main : successfully stopped solving !")

    # 检查参数
    if options == 0 :
        # 打印数据
        for v in wv.vectors() : v.dump()

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("WordVectorization.main :__main__ : ", str(e))
        print("WordVectorization.main :__main__ : unexpected exit !")