# -*- coding: utf-8 -*-
from container.file.DPBOperator import *
from container.file.FPBOperator import *
from container.file.HPBOperator import *

class DataContainer(HPBOperator,
    DPBOperator) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化
        super().__init__()
        # 初始化参数
        self._read_count = 0
        self._write_count = 0

    def _free(self, offset, size_type) :
        # 新建
        description = PageDescription()
        # 设置类型
        description.page_type = \
            PageType.data_page
        # 设置尺寸
        description.size_type = size_type
        # 分配页面
        self._free_page(offset, description)

    def _malloc(self, page_type, size_type) :
        # 新建
        description = PageDescription()
        # 设置类型
        description.page_type = page_type
        # 设置尺寸
        description.size_type = size_type
        # 分配页面
        return self._malloc_page(description)

    def close(self) :
        # 调用父类函数
        HPBOperator.close(self)
        # 调用父类函数
        FPBOperator.close(self)
        # 调用父类函数
        FileContainer.close(self)

    def open(self, file_name) :
        # 检查文件
        exist_flag = os.path.isfile(file_name)
        # 调用父类函数
        HPBOperator.open(self, file_name)
        # 调用父类函数
        FPBOperator.open(self, file_name)
        # 调用父类函数
        FileContainer.open(self, file_name)
        # 检查文件
        if exist_flag :
            # 调用父类函数
            HPBOperator._load(self)
            # 调用父类函数
            FPBOperator._load(self)
        else :
            # 调用父类函数
            HPBOperator._save(self)
            # 调用父类函数
            FPBOperator._save(self)
            # 设置标记
            self._safely_closed = SafelyClosed.closed

    def dump(self) :
        FileContainer.dump(self)
        HPBOperator.dump(self)
        FPBOperator.dump(self)
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
    offset = container.save_data(buffer)
    container.load_data(offset)
    #container.free_data(offset)
    container.remove_data(offset)

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