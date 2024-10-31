# -*- coding: utf-8 -*-

#import traceback

#from RawContent import *
from WordContent import *
#from ContentTool import *
#from NLDB3Content import *
from TokenContent import *
from SentenceContent import *
from DictionaryContent import *

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

def generate_words(length) :
    # 建立原始数据
    raw = RawContent()
    # 加载数据
    raw.load(json_path + "normalized.json")
    # 建立字符表
    words = WordContent()
    # 打印信息
    print("WordContent.load : length = %d !" % length)
    # 设置参数值
    words.length = length
    # 加载数据
    raw.traverse(words.add_item)
    # 打印信息
    print("WordContent.load : total %d word(s) !" % len(words))
    print("WordContent.load : clear useless word(s)  !" )
    # 清理项目
    words.clear_useless()
    # 打印信息
    print("WordContent.load : %d word(s) left !" % len(words))
    # 保存项目
    words.save(json_path + "words{}.json".format(length))

def generate_tokens() :
    # 打印信息
    print("GenerateData.generate_tokens : generate tokens.json !")
    # 建立原始数据
    raw = RawContent()
    # 加载数据
    raw.load(json_path + "normalized.json")
    # 建立字符表
    tokens = TokenContent()
    # 加载数据
    raw.traverse(tokens.add_item)
    # 保存文件
    tokens.save(json_path + "tokens.json")
    # 打印信息
    print("GenerateData.generate_tokens : tokens.json generated !")

def generate_sentences() :
    # 打印信息
    print("GenerateData.generate_sentences : generate sentences.json !")
    # 生成对象
    raw = RawContent()
    # 加载数据
    raw.load(json_path + "normalized.json")
    # 生成对象
    sentences = SentenceContent()
    # 遍历提取
    raw.traverse(sentences.extract_item)
    # 保存数据
    sentences.save(json_path + "sentences.json")
    # 打印信息
    print("GenerateData.generate_sentences : sentences.json generated !")

def generate_dictionary() :
    # 打印信息
    print("GenerateData.generate_dictionary : generate dictionary.json !")
    # 生成对象
    raw = NLDB3Dictionary()
    # 打开数据库
    raw.open()
    # 保存数据文件
    raw.save(json_path + "dictionary.json")
    # 关闭数据库
    raw.close()
    # 打印信息
    print("GenerateData.generate_dictionary : dictionary.json generated !")

    # 打印信息
    print("GenerateData.generate_dictionary : filter dictionary !")
    # 创建对象
    raw = RawContent()
    # 加载对象
    raw.load(json_path + "normalized.json")
    # 创建对象
    dictionary = DictionaryContent()
    # 加载数据
    # 不加载之前保存的计数器，准备重新生成计数器
    dictionary.load(json_path + "dictionary.json", True)
    # 过滤
    raw.traverse(dictionary.count_item)
    # 保存数据
    dictionary.save(json_path + "words.json")
    # 打印信息
    print("GenerateData.generate_dictionary : dictionary filtered !")

def generate_normalized() :
    # 打印信息
    print("GenerateData.generate_normalized : generate normalized.json !")
    # 建立数据库链接
    raw = RawContent()
    # 加载数据
    raw.load(json_path + "raw.json")
    # 正则化处理
    raw.traverse(ContentTool.normalize_item)
    # 保存数据
    raw.save(json_path + "normalized.json")
    # 打印信息
    print("GenerateData.generate_normalized : normalized.json generated !")

def main() :

    # 选项
    options = \
        [
            "exit",
            "raw.json",
            "dictionary.json",
            "normalized.json",
            "all basic json files (raw.json, normalized.json)",
            "tokens.json", # 包含所有字符
            "sentences.json",
            "words[1 - 3].json", # 仅包含常见中文字符
            "words[4 - 8].json", # 仅包含常见中文字符
            "all words json files (words[1 - 8].json)"
        ]

    # 提示信息
    inputMessage = "Please pick an option :\n"
    # 打印选项
    for index, item in enumerate(options) :
        inputMessage += f"{index}) {item}\n"
    # 打印提示
    inputMessage += "Your choice : "

    # 循环处理
    while True :
        # 清理输入项目
        userInput = ""
        # 循环处理
        while userInput.lower() \
                not \
                in map(str, range(0, len(options))) :
            # 继续选择输入
            userInput = input(inputMessage)
        # 开始执行
        if userInput == '0' :
            # 打印信息
            print("GenerateData.main : user exit !"); break
        elif userInput == '1' :
            # 生成raw.json
            generate_raw()
        elif userInput == '2' :
            # 生成dictionary.json
            generate_dictionary()
        elif userInput == '3' :
            # 生成normalized.json
            generate_normalized()
        elif userInput == '4' :
            # 生成raw.json
            generate_raw()
            # 生成normalized.json
            generate_normalized()
        elif userInput == '5' :
            # 生成tokens.json
            generate_tokens()
        elif userInput == '6' :
            # 生成sentences.json
            generate_sentences()
        elif userInput == '7' :
            # 生成words1.json
            generate_words(1)
            # 生成words2.json
            generate_words(2)
            # 生成words3.json
            generate_words(3)
        elif userInput == '8' :
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