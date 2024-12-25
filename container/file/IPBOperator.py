# -*- coding: utf-8 -*-
from container.Container import *
from container.file.ValueEnum import *
from container.file.PBOperator import *
from container.file.FPBOperator import *
from container.file.RPBOperator import *
from container.file.IndexPageBuffer import *

class IPBOperator(FPBOperator, RPBOperator) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 索引集合
        self.__indexes = {}

    def close(self) :
        try :
            # 关闭队列
            self.__flush()
        except Exception as e :
            traceback.print_exc()
            print("IPBOperator.close : ", str(e))
            print("IPBOperator.close : unexpected exit !")

    def __flush(self) :
        # 循环处理
        for page in self.__indexes.values() :
            # 写入
            self._write_fully(page.offset, page)

    def _load(self) :
        # 获得数值
        offset = self._get_index_root()
        # 循环处理
        while offset > 0 :
            # 读取页面
            page = self._load_page(offset, PageType.queue_page)
            # 检查
            if page.identity in self.__queues.keys() :
                raise Exception(f"duplicate identity({page.identity})")
            # 加入集合
            self.__queues[page.identity] = page
            # 设置偏移量
            offset = page.next_page if page.next_page != PageOffset.none else -1

    def dump(self) :
        print(f"IPBOperator.dump : show properties !")
        # 循环处理
        for page in self.__indexes.values() : page.dump()