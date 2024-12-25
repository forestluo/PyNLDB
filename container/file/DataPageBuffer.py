# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PageBuffer import *

class DataPageBuffer(PageBuffer) :
    ##################################################
    #
    # Offsets.
    #
    # Data Bytes      [bytes]
    #
    ##################################################
    # Default Size Type
    default_size_type = SizeType.qqkb
    # Minimum Data Page Size
    #min_data_page_size = min_page_size + SizeOf.byte + SizeOf.integer

    # 初始化
    def __init__(self, size_type = SizeType.qqkb) :
        super().__init__(PageType.data_page, size_type)
        # 参数
        self.buffer = bytearray(SizeType.get_size(size_type))

    def wrap(self, buffer) :
        super().wrap(buffer)
        buffer.put_buffer(self.buffer)

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        self.buffer = buffer.get_buffer()

    def check_valid(self, file_size) :
        super().check_valid(file_size)
        if self.page_type != PageType.data_page :
            raise Exception(f"invalid page type({self.page_type})")

    def dump(self) :
        super().dump()
        print(f"DataPageBuffer.dump : show properties !")
        print(f"\tbytes({len(self.buffer)}) = 0x{self.buffer.hex()}")



