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
        # 临时变量
        self.offset = -1
        # 设置参数
        self.next_page = PageOffset.none
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
        buffer.put_int(SizeOf.integer, PageOffset.e2v(self.next_page))
        # 检查参数
        buffer.put_int(SizeOf.integer, OccupiedSize.e2v(self.occupied_size))

    def unwrap(self, buffer) :
        # 重置位置
        buffer.pos = 0
        # 开始解包
        # 如果数据不在枚举范围内，会自动抛出异常
        self.page_type = PageType(buffer.get_int(SizeOf.byte))
        self.size_type = SizeType(buffer.get_int(SizeOf.byte))
        # 获取数值
        self.next_page = PageOffset.v2e(buffer.get_int(SizeOf.integer))
        # 获取参数
        self.occupied_size = OccupiedSize.v2e(buffer.get_int(SizeOf.integer))

    def check_valid(self, file_size) :
        # 检查
        if not isinstance(self.page_type, PageType) :
            raise Exception(f"invalid page type({self.page_type})")
        # 检查
        if not isinstance(self.size_type, SizeType) \
            or self.size_type == SizeType.invalid :
            raise Exception(f"invalid size type({self.size_type})")
        # 检查
        if isinstance(self.next_page, int) and \
            (self.next_page > file_size or (self.next_page & 0x3F) != 0) :
            raise Exception(f"invalid next page({self.next_page})")
        # 检查
        if isinstance(self.occupied_size, int) and \
            self.occupied_size + PageDescription.size > SizeType.get_size(self.size_type) :
            raise Exception(f"invalid occupied size({self.occupied_size})")

    def dump(self) :
        print(f"PageBuffer.dump : show properties !")
        print(f"\toffset = {self.offset}")
        print(f"\tsize_type = {self.size_type}")
        print(f"\tpage_type = {self.page_type}")
        print(f"\tnext_page = {self.next_page}")
        print(f"\toccupied_size = {self.occupied_size}")

def main() :
    # 新建
    buffer = BytesBuffer(128)
    pd = PageBuffer()
    pd.page_type = PageType.invalid
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