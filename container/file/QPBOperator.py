# -*- coding: utf-8 -*-
from container.Container import *
from container.file.ValueEnum import *
from container.file.PBOperator import *
from container.file.FPBOperator import *
from container.file.QueuePageBuffer import *

class QPBOperator(FPBOperator) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 队列集合
        self.__queues = {}

    def close(self) :
        try :
            # 检查
            if hasattr(self, "_mapped") :
                # 关闭队列
                self.__close()
        except Exception as e :
            traceback.print_exc()
            print("QPBOperator.close : ", str(e))
            print("QPBOperator.close : unexpected exit !")

    def __close(self) :
        # 循环处理
        for page in self.__queues.values() :
            # 写入
            self._write_fully(page.offset, page)

    def _create(self) :
        # 偏移
        offset = HeadPageBuffer.default_size
        offset += FreePageBuffer.default_size
        # 新建
        page = QueuePageBuffer()
        # 设置
        page.offset = offset
        page.identity = 0
        page.size = 0
        page.count = 0
        page.capacity = Capacity.without_limit
        page.root_position = offset
        page.read_position = offset
        page.write_position = offset
        # 写入
        self._write_fully(offset, page)
        # 设置
        self.__queues[page.identity] = page
        # 设置数据尺寸
        self._data_size += QueuePageBuffer.default_size

    def _load(self) :
        # 偏移
        offset = HeadPageBuffer.default_size
        offset += FreePageBuffer.default_size
        # 读取
        page = self._load_page(offset)
        # 检查类型
        if not isinstance(page, QueuePageBuffer) :
            raise Exception(f"invalid queue page buffer")
        if page.identity != 0 :
            raise Exception(f"invalid identity({page.identity}) of root page")
        # 循环处理
        while True :
            # 检查
            if page.identity in self.__queues.keys() :
                raise Exception(f"duplicate identity({page.identity})")
            # 加入集合
            self.__queues[page.identity] = page
            # 检查
            if page.next_page == PageOffset.none : break
            # 新建
            page = self._load_page(page.next_page)
            # 检查
            if not isinstance(page, QueuePageBuffer) :
                raise Exception(f"invalid queue page buffer")

    def dump(self) :
        print(f"QPBOperator.dump : show properties !")
        # 循环处理
        for page in self.__queues.values() : page.dump()