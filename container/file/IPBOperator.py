# -*- coding: utf-8 -*-
from container.Container import *
from container.file.ValueEnum import *
from container.file.PBOperator import *
from container.file.FPBOperator import *
from container.file.IndexPageBuffer import *

class IPBOperator(FPBOperator) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 索引集合
        self.__indexes = {}

    def close(self) :
        try :
            # 检查
            if hasattr(self, "_mapped") :
                # 关闭队列
                self.__close()
        except Exception as e :
            traceback.print_exc()
            print("IPBOperator.close : ", str(e))
            print("IPBOperator.close : unexpected exit !")

    def __close(self) :
        # 循环处理
        for page in self.__indexes.values() :
            # 写入
            self._write_fully(page.offset, page)

    def _create(self) :
        # 偏移
        offset = HeadPageBuffer.default_size
        offset += FreePageBuffer.default_size
        offset += QueuePageBuffer.default_size
        # 新建
        page = IndexPageBuffer()
        # 设置
        page.offset = offset
        page.identity = 0
        page.size = 0
        page.count = 0
        page.capacity = Capacity.without_limit
        # 写入
        self._write_fully(offset, page)
        # 设置
        self.__indexes[page.identity] = page
        # 设置数据尺寸
        self._data_size += IndexPageBuffer.default_size

    def _load(self) :
        # 偏移
        offset = HeadPageBuffer.default_size
        offset += FreePageBuffer.default_size
        offset += QueuePageBuffer.default_size
        # 读取
        page = self._load_page(offset)
        # 检查类型
        if not isinstance(page, IndexPageBuffer) :
            raise Exception(f"invalid index page buffer")
        if page.identity != 0 :
            raise Exception(f"invalid identity({page.identity}) of root page")
        # 循环处理
        while True :
            # 检查
            if page.identity in self.__indexes.keys() :
                raise Exception(f"duplicate identity({page.identity})")
            # 加入集合
            self.__indexes[page.identity] = page
            # 检查
            if page.next_page == PageOffset.none : break
            # 新建
            page = self._load_page(page.next_page)
            # 检查
            if not isinstance(page, IndexPageBuffer) :
                raise Exception(f"invalid index page buffer")

    def dump(self) :
        print(f"IPBOperator.dump : show properties !")
        # 循环处理
        for page in self.__indexes.values() : page.dump()