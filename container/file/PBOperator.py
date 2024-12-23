# -*- coding: utf-8 -*-
from container.file.QueuePageBuffer import QueuePageBuffer
from container.file.ValueEnum import *
from container.file.FileContainer import *
from container.file.FreePageBuffer import *
from container.file.HeadPageBuffer import *
from container.file.DataPageBuffer import *
from container.file.PageDescription import *
from container.file.IndexPageBuffer import *
from container.file.QueueElementBuffer import *

class PBOperator(FileContainer) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 数据尺寸
        # 相当于数据末尾指针
        self._data_size = 0

    def _add_page(self, page) :
        # 保留数据
        offset = self._data_size
        # 写入数据
        self._write_fully(self._data_size, page)
        # 计数
        self._inc_size_and_count()
        # 增加长度
        self._data_size += SizeType.get_size(page.size_type)
        # 返回结果
        return offset

    def _load_page(self, position) :
        # 新建
        description = PageDescription()
        # 读取数据
        self._read_description(position, description)
        # 检查
        if description.page_type == PageType.head_page :
            # 创建
            page = HeadPageBuffer()
        elif description.page_type == PageType.free_page :
            # 创建
            page = FreePageBuffer()
        elif description.page_type == PageType.data_page :
            # 创建
            page = DataPageBuffer()
        elif description.page_type == PageType.index_page :
            # 创建
            page = IndexPageBuffer()
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
        if isinstance(page, QueuePageBuffer) \
            or isinstance(page, IndexPageBuffer) : page.offset = position
        # 返回结果
        return page

    def _read_buffer(self, position, buffer) :
        # 检查
        assert isinstance(buffer, BytesBuffer)
        # 检查
        self._check_read_action(position, buffer.size)
        # 设置位置
        self._mapped.seek(position)
        # 读取
        buffer.bytes = self._mapped.read(buffer.size)

    def _write_buffer(self, position, buffer) :
        # 检查
        assert isinstance(buffer, BytesBuffer)
        # 检查
        self._check_write_action(position, buffer.size)
        # 设置位置
        self._mapped.seek(position)
        # 写入
        self._mapped.write(buffer.bytes)

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
        page.check_valid(self._data_size)

    def _write_fully(self, position, page) :
        # 检查
        assert isinstance(page, PageBuffer) \
            or isinstance(page, PageDescription)
        # 检查
        page.check_valid(self._data_size)
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
        description.check_valid(self._data_size)

    def _write_description(self, position, description) :
        # 检查
        assert isinstance(description, PageDescription)
        # 检查
        description.check_valid(self._data_size)
        # 创建
        buffer = BytesBuffer.create(description.size_type)
        # 打包
        page.wrap(buffer)
        # 写入
        self._write_buffer(position, buffer)
