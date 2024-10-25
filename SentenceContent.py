# -*- coding: utf-8 -*-

import os
import hashlib

from RawContent import *
from ContentTool import *
from SentenceTemplate import *

class SentenceItem:
    # 初始化对象
    def __init__(self, content):
        # 检查参数
        if content is not None :
            assert isinstance(content, str)
        # 设置计数
        self.count = 1
        # 设置内容
        self.content = content

        # 设置长度
        self.length = len(content)
        # 设置hash值
        self.sha256 = hashlib.sha256(content.encode('utf-8'))

    def dump(self):
        # 打印信息
        print("RawItem.dump : show properties !")
        print("\tcount = %d" % self.count)
        print("\tlength = %d" % self.length)
        if self.sha256 is not None:
            print("\tsha256 = 0x%s" % self.sha256.hexdigest())
        if self.content is not None:
            print("\tcontent = \"%s\"" % self.content)

class SentenceContent:
    # 初始化对象
    def __init__(self) :
        # Hash表
        self._sentences = {}

    # 清理
    def clear(self) :
        # 清理数据
        self._sentences.clear()

    # 提取句子
    def extract_item(self, item) :
        # 检查参数
        assert item is not None
        # 提取句子
        sentences = SentenceTemplate.extract(item.content)
        # 循环处理
        for sentence in sentences :
            # 生成项目
            sentenceItem = SentenceItem(sentence)
            # 查询字典
            if sentenceItem.sha256 in self._sentences :
                # 计数器增加
                sentenceItem.count += 1
            else :
                # 加入字典
                self._sentences[sentenceItem.sha256] = sentenceItem
            # 检查句子
            if UnicodeTool.is_rare(sentence):
                print("")
                print("SentenceContent.extract_item : sentence(\"%s\") has rare token !" % sentence)

    # 提取句子
    def extract_dict(self, data) :
        # 检查参数
        assert data is not None
        # 提取句子
        sentences = SentenceTemplate.extract(data["content"])
        # 循环处理
        for sentence in sentences :
            # 生成项目
            sentenceItem = SentenceItem(sentence)
            # 查询字典
            if sentenceItem.sha256 in self._sentences :
                # 计数器增加
                sentenceItem.count += 1
            else :
                # 加入字典
                self._sentences[sentenceItem.sha256] = sentenceItem
            # 检查句子
            if UnicodeTool.is_rare(sentence):
                print("")
                print("SentenceContent.extract_dict : sentence(\"%s\") has rare token !" % sentence)

    # 遍历处理
    def traverse(self, function) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self._sentences)
        # 打印数据总数
        print("SentenceContent.traverse : try to process %d row(s) !" % total)

        # 百分之一
        percent = 0
        onePercent = total / 100.0
        # 检查数据结果
        for item in self._sentences.values() :
            # 计数器加1
            count = count + 1
            # 检查结果
            if count >= (percent + 1) * onePercent :
                # 设置标志位
                newline = True
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
        print("SentenceContent.traverse : %d row(s) processed !" % total)

    def save(self, fileName) :
        # 检查文件名
        if fileName is None:
            fileName = "sentences.json"
        # 打开文件
        jsonFile = open(fileName, "w", encoding = "utf-8")
        # 打印信息
        print("SentenceContent.save : file(\"%s\") opened !" % fileName)
        # 检查文件
        assert jsonFile is not None

        # 计数器
        count = 0
        # 获得总数
        total = len(self._sentences)
        # 打印数据总数
        print("SentenceContent.save : try to save %d row(s) !" % total)
        # 将总数写入文件
        jsonFile.write(str(total))
        jsonFile.write("\n")

        # 百分之一
        percent = 0
        onePercent = total / 100.0
        # 检查数据结果
        for item in self._sentences.values() :
            # 计数器加1
            count = count + 1
            # 数据项
            jsonItem = \
                {
                    "count": item.count,
                    "content": item.content
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
        print("SentenceContent.save : %d row(s) saved !" % total)
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("SentenceContent.save : file(\"%s\") closed !" % fileName)

    # 加载数据
    def load(self, fileName):
        # 检查文件名
        if fileName is None:
            fileName = "sentence.json"
        # 检查文件是否存在
        if not os.path.isfile(fileName):
            # 打印信息
            print("SentenceContent.load : invalid file(\"%s\") !" % fileName)
            return -1
        # 打开文件
        jsonFile = open(fileName, "r", encoding = "utf-8")
        # 打印信息
        print("SentenceContent.load : file(\"%s\") opened !" % fileName)
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
                        print("SentenceContent.load : invalid total(\"%s\") !" % line)
                        break
                    # 设置百分之一
                    onePercent = total / 100.0
                    # 打印数据总数
                    print("SentenceContent.load : try to load %d row(s) !" % total)
                else:
                    # 按照json格式解析
                    jsonItem = json.loads(line)
                    # 生成原始数据对象
                    sentenceItem = \
                        SentenceItem(jsonItem["content"])
                    # 设置计数
                    sentenceItem.count = jsonItem["count"]

                    # 检查结果
                    if (count - 1) >= (percent + 1) * onePercent :
                        # 增加百分之一
                        percent = percent + 1
                        # 打印进度条
                        print("\r", end="")
                        print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                        sys.stdout.flush()

                    # 查询字典
                    if sentenceItem.sha256 in self._sentences :
                        # 打印信息
                        #sentenceItem.dump()
                        # 打印信息
                        print("")
                        print("SentenceContent.load : raw item(\"%s\") exists !" % line)
                        continue
                    # 加入字典
                    self._sentences[sentenceItem.sha256] = sentenceItem
                # 读取下一行
                line = jsonFile.readline()
            # 打印信息
            print("")
            print("SentenceContent.load : %d line(s) processed !" % count)
        except Exception as e:
            traceback.print_exc()
            print("SentenceContent.load : ", str(e))
            print("SentenceContent.load : unexpected exit !")
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("SentenceContent.load : file(\"%s\") closed !" % fileName)
        print("SentenceContent.load : %d item(s) loaded !" % len(self._sentences))
        return total

def main():

    # 生成对象
    rawContent = RawContent()
    # 加载数据
    rawContent.load("normalized.json")

    # 加载模板文件
    count = SentenceTemplate.load("templates.json")
    # 检查结果
    if count <= 0 :
        # 设置缺省模板
        SentenceTemplate.clear(); SentenceTemplate.set_default()

    # 生成对象
    sentenceContent = SentenceContent()
    # 遍历提取
    rawContent.traverse(sentenceContent.extract_item)

    # 保存数据
    sentenceContent.save("sentences.json")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("SentenceTemplate.main :__main__ : ", str(e))
        print("SentenceTemplate.main :__main__ : unexpected exit !")