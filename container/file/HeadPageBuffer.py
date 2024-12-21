# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PageBuffer import *

class _Version :
    value = 0x4100

class _MagicNumber :
    value = 0x19751204

class _Copyright :
    value = "All rights reserved by www.simpleteam.com. Copyright (c) 2004 ~ 2075"

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
    # Default Size Type
    default_size_type = SizeType.hqkb
    # Default Size
    default_size = SizeType.get_size(default_size_type)

    # 初始化
    def __init__(self) :
        super().__init__(PageType.head_page,
        HeadPageBuffer.default_size_type)
        # 设置参数
        self.safely_closed = SafelyClosed.opened
        self.count = 0
        self.capacity = Capacity.without_limit
        self.size = 0
        self.data_size = 0
        self.file_length = 0

    def wrap(self, buffer) :
        super().wrap(buffer)
        buffer.put_int(SizeOf.integer, _MagicNumber.value)
        buffer.put_int(SizeOf.integer, _Version.value)
        # 检查
        if not SafelyClosed.is_valid(self.safely_closed) :
            raise Exception(f"invalid safely closed({self.safely_closed})")
        buffer.put_int(SizeOf.byte, SafelyClosed.e2v(self.safely_closed))
        buffer.put_int(SizeOf.integer, self.count)
        buffer.put_int(SizeOf.integer, Capacity.e2v(self.capacity))
        buffer.put_int(SizeOf.integer, self.size)
        buffer.put_int(SizeOf.long, self.data_size)
        buffer.put_int(SizeOf.long, self.file_length)
        buffer.put_str(_Copyright.value)

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        value = buffer.get_int(SizeOf.integer)
        # 检查
        if value != _MagicNumber.value :
            raise Exception(f"invalid magic number({value})")
        value = buffer.get_int(SizeOf.integer)
        # 检查
        if value != _Version.value :
            raise Exception(f"invalid version({value})")
        self.safely_closed = SafelyClosed.v2e(buffer.get_int(SizeOf.byte))
        # 检查
        if self.safely_closed is None :
            raise Exception(f"invalid safely closed({self.safely_closed})")
        self.count = buffer.get_int(SizeOf.integer)
        self.capacity = Capacity.v2e(buffer.get_int(SizeOf.integer))
        self.size = buffer.get_int(SizeOf.integer)
        self.data_size = buffer.get_int(SizeOf.long)
        self.file_length = buffer.get_int(SizeOf.long)
        value = buffer.get_str()
        # 检查
        if value != _Copyright.value :
            raise Exception(f"invalid copyright({value})")

    def check_valid(self, file_size) :
        super().check_valid(file_size)
        if self.page_type != PageType.head_page :
            raise Exception(f"invalid page type({self.page_type})")
        if self.next_page != NextPage.none :
            raise Exception(f"invalid next page({self.next_page})")
        if not SafelyClosed.is_valid(self.safely_closed) :
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
        print(f"\tmagic_numer = 0x{_MagicNumber.value:08x}")
        print(f"\tversion = 0x{_Version.value:08x}")
        print(f"\tsafely_closed = {self.safely_closed}")
        print(f"\tcount = {self.count}")
        print(f"\tcapacity = {self.capacity}")
        print(f"\tsize = {self.size}")
        print(f"\tdata_size = {self.data_size}")
        print(f"\tfile_length = {self.file_length}")
        print(f"\tcopyright = \"{_Copyright.value}\"")

def main() :
    # 新建
    buffer = BytesBuffer(128)
    hpb = HeadPageBuffer()
    hpb.dump()
    hpb.wrap(buffer)
    hpb.check_valid(1024)
    buffer.pos = 0
    hpb.unwrap(buffer)
    hpb.check_valid(1024)
    hpb.dump()

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("HeadPageBuffer.main :__main__ : ", str(e))
        print("HeadPageBuffer.main :__main__ : unexpected exit !")