# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.FPBOperator import *
from container.file.RPBOperator import *

class QPBOperator(FPBOperator, RPBOperator) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 队列集合
        self.__queues = {}

    def close(self) :
        try :
            # 写入
            QPBOperator._flush(self)
        except Exception as ex :
            traceback.print_exc()
            print("QPBOperator.close : ", str(ex))
            print("QPBOperator.close : unexpected exit !")

    def _flush(self) :
        # 循环处理
        for page in self.__queues.values() :
            # 写入
            self._write_fully(page.offset, page)

    def _load(self) :
        # 清理
        self.__queues.clear()
        # 获得数值
        position = self._get_root(0)
        # 循环处理
        while position != -1 :
            # 读取页面
            page = self._load_page(position, PageType.queue_page)
            # 检查
            if page.identity in self.__queues.keys() :
                raise Exception(f"duplicate identity({page.identity})")
            # 设置偏移量
            position = page.next_page
            # 加入集合
            self.__queues[page.identity] = page

    def create_queue(self, identity) :
        # 检查
        if identity in self.__queues.keys() : return
        # 创建
        page = self.__create_page(identity)
        # 创建
        element = self.__create_element(identity)
        # 设置
        page.size = 1
        page.read_position = element.offset
        page.write_position = element.offset
        # 写入
        self._write_fully(page.offset, page)

    def delete_queue(self, identity) :
        # 检查
        if identity not in self.__queues.keys() : return
        # 获得页面
        page = self.__queues[identity]
        # 加载元素
        element = self._load_page(page.read_position, PageType.queue_element)
        # 循环处理
        while True :
            # 计数器减一
            page.count -= 1; page.size -= 1
            # 释放页面
            self._free_page(element.offset, element.size_type)
            # 检查
            if element.next_page == -1 : break
            # 加载元素
            element = self._load_page(element.next_page, PageType.queue_element)
        # 移除队列
        self.__queues.pop(identity)
        # 注销队列
        self._unregister_root(0, page)
        # 释放队列
        self._free_page(page.offset, page.size_type)

    def read_queue(self, identity) :
        # 检查
        if identity not in self.__queues.keys() :
            raise Exception(f"invalid identity({identity})")
        # 获得页面
        page = self.__queues[identity]
        # 检查
        assert page.read_position != -1
        # 检查
        if page.read_position == page.write_position : return -1
        # 加载元素
        element = self._load_page(page.read_position, PageType.queue_element)
        # 计数器减一
        page.size -= 1; page.count -= 1
        # 设置下一个
        page.read_position = element.next_page
        # 释放
        self._free_page(element.offset, element.size_type)
        # 返回结果
        return element.data_offset

    def write_queue(self, identity, data_offset) :
        # 检查
        if identity not in self.__queues.keys() :
            raise Exception(f"invalid identity({identity})")
        # 获得页面
        page = self.__queues[identity]
        # 检查
        assert page.write_position != -1
        # 加载元素
        element = self._load_page(page.write_position, PageType.queue_element)
        # 检查
        assert element.identity == identity
        # 设置偏移量
        element.data_offset = data_offset
        # 检查
        if element.next_page == -1 :
            # 增加元素
            element = self.__create_element(identity)
            # 计数器加一
            page.size += 1
            # 设置
            element.next_page = element.offset
        # 写入
        self._write_fully(page.write_position, element)
        # 计数器加一
        page.count += 1
        # 设置写位置
        page.write_position = element.next_page

    def clear_queue(self, identity) :
        # 检查
        if identity not in self.__queues.keys() :
            raise Exception(f"invalid identity({identity})")
        # 获得页面
        page = self.__queues[identity]
        # 检查
        assert page.read_position != -1
        # 检查
        while page.read_position != page.write_position :
            # 加载元素
            element = self._load_page(page.read_position, PageType.queue_element)
            # 设置下一个
            page.read_position = element.next_page
            # 计数器减一
            page.count -= 1; page.size -= 1
            # 释放
            self._free_page(element.offset, element.size_type)

    def __create_page(self, identity) :
        # 新建
        page = QueuePageBuffer()
        # 设置
        page.identity = identity
        # 分配页面
        page.offset = self._malloc_page(PageType.queue_page)
        # 检查
        if page.offset == -1 :
            # 追加页面
            page.offset = self._add_page(page)
        else :
            # 写入
            self._write_fully(page.offset, page)
        # 设置
        self.__queues[identity] = page
        # 登记页面
        self._register_root(0, page)
        # 返回结果
        return page

    def __create_element(self, identity, next_page = -1, data_offset = -1) :
        # 新建
        page = QueueElementBuffer()
        # 设置
        page.identity = identity
        # 设置
        page.next_page = next_page
        page.data_offset = data_offset
        # 分配页面
        page.offset = self._malloc_page(PageType.queue_element)
        # 检查
        if page.offset == -1 :
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