# -*- coding: utf-8 -*-

import os

from SentenceTool import *

class SentenceTemplate :
    # 所有模板（静态）
    _templates = []

    # 原始规则
    rules = ""
    # 匹配模板
    _patterns = []

    # 将规则进行预编译
    def __init__(self, rules) :
        # 检查参数
        assert rules is not None
        assert isinstance(rules, list)
        # 原始规则记录在第一项
        self.rules = rules
        # 设置匹配模板
        # 必须使用空对象初始化
        # 否则后续len函数判断长度会失误
        self._patterns = [None] * len(rules)
        # 循环处理
        for i in range(0, len(rules)) :
            # 检查参数
            assert isinstance(rules[i], str)
            # 设置匹配模式
            self._patterns[i] = re.compile(rules[i]) \
                if rules[i][0] != '$' else re.compile("^\\$")

    # 是否匹配
    def __is_matched__(self, segments) :
        # 检查参数
        assert segments is not None
        assert isinstance(segments, list)
        # 检查参数
        # 模板的长度比分段数量多，则肯定无法匹配
        if len(self._patterns) > len(segments) : return False
        # 循环处理
        for i in range(0, len(self._patterns)) :
            # 检查参数
            assert isinstance(segments[i], str)
            assert self._patterns[i] is not None
            # 匹配
            matched = self._patterns[i].match(segments[i])
            # 检查结果
            if not matched or matched.start() != 0 : return False
        # 返回结果
        return True

    @staticmethod
    def clear() :
        # 清除所有模板
        SentenceTemplate._templates.clear()

    @staticmethod
    def append(rules) :
        # 增加模板
        SentenceTemplate._templates.append(SentenceTemplate(rules))

    # 提取句子
    @staticmethod
    def extract(content) :
        # 正则化内容
        content = ContentTool.normalize_content(content)
        # 打散和标记
        segments = SentenceTool.split(content)
        # 合并
        segments = SentenceTool.merge(segments)
        # 提取
        return SentenceTemplate._extract_(segments)

    # 提取句子
    @staticmethod
    def _extract_(segments) :
        # 句子
        sentences = []
        # 循环处理
        # 模板最小长度为2
        # 无标点的短标题，基本会被直接抛弃
        while len(segments) > 1 :
            # 提取句子
            sentence = SentenceTemplate.__extract__(segments)
            # 检查结果
            # 删除开头不能匹配的项目，并继续尝试匹配
            if sentence is None :
                # 跳过该段落
                del segments[0:1]
            # 添加句子
            else : sentences.append(sentence)
        # 返回结果
        return sentences

    # 提取句子
    # 注意：已经匹配的部分会被删除
    # 输入参数是已经处理过的分段内容
    @staticmethod
    def __extract__(segments) :
        # 循环处理
        # 匹配过程遵循最大匹配法原则：即优先匹配最长的部分。
        for template in SentenceTemplate._templates :
            # 检查结果
            if not template.__is_matched__(segments) : continue

            # 句子内容
            sentence = ""
            # 获得长度
            length = len(template._patterns)
            # 组织内容
            for i in range(0, length) :
                # 检查内容
                if segments[i][0] != '$':
                    # 添加内容
                    sentence += segments[i]
                else :
                    # 添加实际内容
                    sentence += segments[i][1:]
            # 删除头部内容，并返回结果
            del segments[0 : length]; return sentence
        # 返回结果
        return None

    @staticmethod
    def save(fileName) :
        # 检查文件名
        if fileName is None:
            fileName = "templates.json"
        # 打开文件
        jsonFile = open(fileName, "w", encoding = "utf-8")
        # 打印信息
        print("SentenceTemplate.save : file(\"%s\") opened !" % fileName)
        # 检查文件
        assert jsonFile is not None

        # 计数器
        count = 0
        # 获得总数
        total = len(SentenceTemplate._templates)
        # 打印数据总数
        print("SentenceTemplate.save : try to save %d row(s) !" % total)
        # 将总数写入文件
        jsonFile.write(str(total))
        jsonFile.write("\n")

        # 百分之一
        percent = 0
        onePercent = total / 100.0
        # 检查数据结果
        for template in SentenceTemplate._templates :
            # 计数器加1
            count = count + 1
            # 写入文件
            jsonFile.write(json.dumps(template.rules, ensure_ascii = False))
            jsonFile.write("\n")
            # 检查结果
            if count >= (percent + 1) * onePercent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end="")
                print("Progress({}%) :".format(int(percent / onePercent)), "▓" * (int(percent / onePercent) * 3 // 5), end="")
                sys.stdout.flush()
        # 打印数据总数
        print("")
        print("SentenceTemplate.save : %d row(s) saved !" % total)
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("SentenceTemplate.save : file(\"%s\") closed !" % fileName)

    # 加载数据
    @staticmethod
    def load(fileName):
        # 检查文件名
        if fileName is None:
            fileName = "templates.json"
        # 检查文件是否存在
        if not os.path.isfile(fileName):
            # 打印信息
            print("SentenceTemplate.load : invalid file(\"%s\") !" % fileName)
            return -1
        # 打开文件
        jsonFile = open(fileName, "r", encoding = "utf-8")
        # 打印信息
        print("SentenceTemplate.load : file(\"%s\") opened !" % fileName)
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
                        print("SentenceTemplate.load : invalid total(\"%s\") !" % line)
                        break
                    # 设置百分之一
                    onePercent = total / 100.0
                    # 打印数据总数
                    print("SentenceTemplate.load : try to load %d row(s) !" % total)
                else:
                    # 加载数据
                    jsonItem = json.loads(line)
                    # 检查结果
                    if isinstance(jsonItem, list) :
                        # 生成原始数据对象
                        SentenceTemplate.append(jsonItem)

                    # 检查结果
                    if (count - 1) >= (percent + 1) * onePercent:
                        # 增加百分之一
                        percent = percent + 1
                        # 打印进度条
                        print("\r", end="")
                        print("Progress({}%) :".format(int(percent / onePercent)), "▓" * (int(percent / onePercent) * 3 // 5), end="")
                        sys.stdout.flush()

                # 读取下一行
                line = jsonFile.readline()
            # 打印信息
            print("")
            print("SentenceTemplate.load : %d line(s) processed !" % count)
        except Exception as e:
            traceback.print_exc()
            print("SentenceTemplate.load : ", str(e))
            print("SentenceTemplate.load : unexpected exit !")
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("SentenceTemplate.load : file(\"%s\") closed !" % fileName)
        print("SentenceTemplate.load : %d item(s) loaded !" % len(SentenceTemplate._templates))
        return total

    # 加载顺序遵从最大匹配法原则
    @staticmethod
    def set_default() :
        # 符号嵌套
        SentenceTemplate.append(["“$", "$a", "(，|：|。|；|？|！)+‘$", "$b", "(。|；|？|！)*’$", "$c", "(。|？|！|…)+”$"])

        SentenceTemplate.append(["“$", "$a", "(，|：|。|；|？|！|…)*”$", "$b", "(，|：)?“$", "$c", "(。|？|！|…)+”$"])
        SentenceTemplate.append(["‘$", "$a", "(，|：|。|；|？|！|…)*’$", "$b", "(，|：)?‘$", "$c", "(。|？|！|…)+’$"])
        SentenceTemplate.append(["「$", "$a", "(，|：|。|；|？|！|…)*」$", "$b", "(，|：)?“$", "$c", "(。|？|！|…)+”$"])
        SentenceTemplate.append(["『$", "$a", "(，|：|。|；|？|！|…)*』$", "$b", "(，|：)?‘$", "$c", "(。|？|！|…)+’$"])
        SentenceTemplate.append(["〝$", "$a", "(，|：|。|；|？|！|…)*〞$", "$b", "(，|：)?“$", "$c", "(。|？|！|…)+”$"])
        SentenceTemplate.append(["【$", "$a", "(，|：|。|；|？|！|…)*】$", "$b", "(，|：)?‘$", "$c", "(。|？|！|…)+’$"])

        SentenceTemplate.append(["$a", "(，|：)?“$", "$b", "(，|；|…)*”$", "$c", "(。|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?‘$", "$b", "(，|；|…)*’$", "$c", "(。|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?「$", "$b", "(，|；|…)*」$", "$c", "(。|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?『$", "$b", "(，|；|…)*』$", "$c", "(。|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?〝$", "$b", "(，|；|…)*〞$", "$c", "(。|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?【$", "$b", "(，|；|…)*】$", "$c", "(。|？|！|…)+$"])

        SentenceTemplate.append(["“$", "$a", "(，|：|。|；|？|！)+‘$", "$b", "(。|；|？|！|…)*’”$"])
        SentenceTemplate.append(["“‘$", "$a", "(，|：|。|；|？|！|…)*’$", "$b", "(。|；|？|！|…)+”$"])

        SentenceTemplate.append(["“$", "$a", "(，|：|。|；|？|！|…)*”$", "$b", "(。|？|！|…)+$"])
        SentenceTemplate.append(["‘$", "$a", "(，|：|。|；|？|！|…)*’$", "$b", "(。|？|！|…)+$"])

        SentenceTemplate.append(["$a", "(，|：)?“$", "$b", "(。|？|！|…)?”$"])
        SentenceTemplate.append(["$a", "(，|：)?‘$", "$b", "(。|？|！|…)?’$"])
        SentenceTemplate.append(["$a", "(，|：)?「$", "$b", "(。|？|！|…)?」$"])
        SentenceTemplate.append(["$a", "(，|：)?『$", "$b", "(。|？|！|…)?』$"])
        SentenceTemplate.append(["$a", "(，|：)?〝$", "$b", "(。|？|！|…)?〞$"])
        SentenceTemplate.append(["$a", "(，|：)?【$", "$b", "(。|？|！|…)?】$"])

        # 常见符号
        SentenceTemplate.append(["$a", "(：)$", "$b", "(。|；|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?“$", "$b", "(。|；|？|！|…)*”$"])
        SentenceTemplate.append(["$a", "(，|：)?‘$", "$b", "(。|；|？|！|…)*’$"])
        SentenceTemplate.append(["$a", "(，|：)?（$", "$b", "(。|；|？|！|…)*）$"])
        SentenceTemplate.append(["$a", "(，|：)?「$", "$b", "(。|；|？|！|…)*」$"])
        SentenceTemplate.append(["$a", "(，|：)?『$", "$b", "(。|；|？|！|…)*』$"])
        SentenceTemplate.append(["$a", "(，|：)?〝$", "$b", "(。|；|？|！|…)*〞$"])

        SentenceTemplate.append(["$a", "(，|：)?《$", "$b", "》(。|？|！|…)+$"])
        SentenceTemplate.append(["$a", "(，|：)?【$", "$b", "】(。|？|！|…)+$"])

        # 符号嵌套
        SentenceTemplate.append(["“‘$", "$a", "(，|：|。|；|？|！|…)*’”$"])
        SentenceTemplate.append(["“（$", "$a", "(，|：|。|；|？|！|…)*）”$"])

        # 常见符号
        SentenceTemplate.append(["“$", "$a", "(，|：|。|；|？|！|…)*”$"])
        SentenceTemplate.append(["‘$", "$a", "(，|：|。|；|？|！|…)*’$"])
        SentenceTemplate.append(["（$", "$a", "(，|：|。|；|？|！|…)*）$"])
        SentenceTemplate.append(["《$", "$a", "(，|：|。|；|？|！|…)*》$"])
        SentenceTemplate.append(["【$", "$a", "(，|：|。|；|？|！|…)*】$"])
        # 比较少见
        SentenceTemplate.append(["「$", "$a", "(，|：|。|；|？|！|…)*」$"])
        SentenceTemplate.append(["『$", "$a", "(，|：|。|；|？|！|…)*』$"])
        SentenceTemplate.append(["〖$", "$a", "(，|：|。|；|？|！|…)*〗$"])
        SentenceTemplate.append(["〝$", "$a", "(，|：|。|；|？|！|…)*〞$"])

        # 最简单的句子
        SentenceTemplate.append(["$a", "(。|；|？|！|…)+$"])

def main():

    # 清理
    SentenceTemplate.clear()
    # 设置缺省数值
    SentenceTemplate.set_default()
    # 保存模板文件
    SentenceTemplate.save("templates.json")
    # 清理
    SentenceTemplate.clear()
    # 加载模板文件
    SentenceTemplate.load("templates.json")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("SentenceTemplate.main :__main__ : ", str(e))
        print("SentenceTemplate.main :__main__ : unexpected exit !")

