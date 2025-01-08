# -*- coding: utf-8 -*-
import os

from widget.ProgressBar import *
from nlp.item.ContentItem import *

class ContentGroup :
    # 初始化对象
    def __init__(self) :
        # Hash表
        self._contents = {}
        # 最大数据长度
        self._max_length = 0

    def __len__(self) :
        # 返回结果
        return len(self._contents)

    def __contains__(self, key) :
        # 返回结果
        return key in self._contents.keys()

    def __getitem__(self, key):
        # 返回结果
        return self._contents[key]

    def __setitem__(self, key, item):
        # 检查参数
        assert isinstance(item, ContentItem)
        # 设置数值
        self._contents[key] = item

    def values(self) :
        # 返回结果
        return self._contents.values()

    # 清理
    def clear(self) :
        # 清理所有数据
        self._contents.clear()

    # 删除元素
    def remove(self, key) :
        # 删除元素
        return self._contents.pop(key, None)

    # 生成新的对象
    def new_item(self, content = None,count = 1) :
        # 返回结果
        return ContentItem(content, count)

    # 最大长度
    @property
    def max_length(self) :
        # 返回结果值
        return self._max_length

    # 复位
    def reset_count(self) :
        # 循环处理
        for item in self._contents.values() : item.reset()

    # 更新
    def update_max_length(self) :
        # 重置最大长度
        self._max_length = 0
        # 执行循环
        for item in self._contents.values() :
            # 检查长度
            if item.length > self._max_length : self._max_length = item.length
        # 返回结果
        return self._max_length

    # 删除计数低于设置的项目
    # 使用尽量少的内存予以处理
    # 在更新计数统计数据之后进行
    def clear_useless(self) :
        # 获得总数
        total = len(self._contents)
        # 进度条
        pb = ProgressBar(total)
        # 打印数据总数
        pb.begin(f"ContentGroup.clear_useless : try to process {total} row(s) !")
        # 结果数据
        contents = {}
        # 检查数据结果
        for (key, item) in self._contents.items() :
            # 进度条
            pb.increase()
            # 检查参数
            if not item.is_useless() : contents[key] = item
        # 设置结果
        self._contents.clear(); self._contents = contents
        # 打印数据总数
        pb.end(f"ContentGroup.clear_useless : {total} row(s) processed !")

    # 删除无效项目
    def clear_invalid(self, max_length = -1) :
        # 获得总数
        total = len(self._contents)
        # 进度条
        pb = ProgressBar(total)
        # 打印数据总数
        pb.begin(f"ContentGroup.clear_invalid : try to process {total} row(s) !")
        # 结果数据
        contents = {}
        # 检查数据结果
        for (key, item) in self._contents.items() :
            # 进度条
            pb.increase()
            # 检查参数
            if item.is_valid(max_length) : contents[key] = item
        # 设置结果
        self._contents.clear(); self._contents = contents
        # 打印数据总数
        pb.end(f"ContentGroup.clear_invalid : {total} row(s) processed !")

    # 带参数，遍历处理
    # 该函数不打印任何信息
    def _traverse(self, function, parameter = None) :
        # 检查数据结果
        for item in self._contents.values() :
            # 检查函数
            # 调用函数处理数据
            if function is not None : function(item, parameter)

    # 带参数，遍历处理
    def traverse(self, function, parameter = None) :
        # 获得总数
        total = len(self._contents)
        # 进度条
        pb = ProgressBar(total)
        # 打印数据总数
        pb.begin(f"ContentGroup.traverse : try to process {total} row(s) !")
        # 检查数据结果
        for item in self._contents.values() :
            # 进度条
            pb.increase()
            # 检查函数
            # 调用函数处理数据
            if function is not None : function(item, parameter)
        # 打印信息
        pb.end(f"ContentGroup.traverse : {total} row(s) processed !")

    def save(self, file_name, sort = False) :
        # 检查文件名
        assert isinstance(file_name, str)
        # 打开文件
        json_file = open(file_name, "w", encoding = "utf-8")
        # 打印信息
        print("ContentGroup.save : file(\"%s\") opened !" % file_name)
        # 检查文件
        assert json_file is not None

        # 获得总数
        total = len(self._contents)
        # 进度条
        pb = ProgressBar(total)
        # 打印数据总数
        pb.begin(f"ContentGroup.save : try to save {total} row(s) !")
        # 将总数写入文件
        json_file.write(str(total))
        json_file.write("\n")
        # 检查标记位
        if not sort :
            # 检查数据结果
            for item in self._contents.values() :
                # 进度条
                pb.increase()
                # 写入文件
                json_file.write(json.dumps(item.json, ensure_ascii = False))
                json_file.write("\n")
        else :
            # 获得列表
            values = sorted(self._contents.values(),
                key = lambda i : i.count, reverse = True)
            # 检查数据结果
            for value in values:
                # 进度条
                pb.increase()
                # 写入文件
                json_file.write(json.dumps(value.json, ensure_ascii = False))
                json_file.write("\n")
        # 打印信息
        pb.end(f"ContentGroup.save : {total} row(s) saved !")
        # 关闭文件
        json_file.close()
        # 打印信息
        print("ContentGroup.save : file(\"%s\") closed !" % file_name)

    # 加载数据
    def load(self, file_name) :
        # 检查文件名
        assert isinstance(file_name, str)
        # 检查文件是否存在
        if not os.path.isfile(file_name):
            # 打印信息
            print("ContentGroup.load : invalid file(\"%s\") !" % file_name)
            return -1
        # 打开文件
        json_file = open(file_name, "r", encoding = "utf-8")
        # 打印信息
        print("ContentGroup.load : file(\"%s\") opened !" % file_name)
        # 检查文件
        assert json_file is not None

        # 进度条
        pb = ProgressBar()
        # 总数
        total = 0

        try:
            # 按行读取
            line = json_file.readline()
            # 循环处理
            while line :
                # 剪裁字符串
                line = line.strip()
                # 检查结果
                if len(line) <= 0:
                    # 读取下一行
                    line = json_file.readline()
                    continue

                # 检查计数器
                if pb.total == 0 :
                    # 获得数据总数
                    total = int(line)
                    # 检查结果
                    if total <= 0 :
                        # 打印信息
                        print("ContentGroup.load : invalid total(\"%s\") !" % line)
                        break
                    # 进度条
                    pb = ProgressBar(total)
                    # 打印数据总数
                    pb.begin(f"ContentGroup.load : try to load {total} row(s) !")
                else:
                    # 生成原始数据对象
                    new_item = self.new_item()
                    # 按照json格式解析
                    new_item.json = json.loads(line)
                    # 计数器加1
                    if pb is not None : pb.increase()
                    # 查询字典
                    if new_item.content not in self :
                        # 加入字典
                        self._contents[new_item.content] = new_item
                # 读取下一行
                line = json_file.readline()
            # 打印信息
            pb.end()
            print("ContentGroup.load : %d line(s) processed !" % pb.count)
        except Exception as e:
            traceback.print_exc()
            print("ContentGroup.load : ", str(e))
            print("ContentGroup.load : unexpected exit !")
        # 关闭文件
        json_file.close()
        # 打印信息
        print("ContentGroup.load : file(\"%s\") closed !" % file_name)
        print("ContentGroup.load : %d item(s) loaded !" % len(self))
        # 更新最大长度
        self.update_max_length()
        # 打印信息
        print("ContentGroup.load : max length(%d) !" % self.max_length)
        return total
