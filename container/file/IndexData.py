# -*- coding: utf-8 -*-

from container.file.ValueEnum import *

class IndexData :
    ##################################################
    #
    # Offsets.
    #
    # Key             [long]
    # Data Offset     [int]
    # Subnode Offset  [int]
    #
    ##################################################
    size = SizeOf.long.value + 2 * SizeOf.integer.value

    # 初始化
    def __init__(self) :
        # 设置参数
        # 临时参数
        self.offset = -1

        # 设置关键字
        self.key = 0
        # 设置数据偏移量
        self.data_offset = PageOffset.none
        # 设置子节点偏移量
        self.subnode_offset = PageOffset.none

    def wrap(self, buffer) :
        buffer.put_int(SizeOf.long, self.key)
        buffer.put_int(SizeOf.integer,
            PageOffset.e2v(self.data_offset))
        buffer.put_int(SizeOf.integer,
            PageOffset.e2v(self.subnode_offset))

    def unwrap(self, buffer) :
        self.key = buffer.get_int(SizeOf.long)
        self.data_offset = \
            PageOffset.v2e(buffer.get_int(SizeOf.integer))
        self.subnode_offset = \
            PageOffset.v2e(buffer.get_int(SizeOf.integer))

    def check_valid(self, file_size) :
        if isinstance(self.data_offset, int) and \
            (self.data_offset > file_size or (self.data_offset & 0x3F) != 0) :
            raise Exception(f"invalid data offset({self.data_offset})")
        if isinstance(self.subnode_offset, int) and \
            (self.subnode_offset > file_size or (self.subnode_offset & 0x3F) != 0) :
            raise Exception(f"invalid data offset({self.subnode_offset})")

    def dump(self) :
        print(f"IndexData.dump : show properties !")
        print(f"\tkey = 0x{self.key :016x}")
        print(f"\tdata_offset = 0x{self.data_offset :016x}")
        print(f"\tsubnode_offset = 0x{self.subnode_offset :016x}")