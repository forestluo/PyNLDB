# -*- coding: utf-8 -*-
from nlp.content.WordContent import *

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

def simple_index_case() :
    # 新建
    container = DataContainer()
    # 开启
    container.open("..\\..\\db\\data.bin")
    # 创建索引
    container.create_index(1)

    words = WordContent()
    for i in range(1) :
        if words.load(f"..\\..\\json\\words{i + 1}.json") <= 0 :
            print("DataCenter.main : fail to load file !")
            return
    for item in words.values() :
        container.save_index(1, item.content, item.count)
        count = container.load_index(1, item.content)
        # 检查
        if count != item.count :
            print(f"incorrect result")

    container.dump()
    print("------------------------------3------------------------------")

    for item in words.values() :
        count = container.delete_index(1,item.content)
        # 检查
        if count != item.count :
            print(f"incorrect result({item.content},{item.count},{count})")

    print("------------------------------4------------------------------")

    container.delete_index(1)
    container.dump()
    print("------------------------------5------------------------------")
    # 关闭
    container.close()

def simple_queue_case() :
    # 新建
    container = DataContainer()
    # 开启
    container.open("..\\..\\db\\data.bin")
    # 打印信息
    container.dump()
    print("------------------------------1------------------------------")

    identity = 1
    data_offset = -1
    container.create_queue(identity)
    container.dump()
    print("------------------------------2------------------------------")
    container.write_queue(identity, data_offset)
    container.dump()
    print("------------------------------3------------------------------")
    container.read_queue(identity)
    container.dump()
    print("------------------------------4------------------------------")
    container.clear_queue(identity)
    container.dump()
    print("------------------------------5------------------------------")
    container.delete_queue(identity)
    container.dump()
    print("------------------------------6------------------------------")

    # 关闭
    container.close()

def simple_data_case() :
    # 新建
    container = DataContainer()
    # 开启
    container.open("..\\..\\db\\data.bin")
    # 数据
    data = BytesBuffer(64)
    data.put_str("Hello World !")
    # 保存数据
    offset = container.save_data(data)
    print("------------------------------1------------------------------")
    # 读取数据
    data = container.load_data(offset)
    # 复位
    data.pos = 0
    # 打印
    print(data.get_str())
    print("------------------------------2------------------------------")
    # 释放数据
    container.free_data(offset)
    print("------------------------------3------------------------------")
    # 关闭
    container.close()
    # 打印信息
    container.dump()

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
    #simple_case()
    #simple_data_case()
    #simple_queue_case()
    simple_index_case()

if __name__ == '__main__':
    try :
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("DataContainer.__main__ : ", str(e))
        print("DataContainer.__main__ : unexpected exit !")