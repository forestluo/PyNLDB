# -*- coding: utf-8 -*-
from container.file.ValueEnum import *

class PageBuffer :
    # 缺省大小
    description_size = 10 * SizeOf.byte
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
    _default_size_type = SizeType.qqkb

    # 初始化
    def __init__(self,
        page_type = PageType.invalid, size_type = SizeType.qqkb) :
        # 临时变量
        self.offset = -1
        # 设置参数
        self.page_type = page_type
        self.size_type = size_type
        self.next_page = -1
        self.occupied_size = -1

    def wrap(self, buffer) :
        # 重置位置
        buffer.pos = 0
        # 打包
        buffer.put_int(SizeOf.byte, self.page_type)
        buffer.put_int(SizeOf.byte, self.size_type)
        buffer.put_int(SizeOf.integer, PageOffset.l2i(self.next_page))
        buffer.put_int(SizeOf.integer, self.occupied_size, True)

    def unwrap(self, buffer) :
        # 重置位置
        buffer.pos = 0
        # 解包
        self.page_type = buffer.get_int(SizeOf.byte)
        self.size_type = buffer.get_int(SizeOf.byte)
        self.next_page = PageOffset.i2l(buffer.get_int(SizeOf.integer))
        self.occupied_size = buffer.get_int(SizeOf.integer, True)

    def check_valid(self, data_size) :
        if not PageType.is_valid(self.page_type) :
            raise Exception(f"invalid page type({self.page_type})")
        if not SizeType.is_valid(self.size_type) :
            raise Exception(f"invalid size type({self.size_type})")
        PageOffset.check_offset(self.next_page, data_size)
        PageType.check_default(self.page_type, self.size_type)
        if self.size_type != SizeType.invalid and self.occupied_size >= 0 :
            if self.occupied_size + PageBuffer.description_size > SizeType.get_size(self.size_type) :
                raise Exception(f"invalid occupied size({self.occupied_size})")

    def dump(self) :
        print(f"PageBuffer.dump : show properties !")
        print(f"\toffset = {self.offset}")
        print(f"\tsize_type = {self.size_type}")
        print(f"\tpage_type = {self.page_type}")
        print(f"\tnext_page = {self.next_page}")
        print(f"\toccupied_size = {self.occupied_size}")
