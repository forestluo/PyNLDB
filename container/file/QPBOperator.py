# -*- coding: utf-8 -*-
from PIL.ImageChops import offset
from pandas.io.sas.sas_constants import dataset_offset

from container.Container import *
from container.file.ValueEnum import *
from container.file.PBOperator import *
from container.file.FPBOperator import *
from container.file.RPBOperator import *
from container.file.QueuePageBuffer import *

class QPBOperator(FPBOperator, RPBOperator) :
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
        # 标识
        identity = 0
        # 检查
        if identity not in \
            self.__queues.keys() :
            # 创建缺省队列
            self.create_queue(identity)

    def _load(self) :
        # 获得数值
        position = self._get_queue_root()
        # 循环处理
        while position > 0 :
            # 读取页面
            page = self._load_page(position)
            # 检查
            if page.identity in self.__queues.keys() :
                raise Exception(f"duplicate identity({page.identity})")
            # 加入集合
            self.__queues[page.identity] = page
            # 设置偏移量
            position = page.next_page if page.next_page != PageOffset.none else -1

    def get_queue(self, identity) :
        # 返回结果
        return self.__queues[identity] \
            if identity in self.__queues.keys() else None

    def create_queue(self, identity) :
        # 创建
        page = self.__create_page(identity)
        # 创建
        element = self.__create_element(page.offset, -1, -1)
        # 设置
        page.root_position = element.offset
        page.read_position = element.offset
        page.write_position = element.offset
        # 写入
        self._write_fully(page.offset, page)

    def remove_queue(self, identity) :
        # 检查
        if identity == 0 :
            raise Exception(f"cannot remove default queue")
        if identity not in self.__queues.keys() :
            raise Exception(f"queue({identity}) not exist")
        # 获得页面
        page = self.__queues[identity]
        # 加载元素
        element = self._load_page(page.root_position)
        # 循环处理
        while True :
            # 数量减一
            page.size -= 1
            # 释放页面
            self._free_page(element.offset, element.size_type)
            # 检查
            if element.next_element == PageOffset.none : break
            # 加载元素
            element = self.__load_element(element.next_element)
        # 注销队列
        self._unregister_queue(page)
        # 释放队列
        self._free_page(page.offset, page.size_type)
        # 移除队列
        self.__queues.pop(identity)

    def __create_page(self, identity) :
        # 检查
        if identity in self.__queues.keys() :
            raise Exception(f"duplicate identity({identity})")
        # 新建
        page = QueuePageBuffer()
        # 设置
        page.identity = identity
        page.size = 1
        # 分配页面
        page.offset = self._malloc_page(PageType.queue_page,
                            QueuePageBuffer.default_size_type)
        # 检查
        if page.offset < 0 :
            # 追加页面
            page.offset = self._add_page(page)
        else :
            # 写入
            self._write_fully(page.offset, page)
        # 设置
        self.__queues[page.identity] = page
        # 登记页面
        self._register_queue(page)
        # 返回结果
        return page

    def __create_element(self, page_offset, next_element, data_offset) :
        # 新建
        page = QueueElementBuffer()
        # 设置
        page.page_offset = PageOffset.none \
            if page_offset < 0 else page_offset
        page.data_offset = PageOffset.none \
            if data_offset < 0 else data_offset
        page.next_element = PageOffset.none \
            if next_element < 0 else next_element
        # 分配页面
        page.offset = self._malloc_page(PageType.queue_element,
                            QueueElementBuffer.default_size_type)
        # 检查
        if page.offset < 0 :
            # 追加页面
            page.offset = self._add_page(page)
        else :
            # 写入
            self._write_fully(page.offset, page)
        # 返回结果
        return page

    def dump(self) :
        print(f"QPBOperator.dump : show properties !")
        # 循环处理
        for page in self.__queues.values() : page.dump()