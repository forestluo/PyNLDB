# -*- coding: utf-8 -*-
from container.Container import *
from container.file.ValueEnum import *
from container.file.PBOperator import *
from container.file.HeadPageBuffer import *
from container.file.FreePageBuffer import *

class FPBOperator(PBOperator) :
    # 偏移量
    default_offset = HeadPageBuffer.default_size

    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 创建
        self.__next_frees = [-1
            for _ in range(FreePageBuffer.default_data_page_types)]

    def close(self) :
        try :
            # 检查
            if hasattr(self, "_mapped") :
                # 关闭文件头
                self.__close()
        except Exception as e :
            traceback.print_exc()
            print("FPBOperator.close : ", str(e))
            print("FPBOperator.close : unexpected exit !")

    def _create(self) :
        # 新建
        page = FreePageBuffer()
        # 循环处理
        for i in range(FreePageBuffer.default_data_page_types) :
            # 设置数值
            if self.__next_frees[i] < 0 :
                page.next_data_pages[i] = PageOffset.none
            else :
                page.next_data_pages[i] = self.__next_frees[i]
        # 写入数据
        self._write_fully(FPBOperator.default_offset, page)
        # 设置数据尺寸
        self._data_size += FreePageBuffer.default_size

    def _load(self) :
        # 读取
        page = self._load_page(HeadPageBuffer.default_size)
        # 检查类型
        if not isinstance(page, FreePageBuffer) :
            raise Exception("invalid free page buffer")
        # 循环处理
        for i in range(FreePageBuffer.default_data_page_types) :
            # 设置参数
            if page.next_data_pages[i] == PageOffset.none :
                self.__next_frees[i] = -1
            else :
                self.__next_frees[i] = page.next_data_pages[i]

    def __close(self) :
        # 新建
        page = FreePageBuffer()
        # 循环处理
        for i in range(FreePageBuffer.default_data_page_types) :
            # 设置数值
            if self.__next_frees[i] < 0 :
                page.next_data_pages[i] = PageOffset.none
            else :
                page.next_data_pages[i] = self.__next_frees[i]
        # 写入数据
        self._write_fully(FPBOperator.default_offset, page)

    def _free_page(self, offset, size_type) :
        # 新建
        description = PageDescription()
        # 设置尺寸
        description.size_type = size_type
        # 分配页面
        self.__free_page(offset, description)

    def _malloc_page(self, page_type, size_type) :
        # 新建
        description = PageDescription()
        # 设置类型
        description.page_type = page_type
        # 设置尺寸
        description.size_type = size_type
        # 分配页面
        return self.__malloc_page(description)

    def __free_page(self, offset, description) :
        # 尺寸类型
        size_type = description.size_type
        # 设置参数
        description.page_type = PageType.invalid
        # 设置占用为被释放状态
        description.occupied_size = 0
        # 检查数据
        if self.__next_frees[size_type.value - 1] < 0 :
            # 设置类型
            description.next_page = PageOffset.none
        else :
            # 设置数值
            description.next_page = self.__next_frees[size_type.value - 1]
        # 设置指针
        self.__next_frees[size_type.value - 1] = offset
        # 写入
        self._write_fully(offset, description)
        # 计数
        self._dec_count()

    def __malloc_page(self, description) :
        # 尺寸类型
        size_type = description.size_type
        # 查询
        offset = self.__next_frees[size_type.value - 1]
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
        index = size_type.value - 1
        # 检查
        if description.next_page == PageOffset.none :
            self.__next_frees[index] = -1
        elif isinstance(description.next_page, int) :
            self.__next_frees[index] = description.next_page
        else : raise Exception(f"invalid next page({description.next_page})")
        # 页面类型
        description.page_type = page_type
        # 设置参数
        description.next_page = PageOffset.none
        # 占用空间
        description.occupied_size = 0
        # 增加计数
        self._inc_count()
        # 返回结果
        return offset

    def dump(self) :
        print(f"FPBOperator.dump : show properties !")
        for i in range(len(self.__next_frees)) :
            if self.__next_frees[i] < 0 : continue
            print(f"\tnext_free[{i}] = 0x{self.__next_frees[i] :016x}")