# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PageBuffer import *

class RootPageBuffer(PageBuffer) :
    # Default Root Page Types
    default_root_page_types = SizeType.total_types()
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
        super().__init__(PageType.root_page,
            RootPageBuffer.default_size_type)
        # 设置参数
        self.occupied_size = \
            18 * SizeOf.integer.value
        # 设置参数
        self.next_root_pages = \
            [PageOffset.none for _ in
             range(RootPageBuffer.default_root_page_types)]

    def wrap(self, buffer) :
        super().wrap(buffer)
        # 循环处理
        for i in range(RootPageBuffer.default_root_page_types) :
            buffer.put_int(SizeOf.integer, PageOffset.e2v(self.next_root_pages[i]))

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        # 循环处理
        for i in range(RootPageBuffer.default_root_page_types) :
            self.next_root_pages[i] = PageOffset.v2e(buffer.get_int(SizeOf.integer))

    def check_valid(self, file_size) :
        super().check_valid(file_size)
        if self.page_type != PageType.root_page :
            raise Exception(f"invalid page type({self.page_type})")
        if self.size_type != RootPageBuffer.default_size_type :
            raise Exception(f"invalid size type({self.size_type})")
        if self.next_page != PageOffset.none :
            raise Exception(f"invalid next page({self.next_page})")
        # 循环处理
        for i in range(RootPageBuffer.default_root_page_types) :
            # 获得数值
            value = self.next_root_pages[i]
            # 检查
            if value == PageOffset.none : continue
            # 检查
            elif isinstance(value, int) :
                if value > file_size or (value & 0x3F) != 0 :
                    raise Exception(f"invalid next root page[{i}]({value})")
            else : raise Exception(f"invalid next root page[{i}]({value}) instance")

    def dump(self) :
        super().dump()
        print("RootPageBuffer.dump : show properties !")
        # 循环处理
        for i in range(RootPageBuffer.default_root_page_types) :
            # 获得数值
            print(f"\tnext_root_pages[{i}] = {self.next_root_pages[i]}")

def main() :
    # 新建
    buffer = BytesBuffer(128)
    rpb = RootPageBuffer()
    rpb.dump()
    rpb.wrap(buffer)
    rpb.check_valid(1024)
    buffer.pos = 0
    rpb.unwrap(buffer)
    rpb.check_valid(1024)
    rpb.dump()

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("RootPageBuffer.__main__ : ", str(e))
        print("RootPageBuffer.__main__ : unexpected exit !")