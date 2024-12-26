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
            6 * SizeOf.integer.value

        # Identity
        self.identity = 0
        # Capacity
        self.capacity = Capacity.without_limit
        # Size
        self.size = 0
        # Count
        self.count = 0

        # Read Position
        self.read_position = -1
        # Write Position
        self.write_position = -1

    def wrap(self, buffer) :
        super().wrap(buffer)
        buffer.put_int(SizeOf.integer, self.identity)
        buffer.put_int(SizeOf.integer,
            Capacity.e2v(self.capacity))
        buffer.put_int(SizeOf.integer, self.size)
        buffer.put_int(SizeOf.integer, self.count)
        buffer.put_int(SizeOf.integer,
            PageOffset.l2i(self.read_position), True)
        buffer.put_int(SizeOf.integer,
            PageOffset.l2i(self.write_position), True)

    def unwrap(self, buffer) :
        super().unwrap(buffer)
        self.identity = buffer.get_int(SizeOf.integer)
        self.capacity = \
            Capacity.v2e(buffer.get_int(SizeOf.integer))
        self.size = buffer.get_int(SizeOf.integer)
        self.count = buffer.get_int(SizeOf.integer)
        self.read_position = \
            PageOffset.i2l(buffer.get_int(SizeOf.integer, True))
        self.write_position = \
            PageOffset.i2l(buffer.get_int(SizeOf.integer, True))

    def check_valid(self, data_size) :
        super().check_valid(data_size)
        if self.page_type != PageType.queue_page :
            raise Exception(f"invalid page type({self.page_type})")
        if self.size_type != QueuePageBuffer.default_size_type :
            raise Exception(f"invalid size type({self.size_type})")
        if self.count > self.size :
            raise Exception(f"invalid count({self.count}) or size({self.size})")
        PageOffset.check_offset(self.read_position, data_size)
        PageOffset.check_offset(self.write_position, data_size)

    def dump(self) :
        super().dump()
        print(f"QueuePageBuffer.dump : show properties !")
        print(f"\tidentity = {self.identity}")
        print(f"\tcapacity = {self.capacity}")
        print(f"\tsize = {self.size}")
        print(f"\tcount = {self.count}")
        print(f"\tread_position = {self.read_position}")
        print(f"\twrite_position = {self.write_position}")
