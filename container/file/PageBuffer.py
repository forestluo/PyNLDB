# -*- coding: utf-8 -*-
from container.file.ValueEnum import *

class PageBuffer :
    # 缺省大小
    description_size = 10 * SizeOf.byte.value
    ##################################################
    #
    # Offsets.
    #
    # Page Type       [byte]
    # Size Type       [byte]
    # Occupied Size   [int]
    # Next Page       [int]
    #
    ##################################################
    # Default Size Type
    default_size_type = SizeType.qqkb

    # 初始化
    def __init__(self,
        page_type = PageType.invalid,
        size_type = SizeType.qqkb) :
        # 临时变量
        self.offset = -1
        # 设置参数
        self.page_type = page_type
        self.size_type = size_type
        self.next_page = -1
        self.occupied_size = 0

    def wrap(self, buffer) :
        # 重置位置
        buffer.pos = 0
        # 打包
        buffer.put_int(SizeOf.byte, self.page_type.value)
        buffer.put_int(SizeOf.byte, self.size_type.value)
        buffer.put_int(SizeOf.integer, PageOffset.l2i(self.next_page), True)
        buffer.put_int(SizeOf.integer, OccupiedSize.e2v(self.occupied_size))

    def unwrap(self, buffer) :
        # 重置位置
        buffer.pos = 0
        # 开始解包
        # 如果数据不在枚举范围内，会自动抛出异常
        self.page_type = PageType(buffer.get_int(SizeOf.byte))
        self.size_type = SizeType(buffer.get_int(SizeOf.byte))
        # 获取数值
        self.next_page = PageOffset.i2l(buffer.get_int(SizeOf.integer, True))
        # 获取参数
        self.occupied_size = OccupiedSize.v2e(buffer.get_int(SizeOf.integer))

    def check_valid(self, data_size) :
        # 检查
        if not isinstance(self.page_type, PageType) :
            raise Exception(f"invalid page type({self.page_type})")
        # 检查
        if not isinstance(self.size_type, SizeType) :
            raise Exception(f"invalid size type({self.size_type})")
        # 检查
        PageOffset.check_offset(self.next_page, data_size)
        # 检查
        if self.size_type != SizeType.invalid and isinstance(self.occupied_size, int) :
            if self.occupied_size + PageBuffer.description_size > SizeType.get_size(self.size_type) :
                raise Exception(f"invalid occupied size({self.occupied_size})")

    def dump(self) :
        print(f"PageBuffer.dump : show properties !")
        print(f"\toffset = {self.offset}")
        print(f"\tsize_type = {self.size_type}")
        print(f"\tpage_type = {self.page_type}")
        print(f"\tnext_page = {self.next_page}")
        print(f"\toccupied_size = {self.occupied_size}")
