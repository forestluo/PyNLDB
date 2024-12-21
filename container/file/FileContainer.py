# -*- coding: utf-8 -*-
import os
import mmap
import traceback
from mmap import *

from container.Container import *
from container.file.ValueEnum import *
from container.file.FreePageBuffer import *
from container.file.HeadPageBuffer import *

class FileContainer(Container) :
    # Max Size
    max_size = 1 << (31 + 6)
    # Default Size Type
    default_size_type = SizeType.mb64

    # 初始化
    def __init__(self) :
        # 调用父类函数
        super().__init__()
        # 文件编号
        self._file_no = 0
        # 文件映射
        self._mapped = None

    def open(self, file_name) :
        # 打开文件
        self._file_no = \
            os.open(file_name, os.O_RDWR | os.O_CREAT)
        # 创建映射
        self._mapped = \
            mmap(self._file_no, self._file_length)
        # 补足数据
        # 前置处理
        size = HeadPageBuffer.default_size \
                + FreePageBuffer.default_size
        # 检查
        while size > self._file_length : self.__append(size)

    def close(self) :
        try :
            # 检查
            if hasattr(self, "_mapped") :
                # 关闭映射
                self._mapped.close()
        except Exception as e :
            traceback.print_exc()
            print("FileContainer.close : ", str(e))
            print("FileContainer.close : unexpected exit !")

        try :
            # 检查
            if hasattr(self, "_file_no") :
                # 关闭文件
                os.close(self._file_no)
        except Exception as e :
            traceback.print_exc()
            print("FileContainer.close : ", str(e))
            print("FileContainer.close : unexpected exit !")

    def _check_read_action(self, position, size) :
        # 检查
        if position < 0 or position + size > self._file_length :
            raise Exception(f"invalid position({position})")

    def _check_write_action(self, position, size) :
        # 检查
        if position + size <= self._file_length : return False
        # 缺省数值
        default_size = SizeType.get_size(FileContainer.default_size_type)
        # 补丁
        padding = position + size - self._file_length
        # 检查补丁
        padding = (padding // default_size + 1) * default_size
        # 扩充文件
        self.__append(padding)
        # 返回结果
        return True

    def __append(self, length) :
        # 检查文件长度
        if self._file_length + length > FileContainer.max_size :
            raise Exception(f"too large({length}) for file({self._file_length})")
        # 关闭映射
        self._mapped.close()
        # 设置文件长度
        self._file_length += length
        # 创建映射
        self._mapped = mmap(self._file_no, self._file_length)

    def dump(self) :
        super().dump()
        print(f"FileContainer.dump : show properties !")
        print(f"\tfile_no = {self._file_no}")
