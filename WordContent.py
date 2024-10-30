# -*- coding: utf-8 -*-

import traceback

from RawContent import *
from SentenceTool import *

class WordItem :
    # 初始化对象
    def __init__(self, word, count = 1) :
        # 检查参数
        assert isinstance(word, str)
        # 设置缺省值
        self.count = count
        # 设置词汇
        self.word = word
        # 只选取最大gamma值的分解模式
        # 设置分解模式
        self.pattern = None
        # 设置最大值
        self.gamma = 0.0 if len(word) > 1 else 1.0

    def is_rare(self) :
        # 返回结果
        return UnicodeTool.is_rare(self.word)

    def is_valid(self) :
        # 返回结果
        if self.count <= 1 : return False
        if self.gamma < 0.00001 : return False
        if len(self.word) <= 0 : return False
        if len(self.word) > 1 and self.pattern is None : return False
        if len(self.word) == 1 and self.pattern is not None : return False
        # 返回结果
        return True

    def is_useless(self):
        # 返回结果
        return self.count <= 1

    def is_chinese(self) :
        # 返回结果
        return ChineseTool.is_chinese(self.word)

    def dump(self):
        # 打印信息
        print("WordItem.dump : show properties !")
        print("\tword = \"%s\"" % self.word)
        print("\tcount = %d" % self.count)
        print("\tgamma = %f" % self.gamma)
        print("\tpattern =\"%s\"" % self.pattern)

    # 更新Gamma数值
    def update_gamma(self, words) :
        # 检查参数
        assert isinstance(self.word, str)
        assert isinstance(words, WordContent)
        # 长度小于1，则返回空
        if len(self.word) < 1 : return
        # 长度为1，则设置gamma为1.0
        if len(self.word) == 1 : self.gamma = 1.0; return
        # 已更新过的内容，则不再更新
        if self.gamma > 0 and self.pattern is not None : return

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
        self.gamma = 0.0
        # 循环处理
        # 选择Gamma值最大的一组数据
        for (key, value) in gammas.items() :
            # 检查结果
            if value > self.gamma : self.gamma = value; self.pattern = key

class WordContent :
    # 初始化对象
    def __init__(self) :
        # Hash表
        self._words = {}
        # 统计总数
        self._total_count = 0
        # 当前长度
        self.limit_length = 1

    def __len__(self) :
        # 返回结果
        return len(self._words)

    def __contains__(self, word) :
        # 检查参数
        assert isinstance(word, str)
        # 返回结果
        return word in self._words.keys()

    def __getitem__(self, word):
        # 检查参数
        assert isinstance(word, str)
        # 返回结果
        return self._words[word]

    def __setitem__(self, word, item):
        # 检查参数
        assert isinstance(word, str)
        assert isinstance(item, WordItem)
        # 设置数值
        self._words[word] = item

    # 清理
    def clear(self) :
        # 清理数据
        self._words.clear()

    @property
    def total_count(self) :
        # 返回结果
        return self._total_count

    # 获得指定长度项目
    def get_items(self, length = -1) :
        # 检查参数
        assert isinstance(length, int)
        # 检查长度
        if length <= 0 :
            # 返回结果
            return [item for item in self._words.values()]
        # 返回结果
        return [item for item in self._words.values() if len(item.word) == length]

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

    def add_item(self, rawItem) :
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
                if i + self.limit_length > len(content) : break

                # 获得单词
                word = content[i : i + self.limit_length]
                # 检查结果
                if word in self._words.keys():
                    # 统计总数加一
                    self._total_count += 1
                    # 计数器加一
                    self._words[word].count += 1
                else:
                    # 检查是否为中文
                    # 如果是纯中文内容，则增加数据项
                    if ChineseTool.is_chinese(word) :
                        # 统计总数加一
                        self._total_count += 1
                        # 增加元素
                        self._words[word] = WordItem(word)

    # 更新Gamma数值
    def update_gammas(self, limit = 10) :
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
            # 清理Gamma和Pattern
            item.gamma = 0.0
            item.pattern = None
            # 检查统计次数
            if item.count > limit :
                # 多于指定次数，才更新数据
                item.update_gamma(self)
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

        # 打印信息
        print("WordContent.update_gammas : clear invalid data !")
        # 清理无效数据
        self._words = {key : item for (key, item) in self._words.items() if item.is_valid()}
        # 打印信息
        print("WordContent.update_gammas : %d row(s) left !" % len(self._words))

    # 删除计数低于设置的项目
    # 使用尽量少的内存予以处理
    # 在更新计数统计数据之后进行
    def clear_useless(self) :
        # 清理无效数据
        self._words = {key : item for (key, item) in self._words.items() if not item.is_useless()}

    # 遍历处理
    def traverse(self, function) :
        # 计数器
        count = 0
        # 获得总数
        total = len(self._words)
        # 打印数据总数
        print("WordContent.traverse : try to process %d row(s) !" % total)

        # 百分之一
        percent = 0
        onePercent = total / 100.0
        # 检查数据结果
        for item in self._words.values() :
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
        print("WordContent.traverse : %d row(s) processed !" % total)

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
                    "gamma" : item.gamma,
                    "pattern" : item.pattern,
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
                    wordItem.gamma = jsonItem["gamma"]
                    wordItem.pattern = jsonItem["pattern"]
                    # 检查记录数
                    # 记录数少于1的不予以加载
                    if not wordItem.is_useless() :
                        # 检查字典
                        if word not in self._words.keys() :
                            # 加入字典
                            self._words[word] = wordItem
                            # 统计总数
                            self._total_count += wordItem.count

                    # 检查结果
                    if (count - 1) >= (percent + 1) * onePercent:
                        # 增加百分之一
                        percent = percent + 1
                        # 打印进度条
                        print("\r", end="")
                        print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                        sys.stdout.flush()
                # 读取下一行
                line = jsonFile.readline()
            # 打印信息
            print("")
            print("WordContent.load : %d line(s) processed !" % count)
            print("\ttotal_count = %d" % self._total_count)
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
