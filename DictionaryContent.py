# -*- coding: utf-8 -*-

import os
import sys
import json
import hashlib
import traceback

class DictionaryItem :
    # 初始化对象
    def __init__(self, content, source = None, remark = None):
        # 检查参数
        assert isinstance(content, str)
        if source is not None :
            assert isinstance(source, str)
        if remark is not None :
            assert isinstance(remark, str)

        # 设置备注
        self.count = 1
        # 设置备注
        self.remark = remark
        # 设置来源
        self.source = source
        # 设置内容
        self.content = content
        # 设置长度
        self.length = len(content)

    @property
    def sha256(self) :
        # 检查参数
        assert isinstance(self.content, str)
        # 返回结果
        return hashlib.sha256(self.content.encode("utf-8"))

    def dump(self):
        # 打印信息
        print("RawItem.dump : show properties !")
        print("\tcount = %d" % self.count)
        print("\tlength = %d" % self.length)
        if self.remark is not None:
            print("\tremark = \"%s\"" % self.remark)
        if self.source is not None:
            print("\tsource = \"%s\"" % self.source)
        if self.content is not None:
            print("\tcontent = \"%s\"" % self.content)

class DictionaryContent:
    # 初始化对象
    def __init__(self) :
        # Hash表
        self._contents = {}

    # 清理
    def clear(self) :
        # 清理所有数据
        self._contents.clear()

    # 遍历处理
    def traverse(self, function) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self._contents)
        # 打印数据总数
        print("DictionaryContent.traverse : try to process %d row(s) !" % total)

        # 百分之一
        percent = 0
        onePercent = total / 100.0
        # 检查数据结果
        for item in self._contents.values() :
            # 计数器加1
            count = count + 1
            # 检查结果
            if count >= (percent + 1) * onePercent :
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
        print("DictionaryContent.traverse : %d row(s) processed !" % total)

    def save(self, fileName):
        # 检查文件名
        if fileName is None:
            fileName = "dictionary.json"
        # 打开文件
        jsonFile = open(fileName, "w", encoding = "utf-8")
        # 打印信息
        print("DictionaryContent.save : file(\"%s\") opened !" % fileName)
        # 检查文件
        assert jsonFile is not None

        # 计数器
        count = 0
        # 获得总数
        total = len(self._contents)
        # 打印数据总数
        print("DictionaryContent.save : try to save %d row(s) !" % total)
        # 将总数写入文件
        jsonFile.write(str(total))
        jsonFile.write("\n")

        # 百分之一
        percent = 0
        onePercent = total / 100.0
        # 检查数据结果
        for item in self._contents.values() :
            # 计数器加1
            count = count + 1
            # 数据项
            jsonItem = \
                {
                    "count" : item.count,
                    "remark" : item.remark,
                    "source" : item.source,
                    "content" : item.content,
                }
            # 写入文件
            jsonFile.write(json.dumps(jsonItem, ensure_ascii = False))
            jsonFile.write("\n")
            # 检查结果
            if count >= (percent + 1) * onePercent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end="")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                sys.stdout.flush()
        # 打印数据总数
        print("")
        print("DictionaryContent.save : %d row(s) saved !" % total)
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("DictionaryContent.save : file(\"%s\") closed !" % fileName)

    # 加载数据
    def load(self, fileName):
        # 检查文件名
        if fileName is None:
            fileName = "dictionary.json"
        # 检查文件是否存在
        if not os.path.isfile(fileName):
            # 打印信息
            print("DictionaryContent.load : invalid file(\"%s\") !" % fileName)
            return -1
        # 打开文件
        jsonFile = open(fileName, "r", encoding = "utf-8")
        # 打印信息
        print("DictionaryContent.load : file(\"%s\") opened !" % fileName)
        # 检查文件
        assert jsonFile is not None

        # 计数器
        count = 0
        # 获得总数
        total = 0
        # 百分之一
        percent = 0
        onePercent = total / 100.0

        try:
            # 按行读取
            line = jsonFile.readline()
            # 循环处理
            while line :
                # 剪裁字符串
                line = line.strip()
                # 检查结果
                if len(line) <= 0:
                    # 读取下一行
                    line = jsonFile.readline()
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
                        print("DictionaryContent.load : invalid total(\"%s\") !" % line)
                        break
                    # 设置百分之一
                    onePercent = total / 100.0
                    # 打印数据总数
                    print("DictionaryContent.load : try to load %d row(s) !" % total)
                else:
                    # 按照json格式解析
                    jsonItem = json.loads(line)
                    # 生成原始数据对象
                    dictionaryItem = DictionaryItem(jsonItem["content"])
                    # 设置参数
                    dictionaryItem.count = jsonItem["count"]
                    dictionaryItem.source = jsonItem["source"]
                    dictionaryItem.remark = jsonItem["remark"]

                    # 检查结果
                    if (count - 1) >= (percent + 1) * onePercent:
                        # 增加百分之一
                        percent = percent + 1
                        # 打印进度条
                        print("\r", end="")
                        print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                        sys.stdout.flush()

                    # 查询字典
                    if dictionaryItem.content not in self._contents :
                        # 加入字典
                        self._contents[dictionaryItem.content] = dictionaryItem
                    else :
                        # 打印信息
                        print("")
                        print("DictionaryContent.load : raw item(\"%s\") exists !" % line)
                # 读取下一行
                line = jsonFile.readline()
            # 打印信息
            print("")
            print("DictionaryContent.load : %d line(s) processed !" % count)
        except Exception as e:
            traceback.print_exc()
            print("DictionaryContent.load : ", str(e))
            print("DictionaryContent.load : unexpected exit !")
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("DictionaryContent.load : file(\"%s\") closed !" % fileName)
        print("DictionaryContent.load : %d item(s) loaded !" % len(self._contents))
        return total