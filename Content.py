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
        self._content = content

    @property
    def content(self) :
        # 返回结果
        return self._content

    @content.setter
    def content(self, value) :
        #设置参数
        self._content = value

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "content" : self._content,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self._content = value["content"]

    @property
    def length(self) :
        # 检查参数
        assert isinstance(self._content, str)
        # 返回结果
        return len(self._content)

    @property
    def sha256(self) :
        # 检查参数
        assert isinstance(self._content, str)
        # 返回结果
        return HashTool.sha256(self._content)

    # 检查有效性
    def is_valid(self, max_length) :
        # 返回结果
        return 1 <= len(self.content) <= max_length

    # 无用
    def is_useless(self):
        # 返回结果
        return self.count <= 1

    # 非常用
    def is_rare(self):
        # 返回结果
        return UnicodeTool.is_rare(self._content)

    # 中文
    def is_chinese(self) :
        # 返回结果
        return ChineseTool.is_chinese(self._content)

    def dump(self):
        # 打印信息
        print("ContentItem.dump : show properties !")
        print("\t"); print("length = %d" % self.length)
        print("\t"); print("count = %d" % self.count)
        print("\t"); print("sha256 = 0x%s" % self.sha256.hexdigest())
        print("\t"); print("content = \"%s\"" % self._content)
        
class ContentGroup :
    # 初始化对象
    def __init__(self) :
        # Hash表
        self._contents = {}
        # 设置标志位
        self._use_sha256 = False

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

    # 清理
    def clear(self) :
        # 清理所有数据
        self._contents.clear()

    # 生成新的对象
    def new_item(self) :
        # 返回结果
        return ContentItem()

    # 获得指定长度项目
    def get_items(self, length = -1) :
        # 检查参数
        assert isinstance(length, int)
        # 检查长度
        if length <= 0 :
            # 返回结果
            return [item for item in self._contents.values()]
        # 返回结果
        return [item for item in self._contents.values() if item.length == length]

    # 删除计数低于设置的项目
    # 使用尽量少的内存予以处理
    # 在更新计数统计数据之后进行
    def clear_useless(self) :
        # 清理无效数据
        self._contents = {key : item for (key, item) in self._contents.items() if not item.is_useless()}

    # 删除无效项目
    def _clear_invalid(self, max_length) :
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
            if function is not None: function(item)
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
    def load(self, file_name, neglect_count = False):
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
                    # 检查标志位
                    if neglect_count : new_item.count = 1

                    # 检查标志位
                    if self._use_sha256 :
                        # 获得哈希
                        sha256 = new_item.sha256
                        # 查询字典
                        if sha256 not in self :
                            # 加入字典
                            self._contents[sha256] = new_item
                    else :
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
        print("ContentGroup.load : %d item(s) loaded !" % len(self))
        print("ContentGroup.load : file(\"%s\") closed !" % file_name)
        return total

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
        print("\t"); print("total = %d" % len(self.__codes))
        # 循环处理
        for (symbol, code) in self.__codes.items() :
            print(f"\tcharacter(code) = \'{symbol}\'({code})")

class TokenItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None) :
        # 调用父类初始化
        super().__init__(content)
        # 检查参数
        if content is not None :
            assert len(content) == 1

    @property
    def content(self) :
        # 返回结果
        return self.content

    @content.setter
    def content(self, value) :
        # 检查参数
        if value is not None :
            assert len(value) == 1
        # 设置参数
        self.content = value

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "content" : self._content,
                "unicode" : ord(self._content),
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self._content = value["content"]

    def dump(self):
        # 打印信息
        print("TokenItem.dump : show properties !")
        print("\t"); print("count = %d" % self.count)
        print("\t"); print("token = \'%c\'" % self.content)
        print("\t"); print("unicode = 0x%4X" % ord(self.content))
        print("\t"); print("remark = \"%s\"" % UnicodeTool.get_remark(self.content))

class TokenContent(ContentGroup) :
    # 生成新的对象
    def new_item(self) :
        # 返回结果
        return TokenItem()

    # 增加项目
    # 用于traverse函数调用
    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_item(TokenItem(item.content))

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
                self[token].count += item.count; return
            # 增加字典内容
            self[token] = TokenItem(token); self[token].count = item.count

    # 计算Gamma值
    def get_gamma(self, tokens) :
        # 检查参数
        assert isinstance(tokens, list)
        # Gamma数值
        gamma = 0.0
        # 内容
        content = ""
        # 循环处理
        for token in tokens :
            # 增加字符
            content += token
            # 检查字典
            if not token in self : return -1.0
            # 获得计数
            count = self[token].count
            # 检查结果
            if count <= 0 : return -1.0
            # 计算结果
            gamma += 1.0 / float(count)
        # 计算总值
        if not content in self : return 0.0
        # 返回结果
        return gamma * float(self[content].count) / float(len(tokens))

class RawItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None, source = None):
        # 调用父类初始化
        super().__init__(content)
        # 设置来源
        self.source = source

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "source" : self.source,
                "content" : self._content,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.source = value["source"]
        self._content = value["content"]

    def dump(self):
        # 打印信息
        print("RawItem.dump : show properties !")
        print("\t"); print("count = %d" % self.count)
        print("\t"); print("length = %d" % self.length)
        print("\t"); print("content = \"%s\"" % self.content)
        print("\t"); print("sha256 = 0x%s" % self.sha256.hexdigest())
        print("\t"); print("source = \"%s\"" % self.source)

class RawContent(ContentGroup) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化
        super().__init__()
        # 设置标志位
        self._use_sha256 = True

    # 生成新的对象
    def new_item(self) :
        # 返回结果
        return RawItem()

    # 增加项目
    # 用于traverse函数调用
    def add_content(self, content):
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_content(RawItem(item.content))

    # 增加项目
    # 用于traverse函数调用
    def add_item(self, item):
        # 检查参数
        assert isinstance(item, ContentItem)
        # 获得哈希
        sha256 = item.sha256
        # 检查字典
        if sha256 in self:
            # 增加计数
            self[sha256].count += item.count; return
        # 增加项目
        self[sha256] = RawItem(content); self[sha256].count = item.count

class DictionaryItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None) :
        # 调用父类初始化函数
        super().__init__(content)

    # 打印信息
    def dump(self):
        # 打印信息
        print("DictionaryItem.dump : show properties !")
        print("\t"); print("length = %d" % len(self.content))
        print("\t"); print("count = %d" % self.count)
        print("\t"); print("sha256 = 0x%s" % self.sha256.hexdigest())
        print("\t"); print("content = \"%s\"" % self.content)

class DictionaryContent(ContentGroup) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 最大长度
        self.max_length = 8
        # 是否需要分割
        self.need_split = True

    # 新对象
    def new_item(self) :
        # 返回结果
        return DictionaryItem()

    # 删除无效项目
    def clear_invalid(self) :
        # 清理无效数据
        self._clear_invalid(self.max_length)

    # 增加项目
    # 用于traverse函数
    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_item(ContentItem(content))

    # 增加项目
    # 用于traverse函数
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
            content = segment[1:]
            # 循环处理
            for i in range(len(content)) :
                # 循环处理
                for length in range(1, 1 + self.max_length) :
                    # 长度限定在当前长度
                    if i + length > len(content) : break
                    # 获得子字符串
                    value = content[i : i + length]
                    # 检查结果
                    if value in self:
                        self[value].count += item.count; continue
                    # 检查内容
                    if ChineseTool.is_chinese(value) :
                        # 增加项目
                        self[value] = DictionaryItem(value); self[value].count = item.count

class SegmentItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None) :
        # 调用父类初始化函数
        super().__init__(content)

    # 打印信息
    def dump(self):
        # 打印信息
        print("SegmentItem.dump : show properties !")
        print("\t"); print("length = %d" % len(self._content))
        print("\t"); print("count = %d" % self.count)
        print("\t"); print("sha256 = 0x%s" % self.sha256.hexdigest())
        print("\t"); print("content = \"%s\"" % self.content)

class SegmentContent(ContentGroup) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 是否需要分割
        self.need_split = True

    # 新对象
    def new_item(self) :
        # 返回结果
        return SegmentItem()

    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_content(SegmentItem(content))

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
            content = segment[1:]
            # 检查结果
            if content in self:
                self[content].count += item.count; return
            # 增加项目
            self[content] = SegmentItem(content); self[content].count = item.count

class WordItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None) :
        # 调用父类初始化函数
        super().__init__(content)
        # 只选取最大gamma值的分解模式
        # 设置最大值
        self.__gamma = 0.0
        # 设置分解模式
        self.__pattern = None

    @property
    def gamma(self) :
        # 返回结果
        return self.__gamma

    @property
    def pattern(self) :
        # 返回结果
        return self.__pattern

    @property
    def json(self) :
        # 返回结果
        return \
            {
                "count" : self.count,
                "content" : self._content,
                "gamma" : self.__gamma,
                "pattern" : self.__pattern,
            }

    @json.setter
    def json(self, value) :
        # 设置参数
        self.count = value["count"]
        self._content = value["content"]
        self.__gamma = value["gamma"]
        self.__pattern = value["pattern"]

    def is_valid(self, max_length) :
        # 返回结果
        if self.count <= 1 : return False
        if self.__gamma < 0.00001 : return False
        if self.length <= 0 : return False
        if self.length > 1 and self.__pattern is None : return False
        if self.length == 1 and self.__pattern is not None : return False
        # 返回结果
        return self.length <= max_length

    def dump(self):
        # 打印信息
        print("WordItem.dump : show properties !")
        print("\t"); print("length = %d" % self.length)
        print("\t"); print("count = %d" % self.count)
        print("\t"); print("content = \"%s\"" % self._content)
        print("\t"); print("sha256 = 0x%s" % self.sha256.hexdigest())
        print("\t"); print("gamma = %f" % self.__gamma)
        print("\t"); print("pattern =\"%s\"" % self.__pattern)

    # 更新Gamma数值
    def update_gamma(self, words) :
        # 检查参数
        assert isinstance(words, WordContent)
        # 长度小于1，则返回空
        if self.length < 1 : return
        # 长度为1，则设置gamma为1.0
        if self.length == 1 : self.__gamma = 1.0; return
        # 已更新过的内容，则不再更新
        if self.__gamma > 0 and self.__pattern is not None : return

        # 结果
        gammas = {}
        # 循环处理
        for i in range(1, len(self.content)) :
            # 获得gamma数值
            gamma = words.get_gamma([self.content[0:i], self.content[i:]])
            # 检查结果
            if gamma <= 0 : continue
            # 移动分隔符
            gammas[self.content[0:i] + '|' + self.content[i:]] = gamma
        # 循环处理
        for i in range(1, len(self.content)) :
            for j in range(i + 1, len(self.content)) :
                # 部分
                gamma = words.get_gamma([self.content[0:i], self.content[i:j], self.content[j:]])
                # 检查结果
                if gamma <= 0 : continue
                # 移动分隔符
                gammas[self.content[0:i] + '|' + self.content[i:j] + '|' + self.content[j:]] = gamma
        # 循环处理
        for i in range(1, len(self.content)) :
            for j in range(i + 1, len(self.content)) :
                for k in range(j + 1, len(self.content)) :
                    # 部分
                    gamma = words.get_gamma([self.content[0:i], self.content[i:j], self.content[j:k], self.content[k:]])
                    # 检查结果
                    if gamma <= 0 : continue
                    # 移动分隔符
                    gammas[self.content[0:i] + '|' + self.content[i:j] + '|' + self.content[j:k] + '|' + self.content[k:]] = gamma
        # 排序
        self.__gamma = 0.0
        # 循环处理
        # 选择Gamma值最大的一组数据
        for (key, value) in gammas.items() :
            # 检查结果
            if value > self.__gamma : self.__gamma = value; self.__pattern = key

class WordContent(ContentGroup) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 当前长度
        self.limit_length = 1
        # 是否需要分割
        self.need_split = True

    # 新对象
    def new_item(self) :
        # 返回结果
        return WordItem()

    def add_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 增加项目
        self.add_content(WordItem(item.content))

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
            content = segment[1:]
            # 循环处理
            for i in range(0, len(content)) :
                # 长度限定在当前长度
                if i + self.limit_length > len(content) : break
                # 获得单词
                word = content[i : i + self.limit_length]
                # 检查结果
                if word in self: self[word].count += item.count; continue
                # 检查是否为中文
                # 如果是纯中文内容，则增加数据项
                if ChineseTool.is_chinese(word) :
                    # 增加项目
                    self[word] = WordItem(word); self[word].count = item.count

    def get_gamma(self, parts) :
        # 检查参数
        assert isinstance(parts, list)
        # Gamma数值
        gamma = 0.0
        # 内容
        content = ""
        # 循环处理
        for part in parts :
            # 增加字符
            content += part
            # 检查字典
            if not part in self : return -1.0
            # 获得计数
            count = self[part].count
            # 检查结果
            if count <= 0 : return -1.0
            # 计算结果
            gamma += 1.0 / float(count)
        # 计算总值
        if not content in self : return 0.0
        # 返回结果
        return gamma * float(self[content].count) / float(len(parts))

    # 更新Gamma数值
    def update_gammas(self) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self)
        # 打印数据总数
        print("WordContent.update_gammas : try to update %d row(s) !" % total)

        # 指定长度
        length = 1
        # 百分之一
        percent = 0
        one_percent = total / 100.0
        # 循环处理
        while count < total :
            # 打印信息
            print("WordContent.update_gammas : try to process !")
            print("\t"); print("length = %d" % length)
            # 循环处理
            for item in self.get_items(length) :
                # 计数器加1
                count = count + 1
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
                # 检查结果
                if count >= (percent + 1) * one_percent:
                    # 增加百分之一
                    percent = percent + 1
                    # 打印进度条
                    print("\r", end = "")
                    print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end = "")
                    sys.stdout.flush()
            # 长度加一
            length += 1
            # 打印信息
            print("")
            print("WordContent.update_gammas : length(%d) processed !" % length)
        # 打印数据总数
        print("")
        print("WordContent.update_gammas : %d row(s) updated !" % total)

class SentenceItem(ContentItem) :
    # 初始化对象
    def __init__(self, content = None) :
        # 调用父类初始化函数
        super().__init__(content)

    # 打印信息
    def dump(self):
        # 打印信息
        print("SentenceItem.dump : show properties !")
        print("\t"); print("count = %d" % self.count)
        print("\t"); print("length = %d" % self.length)
        print("\t"); print("content = \"%s\"" % self._content)
        print("\t"); print("sha256 = 0x%s" % self.sha256.hexdigest())

class SentenceContent(ContentGroup) :
    # 初始化对象
    def __init__(self) :
        # 调用父类初始化函数
        super().__init__()
        # 设置标志位
        self._use_sha256 = True

    # 新对象
    def new_item(self) :
        # 返回结果
        return SentenceItem()

    # 提取句子
    # 用于traverse函数
    def extract_content(self, content) :
        # 检查参数
        assert isinstance(content, str)
        # 提取句子
        self.extract_item(SentenceItem(item.content))

    # 提取句子
    # 用于traverse函数
    def extract_dict(self, data) :
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
        # 循环处理
        for sentence in sentences:
            # 获得哈希
            sha256 = HashTool.sha256(sentence)
            # 检查数据是否存在
            if sha256 in self:
                # 计数器增加
                self[sha256].count += item.count; continue
            # 加入字典
            self[sha256] = SentenceItem(sentence); self[sha256].count = item.count

