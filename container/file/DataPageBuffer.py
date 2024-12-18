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
        self.buffer = bytearray()

    def wrap(self, buffer, wrap_head = True) :
        if wrap_head : super().wrap(buffer)
        buffer.put_buffer(self.buffer)

    def unwrap(self, buffer, unwrap_head = True) :
        if unwrap_head : super().unwrap(buffer)
        self.buffer = buffer.get_buffer()

    def check_valid(self, file_size) :
        super().check_valid(file_size)
        # 检查
        if self.occupied_size == OccupiedSize.full \
            or self.occupied_size > 0 :
            if self.page_type != PageType.data_page :
                raise Exception(f"invalid page type({self.page_type})")
            if self.next_page != NextPage.none :
                raise Exception(f"invalid next page({self.next_page})")
        else :
            if self.next_page != NextPage.none \
                and self.next_page > file_size :
                raise Exception(f"invalid next page({self.next_page})")

    def dump(self) :
        super().dump()
        print(f"DataPageBuffer.dump : show properties !")
        print(f"\tbytes({len(self.buffer)}) = 0x{self.buffer.hex()}")

def main() :
    # 新建
    buffer = BytesBuffer()
    hpb = DataPageBuffer()
    hpb.buffer = bytearray("Hello World !".encode("utf-8"))
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
        print("DataPageBuffer.main :__main__ : ", str(e))
        print("DataPageBuffer.main :__main__ : unexpected exit !")


