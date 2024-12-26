# -*- coding: utf-8 -*-
from container.Container import *
from container.file.ValueEnum import *
from container.file.PBOperator import *
from container.file.FileContainer import *
from container.file.HeadPageBuffer import *

class HPBOperator(PBOperator) :
    # 偏移量
    default_offset = 0

    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 标志位
        self._safely_closed = SafelyClosed.closed

    def close(self) :
        try :
            # 写入
            HPBOperator._save(self)
        except Exception as ex :
            traceback.print_exc()
            print("HPBOperator.close : ", str(ex))
            print("HPBOperator.close : unexpected exit !")

    def _create(self) :
        # 写入
        HPBOperator._save(self)
        # 设置数据尺寸
        self._inc_data(HeadPageBuffer.default_size)

    def _load(self) :
        # 读取
        page = self._load_page \
            (HPBOperator.default_offset, PageType.head_page)
        # 获得数据尺寸
        self._set_data(page.data_size)
        # 获得参数
        self._safely_closed = page.safely_closed
        # 检查
        if page.file_length != self.file_length :
            raise Exception(f"invalid file length({page.file_length})")
        # 设置容量
        if page.capacity == \
            Capacity.without_limit :
            self._set_capacity(-1)
        else :
            self._set_capacity(page.capacity)
        # 设置参数
        self._set_size(page.size)
        # 设置参数
        self._set_count(page.count)

    def _save(self) :
        # 新建
        page = HeadPageBuffer()
        # 设置参数
        page.safely_closed = SafelyClosed.closed
        # 设置数据尺寸
        page.data_size = self.data_size
        # 设置文件长度
        page.file_length = self.file_length
        # 设置容量
        if self.capacity >= 0 :
            page.capacity = self.capacity
        else :
            page.capacity = Capacity.without_limit
        # 设置尺寸
        page.size = self.size
        # 设置计数
        page.count = self.count
        # 写入数据
        self._write_fully(HPBOperator.default_offset, page)

    def dump(self) :
        print(f"HPBOperator.dump : show properties !")
        print(f"\tdata_size = {self.data_size}")
        print(f"\tfile_length = {self.file_length}")
        print(f"\tsafely_closed = {self._safely_closed}")



