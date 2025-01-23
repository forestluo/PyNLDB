# -*- coding: utf-8 -*-
import threading

from nlp.alg.WordVector import *
from nlp.tool.GammaTool import *

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

    # 获得相关系数
    # 兼容效率及格式
    def get_gammas(self, error) :
        # 重建索引
        self.index_vectors()
        # 结束
        print(f"WordVectorization.get_gammas : finished reindexing vectors !")

        # 创建矩阵
        gammas = self._new_gamma()
        # 进度条
        pb = ProgressBar(slef.wsize)
        # 开始
        pb.begin(f"WordVectorization.get_gammas : building matrix !")
        # 初始化相关系数
        for w in self.words() :
            # 增加计数
            pb.increase()
            # 检查结果
            if w.length <= 1 or w.count <= 0 : continue
            # 将词汇进行分解
            for i in range(1, w.length) :
                # 分解
                w1 = w[0:i]; w2 = w[i:]
                # 获得矢量
                v1 = self.vector(w1)
                # 检查结果
                if v1 is None or v1.count <= 0 : continue
                # 获得矢量
                v2 = self.vector(w2)
                # 检查结果
                if v2 is None or v2.count <= 0 : continue
                # 计算Gamma数值
                gamma = 0.5 * w.count / (v1.count + v2.count)
                # 设置数值
                gammas[0][v1.index][v2.index] = gamma
                # 检查结果
                if gamma > error : gammas[1][v1.index][v2.index] = 1.0
        # 结束
        pb.end(f"WordVectorization.get_gammas : finished building matrix !")
        # 返回结果
        return gammas

    # 清理无效数据
    def clear_invalid(self) :
        # 调用父类函数
        super().clear_invalid()
        # 检查参数
        if self.wsize <= 0 : return
        # 创建对象
        removed = WordContent()
        # 进度条
        pb = ProgressBar(self.wsize)
        # 开始
        pb.begin(f"WordVectorization.clear_invalid : clear invalid words !")
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
                if c not in self._vectors : removed.add_item(item)
        # 结束
        pb.end()
        # 检查结果
        if len(removed) > 0 :
            # 进度条
            pb = ProgressBar(len(removed))
            # 开始
            pb.begin(f"WordVectorization.clear_invalid : remove all items !")
            # 清理词汇
            for item in removed.values() :
                # 进度条
                pb.increase()
                # 删除
                if item.content in self._words : self._words.remove(item.content)
            # 结束
            pb.end(f"WordVectorization.clear_invalid : total {len(removed)} item(s) removed !")
        # 打印信息
        print(f"WordVectorization.clear_invalid : {self.wsize} word(s) left !")

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
        # 重建索引
        self.index_vectors()
        # 打印信息
        print(f"WordVectorization.load_example : index of vectors rebuilt !")

    # 加载数据
    def load_default(self, path) :
        # 调用父类函数
        if not super().load_default(path) :
            return False
        # 返回结果
        return self.load_words(path + "words2.json")

    # 加载数据
    def load_words(self, file_name) :
        # 创建
        words = WordContent()
        # 检查结果
        if words.load(file_name) <= 0 :
            # 打印信息
            print(f"WordVectorization.load_words : loading({file_name}) failed !")
            return False
        # 设置参数
        self._words = words
        # 打印信息
        print(f"WordVectorization.load_words : total {self.wsize} item(s) loaded !")
        # 清理无效数据
        self.clear_invalid()
        # 打印信息
        print(f"WordVectorization.load_words : invalid data cleared !")
        # 重建索引
        self.index_vectors()
        # 打印信息
        print(f"WordVectorization.load_words : index of vectors rebuilt !")
        # 返回结果
        return True

# 测试代码
def main() :

    # 生成对象
    wv = WordVectorization(32)

    # 选项
    options = 3
    # 检查选项
    if options == 0 :
        # 加载例程
        wv.load_example()
    elif options == 1 :
        # 初始化
        if not wv.load_default("..\\..\\json\\") :
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
    elif options == 3 :
        # 加载数据
        if wv.load_vectors("..\\..\\json\\cores.json", False) <= 0 :
            # 打印信息
            print("WordVectorization.main : fail to load cores.json !")
            return
        # 循环处理
        for i in range(1, 5) :
            # 加载数据
            if wv.load_words(f"..\\..\\json\\words{i}.json") <= 0 :
                # 打印信息
                print(f"WordVectorization.main : fail to load words{i}.json !")
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