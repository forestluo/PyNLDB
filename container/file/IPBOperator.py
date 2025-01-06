# -*- coding: utf-8 -*-

from container.file.ValueEnum import *
from container.file.FPBOperator import *
from container.file.RPBOperator import *

class IPBOperator(FPBOperator, RPBOperator) :
    # 最大层数
    max_level = 8

    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 索引集合
        self.__indexes = {}

    def close(self) :
        try :
            # 写入
            IPBOperator._flush(self)
        except Exception as ex :
            traceback.print_exc()
            print("IPBOperator.close : ", str(ex))
            print("IPBOperator.close : unexpected exit !")

    def _flush(self) :
        # 循环处理
        for page in self.__indexes.values() :
            # 写入
            self._write_fully(page.offset, page)

    def _load(self) :
        # 清理项目
        self.__indexes.clear()
        # 获得数值
        offset = self._get_root(1)
        # 循环处理
        while offset != -1 :
            # 读取页面
            page = self._load_page(offset, PageType.index_page)
            # 检查
            if page.identity in self.__indexes.keys() :
                raise Exception(f"duplicate identity({page.identity})")
            # 设置偏移量
            offset = page.next_page
            # 加入集合
            self.__indexes[page.identity] = page

    def index_count(self, identity) :
        # 检查
        if identity not in self.__indexes.keys() : return None
        # 返回结果
        return self.__indexes[identity].count

    def create_index(self, identity) :
        # 检查
        if identity in self.__indexes.keys() : return
        # 新建
        page = IndexPageBuffer()
        # 设置
        page.identity = identity
        # 分配页面
        page.offset = self._malloc_page(PageType.index_page)
        # 检查
        if page.offset == -1 :
            # 追加页面
            page.offset = self._add_page(page)
        else :
            # 写入
            self._write_fully(page.offset, page)
        # 设置
        self.__indexes[identity] = page
        # 登记页面
        self._register_root(1, page)

    def __load_index_data(self, offset, data) :
        # 创建
        buffer = BytesBuffer(IndexData.size)
        # 读取
        self._read_buffer(offset + data.offset, buffer)
        # 解包
        data.unwrap(buffer)
        # 检查
        data.check_valid(self.data_size)

    def __save_index_data(self, offset, data) :
        # 检查
        data.check_valid(self.data_size)
        # 创建
        buffer = BytesBuffer(IndexData.size)
        # 解包
        data.wrap(buffer)
        # 写入
        self._write_buffer(offset + data.offset, buffer)

    def load_index(self, identity, key) :
        # 转换关键字
        key = IndexTool.md5(key)
        # 检查
        if identity not in self.__indexes.keys() :
            raise Exception(f"invalid identity({identity})")
        # 获得页面
        page = self.__indexes[identity]
        # 获得子节点
        data = page[key]
        # 检查
        if data.has_key(key) :
            # 返回结果
            return data.data_value
        # 检查子节点
        if data.subnode_offset == -1 : return None

        # 临时变量
        level = 0
        # 子节点偏移量
        subnode_offset = data.subnode_offset
        # 检查子节点
        PageOffset.check_offset(subnode_offset, self.data_size)
        # 循环处理
        while True :
            # 检查
            if subnode_offset == -1 : break
            # 创建
            data = IndexData()
            # 设置偏移量
            data.offset = IndexTool.get_data_offset(key, level)
            # 加载数据
            self.__load_index_data(subnode_offset, data)
            # 检查
            if data.has_key(key) :
                # 返回结果值
                return data.data_value
            # 设置
            subnode_offset = data.subnode_offset; level += 1
            # 检查
            if level > IPBOperator.max_level :
                raise Exception(f"index level overflowed({level})")
            # 检查子节点
            PageOffset.check_offset(subnode_offset, self.data_size)
        # 返回结果
        return None

    def __delete_element(self, element) :
        # 循环处理
        for data in element.datas :
            # 获得子节点偏移量
            subnode_offset = data.subnode_offset
            # 检查
            if subnode_offset == -1 : continue
            # 加载数据
            _element = self._load_page(subnode_offset, PageType.index_element)
            # 递归处理
            self.__delete_element(_element)
        # 释放自身
        self._free_page(element.offset, element.size_type)

    def __create_element(self, identity, key, data_value, level = 0) :
        # 获得尺寸
        size_type = IndexTool.get_size_type(level)
        # 新建
        page = IndexElementBuffer(size_type)
        # 设置
        page.identity = identity
        # 设置数据
        data = page[key]; data.key = key; data.data_value = data_value
        # 分配页面
        page.offset = self._malloc_page(PageType.index_element, size_type)
        # 检查
        if page.offset == -1 :
            # 追加页面
            page.offset = self._add_page(page)
        else :
            # 写入
            self._write_fully(page.offset, page)
        # 返回结果
        return page

    def _delete_index(self, identity) :
        # 获得页面
        page = self.__indexes[identity]
        # 循环处理
        for data in page.datas :
            # 获得子节点偏移量
            subnode_offset = data.subnode_offset
            # 检查
            if subnode_offset == -1 : continue
            # 加载数据
            element = self._load_page(subnode_offset, PageType.index_element)
            # 递归处理
            self.__delete_element(element)
        # 移除队列
        self.__indexes.pop(identity)
        # 注销队列
        self._unregister_root(1, page)
        # 释放队列
        self._free_page(page.offset, page.size_type)

    def delete_index(self, identity, key = None) :
        # 检查
        if key is None :
            self._delete_index(identity); return None
        # 转换关键字
        key = IndexTool.md5(key)
        # 检查
        if identity not in self.__indexes.keys() : return None
        # 获得页面
        page = self.__indexes[identity]
        # 获得子节点
        data = page[key]
        # 检查
        if data.has_key(key) :
            # 计数器
            page.count -= 1
            # 设置
            data.key = None
            # 写入
            self.__save_index_data(page.offset, data)
            # 返回结果
            return data.data_value
        # 检查子节点
        if data.subnode_offset == -1 : return None

        # 临时变量
        level = 0
        # 子节点偏移量
        subnode_offset = data.subnode_offset
        # 检查子节点
        PageOffset.check_offset(subnode_offset, self.data_size)
        # 循环处理
        while True :
            # 检查
            if subnode_offset == -1 : break
            # 创建
            data = IndexData()
            # 设置偏移量
            data.offset = IndexTool.get_data_offset(key, level)
            # 加载数据
            self.__load_index_data(subnode_offset, data)
            # 检查
            if data.has_key(key) :
                # 计数器
                page.count -= 1
                # 设置
                data.key = None
                # 写入
                # 不做空间结构优化处理
                # 如有需要，可以删除重建
                self.__save_index_data(subnode_offset, data)
                # 返回结果值
                return data.data_value
            # 设置
            subnode_offset = data.subnode_offset; level += 1
            # 检查
            if level > IPBOperator.max_level :
                raise Exception(f"index level overflowed({level})")
            # 检查子节点
            PageOffset.check_offset(subnode_offset, self.data_size)
        # 返回结果
        return None

    def save_index(self, identity, key, data_value) :
        # 转换关键字
        key = IndexTool.md5(key)
        # 检查
        if identity not in self.__indexes.keys() :
            raise Exception(f"invalid identity({identity})")
        # 获得页面
        page = self.__indexes[identity]
        # 获得子节点
        data = page[key]
        # 临时变量
        saved_flag = False
        # 检查
        # 没有实质数据，可以占用
        if data.has_key(key) :
            # 保留数据
            _data_value = data.data_value
            # 设置数据
            data.data_value = data_value
            # 写入
            self.__save_index_data(page.offset, data)
            # 返回结果
            return _data_value
        elif not data.valid :
            # 计数器
            page.count += 1
            # 设置标志位
            saved_flag = True
            # 设置新数值
            data.key = key
            data.data_value = data_value
            # 写入
            self.__save_index_data(page.offset, data)
        # 数据不匹配，但无存储的子节点
        elif data.subnode_offset == -1 :
            # 创建元素
            element = self.__create_element \
                (identity, key, data_value)
            # 计数器
            page.count += 1
            page.size += len(element.datas)
            # 设置新数值
            data.subnode_offset = element.offset
            # 写入
            self.__save_index_data(page.offset, data); return None

        # 临时变量
        level = 0
        _data_value = None
        # 临时变量
        subnode_offset = data.subnode_offset
        # 检查子节点
        PageOffset.check_offset(subnode_offset, self.data_size)
        # 循环处理
        while True :
            # 检查
            if subnode_offset == -1 : break
            # 创建
            data = IndexData()
            # 设置偏移量
            data.offset = IndexTool.get_data_offset(key, level)
            # 加载数据
            self.__load_index_data(subnode_offset, data)
            # 检查
            if data.has_key(key) :
                # 保留数据
                _data_value = data.data_value
                # 检查标志位
                if saved_flag :
                    # 计数器
                    page.count -= 1
                    # 设置数据
                    data.key = None
                    data.data_value = -1
                else :
                    # 设置数据
                    data.data_value = data_value
                # 写入
                self.__save_index_data(subnode_offset, data); break
            elif not data.valid :
                # 检查标志位
                if not saved_flag :
                    # 计数器
                    page.count += 1
                    # 设置标志位
                    saved_flag = True
                    # 设置新数值
                    data.key = key
                    data.data_value = data_value
                    # 写入
                    self.__save_index_data(subnode_offset, data)
            elif data.subnode_offset == -1 :
                # 检查标志位
                if saved_flag : break
                # 创建元素
                element = self.__create_element \
                    (identity, key, data_value, level + 1)
                # 计数器
                page.count += 1
                page.size += len(element.datas)
                # 设置新数值
                data.subnode_offset = element.offset
                # 写入
                self.__save_index_data(subnode_offset, data); break
            # 设置
            subnode_offset = data.subnode_offset; level += 1
            # 检查
            if level > IPBOperator.max_level :
                raise Exception(f"index level overflowed({level})")
            # 检查子节点
            PageOffset.check_offset(subnode_offset, self.data_size)
        # 返回结果
        return _data_value

    def dump(self) :
        print(f"IPBOperator.dump : show properties !")
        # 循环处理
        for page in self.__indexes.values() : page.dump()