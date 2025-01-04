# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PageBuffer import *

class FreePageBuffer(PageBuffer) :
    ##################################################
    #
    # Offsets.
    #
    # Page(s) Offset  [N * long] (N = 18)
    #
    ##################################################
    # Default Size
    default_size = SizeType.get_size(SizeType.hqkb)

    # 初始化
    def __init__(self) :
        super().__init__(PageType.free_page, SizeType.hqkb)
        # 设置参数
        self.occupied_size = -1
        # 设置参数
        self.next_free_pages = [-1 for _ in range(SizeType.total_types())]

    def wrap(self, buffer) :
        super().wrap(buffer)
        # 循环处理
        for i in range(len(self.next_free_pages)) :
            buffer.put_int(SizeOf.integer, PageOffset.l2i(self.next_free_pages[i]))

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        # 循环处理
        for i in range(len(self.next_free_pages)) :
            self.next_free_pages[i] = PageOffset.i2l(buffer.get_int(SizeOf.integer))

    def check_valid(self, data_size) :
        super().check_valid(data_size)
        if self.page_type != PageType.free_page :
            raise Exception(f"invalid page type({self.page_type})")
        if self.size_type != SizeType.hqkb :
            raise Exception(f"invalid size type({self.size_type})")
        if self.next_page != -1 :
            raise Exception(f"invalid next page({self.next_page})")
        # 循环处理
        for i in range(len(self.next_free_pages)) :
            PageOffset.check_offset(self.next_free_pages[i], data_size)

    def dump(self) :
        super().dump()
        print("FreePageBuffer.dump : show properties !")
        # 循环处理
        for i in range(len(self.next_free_pages)) :
            if self.next_free_pages[i] == -1 : continue
            # 获得数值
            print(f"\tnext_free_pages[{i}] = {self.next_free_pages[i]}")