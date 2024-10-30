# -*- coding: utf-8 -*-

import heapq

from WordContent import *

class HashTool :
    # 字符串哈希（FNV-1）
    @staticmethod
    def hash(content) :
        # 检查参数
        assert isinstance(content, str)
        # 初始值
        value = 0x811c9dc5
        # 循环处理
        for char in content :
            value = (value * 16777619) ^ ord(char)
        # 返回结果
        return value


class HuffmanNode :
    # 初始化
    def __init__(self, symbol = None, frequency = None) :
        # 设置参数
        self.symbol = symbol
        self.frequency = frequency
        # 子节点
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

class HuffmanTree :
    # 初始化
    def __init__(self) :
        # 设置初始值
        self.__heap = []
        self.__codes = {}

    def __len__(self) :
        # 返回结果
        return len(self.__codes)

    def __contains__(self, word) :
        # 检查参数
        assert isinstance(word, str)
        # 返回结果
        return word in self.__codes.keys()

    def __getitem__(self, word):
        # 检查参数
        assert isinstance(word, str)
        # 返回结果
        return self.__codes[word]

    # 压栈
    def push(self, symbol, frequency) :
        # 检查参数
        assert isinstance(symbol, str)
        assert isinstance(frequency, int)
        # 生成项目并压入
        self.push_item(WordItem(symbol, frequency))

    # 压栈
    def push_item(self, item) :
        # 检查参数
        assert isinstance(item, WordItem)
        # 压栈
        heapq.heappush(self.__heap, HuffmanNode(item.word, item.count))

    # 创建
    def build(self) :
        # 循环处理
        while len(self.__heap) > 1 :
            left = heapq.heappop(self.__heap)
            right = heapq.heappop(self.__heap)
            top = HuffmanNode(frequency = left.frequency + right.frequency)
            top.left = left
            top.right = right
            heapq.heappush(self.__heap, top)
        # 清理编码树
        self.__codes.clear()
        # 生成编码树
        self.__generate_codes__(self.__heap[0])
        # 返回结果
        return self.__heap[0]

    # 生成编码
    def __generate_codes__(self, node, code = '') :
        if node is not None :
            if node.symbol is not None :
                self.__codes[node.symbol] = code
            self.__generate_codes__(node.left, code + '0')
            self.__generate_codes__(node.right, code + '1')

    def dump(self) :
        # 打印信息
        print("CodingTool.HuffmanTree : show codes !")
        print("\ttotal = %d" % len(self.__codes))
        # 循环处理
        for (symbol, code) in self.__codes.items() :
            print(f"\tcharacter(code) = \'{symbol}\'({code})")