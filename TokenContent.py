# -*- coding: utf-8 -*-

import traceback

from RawContent import *
from ContentTool import *

class TokenItem :
    # 初始化对象
    def __init__(self, token):
        # 检查参数
        assert isinstance(token, str)
        # 频次计数器
        self.count = 1
        # 设置字符
        self.token = token
        # 设置Unicode值
        self.unicode = ord(token)

    def is_rare(self) :
        # 返回结果
        return UnicodeTool.is_rare(self.token)

    def dump(self):
        # 打印信息
        print("TokenItem.dump : show properties !")
        print("\ttoken = \'%c\'" % self.token)
        print("\tunicode = 0x%4X" % self.unicode)
        print("\tcount = %d" % self.count)
        print("\tremark = \"%s\"" % UnicodeTool.get_remark(self.token))

class TokenContent :
    # 初始化对象
    def __init__(self) :
        # Hash表
        self._tokens = {}

    def __contains__(self, token) :
        # 检查参数
        assert token is not None and len(token) == 1
        # 返回结果
        return token in self._tokens.keys()

    def __getitem__(self, token) :
        # 检查参数
        assert token is not None and len(token) == 1
        # 返回结果
        return self._tokens[token]

    def __setitem__(self, token, tokenItem) :
        # 检查参数
        assert token is not None and len(token) == 1
        # 设置数值
        self._tokens[token] = tokenItem

    # 清理
    def clear(self) :
        # 清理数据
        self._tokens.clear()

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
            if not token in self._tokens.keys() : return -1.0
            # 获得计数
            count = self._tokens[token].count
            # 检查结果
            if count <= 0 : return -1.0
            # 计算结果
            gamma += 1.0 / float(count)
        # 计算总值
        if not content in self._tokens.keys() : return 0.0
        # 返回结果
        return gamma * float(self._tokens[content].count) / float(len(tokens))

    def add(self, rawItem) :
        # 检查参数
        assert isinstance(rawItem, RawItem)
        # 扫描结果
        for token in rawItem.content :
            # 检查字典
            if token in self._tokens:
                # 获得对象
                self._tokens[token].count += 1
            else:
                # 增加字典内容
                self._tokens[token] = TokenItem(token)
            """
            # 检查字符
            if UnicodeTool.is_rare(token) :
                print("")
                print("TokenContent.add : rare token(\'%c\', 0x%X) !" % (token, ord(token)))
            """

    def save(self, fileName) :
        # 检查文件名
        if fileName is None:
            fileName = "tokens.json"
        # 打开文件
        jsonFile = open(fileName, "w", encoding = "utf-8")
        # 打印信息
        print("TokenContent.save : file(\"%s\") opened !" % fileName)
        # 检查文件
        assert jsonFile is not None

        # 计数器
        count = 0
        # 获得总数
        total = len(self._tokens)
        # 打印数据总数
        print("TokenContent.save : try to save %d row(s) !" % total)
        # 将总数写入文件
        jsonFile.write(str(total))
        jsonFile.write("\n")

        # 百分之一
        percent = 0
        onePercent = total / 100.0
        # 检查数据结果
        for item in self._tokens.values() :
            # 计数器加1
            count = count + 1
            # Json项目
            jsonItem = \
                {
                    "count": item.count,
                    "token": item.token,
                    "unicode": item.unicode,
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
        print("TokenContent.save : %d row(s) saved !" % total)
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("TokenContent.save : file(\"%s\") closed !" % fileName)

    # 加载数据
    def load(self, fileName):
        # 检查文件名
        if fileName is None:
            fileName = "tokens.json"
        # 检查文件是否存在
        if not os.path.isfile(fileName):
            # 打印信息
            print("TokenContent.load : invalid file(\"%s\") !" % fileName)
            return -1
        # 打开文件
        jsonFile = open(fileName, "r", encoding = "utf-8")
        # 打印信息
        print("TokenContent.load : file(\"%s\") opened !" % fileName)
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
                        print("TokenContent.load : invalid total(\"%s\") !" % line)
                        break
                    # 设置百分之一
                    onePercent = total / 100.0
                    # 打印数据总数
                    print("TokenContent.load : try to load %d row(s) !" % total)
                else:
                    # 按照json格式解析
                    jsonItem = json.loads(line)

                    # 获得token
                    token = jsonItem["token"]
                    # 生成原始数据对象
                    tokenItem = TokenItem(token)
                    # 设置计数
                    tokenItem.count = jsonItem["count"]
                    # 检查字典
                    if not token in self._tokens.keys() :
                        # 加入字典
                        self._tokens[token] = tokenItem

                    # 检查结果
                    if (count - 1) >= (percent + 1) * onePercent:
                        # 增加百分之一
                        percent = percent + 1
                        # 打印进度条
                        print("\r", end="")
                        print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                        sys.stdout.flush()
                    # 检查字符
                    # 防止非unicode字符进入词典
                    if UnicodeTool.is_rare(token):
                        print("")
                        print("TokenContent.add : rare token(\'%c\', 0x%X) !" % (token, ord(token)))

                # 读取下一行
                line = jsonFile.readline()
            # 打印信息
            print("")
            print("TokenContent.load : %d line(s) processed !" % count)
        except Exception as e:
            traceback.print_exc()
            print("TokenContent.load : ", str(e))
            print("TokenContent.load : unexpected exit !")
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("TokenContent.load : file(\"%s\") closed !" % fileName)
        print("TokenContent.load : %d item(s) loaded !" % len(self._tokens))
        return total