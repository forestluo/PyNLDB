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
        # 文件尺寸
        self._file_length = -1
        # 标志位
        self._safely_closed = SafelyClosed.closed

    def close(self) :
        try :
            # 检查
            if hasattr(self, "_mapped") :
                # 关闭文件头
                self.__write_fully()
        except Exception as e :
            traceback.print_exc()
            print("HPBOperator.close : ", str(e))
            print("HPBOperator.close : unexpected exit !")

    def open(self, file_name) :
        # 文件长度
        self._file_length = -1
        # 检查文件
        if os.path.isfile(file_name) :
            # 获得文件信息
            states = os.stat(file_name)
            # 获得文件大小
            self._file_length = states.st_size
        # 检查结果
        if self._file_length < 0 :
            self._file_length = SizeType.get_size(self.default_size_type)

    def _create(self) :
        # 新建
        page = HeadPageBuffer()
        # 设置参数
        page.safely_closed = SafelyClosed.opened
        # 设置数据尺寸
        page.data_size = self._data_size
        # 设置文件长度
        page.file_length = self._file_length
        # 设置容量
        if self.capacity > 0 :
            page.capacity = self.capacity
        else :
            page.capacity = Capacity.without_limit
        # 设置尺寸
        page.size = self.size
        # 设置计数
        page.count = self.count
        # 写入数据
        self._write_fully(HPBOperator.default_offset, page)
        # 设置数据尺寸
        self._data_size += HeadPageBuffer.default_size

    def _load(self) :
        # 读取
        page = self._load_page(
            HPBOperator.default_offset, PageType.head_page)
        # 获得数据尺寸
        self._data_size = page.data_size
        # 获得参数
        self._safely_closed = page.safely_closed
        # 检查
        if page.file_length != self._file_length :
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

    def __write_fully(self) :
        # 新建
        page = HeadPageBuffer()
        # 设置参数
        page.safely_closed = SafelyClosed.closed
        # 设置数据尺寸
        page.data_size = self._data_size
        # 设置文件长度
        page.file_length = self._file_length
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
        print(f"\tdata_size = {self._data_size}")
        print(f"\tfile_length = {self._file_length}")
        print(f"\tsafely_closed = {self._safely_closed}")



