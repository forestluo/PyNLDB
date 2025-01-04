# -*- coding: utf-8 -*-

from container.file.IndexData import *
from container.file.PageBuffer import *

class IndexElementBuffer(PageBuffer) :
    ##################################################
    #
    # Offsets.
    #
    # Identity      [int]
    # Hash Datas    [N * IndexData]
    #
    ##################################################

    # 初始化
    def __init__(self, size_type = SizeType.kb1) :
        # 调用父类初始化函数
        super().__init__(PageType.index_element, size_type)
        # 设置参数
        self.occupied_size = -1
        # 设置参数
        self.identity = -1
        # 循环处理
        self.datas = [IndexData()
            for _ in range(self.__get_subnode_count())]
        # 循环处理
        for index, data in enumerate(self.datas) :
            data.offset = PageBuffer.description_size \
                + SizeOf.integer + index * IndexData.size

    def valid(self) :
        # 循环处理
        for data in self.datas :
            # 返回结果
            if data.valid : return True
            if data.subnode_offset != -1 : return True
        # 返回结果
        return False

    # 获得数据
    def __getitem__(self, key) :
        # 返回结果
        return self.datas[self.__get_index_by_key(key)]

    def __get_index_by_key(self, key) :
        # 返回结果
        return IndexTool.get_index(key, self.size_type)

    def __get_subnode_count(self) :
        # 返回结果
        return IndexTool.get_subnode_count(self.size_type)

    def wrap(self, buffer) :
        super().wrap(buffer)
        # 其他数据
        buffer.put_int(SizeOf.integer, self.identity)
        # 循环处理
        for data in self.datas : data.wrap(buffer)

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        # 其他数据
        self.identity = buffer.get_int(SizeOf.integer)
        # 循环处理
        for data in self.datas : data.unwrap(buffer)

    def check_valid(self, data_size) :
        super().check_valid(data_size)
        if self.page_type != PageType.index_element :
            raise Exception(f"invalid page type({self.page_type})")
        if not (2 <= self.size_type <= 11) :
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
            print(f"\tdata[{index}] = [0x{data.key :016x}, "
                  f"0x{data.data_offset :016x}, 0x{data.subnode_offset :016x}]")
