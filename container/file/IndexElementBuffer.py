# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.IndexData import *
from container.file.PageBuffer import *

class IndexElementBuffer(PageBuffer) :
    ##################################################
    #
    # Offsets.
    #
    # Hash Datas    [N * IndexData]
    #
    ##################################################
    # Default Size Type
    default_size_type = SizeType.hqkb
    # Default Size
    default_size = SizeType.get_size(default_size_type)

    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__(PageType.index_element,
            IndexElementBuffer.default_size_type)
        # 设置临时变量
        self.flag = 0
        self.level = -1
        self.index = -1
        # 设置参数
        self.occupied_size = \
            SizeOf.integer.value + \
            self.get_subnode_count() * IndexData.size
        # 设置参数
        self.identity = -1
        # 循环处理
        self.datas = [IndexData() for _ in range(self.get_subnode_count())]

    def get_data_by_key(self, index) :
        # 返回结果
        return self.datas[self.get_index_by_key(key)]

    def get_subnode_count(self) :
        # 返回结果
        return IndexElementBuffer.__get_subnode_count(self.size_type)

    def get_index_by_key(self, key) :
        # 返回结果
        return IndexElementBuffer.__get_subnode_index(self.size_type, key)

    def get_offset_by_index(self, index) :
        # 检查
        assert self.offset >= 0
        # 返回结果
        return self.offset + PageBuffer.default_size \
            + SizeOf.integer.value + index * IndexData.size

    def get_offset_by_key(self, key) :
        # 检查
        assert self.offset >= 0
        # 返回结果
        return self.offset + PageBuffer.default_size \
            + SizeOf.integer.value + self.get_index_by_key(key) * IndexData.size

    @staticmethod
    def __get_subnode_count(size_type) :
        # 检查
        if size_type == SizeType.qqkb :
            pass
        elif size_type == SizeType.hqkb :
            return 7
        elif size_type == SizeType.qkb :
            return 15 # 3 * 5
        elif size_type == SizeType.hkb :
            return 31
        elif size_type == SizeType.kb1 :
            return 61
        elif size_type == SizeType.kb2 :
            return 127
        elif size_type == SizeType.kb4 :
            return 251
        elif size_type == SizeType.kb8 :
            return 509
        elif size_type == SizeType.kb16 :
            return 1021
        elif size_type == SizeType.kb32 :
            return 2039
        elif size_type == SizeType.kb64 :
            return 4093
        raise Exception(f"unsupported size type({size_type})")

    @staticmethod
    def __get_subnode_index(size_type, key) :
        # 返回结果
        return key % IndexElementBuffer.__get_subnode_count(size_type)

    def wrap(self, buffer) :
        super().wrap(buffer)
        buffer.put_int(SizeOf.integer, self.identity)
        # 循环处理
        for data in self.datas : data.wrap(buffer)

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        self.identity = buffer.get_int(SizeOf.integer)
        # 循环处理
        for data in self.datas : data.unwrap(buffer)

    def check_valid(self, data_size) :
        super().check_valid(data_size)
        if self.page_type != PageType.index_element :
            raise Exception(f"invalid page type({self.page_type})")
        if not (2 <= self.size_type.value <= 11) :
            raise Exception(f"invalid size type({self.size_type})")
        # 循环处理
        for data in self.datas : data.check_valid(data_size)

    def dump(self) :
        super().dump()
        print(f"IndexElementBuffer.dump : show properties !")
        print(f"\tidentity = {self.identity}")
        # 循环处理
        for index, data in enumerate(self.datas) :
            # 获得数值
            if data.key == 0 : continue
            # 打印数据
            print(f"\tdata[{index}] = "
                  f"[0x{data.key :016x},"
                  f"0x{data.data_offset :016x},"
                  f"0x{data.subnode_offset :016x}]")
