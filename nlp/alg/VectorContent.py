# -*- coding: utf-8 -*-

import time

import numpy

from nlp.alg.Scripts import *
from nlp.alg.VectorItem import *
from nlp.content.WordContent import *

class VectorContent(ContentGroup) :
    # 初始化
    def __init__(self, dimension) :
        # 调用父类初始化
        super().__init__()
        # 检查参数
        assert dimension >= 2
        # 标志位
        self.init_matrix = True
        # 是否使用CUDA
        self._use_cupy = True
        # 设置维度
        self._dimension = dimension
        # 循环次数
        self._max_loop = 100
        # 误差
        self._error = 0.00001
        # 最小记录次数
        self._min_count = 1024
        # 主动中断循环
        self.break_loop = False
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
            print("VectorContent.init_data : fail to load files !")
            return False
        # 清理移除的数据
        self._remove_data(path)
        # 打印信息
        print("VectorContent.init_data : files have been loaded !")
        # 第一次初始化相关系数
        self._init_gammas()
        # 清理无效数据
        self.clear_invalid()
        # 第二次初始化相关系数
        self._init_gammas()
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
            printf("VectorContent._remove_data : fail to load removed.json !")
            return False
        # 进度条
        pb = ProgressBar(len(removed))
        # 开始
        pb.begin("VectorContent._remove_data : remove vectors and words !")
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
        print(f"VectorContent._remove_data : {len(self)} vector(s) left !")
        print(f"VectorContent._remove_data : {len(self._words)} word(s) left !")
        print(f"VectorContent._remove_data : total {len(removed)} item(s) removed !")
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
                print("VectorContent._load_data : fail to load words1.json !")
                return False
        # 生成数据
        # 自动设置元素的维度
        self._words.traverse(self.add_item)
        # 打印信息
        print("VectorContent._load_data : all vectors added !")
        # 清理
        self._words.clear()
        # 检查文件是否存在
        if os.path.isfile(path + "words2.json") :
            # 加载数据
            if self._words.load(path + "words2.json") <= 0 :
                # 打印信息
                print("VectorContent._load_data : fail to load words2.json !")
                return False
        # 打印信息
        print("VectorContent._load_data : all vectors initialized !")
        # 返回结果
        return True

    # 初始化相关系数
    def _init_gammas(self) :
        # 初始化相关系数
        # 需要使用索引作为临时标记位
        self.__init_gammas()
        # 打印信息
        print("VectorContent._init_gammas : gammas initialized !")
        # 交叉检查，清理无用的矢量
        self._contents = \
            {key : item for (key, item)
             in self._contents.items() if item.index > 0}
        # 打印信息
        print("VectorContent._init_gammas : %d row(s) left !" % len(self))
        print("VectorContent._init_gammas : useless vectors removed !")
        # 进度条
        pb = ProgressBar(len(self))
        # 开始
        pb.begin(f"VectorContent._init_gammas : reindex vectors !")
        # 初始化索引值
        for index, t in enumerate(self.values()) :
            # 进度条
            pb.increase()
            # 设置索引
            t.index = index
        # 结束
        pb.end(f"VectorContent._init_gammas : {len(self)} vector(s) indexed !")
        # 返回结果
        return len(self)

    # 获得标准数据
    def __get_gammas(self, n) :
        # 初始化索引值
        for index, t in enumerate(self.values()) : t.index = index

        # 生成数据
        gammas = numpy.zeros((2, n, n))
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
            gammas[0][i][j] = item.gamma
            # 检查结果
            if item.gamma > self._error : gammas[1][i][j] = 1.0
        # 返回结果
        return cupy.asarray(gammas) if self._use_cupy else gammas

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
        pb.begin(f"VectorContent.__init_gammas : init gammas[{total}] !")
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
            # 检查相关结果
            # 将结果值限定在范围内
            if item.gamma > 1.0 : item.gamma = 1.0
            elif item.gamma <= self._error : item.gamma = 0.0

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
        pb.begin(f"VectorContent.clear_invalid : clear invalid vectors !")
        # 创建对象
        removed = WordContent()
        # 循环处理
        for item in self.values() :
            # 进度条
            pb.increase()
            # 检查计数
            # 至少需要的记录次数
            if item.count >= self._min_count :
                continue
            # 将无效数据加入删除队列中
            if item.content not in removed :
                # 加入数据
                removed.add_item(item)
        # 仅保留有效项目
        self._contents = \
            { key : item for (key, item)
              in self._contents.items() if item.count >= self._min_count}
        # 结束
        pb.end()

        # 进度条
        pb = ProgressBar(len(self._words))
        # 开始
        pb.begin("VectorContent.clear_invalid : clear invalid words !")
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
                print("VectorContent.clear_invalid : removed.json saved !")
            else :
                # 打印信息
                print("VectorContent.clear_invalid : fail to save removed.json !")

        # 进度条
        pb = ProgressBar(len(removed))
        # 开始
        pb.begin("VectorContent.clear_invalid : remove all items !")
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
        print(f"VectorContent.clear_invalid : {len(self)} vector(s) left !")
        print(f"VectorContent.clear_invalid : {len(self._words)} word(s) left !")
        print(f"VectorContent.clear_invalid : total {len(removed)} item(s) removed !")

    def solving(self, algorithm = 0) :
        # 检查算法名称
        if algorithm == 1 :
            return self._l1_solving()
        elif algorithm == 2 :
            # 返回结果
            return self._l2_solving()
        elif algorithm >= 3 :
            # 返回结果
            return self._linf_solving()
        else :
            # 返回结果
            return self._classic_solving()

    # 完成一次全量计算
    def _classic_solving(self):
        # 检查参数
        assert 0 < self._error < 1.0
        # 维度
        n = len(self)
        # 检查内容
        if n < 2 :
            print("VectorContent._classic_solving : insufficient vectors !")
            return numpy.inf

        # 初始化相关系数
        n = self._init_gammas()
        # 相关系数矩阵
        gammas = self.__get_gammas(n)
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
        while i < self._max_loop :
            # 检查标志位
            if self.break_loop : break
            # 计数器加一
            i += 1; j += 1
            # 设置初始误差矩阵
            self._traverse(VectorItem.init_delta)
            # 求解方程
            delta = self.__classic_solving(gammas[0])
            # 打印信息
            print(f"VectorContent._classic_solving : ΔGamma[{i}, {j}] = {delta} !")
            # 检查结果
            if last_delta > delta:
                # 呈下降趋势
                i = 0; last_delta = delta
            # 检查结果
            if delta > self._error:
                # 求平均值
                self._traverse(VectorItem.mul_delta, 1.0 / float(n))
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
                print(f"VectorContent._classic_solving : delta_norm[{j}] = {delta_norm[0]} !")
                break
        # 清除标记
        self.break_loop = False
        # 返回结果
        return last_delta

    # 完成一次全量计算
    def __classic_solving(self, gammas) :
        # 获得总数
        total = len(self) * len(self)
        # 进度条
        pb = ProgressBar(total)
        # 打印信息
        #pb.begin(f"VectorContent.__classic_solving : try to process {total} relation(s) !")
        pb.begin()

        # 最大误差
        max_delta = 0.0
        # 循环处理
        for t1 in self.values() :
            # 检查标志位
            if self.break_loop : break
            # 循环处理
            for t2 in self.values() :
                # 检查标志位
                if self.break_loop : break

                # 相关系数
                gamma = gammas[t1.index][t2.index]
                # 增加计数
                pb.increase()

                # 获得相关系数误差（快捷处置）
                if not self._use_cupy :
                    # 拷贝原始矩阵
                    matrix1 = t1.matrix
                    # 拷贝原始矩阵
                    matrix2 = t2.matrix

                    delta = gamma - \
                            numpy.dot(matrix1[0], matrix2[1])  # Ai.Bj

                    abs_delta = numpy.abs(delta)
                    # 检查结果
                    if abs_delta > max_delta:
                        # 设置误差记录
                        max_delta = abs_delta

                    # 计算模长
                    _bj = numpy.dot(matrix2[1], matrix2[1])
                    _ai = numpy.dot(matrix1[0], matrix1[0])
                    # 计算数据
                    value = delta / (_bj + _ai)
                    # 计算分量（快捷处置）加和误差分量
                    t1.delta[0] += numpy.dot(value, matrix2[1])
                    # 计算分量（快捷处置）加和误差分量
                    t2.delta[1] += numpy.dot(value, matrix1[0])
                else :
                    # 拷贝原始矩阵
                    matrix1 = cupy.asarray(t1.matrix)
                    # 拷贝原始矩阵
                    matrix2 = cupy.asarray(t2.matrix)

                    delta = gamma - \
                            cupy.dot(matrix1[0], matrix2[1])  # Ai.Bj

                    abs_delta = cupy.abs(delta)
                    # 检查结果
                    if abs_delta > max_delta:
                        # 设置误差记录
                        max_delta = abs_delta

                    # 计算模长
                    _bj = cupy.dot(matrix2[1], matrix2[1])
                    _ai = cupy.dot(matrix1[0], matrix1[0])
                    # 计算数据
                    value = delta / (_bj + _ai)
                    # 计算分量（快捷处置）加和误差分量
                    t1.delta[0] += cupy.asnumpy(cupy.dot(value, matrix2[1]))
                    # 计算分量（快捷处置）加和误差分量
                    t2.delta[1] += cupy.asnumpy(cupy.dot(value, matrix1[0]))

        # 打印信息
        pb.end()
        #pb.end(f"VectorContent.__classic_solving : {total} relations(s) processed !")
        # 返回结果
        return max_delta

    # 初始化ais和bjs
    def __init_matrices(self, n) :
        # 生成ais
        ais = cupy_random_matrix(n, self._dimension) \
            if self._use_cupy else get_random_matrix(n, self._dimension)
        # 生成bjs
        bjs = cupy_random_matrix(n, self._dimension) \
            if self._use_cupy else get_random_matrix(n, self._dimension)
        # 归一化
        ais = cupy_normalized(ais) \
            if self._use_cupy else get_normalized(ais)
        bjs = cupy_normalized(bjs) \
            if self._use_cupy else get_normalized(bjs)
        # 返回结果
        return ais, bjs

    # 从ais和bjs矩阵拷贝至Vector
    def __copy_from(self, n, ais, bjs) :
        # 进度条
        pb = ProgressBar(n)
        # 开始
        pb.begin(f"VectorContent.__copy_from : copy matrix[{n}] !")
        # 循环处理
        for item in self.values() :
            # 进度条
            pb.increase()
            # 获得索引值
            index = item.index
            # 检查参数
            if not self._use_cupy :
                item.matrix[0] = ais[index] # Ai
                item.matrix[1] = bjs[index] # Bj
            else :
                item.matrix[0] = cupy.asnumpy(ais[index]) # Ai
                item.matrix[1] = cupy.asnumpy(bjs[index]) # Bj
        # 结束
        pb.end()

    # 从Vector拷贝至ais和bjs矩阵
    def __copy_to(self, n, ais, bjs) :
        # 进度条
        pb = ProgressBar(n)
        # 开始
        pb.begin(f"VectorContent.__copy_to : copy matrix[{n}] !")
        # 循环处理
        for item in self.values() :
            # 进度条
            pb.increase()
            # 获得索引值
            index = item.index
            # 检查参数
            if not self._use_cupy :
                ais[index] = item.matrix[0]  # Ai
                bjs[index] = item.matrix[1]  # Bj
            else :
                ais[index] = cupy.asarray(item.matrix[0])  # Ai
                bjs[index] = cupy.asarray(item.matrix[1])  # Bj
        # 结束
        pb.end()

    # 完成一次全量计算
    def _linf_solving(self) :
        # 检查参数
        assert 0 < self._error < 1.0
        # 总数
        # 也是维度之一
        n = len(self)
        # 检查内容
        if n < 2:
            print("VectorContent._linf_solving : insufficient vectors !")
            return numpy.inf

        # 初始化相关系数
        # 有删除无效数据的行为
        n = self._init_gammas()
        # 相关系数矩阵
        gammas = self.__get_gammas(n)
        # 初始化矢量矩阵
        ais, bjs = self.__init_matrices(n)
        # 检查标记位
        if self.init_matrix :
            # 清理标志位
            self.init_matrix = False
        else :
            # 拷贝数据
            self.__copy_to(n, ais, bjs)
        # 打印信息
        print(f"VectorContent._linf_solving : matrix[{n}] initialized !")

        # 搜索长度
        length = 0
        # 循环计数
        i = 0; j = 0
        # 最大行和范数
        last_delta = numpy.inf
        # 循环直至误差符合要求，或者收敛至最小误差
        while i < self._max_loop :
            # 检查标志位
            if self.break_loop : break

            # 计数器加一
            i += 1; j += 1
            # 开始计时
            start = time.perf_counter()

            # 获得计算值
            delta = cupy_delta_matrix(gammas, ais, bjs) \
                if self._use_cupy else get_delta_matrix(gammas, ais, bjs)
            # 获得一系列误差最大值位置记录
            positions = cupy_max_positions(n, delta, length) \
                if self._use_cupy else get_max_positions(n, delta, length)
            # 检查参数
            assert len(positions) >= 1
            # 先获得最大误差值
            max_delta = positions[0][2]
            # 检查参数
            # numba会强制类型，数组均为浮点型，因此需要强制转换为整数类型
            positions = cupy.array(positions).astype(cupy.int32) \
                if self._use_cupy else numpy.array(positions).astype(numpy.int32)
            # 转换后再取值
            row = int(positions[0][0])
            col = int(positions[0][1])
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
                if length > n // 4 : length = n // 4
            # 通过误差计算步长，并移至下一个步骤
            _dai, _dbj = cupy_next_step(n, ais, bjs, delta, positions) \
                if self._use_cupy else get_next_step(n, ais, bjs, delta, positions)
            # 注意：分成两个步骤计算
            ais += _dai; bjs += _dbj

            # 计时结束
            end = time.perf_counter()
            # 间隔打印
            if numpy.remainder(j, self._max_loop) == 0 :
                # 获得最大值
                sigma = cupy.sum(cupy.square(delta)) \
                    if self._use_cupy else numpy.sum(numpy.square(delta))
                # 打印信息
                print(f"VectorContent._linf_solving : show result !")
                print(f"\tloop[{j},{i},{length}] = {int((end - start) * 1000)} ms")
                print(f"\tMax(|Δγᵢⱼ|) = ({row},{col},{positions[0][2]})")
                if j > 1 : print(f"\tΔMax(|Δγᵢⱼ|) = {_last_delta - max_delta}")
                print(f"\t\tΣ(|Δγᵢⱼ|²) = {sigma}")
        # 清除标记
        self.break_loop = False
        # 设置数据矩阵
        self.__copy_from(n, ais, bjs)
        # 打印信息
        print(f"VectorContent._linf_solving : final matrix[{n}] copied !")
        # 返回结果
        return last_delta

    # 完成一次全量计算
    def _l2_solving(self) :
        # 检查参数
        assert 0 < self._error < 1.0
        # 总数
        # 也是维度之一
        n = len(self)
        # 检查内容
        if n < 2:
            print("VectorContent._l2_solving : insufficient vectors !")
            return numpy.inf

        # 初始化相关系数
        # 有删除无效数据的行为
        n = self._init_gammas()
        # 相关系数矩阵
        gammas = self.__get_gammas(n)
        # 初始化矢量矩阵
        ais, bjs = self.__init_matrices(n)
        # 检查标记位
        if self.init_matrix :
            # 清理标志位
            self.init_matrix = False
        else :
            # 拷贝数据
            self.__copy_to(n, ais, bjs)
        # 打印信息
        print(f"VectorContent._l2_solving : matrix[{n}] initialized !")

        # 循环计数
        i = 0; j = 0
        # 步长倍数
        multiple = 1
        # 步长
        step = self._error
        # 最大行和范数
        last_delta = numpy.inf
        # 循环直至误差符合要求，或者收敛至最小误差
        while i < self._max_loop :
            # 检查标志位
            if self.break_loop : break

            # 计数器加一
            i += 1; j += 1
            # 开始计时
            start = time.perf_counter()

            # 获得计算值
            delta = cupy_delta_matrix(gammas, ais, bjs) \
                if self._use_cupy else get_delta_matrix(gammas, ais, bjs)
            # 获得最大值
            max_delta = cupy.sum(cupy.square(delta)) \
                if self._use_cupy else numpy.sum(numpy.square(delta))
            # 检查结果
            if max_delta <= self._error :
                # 设置数值，并中断循环
                last_delta = max_delta; break
            # 临时记录
            _last_delta = last_delta
            # 检查结果
            if last_delta < max_delta :
                # 呈上升趋势
                multiple = 1
            else :
                # 呈下降趋势
                i = 0
                # 乘数加一
                multiple += 1
                # 保存上次误差
                last_delta = max_delta
                # 检查结果
                if multiple > n : multiple = n
            # 通过误差计算步长，并移至下一个步骤
            _dai, _dbj = cupy_gradient_step(multiple, step, delta, ais, bjs) \
                if self._use_cupy else get_gradient_step(multiple, step, delta, ais, bjs)
            # 注意：分成两个步骤计算
            ais += _dai; bjs += _dbj

            # 计时结束
            end = time.perf_counter()
            # 间隔打印
            if numpy.remainder(j, self._max_loop) == 0 :
                # 获得最大值
                sigma = cupy.sum(cupy.abs(delta)) \
                    if self._use_cupy else numpy.sum(numpy.abs(delta))
                # 获得一系列误差最大值位置记录
                positions = cupy_max_positions(n, delta, 0) \
                    if self._use_cupy else get_max_positions(n, delta, 0)
                # 检查参数
                assert len(positions) >= 1
                # 打印信息
                print(f"VectorContent._l2_solving : show result !")
                print(f"\tloop[{j},{i},{multiple}] = {int((end - start) * 1000)} ms")
                print(f"\tΣ(|Δγᵢⱼ|²)  = {max_delta}")
                if j > 1 : print(f"\t∇Σ(|Δγᵢⱼ|²) = {_last_delta - max_delta}")
                row = int(positions[0][0])
                col = int(positions[0][1])
                print(f"\t\tΣ|Δγᵢⱼ| = {sigma}")
                print(f"\t\tMax(|Δγᵢⱼ|) = ({row},{col},{positions[0][2]})")
        # 清除标记
        self.break_loop = False
        # 设置数据矩阵
        self.__copy_from(n, ais, bjs)
        # 打印信息
        print(f"VectorContent._l2_solving : final matrix[{n}] copied !")
        # 返回结果
        return last_delta

    # 完成一次全量计算
    def _l1_solving(self) :
        # 检查参数
        assert 0 < self._error < 1.0
        # 总数
        # 也是维度之一
        n = len(self)
        # 检查内容
        if n < 2:
            print("VectorContent._l1_solving : insufficient vectors !")
            return numpy.inf

        # 初始化相关系数
        # 有删除无效数据的行为
        n = self._init_gammas()
        # 相关系数矩阵
        gammas = self.__get_gammas(n)
        # 初始化矢量矩阵
        ais, bjs = self.__init_matrices(n)
        # 检查标记位
        if self.init_matrix :
            # 清理标志位
            self.init_matrix = False
        else :
            # 拷贝数据
            self.__copy_to(n, ais, bjs)
        # 打印信息
        print(f"VectorContent._l1_solving : matrix[{n}] initialized !")

        # 乘数
        multiple = 1
        # 循环计数
        i = 0; j = 0
        # 最大行和范数
        last_delta = numpy.inf
        # 循环直至误差符合要求，或者收敛至最小误差
        while i < self._max_loop :
            # 检查标志位
            if self.break_loop : break

            # 计数器加一
            i += 1; j += 1
            # 开始计时
            start = time.perf_counter()

            # 获得计算值
            delta = cupy_delta_matrix(gammas, ais, bjs) \
                if self._use_cupy else get_delta_matrix(gammas, ais, bjs)
            # 获得误差值
            max_delta = cupy.sum(cupy.abs(delta)) \
                if self._use_cupy else numpy.sum(numpy.abs(delta))
            # 检查结果
            if max_delta <= self._error :
                # 设置数值，并中断循环
                last_delta = max_delta; break
            # 临时记录
            _last_delta = last_delta
            # 检查结果
            if last_delta < max_delta :
                # 呈上升趋势
                multiple = 1
            else :
                # 呈下降趋势
                i = 0; multiple += 1
                # 保存上次误差
                last_delta = max_delta
                # 检查结果
                if multiple > n : multiple = n
            # 通过误差计算步长，并移至下一个步骤
            _dai, _dbj = cupy_next_steps(multiple, n, ais, bjs, delta) \
                if self._use_cupy else get_next_step(multiple, n, ais, bjs, delta)
            # 注意：分成两个步骤计算
            ais += _dai; bjs += _dbj

            # 计时结束
            end = time.perf_counter()
            # 间隔打印
            if numpy.remainder(j, self._max_loop) == 0 :
                # 获得最大值
                sigma = cupy.sum(cupy.square(delta)) \
                    if self._use_cupy else numpy.sum(numpy.square(delta))
                # 获得一系列误差最大值位置记录
                positions = cupy_max_positions(n, delta, 0) \
                    if self._use_cupy else get_max_positions(n, delta, 0)
                # 检查参数
                assert len(positions) >= 1
                # 打印信息
                print(f"VectorContent._l1_solving : show result !")
                print(f"\tloop[{j},{i},{multiple}] = {int((end - start) * 1000)} ms")
                print(f"\tΣ|Δγᵢⱼ| = {max_delta}")
                if j > 1 : print(f"\tΔΣ|Δγᵢⱼ| = {_last_delta - max_delta}")
                print(f"\t\tΣ(|Δγᵢⱼ|²) = {sigma}")
                row = int(positions[0][0])
                col = int(positions[0][1])
                print(f"\t\tMax(|Δγᵢⱼ|) = ({row},{col},{positions[0][2]})")
        # 清除标记
        self.break_loop = False
        # 设置数据矩阵
        self.__copy_from(n, ais, bjs)
        # 打印信息
        print(f"VectorContent._l1_solving : final matrix[{n}] copied !")
        # 返回结果
        return last_delta
