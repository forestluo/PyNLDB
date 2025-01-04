# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PageBuffer import *
from container.file.BytesBuffer import *

class DataPageBuffer(PageBuffer) :
    ##################################################
    #
    # Offsets.
    #
    # Data Bytes      [bytes]
    #
    ##################################################

    # 初始化
    def __init__(self, size_type = SizeType.qqkb) :
        super().__init__(PageType.data_page, size_type)
        # 参数
        self.buffer = bytearray(SizeType.get_size(size_type))

    def wrap(self, buffer) :
        # 检查
        assert isinstance(buffer, BytesBuffer)
        super().wrap(buffer)
        # 检查
        # 参数occupied_size需要事先设定
        if self.occupied_size < 0 :
            buffer.put_raw(self.buffer, len(self.buffer))
        else :
            buffer.put_raw(self.buffer, self.occupied_size)

    def unwrap(self, buffer) :
        # 检查
        assert isinstance(buffer, BytesBuffer)
        super().unwrap(buffer)
        # 检查
        # 参数occupied_size需要事先设定
        if self.occupied_size < 0 :
            self.buffer = buffer.get_raw(len(self.buffer))
        else :
            self.buffer = buffer.get_raw(self.occupied_size)

    def check_valid(self, data_size) :
        super().check_valid(data_size)
        if self.page_type != PageType.data_page :
            raise Exception(f"invalid page type({self.page_type})")

    def dump(self) :
        super().dump()
        print(f"DataPageBuffer.dump : show properties !")
        print(f"\tbytes({len(self.buffer)}) = 0x{self.buffer.hex()}")