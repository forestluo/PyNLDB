# -*- coding: utf-8 -*-
import os
import mmap
import traceback
from mmap import *

from container.Container import *
from container.file.ValueEnum import *
from container.file.BytesBuffer import *
from container.file.FreePageBuffer import *
from container.file.HeadPageBuffer import *
from container.file.RootPageBuffer import *

class FileContainer(Container) :
    # Max Size
    _max_size = 1 << (31 + 6)
    # Default Size Type
    _default_size_type = SizeType.mb64

    # 初始化
    def __init__(self) :
        # 调用父类函数
        super().__init__()
        # 文件编号
        self.__file_no = 0
        # 文件映射
        self.__mapped = None
        # 数据尺寸
        # 相当于数据末尾指针
        self.__data_size = 0
        # 文件尺寸
        self.__file_length = -1

    @property
    def data_size(self) :
        # 返回结果
        return self.__data_size

    def _set_data(self, value) :
        # 增加数值
        self.__data_size = value

    def _inc_data(self, value) :
        # 增加数值
        self.__data_size += value

    @property
    def file_length(self) :
        # 返回结果
        return self.__file_length
    
    def open(self, file_name) :
        # 检查文件
        if os.path.isfile(file_name) :
            # 获得文件信息
            states = os.stat(file_name)
            # 获得文件大小
            self.__file_length = states.st_size
        # 检查结果
        if self.__file_length < 0 :
            self.__file_length = \
                SizeType.get_size(FileContainer._default_size_type)

        # 打开文件
        self.__file_no = \
            os.open(file_name, os.O_RDWR | os.O_CREAT)
        # 创建映射
        self.__mapped = \
            mmap(self.__file_no, self.__file_length)
        # 补足数据
        # 前置处理
        size = HeadPageBuffer.default_size
        size += FreePageBuffer.default_size
        size += RootPageBuffer.default_size
        # 检查
        while size > self.__file_length : self.__append(size)

    def close(self) :
        try :
            # 检查
            if hasattr(self, "__mapped") :
                # 关闭映射
                self.__mapped.close()
        except Exception as ex :
            traceback.print_exc()
            print("FileContainer.close : ", str(ex))
            print("FileContainer.close : unexpected exit !")

        try :
            # 检查
            if hasattr(self, "__file_no") :
                # 关闭文件
                os.close(self.__file_no)
        except Exception as ex :
            traceback.print_exc()
            print("FileContainer.close : ", str(ex))
            print("FileContainer.close : unexpected exit !")

    def __check_read_action(self, position, size) :
        # 检查
        if position < 0 or position + size > self.__file_length :
            raise Exception(f"invalid position({position})")

    def __check_write_action(self, position, size) :
        # 检查
        if position + size <= self.__file_length : return
        # 缺省数值
        default_size = SizeType.get_size(FileContainer._default_size_type)
        # 补丁
        padding = position + size - self.__file_length
        # 检查补丁
        padding = (padding // default_size + 1) * default_size
        # 扩充文件
        self.__append(padding)

    def __append(self, length) :
        # 检查文件长度
        if self.__file_length + length > FileContainer._max_size :
            raise Exception(f"too large({length}) for file({self.__file_length})")
        # 关闭映射
        self.__mapped.close()
        # 设置文件长度
        self.__file_length += length
        # 创建映射
        self.__mapped = mmap(self.__file_no, self.__file_length)

    def _read_buffer(self, position, buffer) :
        # 检查
        assert isinstance(buffer, BytesBuffer)
        # 检查
        self.__check_read_action(position, buffer.size)
        # 设置位置
        self.__mapped.seek(position)
        # 读取
        buffer.bytes = self.__mapped.read(buffer.size)

    def _write_buffer(self, position, buffer) :
        # 检查
        assert isinstance(buffer, BytesBuffer)
        # 检查
        self.__check_write_action(position, buffer.size)
        # 设置位置
        self.__mapped.seek(position)
        # 写入
        self.__mapped.write(buffer.bytes)

    def dump(self) :
        super().dump()
        print(f"FileContainer.dump : show properties !")
        print(f"\tfile_no = {self.__file_no}")
