# -*- coding: utf-8 -*-
import traceback

from nlp.corpus.VerbWord import *
from nlp.corpus.RegionName import *
from nlp.corpus.CommonWord import *

from nlp.tool.ContentTool import *
from nlp.content.CoreItem import *
from nlp.content.RawContent import *
from nlp.content.CoreContent import *
from nlp.content.WordContent import *
from nlp.content.TokenContent import *
from nlp.content.SegmentContent import *
from nlp.content.SentenceContent import *
from nlp.content.DictionaryContent import *

from nldb.sqlserver.SQLServerRaw import *
from nldb.sqlserver.SQLServerDictionary import *

json_path = "..\\json\\"

def generate_raw() :
    # 打印信息
    print("GenerateData.generate_raw : generate raw.json !")
    # 生成对象
    raw = SQLServerRaw()
    # 打开数据库
    raw.open()
    # 保存数据文件
    raw.save(json_path + "raw.json")
    # 关闭数据库
    raw.close()
    # 打印信息
    print("GenerateData.generate_raw : raw.json generated !")

def generate_dict() :
    # 打印信息
    print("GenerateData.generate_dict : generate dict.json !")
    # 生成对象
    dictionary = SQLServerDictionary()
    # 打开数据库
    dictionary.open()
    # 保存数据文件
    dictionary.save(json_path + "dict.json")
    # 关闭数据库
    dictionary.close()
    # 打印信息
    print("GenerateData.generate_dict : dict.json generated !")

def generate_normalized() :
    # 打印信息
    print("GenerateData.generate_normalized : generate normalized.json !")
    # 建立数据库链接
    raw = RawContent()
    # 加载数据
    if raw.load(json_path + "raw.json") <= 0 :
        print("GenerateData.generate_normalized : fail to load file !")
        return
    # 正则化处理
    raw.traverse(ContentTool.normalize_item)
    # 保存数据
    raw.save(json_path + "normalized.json")
    # 打印信息
    print("GenerateData.generate_normalized : normalized.json generated !")

def generate_segments() :
    # 建立原始数据
    raw = RawContent()
    # 加载数据
    if raw.load(json_path + "normalized.json") <= 0 :
        print("GenerateData.generate_segments : fail to load file !")
        return
    # 建立分段表
    segments = SegmentContent()
    # 遍历数据，并进行分割处理
    raw.traverse(segments.add_splitted, True)
    # 打印信息
    print("GenerateData.generate_segments : total %d segment(s) !" % len(segments))
    # 保存项目
    segments.save(json_path + "segments.json")

def generate_sentences() :
    # 打印信息
    print("GenerateData.generate_sentences : generate sentences.json !")
    # 生成对象
    raw = RawContent()
    # 加载数据
    if raw.load(json_path + "normalized.json") <= 0 :
        print("GenerateData.generate_sentences : fail to load file !")
        return
    # 生成对象
    sentences = SentenceContent()
    # 遍历数据，并提取句子
    raw.traverse(sentences.add_extracted)
    # 保存数据
    sentences.save(json_path + "sentences.json")
    # 打印信息
    print("GenerateData.generate_sentences : sentences.json generated !")

def generate_tokens() :
    # 打印信息
    print("GenerateData.generate_tokens : generate tokens.json !")
    # 建立原始数据
    raw = RawContent()
    # 加载数据
    if raw.load(json_path + "normalized.json") <= 0 :
        print("GenerateData.generate_tokens : fail to load file !")
        return
    # 建立字符表
    tokens = TokenContent()
    # 遍历数据，并提取符号
    raw.traverse(tokens.add_splitted)
    # 保存文件
    tokens.save(json_path + "tokens.json", True)
    # 打印信息
    print("GenerateData.generate_tokens : tokens.json generated !")

def generate_words(length) :
    # 建立原始数据
    segments = SegmentContent()
    # 加载数据
    if segments.load(json_path + "segments.json") <= 0 :
        print("GenerateData.generate_words : fail to load file !")
        return
    # 建立字符表
    words = WordContent()
    # 打印信息
    print("GenerateData.generate_words : length = %d !" % length)
    # 设置参数值
    # 设定数据处理的限定长度，仅加载指定长度的数据
    words.limit_length = length
    # 加载数据
    segments.traverse(words.add_splitted, False)
    # 打印信息
    print("GenerateData.generate_words : total %d word(s) !" % len(words))
    print("GenerateData.generate_words : clear useless word(s)  !" )
    # 清理项目
    words.clear_useless()
    # 打印信息
    print("GenerateData.generate_words : %d word(s) left !" % len(words))
    # 保存项目
    words.save(json_path + "words{}.json".format(length), length <= 1)

def generate_dictionary() :
    # 打印信息
    print("GenerateData.generate_dictionary : filter dictionary !")
    # 从原始数据加载字典
    dictionary = DictionaryContent.load_dict(json_path + "dict.json")
    # 检查结果
    if len(dictionary) <= 0 :
        print("GenerateData.generate_dictionary : fail to load file !")
        return
    # 保存重新组织后的数据
    dictionary.save(json_path + "dictionary.json")
    # 创建对象
    segments = SegmentContent()
    # 加载数据
    if segments.load(json_path + "segments.json") <= 0 :
        print("GenerateData.generate_dictionary : fail to load file !")
        return
    # 复位计数器
    dictionary.reset_count()
    # 过滤
    segments.traverse(dictionary.count_item, False)
    # 再次保存数据
    dictionary.save(json_path + "dictionary.json")
    # 打印信息
    print("GenerateData.generate_dictionary : dictionary filtered !")

def generate_core() :
    # 生成对象
    cores = CoreContent()
    # 生成对象
    # 加载数据
    if cores.load(json_path + "words1.json") <= 0 :
        print("GenerateData.generate_core : fail to load file !")
        return
    # 生成对象
    dictionary = DictionaryContent()
    # 加载数据
    if dictionary.load(json_path + "dictionary.json") <= 0 :
        print("GenerateData.generate_core : fail to load file !")
        return
    # 获得所有数据
    # 循环处理
    for item in dictionary.values() :
        # 检查数据项目
        if item.count < 10 : continue
        # 检查来源
        if (item.has_source("成语") and item.length == 4) \
            or (item.has_source("地理信息") and item.length > 1) \
            or (item.has_source("现代汉语词典") and item.length > 1) \
            or (item.has_source("新华字典") and item.length in [3, 4]) :
            # 检查数据
            if item.content not in cores :
                # 增加数据
                cores[item.content] = CoreItem(item.content)
    # 加入内置数据
    # 加入常用动词
    for verb in VerbWord.verbs :
        # 检查数据
        if verb not in cores : cores[verb] = CoreItem(verb)
    # 加入地理位置
    for name in RegionName.names :
        # 检查数据
        if name not in cores : cores[name] = CoreItem(name)
    # 加入常用词汇
    for word in CommonWord.words :
        # 检查数据
        if word[0] not in cores : cores[word[0]] = CoreItem(word[0])

    # 创建对象
    segments = SegmentContent()
    # 加载数据
    if segments.load(json_path + "segments.json") <= 0 :
        print("GenerateData.generate_core : fail to load file !")
        return
    # 复位计数器
    cores.reset_count()
    # 更新长度
    cores.update_max_length()
    # 重新计数
    segments.traverse(cores.count_item, False)
    # 保存数据
    cores.save(json_path + "cores.json")

def main() :

    # 选项
    options = \
        [
            "exit",
            "raw.json",
            "dict.json",
            "normalized.json",
            # tokens.json包含所有字符
            # words1.json仅包含常用中文字符
            "tokens.json & words1.json",
            "segments.json",
            "sentences.json",
            "dictionary.json",
            "cores.json",
            "words[2 - 8].json", # 仅包含常见中文字符
            "all basic json files", # 所有基础数据文件
        ]

    # 提示信息
    input_message = "Please pick an option :\n"
    # 打印选项
    for index, item in enumerate(options) :
        input_message += f"{index}) {item}\n"
    # 打印提示
    input_message += "Your choice : "

    # 循环处理
    while True :
        # 清理输入项目
        user_input = ""
        # 循环处理
        while user_input.lower() \
                not \
                in map(str, range(0, len(options))) :
            # 继续选择输入
            user_input = input(input_message)
        # 开始执行
        if user_input == '0' :
            # 打印信息
            print("GenerateData.main : user exit !"); break
        elif user_input == '1' :
            # 生成raw.json
            generate_raw()
        elif user_input == '2' :
            # 生成dict.json
            generate_dict()
        elif user_input == '3':
            # 生成normalized.json
            generate_normalized()
        elif user_input == '4' :
            # 生成tokens.json
            generate_tokens()
            # 生成words1.json
            generate_words(1)
        elif user_input == '5' :
            # 生成segments.json
            generate_segments()
        elif user_input == '6' :
            # 生成sentences.json
            generate_sentences()
        elif user_input == '7' :
            # 生成dictionary.json
            generate_dictionary()
        elif user_input == '8' :
            # 生成核心数据
            generate_core()
        elif user_input == '9' :
            # 生成words2.json
            generate_words(2)
            # 生成words3.json
            generate_words(3)
            # 生成words4.json
            generate_words(4)
            # 生成words5.json
            generate_words(5)
            # 生成words6.json
            generate_words(6)
            # 生成words7.json
            generate_words(7)
            # 生成words8.json
            generate_words(8)
        elif user_input == '10' :
            # 生成raw.json
            generate_raw()
            # 生成dict.json
            generate_dict()
            # 生成normalized.json
            generate_normalized()
            # 生成tokens.json
            generate_tokens()
            # 生成segments.json
            generate_segments()
            # 生成words1.json
            generate_words(1)
            # 生成sentences.json
            generate_sentences()
            # 生成dictionary.json
            generate_dictionary()
            # 生成核心数据
            generate_core()
        else :
            print("GenerateData.main : unknown choice !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("GenerateData.main :__main__ : ", str(e))
        print("GenerateData.main :__main__ : unexpected exit !")