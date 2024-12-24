# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PageBuffer import *

class QueueElementBuffer(PageBuffer) :
    ##################################################
    #
    # Offsets.
    #
    # Data Offset     [int]
    # Next Element    [int]
    # Page Offset     [int]
    #
    ##################################################
    # Default Size Type
    default_size_type = SizeType.qqkb
    # Default Size
    default_size = SizeType.get_size(default_size_type)

    # 初始化
    def __init__(self) :
        # 调用父类函数
        super().__init__(PageType.queue_element,
            QueueElementBuffer.default_size_type)
        # 设置参数
        self.occupied_size = \
            3 * SizeOf.integer.value
        # 设置参数
        self.page_offset = PageOffset.none
        # 设置参数
        self.data_offset = PageOffset.none
        # 设置参数
        self.next_element = PageOffset.none

    def wrap(self, buffer) :
        super().wrap(buffer)
        buffer.put_int(SizeOf.integer,
            PageOffset.e2v(self.page_offset))
        buffer.put_int(SizeOf.integer,
            PageOffset.e2v(self.next_element))
        buffer.put_int(SizeOf.integer,
            PageOffset.e2v(self.data_offset))

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        self.page_offset = \
            PageOffset.v2e(buffer.get_int(SizeOf.integer))
        self.next_element = \
            PageOffset.v2e(buffer.get_int(SizeOf.integer))
        self.data_offset = \
            PageOffset.v2e(buffer.get_int(SizeOf.integer))

    def check_valid(self, file_size) :
        super().check_valid(file_size)
        if self.page_type != PageType.queue_element :
            raise Exception(f"invalid page type({self.page_type})")
        if self.size_type != QueueElementBuffer.default_size_type :
            raise Exception(f"invalid size type({self.size_type})")
        # 获得数值
        offsets = {"page offset" : self.page_offset,
                   "data offset" : self.data_offset,
                   "next element" : self.next_element}
        # 循环处理
        for key, offset in offsets.items() :
            # 检查
            if offset == PageOffset.none : continue
            # 检查
            elif isinstance(offset, int) :
                if offset > file_size or (offset & 0x3F) != 0 :
                    raise Exception(f"invalid {key} ({offset})")
            else :
                raise Exception(f"invalid {key} ({offset}) instance")

    def dump(self) :
        super().dump()
        print(f"QueueElementBuffer.dump : show properties !")
        print(f"\tpage_offset = {self.page_offset}")
        print(f"\tnext_element = {self.next_element}")
        print(f"\tdata_offset = {self.data_offset}")

def main() :
    # 新建
    buffer = BytesBuffer(128)
    qeb = QueueElementBuffer()
    qeb.dump()
    qeb.wrap(buffer)
    qeb.check_valid(1024)
    buffer.pos = 0
    qeb.unwrap(buffer)
    qeb.check_valid(1024)
    qeb.dump()

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("QueueElementBuffer.__main__ : ", str(e))
        print("QueueElementBuffer.__main__ : unexpected exit !")
