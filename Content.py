# -*- coding: utf-8 -*-

import os
import sys
import json
import heapq
import traceback

from ContentTool import *
from SentenceTool import *

class ContentItem :
    # 初始化对象
    def __init__(self, content = None, count = 1) :
        # 设置来源
        self.count = count
        # 设置内容
        self.content = content

    # 复位
    def reset(self) :
        # 复位数据
        self.count = 0

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "content" : self.content,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        # 检查数据
        #assert self.length == value["length"]

    @property
    def length(self) :
        # 检查参数
        assert isinstance(self.content, str)
        # 返回结果
        return len(self.content)

    @property
    def sha256(self) :
        # 检查参数
        assert isinstance(self.content, str)
        # 返回结果
        return HashTool.sha256(self.content)

    # 无用
    def is_useless(self):
        # 返回结果
        return self.count <= 0

    # 检查有效性
    def is_valid(self, max_length = -1) :
        # 检查参数
        if max_length <= 0 :
            # 返回结果
            return 1 <= len(self.content)
        # 返回结果
        return 1 <= len(self.content) <= max_length

    # 非常用
    def is_rare(self):
        # 返回结果
        return UnicodeTool.is_rare(self.content)

    # 中文
    def is_chinese(self) :
        # 返回结果
        return ChineseTool.is_chinese(self.content)

    def dump(self):
        # 打印信息
        print("ContentItem.dump : show properties !")
        print("\t", end = ""); print("length = %d" % self.length)
        print("\t", end = ""); print("count = %d" % self.count)
        print("\t", end = ""); print("content = \"%s\"" % self.content)
        print("\t", end = ""); print("sha256 = 0x%s" % self.sha256.hexdigest())

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

    # 返回所有键值
    def keys(self) :
        # 返回结果
        return self._contents.keys()

    def items(self):
        # 返回结果
        return self._contents.items()

    def values(self) :
        # 返回结果
        return self._contents.values()

    # 清理
    def clear(self) :
        # 清理所有数据
        self._contents.clear()

    # 生成新的对象
    def new_item(self, content = None) :
        # 返回结果
        return ContentItem(content)

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
        # 清理无效数据
        self._contents = {key : item for (key, item) in self._contents.items() if not item.is_useless()}

    # 删除无效项目
    def clear_invalid(self, max_length = -1) :
        # 清理无效数据
        self._contents = {key : item for (key, item) in self._contents.items() if item.is_valid(max_length)}

    # 遍历处理
    def traverse(self, function) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self._contents)
        # 打印数据总数
        print("ContentGroup.traverse : try to process %d row(s) !" % total)

        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 检查数据结果
        for item in self._contents.values() :
            # 计数器加1
            count = count + 1
            # 检查结果
            if count >= (percent + 1) * one_percent :
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end = "")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end = "")
                sys.stdout.flush()
            # 检查函数
            # 调用函数处理数据
            if function is not None : function(item)
        # 打印数据总数
        print("")
        print("ContentGroup.traverse : %d row(s) processed !" % total)

    def save(self, file_name):
        # 检查文件名
        assert isinstance(file_name, str)
        # 打开文件
        json_file = open(file_name, "w", encoding = "utf-8")
        # 打印信息
        print("ContentGroup.save : file(\"%s\") opened !" % file_name)
        # 检查文件
        assert json_file is not None

        # 计数器
        count = 0
        # 获得总数
        total = len(self._contents)
        # 打印数据总数
        print("ContentGroup.save : try to save %d row(s) !" % total)
        # 将总数写入文件
        json_file.write(str(total))
        json_file.write("\n")

        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 检查数据结果
        for item in self._contents.values() :
            # 计数器加1
            count = count + 1
            # 写入文件
            json_file.write(json.dumps(item.json, ensure_ascii = False))
            json_file.write("\n")
            # 检查结果
            if count >= (percent + 1) * one_percent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end = "")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end = "")
                sys.stdout.flush()
        # 打印数据总数
        print("")
        print("ContentGroup.save : %d row(s) saved !" % total)
        # 关闭文件
        json_file.close()
        # 打印信息
        print("ContentGroup.save : file(\"%s\") closed !" % file_name)

    # 加载数据
    def load(self, file_name):
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

        # 计数器
        count = 0
        # 获得总数
        total = 0
        # 百分之一
        percent = 0
        one_percent = total / 100.0

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

                # 计数器加1
                count = count + 1
                # 检查计数器
                if count == 1:
                    # 获得数据总数
                    total = int(line)
                    # 检查结果
                    if total <= 0 :
                        # 打印信息
                        print("ContentGroup.load : invalid total(\"%s\") !" % line)
                        break
                    # 设置百分之一
                    one_percent = total / 100.0
                    # 打印数据总数
                    print("ContentGroup.load : try to load %d row(s) !" % total)
                else:
                    # 生成原始数据对象
                    new_item = self.new_item()
                    # 按照json格式解析
                    new_item.json = json.loads(line)
                    # 查询字典
                    if new_item.content not in self :
                        # 加入字典
                        self._contents[new_item.content] = new_item
                    # 检查结果
                    if (count - 1) >= (percent + 1) * one_percent:
                        # 增加百分之一
                        percent = percent + 1
                        # 打印进度条
                        print("\r", end = "")
                        print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end = "")
                        sys.stdout.flush()
                # 读取下一行
                line = json_file.readline()
            # 打印信息
            print("")
            print("ContentGroup.load : %d line(s) processed !" % count)
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

class RawItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None, source = None):
        # 设置来源
        self.source = source
        # 调用父类初始化
        super().__init__(content)

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "length" : self.length,
                "source" : self.source,
                "content" : self.content,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.content = value["content"]
        # 检查参数
        if "source" in value :
            self.source = value["source"]
        #assert self.length == value["length"]

    def dump(self):
        # 打印信息
        print("RawItem.dump : show properties !")
        print("\t", end = ""); print("count = %d" % self.count)
        print("\t", end = ""); print("length = %d" % self.length)
        print("\t", end = ""); print("content = \"%s\"" % self.content)
        print("\t", end = ""); print("source = \"%s\"" % self.source)
        print("\t", end = ""); print("sha256 = 0x%s" % self.sha256.hexdigest())

class RawContent(ContentGroup) :
    # 生成新的对象
    def new_item(self, content = None) :
        # 返回结果
        return RawItem(content)

    # 增加项目
    # 用于traverse函数调用
    def add_content(self, content):
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_content(RawItem(content))

    # 增加项目
    # 用于traverse函数调用
    def add_item(self, item):
        # 检查参数
        assert isinstance(item, ContentItem)
        # 获得内容
        content = item.content
        # 检查字典
        if content in self:
            # 增加计数
            self[content].count += item.count; return
        # 增加项目
        self[content] = RawItem(item.content, item.source); self[content].count = item.count

class TokenItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None) :
        # 调用父类初始化
        super().__init__(content)
        # 检查参数
        if content is not None :
            assert len(content) == 1

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "content" : self.content,
                "unicode" : ord(self.content),
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        # 检查参数
        assert ord(self.content) == value["unicode"]

    def dump(self):
        # 打印信息
        print("TokenItem.dump : show properties !")
        print("\t", end = ""); print("count = %d" % self.count)
        print("\t", end = ""); print("token = \'%c\'" % self.content)
        print("\t", end = ""); print("unicode = 0x%4X" % ord(self.content))
        print("\t", end = ""); print("remark = \"%s\"" % UnicodeTool.get_remark(self.content))

class TokenContent(ContentGroup) :
    # 生成新的对象
    def new_item(self, content = None) :
        # 返回结果
        return TokenItem(content)

    # 增加项目
    # 用于traverse函数调用
    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_item(TokenItem(content))

    # 增加项目
    # 用于traverse函数调用
    def add_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 扫描结果
        for token in item.content :
            # 检查字典
            if token in self :
                # 增加计数器
                self[token].count += item.count; continue
            # 增加字典内容
            self[token] = TokenItem(token); self[token].count = item.count

    # 计算Gamma值
    def get_gamma(self, content, count = 1) :
        # 检查参数
        assert count >= 0
        assert isinstance(content, str)
        # Gamma数值
        gamma = 0.0
        # 循环处理
        for token in content :
            # 检查字典
            if not token in self : return -1.0
            # 检查结果
            if self[token].count <= 0 : return -1.0
            # 计算结果
            gamma += 1.0 / float(self[token].count)
        # 返回结果
        return gamma * float(count) / float(len(content))

class DictionaryItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None) :
        # 来源与注释
        # source : remark
        self.sources = {}
        # 调用父类初始化函数
        super().__init__(content)

    # 是否为其来源
    def has_source(self, source) :
        # 检查参数
        assert isinstance(source, str)
        # 返回结果
        return source in self.sources.keys()

    # 增加来源
    def add_source(self, source, remark) :
        # 检查参数
        assert isinstance(source, str)
        # 检查数据
        if source not in self.sources.keys() : self.sources[source] = remark

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "content" : self.content,
                "sources" : self.sources,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        # 检查参数
        if "sources" in value :
            self.sources = value["sources"]
        #assert self.length == value["length"]

    # 打印信息
    def dump(self):
        # 打印信息
        print("DictionaryItem.dump : show properties !")
        print("\t", end = ""); print("length = %d" % len(self.content))
        print("\t", end = ""); print("count = %d" % self.count)
        print("\t", end = ""); print("content = \"%s\"" % self.content)
        print("\t", end = ""); print("sources = " + str(self.sources))
        print("\t", end = ""); print("sha256 = 0x%s" % self.sha256.hexdigest())

class DictionaryContent(ContentGroup) :
    # 初始化对象
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 是否需要切分
        self.need_split = True

    # 新对象
    def new_item(self, content = None) :
        # 返回结果
        return DictionaryItem(content)

    # 增加项目
    # 用于traverse函数
    def count_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.count_item(ContentItem(content))

    # 增加项目
    # 用于traverse函数
    def count_item(self, item):
        # 检查参数
        assert isinstance(item, ContentItem)
        # 生成内容
        segments = ['$' + item.content]
        # 检查标志位
        if self.need_split :
            # 拆分内容
            segments = SplitTool.split(item.content)
        # 循环处理
        for segment in segments :
            # 检查结果
            if segment[0] != '$' : continue
            # 获得内容
            content = segment[1 : ]
            # 循环处理
            for i in range(len(content)) :
                # 循环处理
                for length in range(1, 1 + self.max_length) :
                    # 长度限定在当前长度
                    if i + length > len(content) : break
                    # 获得子字符串
                    value = content[i : i + length]
                    # 检查结果
                    if value in self : self[value].count += item.count

    # 加载数据
    @staticmethod
    def load_dict(file_name) :
        # 检查文件名
        assert isinstance(file_name, str)
        # 检查文件是否存在
        if not os.path.isfile(file_name):
            # 打印信息
            print("DictionaryContent.load_dict : invalid file(\"%s\") !" % file_name)
            return -1
        # 打开文件
        json_file = open(file_name, "r", encoding = "utf-8")
        # 打印信息
        print("DictionaryContent.load_dict : file(\"%s\") opened !" % file_name)
        # 检查文件
        assert json_file is not None

        # 计数器
        count = 0
        # 获得总数
        total = 0
        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 创建对象
        dictionary = DictionaryContent()

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

                # 计数器加1
                count = count + 1
                # 检查计数器
                if count == 1:
                    # 获得数据总数
                    total = int(line)
                    # 检查结果
                    if total <= 0 :
                        # 打印信息
                        print("DictionaryContent.load_dict : invalid total(\"%s\") !" % line)
                        break
                    # 设置百分之一
                    one_percent = total / 100.0
                    # 打印数据总数
                    print("DictionaryContent.load_dict : try to load %d row(s) !" % total)
                else:
                    # 按照json格式解析
                    item = json.loads(line)
                    # 获得内容
                    content = item["content"]
                    # 检查数据
                    if content not in dictionary :
                        # 生成数据对象
                        new_item = dictionary.new_item(content)
                        # 设置计数
                        new_item.count = item["count"]
                        # 设置来源
                        new_item.add_source(item["source"], item["remark"])
                        # 设置数据对象
                        dictionary[content] = new_item
                    else :
                        # 检查来源
                        if isinstance(item["source"], str) :
                            # 增加来源
                            dictionary[content].add_source(item["source"], item["remark"])

                    # 检查结果
                    if (count - 1) >= (percent + 1) * one_percent:
                        # 增加百分之一
                        percent = percent + 1
                        # 打印进度条
                        print("\r", end = "")
                        print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end = "")
                        sys.stdout.flush()
                # 读取下一行
                line = json_file.readline()
            # 打印信息
            print("")
            print("DictionaryContent.load_dict : %d line(s) processed !" % count)
        except Exception as e:
            traceback.print_exc()
            print("DictionaryContent.load_dict : ", str(e))
            print("DictionaryContent.load_dict : unexpected exit !")
        # 关闭文件
        json_file.close()
        # 打印信息
        print("DictionaryContent.load_dict : file(\"%s\") closed !" % file_name)
        print("DictionaryContent.load_dict : %d item(s) loaded !" % len(dictionary))
        # 更新数据
        dictionary.update_max_length()
        # 打印信息
        print("DictionaryContent.load_dict : max length(%d) !" % dictionary.max_length)
        return dictionary

class SegmentItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None, source = None) :
        # 来源
        self.sources = []
        # 调用父类初始化函数
        super().__init__(content)
        # 检查参数
        if isinstance(source, str) : self.sources.append(source)

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "content" : self.content,
                "sources" : self.sources,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        # 检查参数
        if "sources" in value :
            self.sources = value["sources"]
        #assert self.length == value["length"]

    # 是否为其来源
    def has_source(self, source) :
        # 检查参数
        assert isinstance(source, str)
        # 返回结果
        return source in self.sources

    # 增加来源
    def add_source(self, source) :
        # 检查参数
        assert isinstance(source, str)
        # 检查参数
        if source not in self.sources : self.sources.append(source)

    # 打印信息
    def dump(self):
        # 打印信息
        print("SegmentItem.dump : show properties !")
        print("\t", end = ""); print("length = %d" % len(self.content))
        print("\t", end = ""); print("count = %d" % self.count)
        print("\t", end = ""); print("content = \"%s\"" % self.content)
        print("\t", end = ""); print("sources = " + str(self.sources))
        print("\t", end = ""); print("sha256 = 0x%s" % self.sha256.hexdigest())

class SegmentContent(ContentGroup) :
    # 新对象
    def new_item(self, content = None) :
        # 返回结果
        return SegmentItem(content)

    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_content(SegmentItem(content))

    def add_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 拆分内容
        segments = SplitTool.split(item.content)
        # 循环处理
        for segment in segments :
            # 检查结果
            if segment[0] != '$' : continue
            # 获得内容
            content = segment[1 : ]
            # 检查结果
            if content in self :
                # 获得元素
                element = self[content]
                # 增加计数
                element.count += item.count
                # 检查来源
                if isinstance(item.source, str) : element.add_source(item.source)

            else :
                # 增加项目
                self[content] = SegmentItem(content, item.source); self[content].count = item.count

class WordItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None) :
        # 调用父类初始化函数
        super().__init__(content)

    def dump(self):
        # 打印信息
        print("WordItem.dump : show properties !")
        print("\t", end = ""); print("length = %d" % self.length)
        print("\t", end = ""); print("count = %d" % self.count)
        print("\t", end = ""); print("content = \"%s\"" % self.content)
        print("\t", end = ""); print("sha256 = 0x%s" % self.sha256.hexdigest())

class WordContent(ContentGroup) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 当前长度
        self.limit_length = 1
        # 输入内容时，是否需要分割
        self.need_split = True

    # 新对象
    def new_item(self, content = None) :
        # 返回结果
        return WordItem(content)

    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_item(WordItem(content))

    def add_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 生成内容
        segments = ['$' + item.content]
        # 检查标志位
        if self.need_split :
            # 拆分内容
            segments = SplitTool.split(item.content)
        # 循环处理
        for segment in segments :
            # 检查结果
            if segment[0] != '$' : continue
            # 获得内容
            content = segment[1 : ]
            # 循环处理
            for i in range(len(content)) :
                # 长度限定在当前长度
                if i + self.limit_length > len(content) : break
                # 获得单词
                word = content[i : i + self.limit_length]
                # 检查结果
                if word in self :
                    # 增加计数器
                    self[word].count += item.count; continue
                # 检查是否为中文
                # 如果是纯中文内容，则增加数据项
                if ChineseTool.is_chinese(word) :
                    # 增加项目
                    self[word] = WordItem(word); self[word].count = item.count

class SentenceItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None, source = None) :
        # 设置参数
        self.source = source
        # 调用父类初始化函数
        super().__init__(content)

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "source" : self.source,
                "content" : self.content,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        # 检查参数
        if "source" in value :
            self.source = value["source"]
        #assert self.length == value["length"]

    # 打印信息
    def dump(self):
        # 打印信息
        print("SentenceItem.dump : show properties !")
        print("\t", end = ""); print("count = %d" % self.count)
        print("\t", end = ""); print("length = %d" % self.length)
        print("\t", end = ""); print("source = \"%s\"" % self.source)
        print("\t", end = ""); print("content = \"%s\"" % self.content)
        print("\t", end = ""); print("sha256 = 0x%s" % self.sha256.hexdigest())

class SentenceContent(ContentGroup) :
    # 新对象
    def new_item(self, content = None) :
        # 返回结果
        return SentenceItem(content)

    # 提取句子
    # 用于traverse函数
    def extract_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 提取句子
        self.extract_item(SentenceItem(content))

    # 提取句子
    # 用于traverse函数
    def extract_data(self, data) :
        # 检查参数
        assert isinstance(data, dict)
        # 提取句子
        self.extract_content(SentenceItem(data["content"]))

    # 提取句子
    # 用于traverse函数
    def extract_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 提取句子
        sentences = SentenceTemplate.extract(item.content)
        # 循环处理f
        for sentence in sentences:
            # 检查数据是否存在
            if sentence in self:
                # 计数器增加
                self[sentence].count += item.count; continue
            # 加入字典
            self[sentence] = SentenceItem(sentence, item.source); self[sentence].count = item.count

class CoreItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None) :
        # 调用父类初始化函数
        super().__init__(content)
        # 只选取最大gamma值的分解模式
        # 设置最大值
        self.gamma = 0.0
        # 设置分解模式
        self.pattern = None

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "length" : self.length,
                "content" : self.content,
                "gamma" : self.gamma,
                "pattern" : self.pattern,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self.content = value["content"]
        # 检查数据
        if "gamma" in value :
            self.gamma = value["gamma"]
        if "pattern" in value :
            self.pattern = value["pattern"]
        # 检查参数
        #assert self.length == value["length"]

    def is_valid(self, max_length = -1) :
        # 返回结果
        if self.count <= 1 : return False
        if self.length <= 0 : return False
        if self.gamma < 0.00001 : return False
        if self.length > 1 and self.pattern is None : return False
        if self.length == 1 and self.pattern is not None : return False
        # 返回结果
        return Ture if max_length <= 0 else self.length <= max_length

    def dump(self):
        # 打印信息
        print("WordItem.dump : show properties !")
        print("\t", end = ""); print("length = %d" % self.length)
        print("\t", end = ""); print("count = %d" % self.count)
        print("\t", end = ""); print("content = \"%s\"" % self.content)
        print("\t", end = ""); print("gamma = %f" % self.gamma)
        print("\t", end = ""); print("pattern =\"%s\"" % self.pattern)
        print("\t", end = ""); print("sha256 = 0x%s" % self.sha256.hexdigest())

    # 更新Gamma数值
    def update_gamma(self, cores) :
        # 检查参数
        assert isinstance(cores, CoreContent)
        # 长度小于1，则返回空
        if self.length < 1 : return
        # 长度为1，则设置gamma为1.0
        if self.length == 1 : self.gamma = 1.0; return
        # 已更新过的内容，则不再更新
        if self.gamma > 0 and self.pattern is not None : return

        # 结果
        gammas = {}
        # 循环处理
        for i in range(1, len(self.content)) :
            # 获得gamma数值
            gamma = cores.get_gamma([self.content[0:i], self.content[i:]])
            # 检查结果
            if gamma <= 0 : continue
            # 移动分隔符
            gammas[self.content[0:i] + '|' + self.content[i:]] = gamma
        # 循环处理
        for i in range(1, len(self.content)) :
            for j in range(i + 1, len(self.content)) :
                # 部分
                gamma = cores.get_gamma([self.content[0:i], self.content[i:j], self.content[j:]])
                # 检查结果
                if gamma <= 0 : continue
                # 移动分隔符
                gammas[self.content[0:i] + '|' + self.content[i:j] + '|' + self.content[j:]] = gamma
        # 循环处理
        for i in range(1, len(self.content)) :
            for j in range(i + 1, len(self.content)) :
                for k in range(j + 1, len(self.content)) :
                    # 部分
                    gamma = cores.get_gamma([self.content[0:i], self.content[i:j], self.content[j:k], self.content[k:]])
                    # 检查结果
                    if gamma <= 0 : continue
                    # 移动分隔符
                    gammas[self.content[0:i] + '|' + self.content[i:j] + '|' + self.content[j:k] + '|' + self.content[k:]] = gamma
        # 排序
        self.gamma = 0.0
        # 循环处理
        # 选择Gamma值最大的一组数据
        for (key, value) in gammas.items() :
            # 检查结果
            if value > self.gamma : self.gamma = value; self.pattern = key

class CoreContent(ContentGroup) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 输入内容时，是否需要分割
        self.need_split = True

    # 新对象
    def new_item(self, content = None) :
        # 返回结果
        return CoreItem(content)

    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_item(CoreItem(content))

    def add_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 检查结果
        if item.content not in self :
            # 检查是否为中文
            # 如果是纯中文内容，则增加数据项
            if item.is_chinese() : self[item.content] = item

    # 增加项目
    # 用于traverse函数
    def count_item(self, item):
        # 检查参数
        assert isinstance(item, ContentItem)
        # 生成内容
        segments = ['$' + item.content]
        # 检查标志位
        if self.need_split :
            # 拆分内容
            segments = SplitTool.split(item.content)
        # 循环处理
        for segment in segments :
            # 检查结果
            if segment[0] != '$' : continue
            # 获得内容
            content = segment[1 : ]
            # 循环处理
            for i in range(len(content)) :
                # 循环处理
                for length in range(1, 1 + self.max_length) :
                    # 长度限定在当前长度
                    if i + length > len(content) : break
                    # 获得子字符串
                    value = content[i : i + length]
                    # 检查结果
                    if value in self : self[value].count += item.count

    def get_gamma(self, segments) :
        # 检查参数
        assert isinstance(segments, list)
        # Gamma数值
        gamma = 0.0
        # 内容
        content = ""
        # 循环处理
        for segment in segments :
            # 增加字符
            content += segment
            # 检查字典
            if segment not in self : return -1.0
            # 获得计数
            count = self[segment].count
            # 检查结果
            if count <= 0 : return -1.0
            # 计算结果
            gamma += 1.0 / float(count)
        # 计算总值
        if not content in self : return 0.0
        # 返回结果
        return gamma * float(self[content].count) / float(len(segments))

    # 更新Gamma数值
    def update_gammas(self) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self)
        # 打印数据总数
        print("CoreContent.update_gammas : try to update %d row(s) !" % total)

        # 指定长度
        length = 1
        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 循环处理
        while count < total :
            # 打印信息
            print("CoreContent.update_gammas : try to process !")
            print("\t", end = ""); print("length = %d" % length)
            # 循环处理
            for item in self._contents.values() :
                # 检查长度
                if item.length != length : continue
                # 计数器加1
                count = count + 1
                # 复位数据
                item.gamma = 0.0
                item.pattern = None
                # 检查长度
                if item.length == 1 :
                    # 直接设定
                    item.gamma = 1.0
                    item.pattern = None
                else :
                    # 重置
                    item.gamma = 0.0
                    item.pattern = None
                    # 更新数值
                    item.update_gamma(self)
            # 长度加一
            length += 1
            # 检查结果
            if count >= (percent + 1) * one_percent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end = "")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end = "")
                sys.stdout.flush()
            # 打印信息
            print("")
            print("CoreContent.update_gammas : length(%d) processed !" % length)
        # 打印数据总数
        print("")
        print("CoreContent.update_gammas : %d row(s) updated !" % total)

class HuffmanNode :
    # 初始化
    def __init__(self, symbol = None, frequency = None) :
        # 设置参数
        self.symbol = symbol
        self.frequency = frequency
        # 子节点
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

class HuffmanTree :
    # 初始化
    def __init__(self) :
        # 设置初始值
        self.__heap = []
        self.__codes = {}

    def __len__(self) :
        # 返回结果
        return len(self.__codes)

    def __contains__(self, word) :
        # 检查参数
        assert isinstance(word, str)
        # 返回结果
        return word in self.__codes.keys()

    def __getitem__(self, word):
        # 检查参数
        assert isinstance(word, str)
        # 返回结果
        return self.__codes[word]

    # 压栈
    def push(self, symbol, frequency) :
        # 检查参数
        assert isinstance(symbol, str)
        assert isinstance(frequency, int)
        # 生成项目并压入
        self.push_item(ContentItem(symbol, frequency))

    # 压栈
    def push_item(self, item) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 压栈
        heapq.heappush(self.__heap, HuffmanNode(item.content, item.count))

    # 创建
    def build(self) :
        # 循环处理
        while len(self.__heap) > 1 :
            left = heapq.heappop(self.__heap)
            right = heapq.heappop(self.__heap)
            top = HuffmanNode(frequency = left.frequency + right.frequency)
            top.left = left
            top.right = right
            heapq.heappush(self.__heap, top)
        # 清理编码树
        self.__codes.clear()
        # 生成编码树
        self.__generate_codes__(self.__heap[0])
        # 返回结果
        return self.__heap[0]

    # 生成编码
    def __generate_codes__(self, node, code = '') :
        if node is not None :
            if node.symbol is not None :
                self.__codes[node.symbol] = code
            self.__generate_codes__(node.left, code + '0')
            self.__generate_codes__(node.right, code + '1')

    def dump(self) :
        # 打印信息
        print("Content.HuffmanTree : show codes !")
        print("\t", end = ""); print("total = %d" % len(self.__codes))
        # 循环处理
        for (symbol, code) in self.__codes.items() :
            print(f"\tcharacter(code) = \'{symbol}\'({code})")
