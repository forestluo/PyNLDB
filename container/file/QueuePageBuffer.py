# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PageBuffer import *

class QueuePageBuffer(PageBuffer) :
    ##################################################
    #
    # Offsets.
    #
    # Identity        [int]
    # Capacity        [int]
    # Size            [int]
    # Count           [int]
    # Root Position   [int]
    # Read Position   [int]
    # Write Position  [int]
    #
    ##################################################
    # Default Size Type
    default_size_type = SizeType.qqkb
    # Default Size
    default_size = SizeType.get_size(default_size_type)

    # 初始化
    def __init__(self) :
        # 调用父类函数
        super().__init__(PageType.queue_page,
            QueuePageBuffer.default_size_type)

        # Occupied Size
        self.occupied_size = \
            7 * SizeOf.integer.value

        # Identity
        self.identity = 0
        # Capacity
        self.capacity = Capacity.without_limit
        # Size
        self.size = 0
        # Count
        self.count = 0

        # Root Position
        self.root_position = PageOffset.none
        # Read Position
        self.read_position = PageOffset.none
        # Write Position
        self.write_position = PageOffset.none

    def wrap(self, buffer) :
        super().wrap(buffer)
        buffer.put_int(SizeOf.integer, self.identity)
        buffer.put_int(SizeOf.integer,
            Capacity.e2v(self.capacity))
        buffer.put_int(SizeOf.integer, self.size)
        buffer.put_int(SizeOf.integer, self.count)
        buffer.put_int(SizeOf.integer,
            PageOffset.e2v(self.root_position))
        buffer.put_int(SizeOf.integer,
            PageOffset.e2v(self.read_position))
        buffer.put_int(SizeOf.integer,
            PageOffset.e2v(self.write_position))

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        self.identity = buffer.get_int(SizeOf.integer)
        self.capacity = \
            Capacity.v2e(buffer.get_int(SizeOf.integer))
        self.size = buffer.get_int(SizeOf.integer)
        self.count = buffer.get_int(SizeOf.integer)
        self.root_position = \
            PageOffset.v2e(buffer.get_int(SizeOf.integer))
        self.read_position = \
            PageOffset.v2e(buffer.get_int(SizeOf.integer))
        self.write_position = \
            PageOffset.v2e(buffer.get_int(SizeOf.integer))

    def check_valid(self, file_size) :
        super().check_valid(file_size)
        if self.page_type != PageType.queue_page :
            raise Exception(f"invalid page type({self.page_type})")
        if self.size_type != QueuePageBuffer.default_size_type :
            raise Exception(f"invalid size type({self.size_type})")
        # 检查
        if self.count > self.size :
            raise Exception(f"invalid count({self.count}) or size({self.size})")
        # 获得数值
        positions = {"root position" : self.root_position,
                     "read position" : self.read_position,
                     "write position" : self.write_position}
        # 循环处理
        for key, position in positions.items() :
            # 检查
            if isinstance(position, int) and \
                (position > file_size or (position & 0x3F) != 0) :
                raise Exception(f"invalid {key} ({position})")

    def dump(self) :
        super().dump()
        print(f"QueuePageBuffer.dump : show properties !")
        print(f"\tidentity = {self.identity}")
        print(f"\tcapacity = {self.capacity}")
        print(f"\tsize = {self.size}")
        print(f"\tcount = {self.count}")
        print(f"\troot_position = {self.root_position}")
        print(f"\tread_position = {self.read_position}")
        print(f"\twrite_position = {self.write_position}")
