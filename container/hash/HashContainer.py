# -*- coding: utf-8 -*-
import time
import random
import traceback

from container.Container import *
from container.hash.HashElement import *

class HashContainer(Container) :
    # 质数表
    _primes = \
        [
            107, 109, 113, 127, 131, 137, 139, 149, 151, 157,
            163, 167, 173, 179, 181, 191, 193, 197, 199, 211,
            217, 223, 227, 229, 233, 239, 241, 247, 251, 253,
            255, 256
        ]

    # 初始化
    def __init__(self, capacity = -1) :
        # 调用父类初始化函数
        super().__init__(capacity)
        # 设置参数
        # 增加空间
        self._inc_size()
        # 最大层数
        self.__max_level = 0
        # 根节点
        self.__root = HashElement(HashContainer._primes[0])

    @property
    def max_level(self) :
        # 返回结果
        return self.__max_level

    # 返回结果
    def __getitem__(self, key) :
        # 返回结果
        return self.get(key)

    def __setitem__(self, key, value) :
        # 返回结果
        return self.set(key, value)

    def __contains__(self, key) :
        # 获得节点
        return True \
            if self.get(key) is not None else False

    # 获得余数
    @staticmethod
    def __get_remainder(key, level) :
        # 返回结果
        return hash(key) % HashContainer._primes[level]

    def get(self, key) :
        # 检查参数
        assert key is not None
        # 搜索层次
        level = 0
        # 当前节点
        node = self.__root
        # 循环处理
        while node is not None :
            # 检查节点数据
            if not node.is_none \
                and node.key == key : return node.value
            # 获得余数
            index = HashContainer.\
                __get_remainder(key, level)
            # 检查结果
            if 0 <= index \
                < HashContainer._primes[level] :
                # 获得子节点
                node = node[index]; level += 1
            else :
                raise Exception(f"incorrect index({index})")
        # 返回结果
        return None

    def set(self, key, value) :
        # 检查参数
        assert key is not None
        # 搜索层次
        level = 0
        # 当前节点
        node = self.__root
        # 记录节点
        _node = None
        # 循环处理
        while node is not None :
            # 检查节点
            if node.is_none : _node = node
            # 检查关键字
            elif node.key == key :
                # 保留原始值
                _value = node.value
                # 检查记录
                if _node is None :
                    # 设置数值
                    node.value = value
                else :
                    # 清理节点
                    node.clear()
                    # 设置数值
                    _node.set(key, value)
                # 返回结果
                return _value
            # 获得余数
            index = HashContainer. \
                __get_remainder(key, level)
            # 检查结果
            if 0 <= index \
                < HashContainer._primes[level] :
                # 层数加一
                level += 1
                # 检查子节点
                if node[index] is not None :
                    # 向下搜索
                    node = node[index]
                else :
                    # 检查层数
                    if level > self.__max_level :
                        # 设置最大层数
                        self.__max_level = level
                    # 增加计数
                    self._inc_size_and_count()
                    # 设置节点
                    node[index] = HashElement(
                        HashContainer._primes[level], key, value)
                    break
            else :
                raise Exception(f"incorrect index({index})")
        # 返回结果
        return None

    def remove(self, key) :
        # 检查参数
        assert key is not None
        # 搜索层次
        level = 0
        # 记录节点
        ups = []
        # 当前节点
        node = self.__root
        # 循环处理
        while node is not None :
            # 记录匹配节点
            if node.key == key :
                # 记录数值
                value = node.value
                # 设置标记
                node.clear()
                # 计数器减一
                self._dec_count()
                # 计数器
                i = len(ups)
                # 检查标记
                while node.is_none \
                    and not node.has_child :
                    # 计数器减一
                    i -= 1
                    # 检查数据
                    if i < 0 : break
                    # 计数器减一
                    self._dec_size()
                    # 节点
                    node = ups[i][0]
                    # 删除引用
                    node[ups[i][1]] = None
                # 返回结果
                return value
            # 获得余数
            index = HashContainer. \
                __get_remainder(key, level)
            # 检查结果
            if 0 <= index \
                < HashContainer._primes[level] :
                # 检查子节点
                if node[index] is None : break
                # 记录数据
                ups.append([node, index])
                # 向下搜索
                node = node[index]; level += 1
            else :
                raise Exception(f"incorrect index({index})")
        # 返回结果
        return None

    def dump(self) :
        print(f"HashContainer.dump : show properties !")
        print(f"\tcapacity = {self.capacity}")
        print(f"\tsize = {self.size}")
        print(f"\tcount = {self.count}")
        print(f"\tis_full = {self.is_full}")
        print(f"\tis_empty = {self.is_empty}")
        print(f"\tmax_level = {self.max_level}")

def main() :
    # 计数
    count = 2000000
    # 容量
    capacity = 100000

    # 标准方法
    data = {}
    # 新建
    container = HashContainer()
    # 循环处理
    for i in range(count) :
        # 获得随机值
        key = random.randint(1, capacity)
        # 设置数值
        value = random.randint(1, count)
        # 打印信息
        #print(f"HashContainer.main : set({key}) = {value} !")
        # 设置数值
        data[key] = value
        # 设置数值
        container[key] = value
    # 打印信息
    container.dump()
    """
    # 打印信息
    print(f"HashContainer.main : compare two containers !")
    # 比较两个对象
    for key, value in data.items() :
        print(f"\tcontainer({key}) = {container[key]} ({value})")
    """
    # 开始计时
    start = time.perf_counter()
    # 循环处理
    for i in range(count) :
        # 获得操作数
        value = random.randint(0, 100)
        # 增加操作
        if value == 0 :
            # 仅作增加
            key = random.randint(1, capacity)
            # 设置数值
            value = random.randint(1, count)
            # 打印信息
            #print(f"HashContainer.main : set({key}) = {value} !")
            # 设置数值
            data[key] = value
            # 设置数值
            container[key] = value
        # 查询操作
        elif value == 1 :
            # 仅作查询
            key = random.randint(1, capacity)
            # 打印信息
            #print(f"HashContainer.main : get({key}) !")
            # 查询内容
            value = container[key]
            # 检查内容
            if key in data :
                # 获得数值
                data_value = data[key]
                # 检查结果
                if data_value != value :
                    # 打印信息
                    print(f"HashContainer.main : get incorrect result !")
                    print(f"\tkey = {key}")
                    print(f"\tvalue = {value}")
                    print(f"\tdata_value = {data_value}")
            else :
                # 检查数值
                if value is not None :
                    # 打印信息
                    print(f"HashContainer.main : get incorrect result !")
                    print(f"\tkey = {key}")
                    print(f"\tvalue = {value}")
                    print(f"\tdata_value = None")
        else :
            # 仅作删除
            key = random.randint(1, capacity)
            # 打印信息
            #print(f"HashContainer.main : remove({key}) !")
            # 删除内容
            value = container.remove(key)
            # 删除内容
            if key in data :
                # 获得数值
                data_value = data[key]
                # 删除内容
                data.pop(key)
                # 检查结果
                if data_value != value :
                    # 打印信息
                    print(f"HashContainer.main : incorrect removed result !")
                    print(f"\tkey = {key}")
                    print(f"\tvalue = {value}")
                    print(f"\tdata_value = {data_value}")
            else :
                # 检查数值
                if value is not None :
                    # 打印信息
                    print(f"HashContainer.main : incorrect removed result !")
                    print(f"\tkey = {key}")
                    print(f"\tvalue = {value}")
                    print(f"\tdata_value = None")
    # 打印信息
    container.dump()
    # 计时结束
    end = time.perf_counter()
    print(f"HashContainer.main : show efficiency !")
    print(f"\ttimespan = {end - start} ms")
    print(f"\tspeed = {count / float(end - start)} op/sec")
    """
    # 打印信息
    print(f"HashContainer.main : compare two containers !")
    # 比较两个对象
    for key, value in data.items() :
        print(f"\tcontainer({key}) = {container[key]} ({value})")
    """

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("HashContainer.main :__main__ : ", str(e))
        print("HashContainer.main :__main__ : unexpected exit !")