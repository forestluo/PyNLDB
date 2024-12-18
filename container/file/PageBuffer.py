# -*- coding: utf-8 -*-
from container.file.ValueEnum import *
from container.file.PageDescription import *

class PageBuffer :
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
    # Minimum Page Size
    minimum_page_size = PageDescription.size

    # 初始化
    def __init__(self,
        page_type = PageType.invalid,
        size_type = SizeType.invalid) :
        self.next_page = NextPage.none
        self.occupied_size = 0
        self.page_type = page_type
        self.size_type = size_type

    def set_description(self, description) :
        self.page_type = description.page_type
        self.size_type = description.size_type
        self.occupied_size = description.occupied_size
        self.next_page = description.next_page

    def wrap(self, buffer) :
        # 重置位置
        buffer.pos = 0
        # 开始打包
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
        # 重置位置
        buffer.pos = 0
        # 开始解包
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
        print(f"PageBuffer.dump : show properties !")
        print(f"\tsize_type = {self.size_type}")
        print(f"\tpage_type = {self.page_type}")
        print(f"\tnext_page = {self.next_page}")
        print(f"\toccupied_size = {self.occupied_size}")

def main() :
    # 新建
    buffer = BytesBuffer()
    pd = PageBuffer()
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
        print("PageBuffer.main :__main__ : ", str(e))
        print("PageBuffer.main :__main__ : unexpected exit !")