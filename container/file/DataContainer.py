# -*- coding: utf-8 -*-
from container.file.DPBOperator import *
from container.file.FPBOperator import *
from container.file.HPBOperator import *
from container.file.IPBOperator import *
from container.file.QPBOperator import *
from container.file.RPBOperator import *

class DataContainer(HPBOperator,
    DPBOperator, QPBOperator, IPBOperator) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化
        super().__init__()
        # 初始化参数
        self._read_count = 0
        self._write_count = 0

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
            # 按照顺序创建缺省项目
            # 调用父类函数
            HPBOperator._create(self)
            # 调用父类函数
            FPBOperator._create(self)
            # 调用父类函数
            RPBOperator._create(self)
            # 调用父类函数
            QPBOperator._create(self)
            # 设置标记
            self._safely_closed = SafelyClosed.closed

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

def data_operator_case() :
    # 新建
    container = DataContainer()
    # 开启
    container.open("..\\..\\db\\data.bin")
    # 打印信息
    container.dump()

    buffer = BytesBuffer(1234)
    position = container.save_data(buffer)
    container.load_data(position)
    container.free_data(position)

    identity = 1
    container.create_queue(identity)
    container.dump()
    print("----------")
    container.remove_queue(identity)
    container.dump()

    # 关闭
    container.close()

def simple_case() :
    # 新建
    container = DataContainer()
    # 开启
    container.open("..\\..\\db\\data.bin")
    # 关闭
    container.close()
    # 打印信息
    container.dump()

def main() :
    simple_case()
    data_operator_case()

if __name__ == '__main__':
    try :
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("DataContainer.__main__ : ", str(e))
        print("DataContainer.__main__ : unexpected exit !")