# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PBOperator import *
from container.file.HeadPageBuffer import *

class HPBOperator(PBOperator) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 标志位
        self._safely_closed = 1

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

    def _save(self) :
        # 新建
        page = HeadPageBuffer()
        # 设置参数
        page.safely_closed = 1
        # 设置数据尺寸
        page.data_size = self.data_size
        # 设置文件长度
        page.file_length = self.file_length
        # 设置容量
        page.capacity = self.capacity
        # 设置尺寸
        page.size = self.size
        # 设置计数
        page.count = self.count
        # 写入数据
        self._write_fully(0, page)

    def _load(self) :
        # 读取
        page = self._load_page(0, PageType.head_page)
        # 获得数据尺寸
        self._set_data(page.data_size)
        # 获得参数
        self._safely_closed = page.safely_closed
        # 检查
        if page.file_length != self.file_length :
            raise Exception(f"invalid file length({page.file_length})")
        # 设置容量
        page.capacity = self.capacity
        # 设置参数
        self._set_size(page.size)
        # 设置参数
        self._set_count(page.count)

    def dump(self) :
        print(f"HPBOperator.dump : show properties !")
        print(f"\tdata_size = {self.data_size}")
        print(f"\tfile_length = {self.file_length}")
        print(f"\tsafely_closed = {self._safely_closed}")



