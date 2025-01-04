# -*- coding: utf-8 -*-

from container.file.IndexData import *
from container.file.PageBuffer import *

class IndexPageBuffer(PageBuffer) :
    ##################################################
    #
    # Offsets.
    #
    # Identity        [int]
    # Capacity        [int]
    # Size            [int]
    # Count           [int]
    # Hash Datas      [N * IndexData]
    #
    ##################################################

    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__(PageType.index_page, SizeType.mb1)

        # 设置参数
        self.identity = 0
        self.size = self.__get_subnode_count()
        self.count = 0
        self.capacity = -1
        # 循环处理
        self.datas = [IndexData() for _ in range(self.size)]
        # 循环处理
        for index, data in enumerate(self.datas) :
            data.offset = PageBuffer.description_size \
                + 4 * SizeOf.integer + index * IndexData.size

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
        buffer.put_int(SizeOf.integer, self.identity)
        buffer.put_int(SizeOf.integer, self.capacity, True)
        buffer.put_int(SizeOf.integer, self.size, True)
        buffer.put_int(SizeOf.integer, self.count, True)
        # 循环处理
        for data in self.datas : data.wrap(buffer)

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        self.identity = buffer.get_int(SizeOf.integer)
        self.capacity = buffer.get_int(SizeOf.integer, True)
        self.size = buffer.get_int(SizeOf.integer, True)
        self.count = buffer.get_int(SizeOf.integer, True)
        # 循环处理
        for data in self.datas : data.unwrap(buffer)

    def check_valid(self, data_size) :
        super().check_valid(data_size)
        if self.page_type != PageType.index_page :
            raise Exception(f"invalid page type({self.page_type})")
        if not (15 <= self.size_type <= 21) :
            raise Exception(f"invalid size type({self.size_type})")
        # 检查
        if self.count > self.size :
            raise Exception(f"invalid count({self.count}) or size({self.size})")
        # 循环处理
        for data in self.datas : data.check_valid(data_size)

    def dump(self) :
        super().dump()
        print(f"IndexPageBuffer.dump : show properties !")
        print(f"\tidentity = {self.identity}")
        print(f"\tcapacity = {self.capacity}")
        print(f"\tsize = {self.size}")
        print(f"\tcount = {self.count}")
        """
        # 循环处理
        for index, data in enumerate(self.datas) :
            # 获得数值
            if not data.valid : continue
            # 打印数据
            print(f"\tdata[{index}] = [0x{data.key.hex()}, "
                  f"{data.subnode_offset}, {data.data_value}]")
        """