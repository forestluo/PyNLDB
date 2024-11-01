# -*- coding: utf-8 -*-

from Content import *
from NLDB3Content import *
from SentenceTool import *
from QuantityTool import *

json_path = ".\\json\\"

def generate_raw() :
    # 打印信息
    print("GenerateData.generate_raw : generate raw.json !")
    # 生成对象
    raw = NLDB3Raw()
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
    raw = NLDB3Dictionary()
    # 打开数据库
    raw.open()
    # 保存数据文件
    raw.save(json_path + "dict.json")
    # 关闭数据库
    raw.close()
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
    # 设置参数值
    segments.need_split = True
    # 加载数据
    raw.traverse(segments.add_item)
    # 打印信息
    print("GenerateData.generate_segments : total %d word(s) !" % len(segments))
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
    # 遍历提取
    raw.traverse(sentences.extract_item)
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
    # 加载数据
    raw.traverse(tokens.add_item)
    # 保存文件
    tokens.save(json_path + "tokens.json")
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
    words.length = length
    words.need_split = False
    # 加载数据
    segments.traverse(words.add_item)
    # 打印信息
    print("GenerateData.generate_words : total %d word(s) !" % len(words))
    print("GenerateData.generate_words : clear useless word(s)  !" )
    # 清理项目
    words.clear_useless()
    # 打印信息
    print("GenerateData.generate_words : %d word(s) left !" % len(words))
    # 保存项目
    words.save(json_path + "words{}.json".format(length))

def generate_dictionary() :
    # 打印信息
    print("GenerateData.generate_dictionary : filter dictionary !")
    # 创建对象
    segments = SegmentContent()
    # 加载数据
    if segments.load(json_path + "segments.json") <= 0 :
        print("GenerateData.generate_dictionary : fail to load file !")
        return
    # 创建对象
    dictionary = DictionaryContent()
    # 加载数据
    # 不加载之前保存的计数器，准备重新生成计数器
    if dictionary.load(json_path + "dict.json", True) <= 0 :
        print("GenerateData.generate_dictionary : fail to load file !")
        return
    # 设置参数
    dictionary.need_split = False
    # 过滤
    segments.traverse(dictionary.add_item)
    # 保存数据
    dictionary.save(json_path + "dictionary.json")
    # 打印信息
    print("GenerateData.generate_dictionary : dictionary filtered !")

def random_quantity() :
    # 建立数据库链接
    raw = NLDB3Raw()
    # 打开数据库链接
    raw.open()
    # 随机抽取一条记录
    data = raw.random()
    # 关闭数据库链接
    raw.close()
    # 处理数据
    content = ContentTool.normalize_content(data["content"])
    # 打印结果
    print("GenerateData.random_quantity : normalized result !")
    print("\t"); print("original   =\"%s\"" % data["content"])
    print("\t"); print("normalized =\"%s\"" % content)

    # 提取数量词
    group = QuantityTemplate.extract(content)
    # 检查结果
    if group is not None :
        # 打印信息
        group.dump()
    else :
        # 打印信息
        print("GenerateData.random_quantity : no matched !")

def random_sentences() :
    # 建立数据库链接
    raw = NLDB3Raw()
    # 打开数据库链接
    raw.open()
    # 随机抽取一条记录
    data = raw.random()
    # 关闭数据库链接
    raw.close()
    # 处理数据
    content = ContentTool.normalize_content(data["content"])
    # 打印结果
    print("GenerateData.random_sentence : normalized result !")
    print("\toriginal   =\"%s\"" % data["content"])
    print("\tnormalized =\"%s\"" % content)

    # 打散和标记
    segments = SentenceTool.split(content)
    # 打印结果
    print("GenerateData.random_sentence : split result !")
    # 打印结果
    for segment in segments : print("\t%s" % segment)

    # 合并
    segments = SentenceTool.merge(segments)
    # 打印结果
    print("GenerateData.random_sentence : merged result !")
    # 打印结果
    for segment in segments : print("\t%s" % segment)

def main() :

    # 选项
    options = \
        [
            "exit",
            "raw.json",
            "dict.json",
            "normalized.json",
            "tokens.json", # 包含所有字符
            "segments.json",
            "sentences.json",
            "dictionary.json",
            "words[1 - 3].json", # 仅包含常见中文字符
            "words[4 - 8].json", # 仅包含常见中文字符
            "random quantity",
            "random sentences",
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
            # 生成words1.json
            generate_words(1)
            # 生成words2.json
            generate_words(2)
            # 生成words3.json
            generate_words(3)
        elif user_input == '9' :
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
        elif user_input == '10':
            # 提取数量词测试
            random_quantity()
        elif user_input == '11':
            # 提取句子测试
            random_sentences()
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