import math
import numpy

from Content import *
from CommonTool import *

# 归一化处理
# matrix[2][d]
#@jit (axis 选项不支持)
def _normalize(matrix) :
    # 计算模长
    norm = numpy.linalg.norm(matrix, axis = 1)
    # 返回结果
    return (matrix.T * numpy.reciprocal(norm)).T

class VectorItem(ContentItem) :
    # 初始化对象
    def __init__(self, dimension, content = None, count = 1) :
        # 调用父类初始化函数
        super().__init__(content, count)
        # 检查参数
        assert dimension >= 2
        # 索引
        self.index = -1
        # 增量
        self.__delta = numpy.zeros((2, dimension))
        # 矩阵
        self.__matrix = numpy.zeros((2, dimension))

    @property
    def delta(self) :
        # 返回结果
        return self.__delta

    @property
    def matrix(self) :
        # 返回结果
        return self.__matrix

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
                "index" : self.index,
                "matrix" : self.__matrix.tolist(),
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.index = value["index"]
        self.count = value["count"]
        self.content = value["content"]
        # 检查长度
        #assert self.length == value["length"]
        # 设置举着
        self.__matrix = numpy.array(value["matrix"])

    def dump(self, dump_matrix = True, dump_delta = True):
        # 打印信息
        print("VectorItem.dump : show properties !")
        print(f"\tindex = {self.index}")
        print(f"\tcount = {self.count}")
        print(f"\tlength = {self.length}")
        print(f"\tcontent = \"{self.content}\"")
        if dump_matrix : print("matrix : "); print(self.__matrix)
        if dump_delta :   print("delta : ");  print(self.__delta)

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
        t.__matrix = 1 - 2 * \
            numpy.random.random(t.__matrix.shape)

    # 求单位向量
    @staticmethod
    def normalize(t, p = None) :
        # 计算结果
        t.__matrix = \
            _normalize(t.__matrix)

    # 遍历函数
    # 缩放误差
    @staticmethod
    def mul_delta(t, value) :
        # 矩阵加和
        t.__delta = \
            numpy.dot(value, t.__delta)

    # 遍历函数
    # 加和误差
    @staticmethod
    def add_delta(t, delta = None) :
        # 检查参数
        if delta is not None :
            # 矩阵加和
            t.__matrix += delta
        else :
            # 矩阵加和
            t.__matrix += t.__delta

    # 遍历函数
    # 寻找行和范数
    @staticmethod
    def max_delta(t, max_delta) :
        # 返回结果
        # 1: 列和范数
        # inf : 行和范数
        value = numpy.linalg.\
            norm(t.__delta, numpy.inf)
        # 检查结果
        if value > max_delta[0] : max_delta[0] = value

    # 遍历函数
    # 初始化误差矩阵
    # 将误差值设置为零
    @staticmethod
    def init_delta(t, delta = None) :
        # 检查参数
        if delta is not None :
            # 设置矩阵
            # 数组分别赋值
            t.__delta[0] = delta[0][t.index] # dAi
            t.__delta[1] = delta[1][t.index] # dBi
        else :
            # 设置初始值
            t.__delta = numpy.zeros(t.__delta.shape)

    # 遍历函数
    # 初始化矢量矩阵
    # 给矩阵赋予随机数值
    @staticmethod
    def init_matrix(t, matrix = None) :
        # 检查参数
        if matrix is not None :
            # 设置矩阵
            t.__matrix[0] = matrix[0][t.index] # Ai
            t.__matrix[1] = matrix[1][t.index] # Bi
        else :
            # 设置矩阵
            t.__matrix = 1 - 2 * \
                numpy.random.random(t.__matrix.shape)

    # 求相关系数
    # 按照公式正常处置
    @staticmethod
    def cal_gamma(t1, t2) :
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

    # 按照公式正常处置
    @staticmethod
    def cal_delta(t1, t2, delta) :
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

class VectorGroup(ContentGroup) :
    # 初始化
    def __init__(self, dimension) :
        # 调用父类初始化
        super().__init__()
        # 检查参数
        assert dimension >= 2
        # 标志位
        self.init_matrix = True
        # 设置维度
        self._dimension = dimension
        # 循环次数
        self._max_loop = 10
        # 误差
        self._error = 1.0e-5
        # 设置词汇组
        self._words = WordContent()

    # 维度
    @property
    def dimension(self) :
        # 返回结果
        return self._dimension

    # 清理
    def clear(self) :
        # 调用父类函数
        super().clear()
        # 清理词汇内容
        self._words.clear()

    # 加载数据
    def load(self, file_name):
        # 清理矢量
        super().clear()
        # 再调用父类加载数据
        super().load(file_name)
        # 设置初始化标志位
        self.init_matrix = False

    # 通过索引获得词
    def get_item(self, index) :
        # 循环处理
        for item in self.values() :
            # 返回结果
            if item.index == index : return item
        # 返回结果
        return None

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
        # 返回结果
        return item

    # 生成新的对象
    def new_item(self, content = None, count = 1) :
        # 返回结果
        return VectorItem(self._dimension, content, count)

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
        # 检查类型
        if isinstance(item, VectorItem) :
            # 增加项目
            self[content] = item
        else :
            # 增加项目
            self[content] = self.new_item(item.content, item.count)

    # 初始化
    def init_data(self, path) :
        # 加载数文件
        if not self._load_data(path):
            # 打印信息
            print("VectorGroup.init_data : fail to load files !")
            return False
        # 清理移除的数据
        vectors._remove_data(path)
        # 打印信息
        print("VectorGroup.init_data : files have been loaded !")
        # 第一次初始化相关系数
        vectors._init_gammas()
        # 清理无效数据
        vectors.clear_invalid()
        # 第二次初始化相关系数
        vectors._init_gammas()
        # 设置标志位
        self.init_matrix = True
        # 返回结果
        return True

    # 清理被移除的数据
    def _remove_data(self, path) :
        # 检查文件是否存在
        if not os.path.isfile(path + "removed.json") :
            return True
        # 清理
        removed = WordContent()
        # 加载数据
        if removed.load(path + "removed.json") <= 0 :
            # 打印信息
            printf("VectorGroup._remove_data : fail to load removed.json !")
            return False
        # 进度条
        pb = ProgressBar(len(removed))
        # 开始
        pb.begin("VectorGroup._remove_data : remove vectors and words !")
        # 循环处理
        for item in removed.values() :
            # 进度条
            pb.increase()
            # 删除已被判定需要被移除的数据
            if item.content in self :
                # 删除项目
                self.remove(item.content)
            elif item.content in self._words :
                # 删除项目
                self._words.remove(item.content)
        # 结束
        pb.end()
        # 打印信息
        print(f"VectorGroup._remove_data : {len(self)} vector(s) left !")
        print(f"VectorGroup._remove_data : {len(self._words)} word(s) left !")
        print(f"VectorGroup._remove_data : total {len(removed)} item(s) removed !")
        return True

    # 加载数据
    def _load_data(self, path) :
        # 清理
        self.clear()
        # 检查文件是否存在
        if os.path.isfile(path + "words1.json") :
            # 加载数据
            if self._words.load(path + "words1.json") <= 0 :
                # 打印信息
                print("VectorGroup._load_data : fail to load words1.json !")
                return False
        # 生成数据
        # 自动设置元素的维度
        self._words.traverse(self.add_item)
        # 打印信息
        print("VectorGroup._load_data : all vectors added !")
        # 清理
        self._words.clear()
        # 检查文件是否存在
        if os.path.isfile(path + "words2.json") :
            # 加载数据
            if self._words.load(path + "words2.json") <= 0 :
                # 打印信息
                print("VectorGroup._load_data : fail to load words2.json !")
                return False
        # 打印信息
        print("VectorGroup._load_data : all vectors initialized !")
        # 返回结果
        return True

    # 初始化相关系数
    def _init_gammas(self) :
        # 初始化相关系数
        # 需要使用索引作为临时标记位
        self.__init_gammas()
        # 打印信息
        print("VectorGroup._init_gammas : gammas initialized !")
        # 交叉检查，清理无用的矢量
        self._contents = \
            {key : item for (key, item)
             in self._contents.items() if item.index > 0}
        # 打印信息
        print("VectorGroup._init_gammas : %d row(s) left !" % len(self))
        print("VectorGroup._init_gammas : useless vectors removed !")
        # 初始化索引值
        for index, t in enumerate(self.values()) : t.index = index
        # 返回结果
        return len(self)

    # 获得标准数据
    def _get_gammas(self) :
        # 初始化索引值
        for index, t in enumerate(self.values()) : t.index = index

        # 获得维度
        n = len(self)
        # 生成数据
        gammas = numpy.zeros((n, n))
        # 初始化相关系数
        for item in self._words.values() :
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
            if c1 not in self : continue
            # 获得索引值
            i = self[c1].index

            # 获得单词
            c2 = c[-1]
            # 检查数据
            if c2 not in self : continue
            # 获得索引值
            j = self[c2].index

            # 设置数值
            gammas[i][j] = item.gamma \
                if 0 <= item.gamma <= 1.0 else 0.0
        # 返回结果
        return gammas

    # 初始化相关系数
    def __init_gammas(self) :
        # 索引清零
        # 临时做为标记位使用
        for t in self.values() : t.index = 0

        # 总数
        total = len(self._words)
        # 进度条
        pb = ProgressBar(total)
        # 开始
        pb.begin(f"VectorGroup.__init_gammas : init gammas[{total}] !")
        # 初始化相关系数
        for item in self._words.values() :
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
            # 检查结果
            if item.gamma > 1.0 : item.gamma = 0.0
        # 结束
        pb.end()

    # 清理无效数据
    def clear_invalid(self, path = None) :
        # 调用父类函数
        super().clear_invalid()

        # 清理无效数据
        # 进度条
        pb = ProgressBar(len(self))
        # 开始
        pb.begin(f"VectorGroup.clear_invalid : clear invalid vectors !")
        # 创建对象
        removed = WordContent()
        # 循环处理
        for item in self.values() :
            # 进度条
            pb.increase()
            # 检查计数
            # 至少需要的记录次数
            if item.count >= 256 :
                continue
            # 将无效数据加入删除队列中
            if item.content not in removed :
                # 加入数据
                removed.add_item(item)
        # 仅保留有效项目
        self._contents = \
            { key : item for (key, item)
              in self._contents.items() if item.count >= 2 * self._dimension}
        # 结束
        pb.end()

        """
        # 进度条
        pb = ProgressBar(len(self))
        # 开始
        pb.begin("VectorGroup.clear_invalid : clear invalid vectors !")
        # 获得相关系数
        gammas = self._get_gammas()
        # 获得关系系数符号矩阵
        signs = numpy.sum(numpy.abs(numpy.sign(gammas)), axis = 1)
        # 循环检查
        for item in self.values() :
            # 进度条
            pb.increase()
            # 获得索引
            index = item.index
            # 检查结果
            if signs[index] < 2 * self._dimension :
                # 相关关系数量不能低于维度
                # 关系方程不足，则方程必定无解
                if item.content not in removed : removed.add_item(item)
        # 结束
        pb.end()
        # 打印信息
        print(f"VectorGroup.clear_invalid : average ({int(numpy.mean(signs))}) relation(s) !")
        """

        # 进度条
        pb = ProgressBar(len(self._words))
        # 开始
        pb.begin("VectorGroup.clear_invalid : clear invalid words !")
        # 清理词汇
        for item in self._words.values() :
            # 进度条
            pb.increase()
            # 获得词汇
            content = item.content
            # 逐个检查单词
            for c in content :
                # 检查状态
                if c not in removed : continue
                # 如果发现有字符在被删除要求中
                # 将无效词汇数据加入删除队列中
                if item.content not in removed : removed.add_item(item)
        # 结束
        pb.end()

        # 保存文件
        if isinstance(path, str) :
            # 保存被删除的文件
            if removed.save(path + "removed.json") :
                # 打印信息
                print("VectorGroup.clear_invalid : removed.json saved !")
            else :
                # 打印信息
                print("VectorGroup.clear_invalid : fail to save removed.json !")

        # 进度条
        pb = ProgressBar(len(removed))
        # 开始
        pb.begin("VectorGroup.clear_invalid : remove all items !")
        # 清理词汇
        for item in removed.values() :
            # 进度条
            pb.increase()
            # 删除
            if item.content in self : self.remove(item.content)
            if item.content in self._words : self._words.remove(item.content)
        # 结束
        pb.end()
        # 打印信息
        print(f"VectorGroup.clear_invalid : {len(self)} vector(s) left !")
        print(f"VectorGroup.clear_invalid : {len(self._words)} word(s) left !")
        print(f"VectorGroup.clear_invalid : total {len(removed)} item(s) removed !")

    # 完成一次全量计算
    def solving(self):
        # 检查参数
        assert 0 < self._error < 1.0
        # 检查内容
        if len(self) < 2:
            print("VectorGroup.solving : insufficient vectors !")
            return numpy.inf

        # 初始化相关系数
        self._init_gammas()
        # 相关系数矩阵
        gammas = self._get_gammas()
        # 检查标记位
        if self.init_matrix:
            # 清除标记位
            self.init_matrix = False
            # 初始化矩阵
            self.traverse(VectorItem.init_matrix)

        # 循环计数
        i = 0; j = 0
        # 最大行和范数
        last_delta = numpy.inf
        # 循环直至误差符合要求，或者收敛至最小误差
        while i < self._max_loop:
            # 计数器加一
            i += 1; j += 1
            # 设置初始误差矩阵
            self._traverse(VectorItem.init_delta)
            # 求解方程
            delta = self.__solving(gammas)
            # 打印信息
            print(f"VectorGroup.solving : ΔGamma[{i}, {j}] = {delta} !")
            # 检查结果
            if last_delta > delta:
                # 呈下降趋势
                i = 0; last_delta = delta
            # 检查结果
            if delta > self._error:
                # 求平均值
                self._traverse(VectorItem.mul_delta, 1.0 / float(len(self)))
                # 进行加和计算
                self._traverse(VectorItem.add_delta)
                # 重置无效的数据
                self._traverse(VectorItem.reset_useless)
            else:
                # 最大行和范数
                delta_norm = [0]
                # 获得误差矩阵的最大行和范数
                self._traverse(VectorItem.max_delta, delta_norm)
                # 打印结果
                print(f"VectorGroup.solving : delta_norm[{j}] = {delta_norm[0]} !")
                break
        # 返回结果
        return last_delta

    # 完成一次全量计算
    def __solving(self, gammas) :
        # 获得总数
        total = len(self) * len(self)
        # 进度条
        pb = ProgressBar(total)
        # 打印信息
        #pb.begin(f"VectorGroup.__solving : try to process {total} relation(s) !")
        pb.begin()

        # 最大误差
        max_delta = 0.0
        # 最大误差位置
        row = -1; col = -1
        # 循环处理
        for t1 in self.values() :
            # 循环处理
            for t2 in self.values() :
                # 相关系数
                gamma = gammas[t1.index][t2.index]
                # 增加计数
                pb.increase()

                # 拷贝原始矩阵
                matrix1 = t1.matrix
                # 拷贝原始矩阵
                matrix2 = t2.matrix
                # 获得相关系数误差（快捷处置）
                delta = gamma - \
                        numpy.dot(matrix1[0], matrix2[1])  # Ai.Bj

                # 增加处理过程
                abs_delta = numpy.abs(delta)
                # 检查结果
                if abs_delta > max_delta :
                    # 设置误差记录
                    max_delta = abs_delta

                # 计算模长
                _Bj = numpy.dot(matrix2[1], matrix2[1])
                _Ai = numpy.dot(matrix1[0], matrix1[0])
                # 计算数据
                value = delta / (_Bj + _Ai)
                # 计算分量（快捷处置）加和误差分量
                t1.delta[0] += numpy.dot(value, matrix2[1])
                # 计算分量（快捷处置）加和误差分量
                t2.delta[1] += numpy.dot(value, matrix1[0])
        # 打印信息
        pb.end()
        #pb.end(f"VectorGroup.__solving : {total} relations(s) processed !")
        # 返回结果
        return max_delta

    # 获得掩码矩阵
    def __get_max_positions(self, n, delta, length) :
        # 检查参数
        if length < 0 : length = 0
        elif length >= n : length = n - 1
        # 打印信息
        #print(f"VectorGroup.__get_max_positions : {length + 1} required !")
        # 位置记录
        positions = []
        # 获得误差的绝对值
        abs_delta = numpy.abs(delta)

        # 查找最大值的位置
        pos = numpy.argmax(abs_delta)
        # 获得索引
        row = pos // n
        col = pos - row * n
        max_delta = abs_delta[row][col]
        # 记录位置
        positions.append([row, col, max_delta])

        # 检查结果
        if max_delta > self._error :
            # 循环处理
            for i in range(length) :
                # 查找最大值的位置
                pos = numpy.argmax(abs_delta)
                # 获得索引
                row = pos // n
                col = pos - row * n
                value = abs_delta[row][col]
                # 检查结果
                if value <= self._error: break
                # 记录位置
                positions.append([row, col, value])
                # 划去该位置的行列数据
                abs_delta[row][:] = 0.0; abs_delta[:][col] = 0.0
        # 返回结果
        return positions

    # 完成一次全量计算
    def fast_solving(self) :
        # 检查参数
        assert 0 < self._error < 1.0
        # 总数
        # 也是维度之一
        n = len(self)
        # 检查内容
        if n < 2:
            print("VectorGroup.fast_solving : insufficient vectors !")
            return numpy.inf

        # 初始化相关系数
        # 有删除无效数据的行为
        n = self._init_gammas()
        # 相关系数矩阵
        gammas = self._get_gammas()

        # 生成Ais
        ais = 1.0 - 2.0 * \
            numpy.random.random((n, self._dimension))
        # 生成Bjs
        bjs = 1.0 - 2.0 * \
            numpy.random.random((n, self._dimension))
        # 检查标记位
        if not self.init_matrix :
            # 进度条
            pb = ProgressBar(n)
            # 开始
            pb.begin(f"VectorGroup.fast_solving : copy matrix[{n}] !")
            # 循环处理
            for item in self.values() :
                # 进度条
                pb.increase()
                # 获得索引值
                index = item.index
                # 循环处理
                # 复制过程不能破坏完整性
                # 复制过程将隔离原始数据和计算数据
                for k in range(self._dimension) :
                    # 复制Ai
                    ais[index][k] = item.matrix[0][k]
                    # 复制Bi
                    bjs[index][k] = item.matrix[1][k]
            # 结束
            pb.end()
        else :
            # 归一化
            ais = _normalize(ais)
            bjs = _normalize(bjs)
            # 清理标志位
            self.init_matrix = False
            # 初始化矩阵
            self.traverse(VectorItem.init_matrix, [ais, bjs])
            # 打印信息
            print(f"VectorGroup.fast_solving : matrix[{n}] initialized !")

        # 搜索长度
        length = 0
        # 循环计数
        i = 0; j = 0
        # 最大行和范数
        last_delta = numpy.inf
        # 循环直至误差符合要求，或者收敛至最小误差
        while i < self._max_loop :
            # 计数器加一
            i += 1; j += 1

            # 获得计算值
            delta = gammas - numpy.dot(ais, bjs.T)

            # 获得一系列误差最大值位置记录
            positions = self.__get_max_positions(n, delta, length)
            # 检查参数
            assert len(positions) >= 1
            # 获得最大误差值
            row = positions[0][0]
            col = positions[0][1]
            max_delta = positions[0][2]
            # 检查结果
            if max_delta <= self._error :
                # 设置数值，并中断循环
                last_delta = max_delta; break
            # 临时记录
            _last_delta = last_delta
            # 检查结果
            if last_delta < max_delta :
                # 呈上升趋势
                length = 0
            else :
                # 呈下降趋势
                i = 0; length += 1
                # 保存上次误差
                last_delta = max_delta
                # 检查结果
                if length > n // 2 : length = n // 2

            # 生成掩码矩阵
            _mask = numpy.zeros((n, n))
            # 设置掩码矩阵
            for pos in positions :
                _mask[pos[0]][pos[1]] = 1.0
            # 屏蔽其他数据
            delta = numpy.multiply(delta, _mask)

            # 通过误差计算步长，并移至下一个步骤
            # 计算模长
            _Ais = numpy.sum(numpy.square(ais), axis = 1)
            _Ais = numpy.reshape(_Ais, (n, 1))
            _Ais = numpy.tile(_Ais, (1, n))
            # 计算模长
            _Bjs = numpy.sum(numpy.square(bjs), axis = 1)
            _Bjs = numpy.reshape(_Bjs, (1, n))
            _Bjs = numpy.tile(_Bjs, (n, 1))
            # 计算系数矩阵
            _L = numpy.multiply(delta, numpy.reciprocal(_Bjs + _Ais))
            # 计算误差分量
            _dAi = numpy.dot(_L, bjs)
            _dBj = numpy.dot(_L.T, ais)
            # 注意：分成两个步骤计算！！！
            ais += _dAi; bjs += _dBj

            # 打印信息
            print(f"VectorGroup.fast_solving : show result !")
            print(f"\t<{length}>:Gamma = {gammas[row][col]}")
            print(f"\t∇Gamma[{i},{j}] = {max_delta}")
            if j > 1 : print(f"\t∇²Gamma[{i},{j}] = {_last_delta - max_delta}")
            # 保存文件
            with open("solving.csv", "a+") as file:
                file.writelines(f"{i},{length},{gammas[row][col]},{max_delta},{_last_delta - max_delta}\n")
                file.close()

        # 设置数据矩阵
        self.traverse(VectorItem.init_matrix, [ais, bjs])
        # 打印信息
        print(f"VectorGroup.fast_solving : final matrix[{n}] copied !")
        # 返回结果
        return last_delta

    def kick_out(self, t1, t2) :
        # 维度
        n = len(self)
        # 断言
        assert t1 is not None and t2 is not None
        # 删除该项目
        content = t1.content + t2.content
        # 设置相关系数
        word = WordItem(content, 0); word.gamma = 0
        # 检查参数
        if content in self._words: word = self._words[content]

        # 删除项目
        if t1.content in self :
            self.remove(t1.content)
        if t2.content in self :
            self.remove(t2.content)
        if word.content in self._words :
            self._words.remove(content)
        # 打印计算值
        print("VectorGroup.kick_out : kick_out vectors !")
        print(f"\tt1[{t1.index},\"{t1.content}\"].count = {t1.count}")
        print(f"\tt2[{t2.index},\"{t2.content}\"].count = {t2.count}")
        print(f"\tword(\"{word.content}\").count = {word.count} ({word.gamma})")

    # 直接拟合两个词汇
    def disturb(self, t1, t2) :
        # 维度
        n = len(self)
        # 断言
        assert t1 is not None and t2 is not None
        # 删除该项目
        content = t1.content + t2.content
        # 设置相关系数
        word = WordItem(content, 0); word.gamma = 0
        # 检查参数
        if content in self._words: word = self._words[content]

        # 获得计算相关系数
        gamma = VectorItem.cal_gamma(t1, t2)
        # 计算两者的相关系数误差
        delta = word.gamma - gamma
        # 计算两者直接的误差分量
        _dAi, _dBj = VectorItem.cal_delta(t1, t2, delta / 2)
        # 直接纠正矢量
        VectorItem.add_delta(t1, _dAi)
        VectorItem.add_delta(t2, _dBj)

        # 打印计算值
        print("VectorGroup.disturb : disturb vectors !")
        print(f"\tt1[{t1.index},\"{t1.content}\"].count = {t1.count}")
        print(f"\tt2[{t2.index},\"{t2.content}\"].count = {t2.count}")
        print(f"\tword(\"{word.content}\").count = {word.count} ({word.gamma})")

# 路径
json_path = ".\\json\\"
# 生成对象
vectors = VectorGroup(2048)

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

def solving() :
    # 检查参数
    if len(vectors) <= 0 :
        # 打印信息
        print("Word2Vector.solving : insufficient vectors !")
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
            print("Word2Vector.solving : fail to solve !")
        else :
            print("Word2Vector.solving : successfully done !"); break

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
            solving()
        elif user_input == '6' :
            # 验证
            verify_vectors()
        elif user_input == '7' :
            # 计算例子
            fast_calculation_example()
        elif user_input == '8' :
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