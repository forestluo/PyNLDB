# -*- coding: utf-8 -*-
from container.Container import *
from container.file.ValueEnum import *
from container.file.PBOperator import *
from container.file.HeadPageBuffer import *
from container.file.RootPageBuffer import *

class RPBOperator(PBOperator) :
    # 偏移量
    default_offset = HeadPageBuffer.default_size \
                    + FreePageBuffer.default_size

    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 创建
        self.__next_roots = [-1
            for _ in range(RootPageBuffer.default_root_page_types)]

    def _get_queue_root(self) :
        # 返回结果
        return self.__next_roots[0]

    def _get_index_root(self) :
        # 返回结果
        return self.__next_roots[1]

    def _register_queue(self, page) :
        # 检查
        assert isinstance(page, QueuePageBuffer)
        # 设置页面指针
        page.next_page  = \
            self.__next_roots[0]
        # 设置当前指针
        self.__next_roots[0] = page.offset
        # 写入
        self.__write_fully()
        # 检查
        if page.next_page < 0 : page.next_page = PageOffset.none

    def _unregister_queue(self, page) :
        # 检查
        assert isinstance(page, QueuePageBuffer)
        # 检查
        # 当前并无登记的页面
        if self.__next_roots[0] < 0 :
            raise Exception(f"no page registered")
        # 父指针
        parent = None
        # 获得当前指针
        position = self.__next_roots[0]
        # 循环处理
        while position != page.offset :
            # 加载页面
            _page = self._load_page(
                position, PageType.queue_page)
            # 设置父指针
            parent = _page; position = _page.next_page
        # 检查
        # 页面不在登记队列之中
        if position < 0 :
            raise Exception(f"page not registered")
        # 检查结果
        if parent is None :
            # 设置指针
            self.__next_roots[0] = page.next_page
            # 写入
            self.__write_fully()
        else :
            # 设置指针
            parent.next_page = page.next_page
            # 写入
            self._write_fully(parent.offset, parent)

    def _register_index(self, page) :
        # 检查
        assert isinstance(page, IndexPageBuffer)
        # 设置页面指针
        page.next_page  = \
            self.__next_roots[1]
        # 设置当前指针
        self.__next_roots[1] = page.offset
        # 检查
        if page.next_page < 0 : page.next_page = PageOffset.none

    def close(self) :
        try :
            # 检查
            if hasattr(self, "_mapped") :
                # 关闭文件头
                self.__write_fully()
        except Exception as e :
            traceback.print_exc()
            print("RPBOperator.close : ", str(e))
            print("RPBOperator.close : unexpected exit !")

    def _create(self) :
        # 新建
        page = RootPageBuffer()
        # 循环处理
        for i in range(RootPageBuffer.default_root_page_types) :
            # 设置数值
            if self.__next_roots[i] < 0 :
                page.next_root_pages[i] = PageOffset.none
            else :
                page.next_root_pages[i] = self.__next_roots[i]
        # 写入数据
        self._write_fully(RPBOperator.default_offset, page)
        # 设置数据尺寸
        self._data_size += RootPageBuffer.default_size

    def _load(self) :
        # 读取
        page = self._load_page(
            RPBOperator.default_offset, PageType.root_page)
        # 循环处理
        for i in range(RootPageBuffer.default_root_page_types) :
            # 设置参数
            if page.next_root_pages[i] == PageOffset.none :
                self.__next_roots[i] = -1
            else :
                self.__next_roots[i] = page.next_root_pages[i]

    def __write_fully(self) :
        # 新建
        page = RootPageBuffer()
        # 循环处理
        for i in range(RootPageBuffer.default_root_page_types) :
            # 设置数值
            if self.__next_roots[i] < 0 :
                page.next_root_pages[i] = PageOffset.none
            else :
                page.next_root_pages[i] = self.__next_roots[i]
        # 写入数据
        self._write_fully(RPBOperator.default_offset, page)

    def dump(self) :
        print(f"RPBOperator.dump : show properties !")
        for i in range(len(self.__next_roots)) :
            if self.__next_roots[i] < 0 : continue
            print(f"\tnext_root[{i}] = 0x{self.__next_roots[i] :016x}")