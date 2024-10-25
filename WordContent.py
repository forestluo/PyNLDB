# -*- coding: utf-8 -*-

import traceback

from RawContent import *
from SentenceTool import *

class WordItem :
    # 保留数量
    _keep_count = 5

    # 初始化对象
    def __init__(self, word) :
        # 检查参数
        assert isinstance(word, str)
        # 设置缺省值
        self.count = 1
        # 设置词汇
        self.word = word
        # 设置gamma表
        self.gammas = None

    def is_rare(self) :
        # 返回结果
        return UnicodeTool.is_rare(self.word)

    def dump(self):
        # 打印信息
        print("WordItem.dump : show properties !")
        print("\tword = \'%s\'" % self.word)
        print("\tcount = %d" % self.count)
        # 检查gammas
        if self.gammas is not None :
            # 循环处理
            for key, value in self.gammas.items() :
                print("\tgamma(\"%s\") = %f" % (key, value))

    # 更新Gamma数值
    def update_gammas(self, words) :
        # 检查参数
        assert isinstance(self.word, str)
        assert isinstance(words, WordContent)
        # 长度小于2，则返回空
        if len(self.word) < 2 : return
        # 结果
        gammas = {}
        # 循环处理
        for i in range(1, len(self.word)) :
            # 获得gamma数值
            gamma = words.get_gamma([self.word[0:i], self.word[i:]])
            # 检查结果
            if gamma <= 0 : continue
            # 移动分隔符
            gammas[self.word[0:i] + '|' + self.word[i:]] = gamma
        # 循环处理
        for i in range(1, len(self.word)) :
            for j in range(i + 1, len(self.word)) :
                # 部分
                gamma = words.get_gamma([self.word[0:i], self.word[i:j], self.word[j:]])
                # 检查结果
                if gamma <= 0 : continue
                # 移动分隔符
                gammas[self.word[0:i] + '|' + self.word[i:j] + '|' + self.word[j:]] = gamma
        # 循环处理
        for i in range(1, len(self.word)) :
            for j in range(i + 1, len(self.word)) :
                for k in range(j + 1, len(self.word)) :
                    # 部分
                    gamma = words.get_gamma([self.word[0:i], self.word[i:j], self.word[j:k], self.word[k:]])
                    # 检查结果
                    if gamma <= 0 : continue
                    # 移动分隔符
                    gammas[self.word[0:i] + '|' + self.word[i:j] + '|' + self.word[j:k] + '|' + self.word[k:]] = gamma
        # 排序
        # Gamma数值大的排前面
        sorted(gammas.items(), key = lambda kv : (kv[1], kv[0]), reverse = True)
        # 仅保留最大的几个数值，其余部分抛弃
        index = 0
        # 初始化字典
        self.gammas = {}
        # 循环处理
        for (key, value) in gammas.items() :
            # 计数器加一
            index += 1
            # 增加到数据记录中
            self.gammas[key] = value
            # 检查索引值
            if index > WordItem._keep_count : break

class WordContent :
    # 初始化对象
    def __init__(self) :
        # 当前长度
        self.length = 1
        # Hash表
        self._words = {}

    def __len__(self) :
        # 返回结果
        return len(self._words)

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

    # 清理
    def clear(self) :
        # 清理数据
        self._words.clear()

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
            if not part in self._words.keys() : return -1.0
            # 获得计数
            count = self._words[part].count
            # 检查结果
            if count <= 0 : return -1.0
            # 计算结果
            gamma += 1.0 / float(count)
        # 计算总值
        if not content in self._words.keys() : return 0.0
        # 返回结果
        return gamma * float(self._words[content].count) / float(len(parts))

    def add(self, rawItem):
        # 检查参数
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
            for i in range(0, len(content)) :
                # 长度限定在当前长度
                if i + self.length > len(content) : break

                # 获得单词
                word = content[i : i + self.length]
                # 检查结果
                if word in self._words.keys():
                    # 计数器加一
                    self._words[word].count += 1
                else:
                    # 增加单词项目
                    self._words[word] = WordItem(word)
                # 检查结果
                if UnicodeTool.is_rare(word) :
                    print("")
                    print("WordContent.add : word (\"%s\") has rare token !" % word)

    # 更新Gamma数值
    def update_gammas(self) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self._words)
        # 打印数据总数
        print("WordContent.update_gammas : try to update %d row(s) !" % total)

        # 百分之一
        percent = 0
        onePercent = total / 100.0
        # 循环处理
        for item in self._words.values() :
            # 计数器加1
            count = count + 1
            # 更新数据
            item.update_gammas()
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
        print("WordContent.update_gammas : %d row(s) updated !" % total)

    # 删除计数低于设置的项目
    def clear_useless(self, count) :
        # 删除计数器为1的项目
        self._words = {key : value for (key, value) in self._words.items() if value.count > count}

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
            # 检查数据
            # 计数不超过1的不予以保存
            if item.count <= 1 : continue
            # json项目
            jsonItem = \
                {
                    "word" : item.word,
                    "count" : item.count,
                    "gammas" : item.gammas
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
                    # 获得词汇
                    word = jsonItem["word"]
                    # 生成词汇项目
                    wordItem = WordItem(word)
                    wordItem.count = jsonItem["count"]
                    wordItem.gammas = jsonItem["gammas"]
                    # 检查记录数
                    # 记录数少于1的不予以加载
                    if wordItem.count > 1 :
                        # 检查字典
                        if not word in self._words.keys() :
                            # 加入字典
                            self._words[word] = wordItem

                    # 检查结果
                    if (count - 1) >= (percent + 1) * onePercent:
                        # 增加百分之一
                        percent = percent + 1
                        # 打印进度条
                        print("\r", end="")
                        print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                        sys.stdout.flush()
                    # 检查结果
                    if UnicodeTool.is_rare(word):
                        print("")
                        print("WordContent.add : word (\"%s\") has rare token !" % word)

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

    # 建立字符表
    wordContent = WordContent()
    # 循环处理
    for i in range(1, 8) :
        # 打印信息
        print("WordContent.load : length = %d !" % i)
        # 设置参数值
        wordContent.length = i

        # 加载数据
        rawContent.traverse(wordContent.add)
        # 打印信息
        print("WordContent.load : %d row(s) !" % len(wordContent))

        # 打印信息
        print("WordContent.load : clear useless word (count <= 1) !")
        # 清理项目
        wordContent.clear_useless(1)

        # 保存中间过程数据
        wordContent.save("words.json")
        # 打印信息
        print("WordContent.load : %d row(s) !" % len(wordContent))

    # 更新Gamma数值
    wordContent.update_gammas()
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

