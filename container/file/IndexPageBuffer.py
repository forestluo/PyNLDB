# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
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
    # Default Size Type
    default_size_type = SizeType.mb64
    # Default Size
    default_size = SizeType.get_size(default_size_type)

    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__(PageType.index_page,
            IndexPageBuffer.default_size_type)
        # 设置参数
        self.identity = 0
        self.size = 0
        self.count = 0
        self.capacity = Capacity.without_limit
        # 循环处理
        self.datas = [IndexData() for _ in range(self.get_subnode_count())]

    def get_data_by_key(self, key) :
        # 返回结果
        return self.datas[self.get_index_by_key(key)]

    def get_subnode_count(self) :
        # 返回结果
        return IndexPageBuffer.__get_subnode_count(self.size_type)

    def get_index_by_key(self, key) :
        # 返回结果
        return IndexPageBuffer.__get_subnode_index(self.size_type, key)

    def get_offset_by_index(self, index) :
        # 检查
        assert self.offset > 0
        # 返回结果
        return self.offset + PageBuffer.default_size \
            + 4 * SizeOf.integer.value + index * IndexData.size

    def get_offset_by_key(self, key) :
        # 检查
        assert self.offset > 0
        # 返回结果
        return self.offset + PageBuffer.default_size \
            + 4 * SizeOf.integer.value + get_index_by_key(key) * IndexData.size

    @staticmethod
    def __get_subnode_count(size_type) :
        # 检查
        if size_type == SizeType.mb1 :
            return 65521
        elif size_type == SizeType.mb2 :
            return 131063
        elif size_type == SizeType.mb4 :
            return 262139
        elif size_type == SizeType.mb8 :
            return 524269
        elif size_type == SizeType.mb16 :
            return 1048573
        elif size_type == SizeType.mb32 :
            return 2097143
        elif size_type == SizeType.mb64 :
            return 4194301
        # 抛出异常
        raise Exception(f"unsupported size type({size_type})")

    @staticmethod
    def __get_subnode_index(size_type, key) :
        # 返回结果
        return key % IndexPageBuffer.__get_subnode_count(size_type)

    def wrap(self, buffer) :
        super().wrap(buffer)
        buffer.put_int(SizeOf.integer, self.identity)
        buffer.put_int(SizeOf.integer,
            Capacity.e2v(self.capacity))
        buffer.put_int(SizeOf.integer, self.size)
        buffer.put_int(SizeOf.integer, self.count)
        # 循环处理
        for data in self.datas : data.wrap(buffer)

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        self.identity = buffer.get_int(SizeOf.integer)
        self.capacity = Capacity.v2e(buffer.get_int(SizeOf.integer))
        self.size = buffer.get_int(SizeOf.integer)
        self.count = buffer.get_int(SizeOf.integer)
        # 循环处理
        for data in self.datas : data.unwrap(buffer)

    def check_valid(self, data_size) :
        super().check_valid(data_size)
        if self.page_type != PageType.index_page :
            raise Exception(f"invalid page type({self.page_type})")
        if not (15 <= self.size_type.value <= 21) :
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
        # 循环处理
        for index, data in enumerate(self.datas) :
            # 获得数值
            if data.key == 0 : continue
            # 打印数据
            print(f"\tdata[{index}] = "
                  f"[{data.key : 016x},"
                  f"{data.data_offset : 016x},"
                  f"{data.subnode_offset : 016x}]")
