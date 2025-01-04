# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PageBuffer import *

class QueueElementBuffer(PageBuffer) :
    ##################################################
    #
    # Offsets.
    #
    # Identity        [int]
    # Data Offset     [int]
    #
    ##################################################

    # 初始化
    def __init__(self) :
        # 调用父类函数
        super().__init__(PageType.queue_element, SizeType.qqkb)
        # 设置参数
        self.identity = -1
        # 设置参数
        self.data_offset = -1

    def wrap(self, buffer) :
        super().wrap(buffer)
        buffer.put_int(SizeOf.integer, self.identity)
        buffer.put_int(SizeOf.integer, PageOffset.l2i(self.data_offset))

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        self.identity = buffer.get_int(SizeOf.integer)
        self.data_offset = PageOffset.i2l(buffer.get_int(SizeOf.integer))

    def check_valid(self, data_size) :
        super().check_valid(data_size)
        if self.page_type != PageType.queue_element :
            raise Exception(f"invalid page type({self.page_type})")
        if self.size_type != SizeType.qqkb :
            raise Exception(f"invalid size type({self.size_type})")
        PageOffset.check_offset(self.data_offset, data_size)

    def dump(self) :
        super().dump()
        print(f"QueueElementBuffer.dump : show properties !")
        print(f"\tidentity = {self.identity}")
        print(f"\tdata_offset = {self.data_offset}")
