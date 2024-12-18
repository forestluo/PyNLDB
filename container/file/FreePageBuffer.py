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
        self.next_data_pages = \
            [NextPage.none for _ in
            range(FreePageBuffer.default_data_page_types)]

    def wrap(self, buffer, wrap_head = True) :
        if wrap_head : super().wrap(buffer)
        # 循环处理
        for i in range(FreePageBuffer.default_data_page_types) :
            if self.next_data_pages[i] == NextPage.none :
                buffer.put_int(SizeOf.integer, NextPage.none.value)
            else :
                buffer.put_int(SizeOf.integer, self.next_data_pages[i] >> 6)

    def unwrap(self, buffer, unwrap_head = True) :
        if unwrap_head : super().unwrap(buffer)
        # 循环处理
        for i in range(FreePageBuffer.default_data_page_types) :
            value = buffer.get_int(SizeOf.integer)
            # 检查
            if value != NextPage.none.value :
                self.next_data_pages[i] = value << 6
            else :
                self.next_data_pages[i] = NextPage.none

    def check_valid(self, file_size) :
        super().check_valid(file_size)
        if self.next_page != NextPage.none :
            raise Exception(f"invalid next page({self.next_page})")
        # 循环处理
        for i in range(FreePageBuffer.default_data_page_types) :
            # 获得数值
            value = self.next_data_pages[i]
            # 检查
            if value == NextPage.none : continue
            # 检查
            if value > self.file_size or (value & 0x3F) != 0 :
                raise Exception(f"invalid next data page[{i}]({value})")

    def dump(self) :
        super().dump()
        print("FreePageBuffer.dump : show properties !")
        # 循环处理
        for i in range(FreePageBuffer.default_data_page_types) :
            # 获得数值
            print(f"\tnext_data_pages[{i}] = {self.next_data_pages[i]}")

def main() :
    # 新建
    buffer = BytesBuffer()
    hpb = FreePageBuffer()
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
        print("FreePageBuffer.main :__main__ : ", str(e))
        print("FreePageBuffer.main :__main__ : unexpected exit !")