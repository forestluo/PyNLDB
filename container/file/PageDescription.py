# -*- coding: utf-8 -*-
from container.file.ValueEnum import *
from container.file.BytesBuffer import *

class PageDescription :
    # 缺省大小
    size = 10 * SizeOf.byte.value
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
    def __init__(self) :
        self.occupied_size = 0
        self.next_page = NextPage.none
        self.page_type = PageType.invalid
        self.size_type = SizeType.invalid

    def wrap(self, buffer) :
        buffer.put_int(SizeOf.byte, self.page_type.value)
        buffer.put_int(SizeOf.byte, self.size_type.value)
        # 检查参数
        if self.occupied_size != OccupiedSize.full :
            buffer.put_int(SizeOf.integer, self.occupied_size)
        else :
            buffer.put_int(SizeOf.integer, OccupiedSize.full.value)
        # 检查参数
        if self.next_page != NextPage.none :
            buffer.put_int(SizeOf.integer, self.next_page >> 6)
        else :
            buffer.put_int(SizeOf.integer, NextPage.none.value)

    def unwrap(self, buffer) :
        self.page_type = PageType(buffer.get_int(SizeOf.byte))
        self.size_type = SizeType(buffer.get_int(SizeOf.byte))
        # 获取参数
        value = buffer.get_int(SizeOf.integer)
        # 检查结果
        if value != OccupiedSize.full.value :
            self.occupied_size = value
        else :
            self.occupied_size = OccupiedSize.full
        # 获取数值
        value = buffer.get_int(SizeOf.integer)
        # 检查结果
        if value != NextPage.none.value :
            self.next_page = value << 6
        else :
            self.next_page = NextPage.none

    def check_valid(self, file_size) :
        # 检查
        if not PageType.is_valid(self.page_type) :
            raise Exception(f"invalid page type({self.page_type})")
        # 检查
        if not SizeType.is_valid(self.size_type) :
            raise Exception(f"invalid size type({self.size_type})")
        # 检查
        if self.page_type == PageType.head_page :
            if self.size_type != SizeType.hqkb :
                raise Exception(f"invalid size type({self.size_type})")
        # 检查
        elif self.page_type == PageType.free_page :
            if self.size_type != SizeType.hqkb :
                raise Exception(f"invalid size type({self.size_type})")
        # 检查
        if self.next_page != NextPage.none and \
            (self.next_page > file_size or (self.next_page & 0x3F) != 0) :
            raise Exception(f"invalid next page({self.next_page})")
        # 检查
        if self.occupied_size != OccupiedSize.full and \
            self.occupied_size + PageDescription.size > SizeType.get_size(self.size_type) :
            raise Exception(f"invalid occupied size({self.occupied_size}")

    def dump(self) :
        print(f"PageDescription.dump : show properties !")
        print(f"\tsize_type = {self.size_type}")
        print(f"\tpage_type = {self.page_type}")
        print(f"\tnext_page = {self.next_page}")
        print(f"\toccupied_size = {self.occupied_size}")

def main() :
    # 新建
    buffer = BytesBuffer()
    pd = PageDescription()
    pd.page_type = PageType.free_page
    pd.size_type = SizeType.hqkb
    pd.dump()
    pd.wrap(buffer)
    pd.check_valid(1024)
    buffer.pos = 0
    pd.unwrap(buffer)
    pd.check_valid(1024)
    pd.dump()

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("PageDescription.main :__main__ : ", str(e))
        print("PageDescription.main :__main__ : unexpected exit !")