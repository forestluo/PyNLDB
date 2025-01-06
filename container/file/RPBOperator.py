# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.PBOperator import *
from container.file.HeadPageBuffer import *
from container.file.RootPageBuffer import *

class RPBOperator(PBOperator) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 创建
        self.__next_roots = [-1
            for _ in range(SizeType.total_types())]

    def close(self) :
        try :
            # 写入
            RPBOperator._save(self)
        except Exception as ex :
            traceback.print_exc()
            print("RPBOperator.close : ", str(ex))
            print("RPBOperator.close : unexpected exit !")

    def _create(self) :
        # 写入
        RPBOperator._save(self)
        # 设置数据尺寸
        self._inc_data(RootPageBuffer.default_size)

    def _save(self) :
        # 新建
        page = RootPageBuffer()
        page.offset = HeadPageBuffer.default_size
        page.offset += FreePageBuffer.default_size
        # 循环处理
        for i in range(len(self.__next_roots)) :
            page.next_root_pages[i] = self.__next_roots[i]
        # 写入数据
        self._write_fully(page.offset, page)

    def _load(self) :
        # 偏移量
        offset = HeadPageBuffer.default_size
        offset += FreePageBuffer.default_size
        # 读取
        page = self._load_page(offset, PageType.root_page)
        # 循环处理
        for i in range(len(self.__next_roots)) :
            self.__next_roots[i] = page.next_root_pages[i]

    def _get_root(self, index) :
        # 返回结果
        return self.__next_roots[index]

    def _register_root(self, index, page) :
        # 设置页面指针
        page.next_page  = \
            self.__next_roots[index]
        # 同步写入
        self._write_fully(page.offset, page)
        # 设置当前指针
        self.__next_roots[index] = page.offset

    def _unregister_root(self, index, page) :
        # 检查
        # 当前并无登记的页面
        if self.__next_roots[index] == -1 :
            raise Exception(f"no page registered")
        # 父指针
        parent = self.__get_parent(index, page)
        # 检查结果
        if parent is not None :
            # 设置指针
            parent.next_page = page.next_page
            # 写入
            self._write_fully(parent.offset, parent)
        else :
            # 设置指针
            self.__next_roots[index] = page.next_page

    def __get_parent(self, index, page) :
        # 父指针
        parent = None
        # 获得当前指针
        position = self.__next_roots[index]
        # 循环处理
        while position != page.offset :
            # 加载页面
            _page = self._load_page(position)
            # 检查
            if (index == 0 and _page.page_type != PageType.queue_page) \
                or (index == 1 and _page.page_type != PageType.index_page) :
                raise Exception(f"invalid page type({_page.page_type})")
            # 设置父指针
            parent = _page; position = _page.next_page
        # 检查
        # 页面不在登记队列之中
        if position == -1 :
            raise Exception(f"page({page.offset}) not registered")
        # 返回结果
        return parent

    def dump(self) :
        print(f"RPBOperator.dump : show properties !")
        for i in range(len(self.__next_roots)) :
            if self.__next_roots[i] == -1 : continue
            print(f"\tnext_root[{i}] = 0x{self.__next_roots[i] :016x}")