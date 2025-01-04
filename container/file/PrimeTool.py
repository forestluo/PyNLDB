# -*- coding: utf-8 -*-

from ValueEnum import *

class PrimeTool :
    # 1000以内的质数
    _primes = \
    [
        2, 3, 5, 7, 11, 13, 17, 19, 23,
        29, 31, 37, 41, 43, 47, 53, 59, 61,
        67, 71, 73, 79, 83, 89, 97, 101, 103,
        107, 109, 113, 127, 131, 137, 139, 149, 151,
        157, 163, 167, 173, 179, 181, 191, 193, 197,
        199, 211, 223, 227, 229, 233, 239, 241, 251,
        257, 263, 269, 271, 277, 281, 283, 293, 307,
        311, 313, 317, 331, 337, 347, 349, 353, 359,
        367, 373, 379, 383, 389, 397, 401, 409, 419,
        421, 431, 433, 439, 443, 449, 457, 461, 463,
        467, 479, 487, 491, 499, 503, 509, 521, 523,
        541, 547, 557, 563, 569, 571, 577, 587, 593,
        599, 601, 607, 613, 617, 619, 631, 641, 643,
        647, 653, 659, 661, 673, 677, 683, 691, 701,
        709, 719, 727, 733, 739, 743, 751, 757, 761,
        769, 773, 787, 797, 809, 811, 821, 823, 827,
        829, 839, 853, 857, 859, 863, 877, 881, 883,
        887, 907, 911, 919, 929, 937, 941, 947, 953,
        967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021,
    ]

    @staticmethod
    def is_prime(value) :
        # 设置初始值
        i = 1
        # 循环处理
        while i * i <= value :
            # 计器加一
            i += 1
            # 检查
            if value % i == 0 : return False
        # 返回结果
        return True

    @staticmethod
    def get_max_prime(value) :
        # 循环处理
        for k in range(value, 1, -1) :
            # 检查
            if PrimeTool.is_prime(k) : return k
        # 返回结果
        return -1

    @staticmethod
    def calc_index_page() :
        # 循环处理
        for i in range(7) :
            # 尺寸类型
            size_type = SizeType.mb1 + i
            # 子节点数据尺寸
            size = SizeType.get_size(size_type) - 4 * SizeOf.integer.value - 10
            # 整除
            N = size // IndexData.size
            # 打印
            print(f"size_type({size_type}) = {N} * {IndexData.size} + 10 + {size - N * IndexData.size}")
            N = PrimeTool.get_max_prime(N)
            print(f"prime = {PrimeTool.get_max_prime(N)}")
            # print(f"size_type({size_type}) = {N} * {IndexData.size} + 10 + {size - N * IndexData.size}")
            # print("")

    @staticmethod
    def calc_index_element() :
        # 循环处理
        for i in range(10) :
            # 尺寸类型
            size_type = SizeType.kb1.value + i
            # 子节点数据尺寸
            size = SizeType.get_size(size_type) - 10
            # 整除
            N = size // IndexData.size
            # 打印
            print(f"size_type({size_type}) = {N} * {IndexData.size} + 10 + {size - N * IndexData.size}")
            N = PrimeTool.get_max_prime(N)
            print(f"prime = {PrimeTool.get_max_prime(N)}")
            print(f"size_type({size_type}) = {N} * {IndexData.size} + 10 + {size - N * IndexData.size}")
            print("")

def main() :

    for i in range(5, 1000) :
        print(f"{i} : {PrimeTool.is_prime(i)} {PrimeTool.get_max_prime(i)} ")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("PrimeTool.main :__main__ : ", str(e))
        print("PrimeTool.main :__main__ : unexpected exit !")
