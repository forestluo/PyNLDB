# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PageBuffer import *

class FreePageBuffer(PageBuffer) :
    # Default Data Page Types
    default_data_page_types = SizeType.total_types()
    ##################################################
    #
    # Offsets.
    #
    # Page(s) Offset  [N * long] (N = 18)
    #
    ##################################################
    # Default Size Type
    default_size_type = SizeType.hqkb
    # Default Size
    default_size = SizeType.get_size(default_size_type)

    # 初始化
    def __init__(self) :
        super().__init__(PageType.free_page,
            FreePageBuffer.default_size_type)
        # 设置参数
        self.occupied_size = \
            18 * SizeOf.integer.value
        # 设置参数
        self.next_free_pages = \
            [-1
             for _ in range(FreePageBuffer.default_data_page_types)]

    def wrap(self, buffer) :
        super().wrap(buffer)
        # 循环处理
        for i in range(FreePageBuffer.default_data_page_types) :
            buffer.put_int(SizeOf.integer,
                PageOffset.l2i(self.next_free_pages[i]), True)

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        # 循环处理
        for i in range(FreePageBuffer.default_data_page_types) :
            self.next_free_pages[i] = \
                PageOffset.i2l(buffer.get_int(SizeOf.integer, True))

    def check_valid(self, data_size) :
        super().check_valid(data_size)
        if self.page_type != PageType.free_page :
            raise Exception(f"invalid page type({self.page_type})")
        if self.size_type != FreePageBuffer.default_size_type :
            raise Exception(f"invalid size type({self.size_type})")
        if self.next_page != -1 :
            raise Exception(f"invalid next page({self.next_page})")
        # 循环处理
        for i in range(FreePageBuffer.default_data_page_types) :
            # 检查
            PageOffset.check_offset(self.next_free_pages[i], data_size)

    def dump(self) :
        super().dump()
        print("FreePageBuffer.dump : show properties !")
        # 循环处理
        for i in range(FreePageBuffer.default_data_page_types) :
            # 检查
            if self.next_free_pages[i] < 0 : continue
            # 获得数值
            print(f"\tnext_free_pages[{i}] = {self.next_free_pages[i]}")