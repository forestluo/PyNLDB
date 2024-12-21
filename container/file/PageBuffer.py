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

    def wrap(self, buffer) :
        # 重置位置
        buffer.pos = 0
        # 开始打包
        buffer.put_int(SizeOf.byte, self.page_type.value)
        buffer.put_int(SizeOf.byte, self.size_type.value)
        # 检查参数
        buffer.put_int(SizeOf.integer, OccupiedSize.e2v(self.occupied_size))
        # 检查参数
        buffer.put_int(SizeOf.integer, NextPage.e2v(self.next_page))

    def unwrap(self, buffer) :
        # 重置位置
        buffer.pos = 0
        # 开始解包
        self.page_type = PageType(buffer.get_int(SizeOf.byte))
        self.size_type = SizeType(buffer.get_int(SizeOf.byte))
        # 获取参数
        self.occupied_size = OccupiedSize.v2e(buffer.get_int(SizeOf.integer))
        # 获取数值
        self.next_page = NextPage.v2e(buffer.get_int(SizeOf.integer))

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
        if isinstance(self.next_page, int) and \
            (self.next_page > file_size or (self.next_page & 0x3F) != 0) :
            raise Exception(f"invalid next page({self.next_page})")
        # 检查
        if isinstance(self.occupied_size, int) and \
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
    buffer = BytesBuffer(128)
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