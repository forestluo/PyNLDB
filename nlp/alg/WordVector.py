# -*- coding: utf-8 -*-
from nlp.item.VectorItem import *
from nlp.content.VectorContent import *

class WordVector :
    # 初始化
    def __init__(self, dimension) :
        # 检查参数
        assert dimension >= 2
        # 最小记录次数
        self.min_count = 128
        # 拷贝数据
        self.copy_data = False
        # 设置是两组
        self._vectors = VectorContent(dimension)

    # 析构
    def __del__(self) :
        # 清理
        self._vectors.clear()
        # 删除
        del self._vectors

    # 维度
    @property
    def dimension(self) :
        # 返回结果
        return self._vectors.dimension

    @property
    def vsize(self) :
        # 返回结果
        return len(self._vectors)

    def clear(self) :
        # 清理
        self._vectors.clear()

    def vectors(self) :
        # 返回结果
        return self._vectors.values()

    # 获得词汇
    def vector(self, key) :
        # 检查参数
        if key in self._vectors :
            # 返回结果
            return self._vectors[key]
        # 返回结果
        return None

    # 新建相关系数矩阵
    def _new_gamma(self) :
        # 创建矢量矩阵
        # 只有这样定义二维数组才能防止“粘连”
        # 即，数组按行或者按列形成了完全绑定关系
        return [[[0.0
            for _ in range(self.vsize)]
            for _ in range(self.vsize)] for _ in range(2)]

    # 保存数据
    def save_vectors(self, file_name) :
        # 保存文件
        self._vectors.save(file_name)
        # 打印信息
        print(f"WordVector.save_vectors : file was saved !")

    # 重建索引
    def index_vectors(self) :
        # 进度条
        pb = ProgressBar(self.vsize)
        # 开始
        pb.begin(f"WordVector.index_vectors : reindex vectors !")
        # 初始化索引值
        for index, v in enumerate(self.vectors()) :
            # 进度条
            pb.increase()
            # 设置索引
            v.index = index
        # 结束
        pb.end(f"WordVector.index_vectors : {self.vsize} vector(s) indexed !")

    # 加载数据
    def load_vectors(self, file_name) :
        # 清理
        vectors = VectorContent(self.dimension)
        # 加载矢量数据
        result = vectors.load(file_name)
        # 检查结果
        if result <= 0 : return result
        # 打印信息
        print(f"WordVector.load_vectors : file was loaded !")
        # 进度条
        pb = ProgressBar(len(vectors))
        # 开始
        pb.begin(f"WordVector.load_vectors : checking dimension of vectors !")
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
            if dimension < 0 : dimension = size
            elif size != dimension :
                # 打印信息
                print(f"WordVector.load_vectors : incorrect dimension({size}) !")
                return -1
        # 结束
        pb.end()
        # 检查维度
        if dimension < 2 :
            # 打印信息
            print(f"WordVector.load_vectors : improper dimension({dimension}) !")
            return -1
        # 设置矢量
        self._vectors = vectors
        # 打印信息
        print(f"WordVector.load_vectors : vectors were set !")
        # 重建索引
        self.index_vectors()
        # 打印信息
        print(f"WordVector.load_vectors : index of vectors rebuilt !")
        # 设置维度
        self._vectors.dimension = dimension
        # 打印信息
        print(f"WordVector.load_vectors : vectors(dimension = {dimension}) loaded !")
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
        print(f"WordVector.get_solution : unrecognized method(\"{method}\") !")
        # 返回结果
        return None
