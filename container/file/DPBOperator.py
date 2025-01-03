# -*- coding: utf-8 -*-
from container.Container import *
from container.file.ValueEnum import *
from container.file.PBOperator import *
from container.file.FPBOperator import *
from container.file.DataPageBuffer import *

class DPBOperator(FPBOperator) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()

    # 释放数据
    def free_data(self, offset) :
        # 检查
        PageOffset.check_offset(offset, self.data_size)
        # 新建
        description = PageBuffer()
        # 读取
        self._read_fully(offset, description)
        # 检查
        if description.page_type != PageType.data_page :
            raise Exception(f"invalid page type({description.page_type})")
        # 释放页面
        self._free_page(offset, description.size_type)

    # 加载数据
    def load_data(self, offset) :
        # 检查
        PageOffset.check_offset(offset, self.data_size)
        # 新建
        description = PageBuffer()
        # 读取
        self._read_fully(offset, description)
        # 检查
        if description.page_type != PageType.data_page :
            raise Exception(f"invalid page type({description.page_type})")
        # 检查
        if description.occupied_size != OccupiedSize.full :
            # 新建
            buffer = BytesBuffer(description.occupied_size)
        else :
            # 新建
            buffer = BytesBuffer(SizeType.get_size(description.size_type))
        # 读取数据
        # 跳过页面头部描述
        self._read_buffer(offset + description.size, buffer)
        # 返回结果
        return buffer

    # 保存数据
    def save_data(self, buffer) :
        # 检查
        assert isinstance(buffer, BytesBuffer)
        # 计算页面尺寸
        page_size = buffer.size + PageBuffer.default_size
        # 取得合适页面类型
        size_type = SizeType.get_type(page_size)
        # 检查结果
        if size_type is None :
            raise Exception(f"unsupported size({page_size}) of page")
        # 创建
        description = PageBuffer()
        # 设置尺寸类型
        description.size_type = size_type
        # 设置页面类型
        description.page_type = PageType.data_page
        # 分配页面
        offset = self._malloc_page \
            (description.page_type, description.size_type)
        # 检查
        if offset < 0 :
            # 创建
            page = DataPageBuffer()
            # 设置尺寸类型
            page.size_type = size_type
            # 设置占用尺寸
            page.occupied_size = buffer.size
            # 设置数据
            page.buffer[:buffer.size] = buffer.bytes[:]
            # 将页面添加至文件尾部
            offset = self._add_page(page)
        else :
            # 设置占用尺寸
            description.occupied_size = buffer.size
            # 写入描述
            self._write_fully(offset, description)
            # 写入数据
            self._write_buffer(offset + PageBuffer.default_size , buffer)
        # 返回结果
        return offset