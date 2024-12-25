# -*- coding: utf-8 -*-
from container.file.ValueEnum import *
from container.file.FileContainer import *
from container.file.FreePageBuffer import *
from container.file.RootPageBuffer import *
from container.file.HeadPageBuffer import *
from container.file.DataPageBuffer import *
from container.file.PageDescription import *
from container.file.IndexPageBuffer import *
from container.file.QueuePageBuffer import *
from container.file.IndexElementBuffer import *
from container.file.QueueElementBuffer import *

class PBOperator(FileContainer) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()

    def _add_page(self, page) :
        # 保留数据
        offset = self.data_size
        # 写入数据
        self._write_fully(self.data_size, page)
        # 计数
        self._inc_size_and_count()
        # 增加长度
        self._inc_data(SizeType.get_size(page.size_type))
        # 返回结果
        return offset

    def _load_page(self, position, page_type = None) :
        # 新建
        description = PageDescription()
        # 读取数据
        self._read_description(position, description)
        # 检查
        if page_type is not None :
            # 检查
            PBOperator._check_valid(description, page_type)
        # 检查
        if description.page_type == PageType.head_page :
            # 创建
            page = HeadPageBuffer()
        elif description.page_type == PageType.free_page :
            # 创建
            page = FreePageBuffer()
        elif description.page_type == PageType.root_page :
            # 创建
            page = RootPageBuffer()
        elif description.page_type == PageType.data_page :
            # 创建
            page = DataPageBuffer()
        elif description.page_type == PageType.index_page :
            # 创建
            page = IndexPageBuffer()
        elif description.page_type == PageType.index_element :
            # 创建
            page = IndexElementBuffer()
        elif description.page_type == PageType.queue_page :
            # 创建
            page = QueuePageBuffer()
        elif description.page_type == PageType.queue_element :
            # 创建
            page = QueueElementBuffer()
        else :
            raise Exception(f"invalid page type({description.page_type})")
        # 读取整个页面
        self._read_fully(position, page)
        # 后置处理
        page.offset = position
        # 返回结果
        return page

    def _read_fully(self, position, page) :
        # 检查
        assert isinstance(page, PageBuffer) \
            or isinstance(page, PageDescription)
        # 创建
        buffer = BytesBuffer.create(page.size_type)
        # 读取
        self._read_buffer(position, buffer)
        # 解包
        page.unwrap(buffer)
        # 检查
        page.check_valid(self.data_size)

    def _write_fully(self, position, page) :
        # 检查
        assert isinstance(page, PageBuffer) \
            or isinstance(page, PageDescription)
        # 检查
        page.check_valid(self.data_size)
        # 创建
        buffer = BytesBuffer.create(page.size_type)
        # 打包
        page.wrap(buffer)
        # 写入
        self._write_buffer(position, buffer)

    def _read_description(self, position, description) :
        # 检查
        assert isinstance(description, PageDescription)
        # 创建
        buffer = BytesBuffer.create(description.size_type)
        # 读取
        self._read_buffer(position, buffer)
        # 解包
        description.unwrap(buffer)
        # 检查
        description.check_valid(self.data_size)

    def _write_description(self, position, description) :
        # 检查
        assert isinstance(description, PageDescription)
        # 检查
        description.check_valid(self.data_size)
        # 创建
        buffer = BytesBuffer.create(description.size_type)
        # 打包
        page.wrap(buffer)
        # 写入
        self._write_buffer(position, buffer)

    @staticmethod
    def _check_valid(description, page_type) :
        # 检查
        if page_type != description.page_type :
            raise Exception(f"invalid page type({description.page_type})")
        elif page_type == PageType.head_page :
            if description.size_type != HeadPageBuffer.default_size_type :
                raise Exception(f"invalid size type({description.size_type})")
        elif page_type == PageType.free_page :
            if description.size_type != FreePageBuffer.default_size_type :
                raise Exception(f"invalid size type({description.size_type})")
        elif page_type == PageType.root_page :
            if description.size_type != RootPageBuffer.default_size_type :
                raise Exception(f"invalid size type({description.size_type})")
        elif page_type == PageType.data_page :
            pass
        elif page_type == PageType.index_page :
            if not (15 <= description.size_type.value <= 21) :
                raise Exception(f"invalid size type({description.size_type})")
        elif page_type == PageType.index_element :
            if not (2 <= description.size_type.value <= 11) :
                raise Exception(f"invalid size type({description.size_type})")
        elif page_type == PageType.queue_page :
            if description.size_type != QueuePageBuffer.default_size_type :
                raise Exception(f"invalid size type({description.size_type})")
        elif page_type == PageType.queue_element :
            if description.size_type != QueueElementBuffer.default_size_type :
                raise Exception(f"invalid size type({description.size_type})")
        else :
            raise Exception(f"invalid page type({description.page_type})")
