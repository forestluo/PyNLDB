# -*- coding: utf-8 -*-

import traceback

from RawContent import *
from SentenceTool import *
from TokenContent import *

class WordItem :
    # 初始化对象
    def __init__(self, word) :
        # 检查参数
        assert word is not None
        assert isinstance(word, str) and len(word) == 2
        # 设置缺省值
        self.count = 1
        self.gamma = 0.0
        # 设置词汇
        self.word = word

    def dump(self):
        # 打印信息
        print("WordItem.dump : show properties !")
        print("\tword = \'%s\'" % self.word)
        print("\tcount = %d" % self.count)
        print("\tgamma = %f" % self.gamma)

class WordContent :
    # 初始化对象
    def __init__(self) :
        # Hash表
        self._words = {}

    def __contains__(self, word) :
        # 检查参数
        assert word is not None and len(word) == 1
        # 返回结果
        return word in self._words.keys()

    def __getitem__(self, word):
        # 检查参数
        assert word is not None and len(word) == 1
        # 返回结果
        return self._words[word]

    def __setitem__(self, word, wordItem):
        # 检查参数
        assert word is not None and len(word) == 1
        # 设置数值
        self._words[word] = wordItem

    def add(self, rawItem):
        # 检查参数
        assert rawItem is not None
        assert isinstance(rawItem, RawItem)

        # 拆分内容
        segments = SplitTool.split(rawItem.content)
        # 循环处理
        for segment in segments :
            # 检查结果
            if segment[0] != '$' : continue
            # 获得内容
            content = segment[1:]
            # 循环处理
            for i in range(0, len(content) - 1) :
                # 获得单词
                word = content[i : i + 2]
                # 检查结果
                if word in self._words.keys() :
                    # 计数器加一
                    self._words[word].count += 1
                else :
                    # 增加单词项目
                    self._words[word] = WordItem(word)

    # 更新Gamma数值
    def update_gamma(self, tokens) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self._words)
        # 打印数据总数
        print("WordContent.update_gamma : try to update %d row(s) !" % total)

        # 百分之一
        percent = 0
        onePercent = total / 100.0

        # 异常项目
        items = []
        # 循环处理
        for item in self._words.values() :
            # 计数器加1
            count = count + 1
            # 设置初始值
            item.gamma = 0.0
            # 获得数据
            for token in item.word :
                # 检查字符
                if not token in tokens \
                    or tokens[token].count <= 0 :
                    # 设置异常数值
                    item.gamma = -1.0; break
                # 计算每个分项数值
                item.gamma += float(item.count) / float(tokens[token].count)
            # 检查分项加和值
            if item.gamma <= 0.0 :
                # 加入异常项
                # 准备后期删除
                items.append(item)
            else :
                # 求平均值
                item.gamma /= float(len(item.word))
            # 检查结果
            if count >= (percent + 1) * onePercent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end="")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                sys.stdout.flush()
        # 删除异常项目
        for item in items : del self._words[item.word]
        # 打印数据总数
        print("")
        print("WordContent.update_gamma : %d row(s) updated !" % total)

    def save(self, fileName) :
        # 检查文件名
        if fileName is None:
            fileName = "words.json"
        # 打开文件
        jsonFile = open(fileName, "w", encoding = "utf-8")
        # 打印信息
        print("WordContent.save : file(\"%s\") opened !" % fileName)
        # 检查文件
        assert jsonFile is not None

        # 计数器
        count = 0
        # 获得总数
        total = len(self._words)
        # 打印数据总数
        print("WordContent.save : try to save %d row(s) !" % total)
        # 将总数写入文件
        jsonFile.write(str(total))
        jsonFile.write("\n")

        # 百分之一
        percent = 0
        onePercent = total / 100.0
        # 检查数据结果
        for item in self._words.values() :
            # 计数器加1
            count = count + 1
            # json项目
            jsonItem = \
                {
                    "word" : item.word,
                    "count" : item.count,
                    "gamma" : item.gamma
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
        print("WordContent.save : %d row(s) saved !" % total)
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("WordContent.save : file(\"%s\") closed !" % fileName)

    # 加载数据
    def load(self, fileName):
        # 检查文件名
        if fileName is None:
            fileName = "words.json"
        # 检查文件是否存在
        if not os.path.isfile(fileName):
            # 打印信息
            print("WordContent.load : invalid file(\"%s\") !" % fileName)
            return -1
        # 打开文件
        jsonFile = open(fileName, "r", encoding = "utf-8")
        # 打印信息
        print("WordContent.load : file(\"%s\") opened !" % fileName)
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
                        print("WordContent.load : invalid total(\"%s\") !" % line)
                        break
                    # 设置百分之一
                    onePercent = total / 100.0
                    # 打印数据总数
                    print("WordContent.load : try to load %d row(s) !" % total)
                else:
                    # 按照json格式解析
                    jsonItem = json.loads(line)
                    # 生成词汇项目
                    wordItem = \
                        WordItem(jsonItem["word"])
                    wordItem.count = jsonItem["count"]
                    wordItem.gamma = jsonItem["gamma"]
                    # 检查结果
                    if (count - 1) >= (percent + 1) * onePercent:
                        # 增加百分之一
                        percent = percent + 1
                        # 打印进度条
                        print("\r", end="")
                        print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                        sys.stdout.flush()
                    # 加入字典
                    self._words[wordItem.word] = wordItem
                # 读取下一行
                line = jsonFile.readline()
            # 打印信息
            print("")
            print("WordContent.load : %d line(s) processed !" % count)
        except Exception as e:
            traceback.print_exc()
            print("WordContent.load : ", str(e))
            print("WordContent.load : unexpected exit !")
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("WordContent.load : file(\"%s\") closed !" % fileName)
        print("WordContent.load : %d item(s) loaded !" % len(self._words))
        return total

def main():

    # 建立原始数据
    rawContent = RawContent()
    # 加载数据
    rawContent.load("normalized.json")

    # 建立单字表
    tokenContent = TokenContent()
    # 加载数据
    tokenContent.load("tokens.json")

    # 建立字符表
    wordContent = WordContent()
    # 加载数据
    rawContent.traverse(wordContent.add)
    # 更新Gamma数值
    wordContent.update_gamma(tokenContent)
    # 保存文件
    wordContent.save("words.json")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("WordContent.main :__main__ : ", str(e))
        print("WordContent.main :__main__ : unexpected exit !")

