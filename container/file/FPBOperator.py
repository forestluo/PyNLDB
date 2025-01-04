# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PBOperator import *
from container.file.HeadPageBuffer import *
from container.file.FreePageBuffer import *

class FPBOperator(PBOperator) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 创建
        # 长整数指针
        self.__next_frees = [-1
            for _ in range(SizeType.total_types())]

    def close(self) :
        try :
            # 写入
            FPBOperator._save(self)
        except Exception as ex :
            traceback.print_exc()
            print("FPBOperator.close : ", str(ex))
            print("FPBOperator.close : unexpected exit !")

    def _create(self) :
        # 写入
        FPBOperator._save(self)
        # 设置数据尺寸
        self._inc_data(FreePageBuffer.default_size)

    def _save(self) :
        # 新建
        page = FreePageBuffer()
        # 循环处理
        for i in range(len(self.__next_frees)) :
            # 设置数值
            page.next_free_pages[i] = self.__next_frees[i]
        # 写入数据
        self._write_fully(HeadPageBuffer.default_size, page)

    def _load(self) :
        # 偏移量
        offset = HeadPageBuffer.default_size
        # 读取
        page = self._load_page(offset, PageType.free_page)
        # 循环处理
        for i in range(len(self.__next_frees)) :
            # 设置数值
            self.__next_frees[i] = page.next_free_pages[i]

    def _free_page(self, offset, size_type) :
        # 检查
        PageOffset.check_offset(offset, self.data_size)
        # 新建
        description = PageBuffer()
        # 设置尺寸
        description.size_type = size_type
        # 分配页面
        self.__free_page(offset, description)

    def _malloc_page(self, page_type, size_type = None) :
        # 新建
        description = PageBuffer()
        # 设置类型
        description.page_type = page_type
        description.size_type = size_type \
            if size_type is not None \
            else PageType.get_default(page_type)
        # 分配页面
        return self.__malloc_page(description)

    def __free_page(self, offset, description) :
        # 尺寸类型
        size_type = description.size_type
        # 设置参数
        description.page_type = PageType.invalid
        # 设置占用为被释放状态
        description.occupied_size = -1
        # 索引
        index = size_type - 1
        # 设置数值
        description.next_page = self.__next_frees[index]
        # 设置指针
        self.__next_frees[size_type - 1] = offset
        # 写入
        self._write_fully(offset, description)
        # 计数
        self._dec_count()

    def __malloc_page(self, description) :
        # 尺寸类型
        size_type = description.size_type
        # 查询
        offset = self.__next_frees[size_type - 1]
        # 检查
        if offset < 0 : return -1
        # 页面类型
        page_type = description.page_type
        # 读取页面描述
        self._read_fully(offset, description)
        # 检查
        if description.size_type != size_type :
            raise Exception(f"invalid size type({description.size_type})")
        # 索引
        index = size_type - 1
        # 设置数值
        self.__next_frees[index] = description.next_page
        # 页面类型
        description.page_type = page_type
        # 设置参数
        description.next_page = -1
        # 占用空间
        description.occupied_size = -1
        # 增加计数
        self._inc_count()
        # 返回结果
        return offset

    def dump(self) :
        print(f"FPBOperator.dump : show properties !")
        for i in range(len(self.__next_frees)) :
            if self.__next_frees[i] == -1 : continue
            print(f"\tnext_free[{i}] = 0x{self.__next_frees[i] :016x}")