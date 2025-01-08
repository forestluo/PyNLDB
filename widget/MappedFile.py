# -*- coding: utf-8 -*-
import os
import mmap
import traceback
from mmap import *

class MappedFile :
    # 初始化
    def __init__(self, file_name) :
        # 文件编号
        self.__file_no = 0
        # 文件映射
        self.__mapped = None
        # 设置参数
        self.__file_name = file_name

    def read(self) :
        # 检查
        assert self.__mapped is not None
        # 返回结果
        return self.__mapped.read()

    def readline(self) :
        # 检查
        assert self.__mapped is not None
        # 返回结果
        return self.__mapped.readline()

    def exists(self) :
        # 检查文件
        return os.path.isfile(self.__file_name)

    def length(self) :
        # 检查文件
        if not os.path.isfile(self.__file_name) :
            return -1
        # 返回结果
        return os.stat(self.__file_name).st_size

    # 仅为读取开启
    def open(self) :
        # 检查文件
        file_length = self.length()
        # 检查结果
        if file_length > 0 :
            # 打开文件
            self.__file_no = \
                os.open(file_name, os.O_RDONLY)
            # 创建映射
            self.__mapped = \
                mmap(self.__file_no, file_length)
        # 返回结果
        return file_length

    def close(self) :
        try :
            # 检查
            if hasattr(self, "__mapped") :
                # 关闭映射
                self.__mapped.close()
        except Exception as ex :
            traceback.print_exc()
            print("MappedFile.close : ", str(ex))
            print("MappedFile.close : unexpected exit !")

        try :
            # 检查
            if hasattr(self, "__file_no") :
                # 关闭文件
                os.close(self.__file_no)
        except Exception as ex :
            traceback.print_exc()
            print("MappedFile.close : ", str(ex))
            print("MappedFile.close : unexpected exit !")
