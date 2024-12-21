# -*- coding: utf-8 -*-

class Container :
    # 初始化
    def __init__(self, capacity = -1) :
        # 设置参数
        self.__size = 0
        self.__count = 0
        self.__capacity = capacity

    @property
    def size(self) :
        return self.__size

    @property
    def count(self) :
        return self.__count

    @property
    def capacity(self) :
        return self.__capacity

    def _set_size(self, size) :
        # 检查参数
        assert size >= 0
        # 设置参数
        self.__size = size

    def _set_count(self, count) :
        # 检查参数
        assert count >= 0
        # 设置参数
        self.__count = count

    def _set_capacity(self, capacity) :
        # 检查参数
        assert capacity != 0
        # 设置参数
        self.__capacity = capacity \
            if capacity > 0 else -1

    def _inc_size(self, size = 1) :
        # 设置参数
        self.__size += size

    def _dec_size(self, size = 1) :
        # 设置参数
        self.__size -= size

    def _inc_count(self, count = 1) :
        # 设置参数
        self.__count += count

    def _dec_count(self, count = 1) :
        # 设置参数
        self.__count -= count

    def _inc_size_and_count(self) :
        # 设置参数
        self.__size += 1
        self.__count += 1

    def _dec_size_and_count(self) :
        # 设置参数
        self.__size -= 1
        self.__count -= 1

    def clear(self) :
        # 设置参数
        self.__size = 0
        self.__count = 0

    @property
    def is_empty(self) :
        # 返回结果
        return self.__count <= 0

    @property
    def is_full(self) :
        # 返回结果
        return 0 < self.__capacity <= self.__count

    def dump(self) :
        print(f"Container.dump : show properties !")
        print(f"\tcapacity = {self.capacity}")
        print(f"\tsize = {self.size}")
        print(f"\tcount = {self.count}")
        print(f"\tis_full = {self.is_full}")
        print(f"\tis_empty = {self.is_empty}")
