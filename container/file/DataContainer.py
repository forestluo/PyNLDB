# -*- coding: utf-8 -*-
from container.file.HPBOperator import *
from container.file.FPBOperator import *
from container.file.RPBOperator import *
from container.file.DPBOperator import *
from container.file.QPBOperator import *
from container.file.IPBOperator import *

class DataContainer(HPBOperator,
    DPBOperator, QPBOperator, IPBOperator) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化
        super().__init__()
        # 初始化参数
        self._read_count = 0
        self._write_count = 0

    def save(self) :
        # 调用父类函数
        IPBOperator._flush(self)
        # 调用父类函数
        QPBOperator._flush(self)
        # 保存
        RPBOperator._save(self)
        # 保存
        FPBOperator._save(self)
        # 保存
        HPBOperator._save(self)

    def close(self) :
        # 调用父类函数
        IPBOperator.close(self)
        # 调用父类函数
        QPBOperator.close(self)
        # 调用父类函数
        RPBOperator.close(self)
        # 调用父类函数
        FPBOperator.close(self)
        # 调用父类函数
        HPBOperator.close(self)
        # 调用父类函数
        FileContainer.close(self)

    def open(self, file_name) :
        # 检查文件
        exist_flag = \
            os.path.isfile(file_name)
        # 调用父类函数
        FileContainer.open(self, file_name)
        # 检查文件
        if exist_flag :
            # 按照顺序创建缺省项目
            # 调用父类函数
            HPBOperator._load(self)
            # 调用父类函数
            FPBOperator._load(self)
            # 调用父类函数
            RPBOperator._load(self)
            # 调用父类函数
            QPBOperator._load(self)
            # 调用父类函数
            IPBOperator._load(self)
        else :
            # 设置标记
            self._safely_closed = 1
            # 按照顺序创建缺省项目
            # 调用父类函数
            HPBOperator._create(self)
            # 调用父类函数
            FPBOperator._create(self)
            # 调用父类函数
            RPBOperator._create(self)

    def dump(self) :
        FileContainer.dump(self)
        HPBOperator.dump(self)
        FPBOperator.dump(self)
        RPBOperator.dump(self)
        QPBOperator.dump(self)
        IPBOperator.dump(self)
        print(f"DataContainer.dump : show properties !")
        print(f"\tread_count = {self._read_count}")
        print(f"\twrite_count = {self._write_count}")
