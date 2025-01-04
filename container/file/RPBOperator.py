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
        # 循环处理
        for i in range(len(self.__next_roots)) :
            page.next_root_pages[i] = self.__next_roots[i]
        # 写入数据
        self._write_fully(HeadPageBuffer.default_size +
                        FreePageBuffer.default_size, page)

    def _load(self) :
        # 偏移量
        offset = HeadPageBuffer.default_size
        offset += FreePageBuffer.default_size
        # 读取
        page = self._load_page(offset, PageType.root_page)
        # 循环处理
        for i in range(len(self.__next_roots)) :
            self.__next_roots[i] = page.next_root_pages[i]

    def _get_queue_root(self) :
        # 返回结果
        return self.__next_roots[0]

    def _register_queue(self, page) :
        # 检查
        assert isinstance(page, QueuePageBuffer)
        # 设置页面指针
        page.next_page  = self.__next_roots[0]
        # 设置当前指针
        self.__next_roots[0] = page.offset
        # 写入
        RPBOperator._save(self)

    def _unregister_queue(self, page) :
        # 检查
        assert isinstance(page, QueuePageBuffer)
        # 检查
        # 当前并无登记的页面
        if self.__next_roots[0] == -1 :
            raise Exception(f"no page registered")
        # 父指针
        parent = None
        # 获得当前指针
        position = self.__next_roots[0]
        # 循环处理
        while position != page.offset :
            # 加载页面
            _page = self._load_page(position, PageType.queue_page)
            # 设置父指针
            parent = _page; position = _page.next_page
        # 检查
        # 页面不在登记队列之中
        if position == -1 :
            raise Exception(f"page not registered")
        # 检查结果
        if parent is None :
            # 设置指针
            self.__next_roots[0] = page.next_page
        else :
            # 设置指针
            parent.next_page = page.next_page
            # 写入
            self._write_fully(parent.offset, parent)
        # 写入
        RPBOperator._save(self)

    def _get_index_root(self) :
        # 返回结果
        return self.__next_roots[1]

    def _register_index(self, page) :
        # 检查
        assert isinstance(page, IndexPageBuffer)
        # 设置页面指针
        page.next_page  = self.__next_roots[1]
        # 设置当前指针
        self.__next_roots[1] = page.offset
        # 写入
        RPBOperator._save(self)

    def _unregister_index(self, page) :
        # 检查
        assert isinstance(page, IndexPageBuffer)
        # 检查
        # 当前并无登记的页面
        if self.__next_roots[1] == -1 :
            raise Exception(f"no page registered")
        # 父指针
        parent = None
        # 获得当前指针
        position = self.__next_roots[1]
        # 循环处理
        while position != page.offset :
            # 加载页面
            _page = self._load_page(position, PageType.index_page)
            # 设置父指针
            parent = _page; position = _page.next_page
        # 检查
        # 页面不在登记队列之中
        if position == -1 :
            raise Exception(f"page not registered")
        # 检查结果
        if parent is None :
            # 设置指针
            self.__next_roots[1] = page.next_page
        else :
            # 设置指针
            parent.next_page = page.next_page
            # 写入
            self._write_fully(parent.offset, parent)
        # 写入
        RPBOperator._save(self)

    def dump(self) :
        print(f"RPBOperator.dump : show properties !")
        for i in range(len(self.__next_roots)) :
            if self.__next_roots[i] == -1 : continue
            print(f"\tnext_root[{i}] = 0x{self.__next_roots[i] :016x}")