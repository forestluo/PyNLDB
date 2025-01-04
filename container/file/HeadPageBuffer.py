# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PageBuffer import *

_version = 0x4100
_magic_number = 0x19751204
_copyright = "All rights reserved by www.simpleteam.com. Copyright (c) 2004 ~ 2075"

class HeadPageBuffer(PageBuffer) :
    ##################################################
    #
    # Offsets.
    #
    # Magic Number    [int]
    # Version         [int]
    # Safely Closed   [byte]
    # Count           [int]
    # Capacity        [int]
    # Size            [int]
    # Data Size       [long]
    # File Length     [long]
    # Copyright       [string]
    #
    ##################################################
    # Default Size
    default_size = SizeType.get_size(SizeType.hqkb)

    # 初始化
    def __init__(self) :
        super().__init__(PageType.head_page, SizeType.hqkb)
        # 设置参数
        self.occupied_size = -1
        # 设置参数
        self.safely_closed = 1
        self.count = 0
        self.capacity = -1
        self.size = 0
        self.data_size = 0
        self.file_length = 0

    def wrap(self, buffer) :
        super().wrap(buffer)
        buffer.put_int(SizeOf.integer, _magic_number)
        buffer.put_int(SizeOf.integer, _version)
        buffer.put_int(SizeOf.byte, self.safely_closed)
        buffer.put_int(SizeOf.integer, self.count)
        buffer.put_int(SizeOf.integer, self.capacity, True)
        buffer.put_int(SizeOf.integer, self.size)
        buffer.put_int(SizeOf.long, self.data_size)
        buffer.put_int(SizeOf.long, self.file_length)
        buffer.put_str(_copyright)

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        # 获取数值
        value = buffer.get_int(SizeOf.integer)
        # 检查
        if value != _magic_number :
            raise Exception(f"invalid magic number({value})")
        # 获取数值
        value = buffer.get_int(SizeOf.integer)
        # 检查
        if value != _version :
            raise Exception(f"invalid version({value})")
        # 获取数值
        # 如果不在枚举范围内，会抛出异常
        self.safely_closed = buffer.get_int(SizeOf.byte)
        self.count = buffer.get_int(SizeOf.integer)
        self.capacity = buffer.get_int(SizeOf.integer, True)
        self.size = buffer.get_int(SizeOf.integer)
        self.data_size = buffer.get_int(SizeOf.long)
        self.file_length = buffer.get_int(SizeOf.long)
        # 获取数值
        value = buffer.get_str()
        # 检查
        if value != _copyright :
            raise Exception(f"invalid copyright({value})")

    def check_valid(self, file_size) :
        super().check_valid(file_size)
        if self.page_type != PageType.head_page :
            raise Exception(f"invalid page type({self.page_type})")
        if self.size_type != SizeType.hqkb :
            raise Exception(f"invalid size type({self.size_type})")
        if self.next_page != -1 :
            raise Exception(f"invalid next page({self.next_page})")
        if not (0 <= self.safely_closed <= 1) :
            raise Exception(f"invalid safely closed({self.safely_closed})")
        if self.data_size < 0 or (self.data_size & 0x3F) != 0 :
            raise Exception(f"invalid data size({self.data_size})")
        if self.file_length < 0 or (self.file_length & 0x3F) != 0 :
            raise Exception(f"invalid file length({self.file_length})")
        if self.data_size > self.file_length :
            raise Exception(f"invalid data size({self.data_size}) or file length({self.file_length})")
        if self.size < 0 :
            raise Exception(f"invalid size({self.size})")
        if self.count < 0 :
            raise Exception(f"invalid count({self.count})")
        if self.count > self.size :
            raise Exception(f"invalid count({self.count}) or size({self.size})")

    def dump(self) :
        super().dump()
        print(f"HeadPageBuffer.dump : show properties !")
        print(f"\tdata_size = {self.data_size}")
        print(f"\tfile_length = {self.file_length}")
        print(f"\tsafely_closed = {self.safely_closed}")
        print(f"\tcapacity = {self.capacity}")
        print(f"\tsize = {self.size}")
        print(f"\tcount = {self.count}")
