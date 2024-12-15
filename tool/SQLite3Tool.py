# -*- coding: utf-8 -*-

from nldb.sqlite.SQRaw import *
from nldb.sqlite.SQWords import *
from nldb.sqlite.SQTokens import *
from nldb.sqlite.SQSegments import *
from nldb.sqlite.SQSentences import *
from nldb.sqlite.SQDictionary import *

from nlp.content.RawContent import *
from nlp.content.CoreContent import *
from nlp.content.WordContent import *
from nlp.content.TokenContent import *
from nlp.content.SegmentContent import *
from nlp.content.SentenceContent import *

json_path = "../json\\"

def upload_raw() :
    # 生成对象
    raw = RawContent()
    # 加载文件
    if raw.load(json_path + "raw.json") <= 0 :
        # 打印信息
        print("SQLite3Tool.upload_raw : fail to load file !")
        return
    # 生成对象
    nldb3 = NLDB3Raw()
    # 打开数据库
    if not nldb3.open() :
        # 打印信息
        print("SQLite3Tool.upload_raw : fail to open database !")
        return
    # 删除原数据表
    nldb3.drop_table()
    # 打印信息
    print("SQLite3Tool.upload_raw : previous table dropped !")
    # 创建新数据表
    nldb3.create_table()
    # 打印信息
    print("SQLite3Tool.upload_raw : new table created !")
    # 遍历
    raw.traverse(nldb3.insert_table)
    # 关闭数据库
    nldb3.close()
    # 打印信息
    print("SQLite3Tool.upload_raw : database closed !")

def upload_normalized() :
    # 生成对象
    raw = RawContent()
    # 加载文件
    if raw.load(json_path + "normalized.json") <= 0 :
        # 打印信息
        print("SQLite3Tool.upload_normalized : fail to load file !")
        return
    # 生成对象
    nldb3 = NLDB3Raw()
    # 打开数据库
    if not nldb3.open() :
        # 打印信息
        print("SQLite3Tool.upload_normalized : fail to open database !")
        return
    # 删除原数据表
    nldb3.drop_table()
    # 打印信息
    print("SQLite3Tool.upload_normalized : previous table dropped !")
    # 创建新数据表
    nldb3.create_table()
    # 打印信息
    print("SQLite3Tool.upload_normalized : new table created !")
    # 遍历
    raw.traverse(nldb3.insert_table)
    # 关闭数据库
    nldb3.close()
    # 打印信息
    print("SQLite3Tool.upload_normalized : database closed !")

def upload_tokens() :
    # 生成对象
    tokens = TokenContent()
    # 加载文件
    if tokens.load(json_path + "tokens.json") <= 0 :
        # 打印信息
        print("SQLite3Tool.upload_tokens : fail to load file !")
        return
    # 生成对象
    nldb3 = SQTokens()
    # 打开数据库
    if not nldb3.open() :
        # 打印信息
        print("SQLite3Tool.upload_tokens : fail to open database !")
        return
    # 删除原数据表
    nldb3.drop_table()
    # 打印信息
    print("SQLite3Tool.upload_tokens : previous table dropped !")
    # 创建新数据表
    nldb3.create_table()
    # 打印信息
    print("SQLite3Tool.upload_tokens : new table created !")
    # 遍历
    tokens.traverse(nldb3.insert_table)
    # 关闭数据库
    nldb3.close()
    # 打印信息
    print("SQLite3Tool.upload_tokens : database closed !")

def upload_segments() :
    # 生成对象
    segments = SegmentContent()
    # 加载文件
    if segments.load(json_path + "segments.json") <= 0 :
        # 打印信息
        print("SQLite3Tool.upload_segments : fail to load file !")
        return
    # 生成对象
    nldb3 = SQSegments()
    # 打开数据库
    if not nldb3.open() :
        # 打印信息
        print("SQLite3Tool.upload_segments : fail to open database !")
        return
    # 删除原数据表
    nldb3.drop_table()
    # 打印信息
    print("SQLite3Tool.upload_segments : previous table dropped !")
    # 创建新数据表
    nldb3.create_table()
    # 打印信息
    print("SQLite3Tool.upload_segments : new table created !")
    # 遍历
    segments.traverse(nldb3.insert_table)
    # 关闭数据库
    nldb3.close()
    # 打印信息
    print("SQLite3Tool.upload_segments : database closed !")

def upload_sentences() :
    # 生成对象
    sentences = SentenceContent()
    # 加载文件
    if sentences.load(json_path + "sentences.json") <= 0 :
        # 打印信息
        print("SQLite3Tool.upload_sentences : fail to load file !")
        return
    # 生成对象
    nldb3 = SQSentences()
    # 打开数据库
    if not nldb3.open() :
        # 打印信息
        print("SQLite3Tool.upload_sentences : fail to open database !")
        return
    # 删除原数据表
    nldb3.drop_table()
    # 打印信息
    print("SQLite3Tool.upload_sentences : previous table dropped !")
    # 创建新数据表
    nldb3.create_table()
    # 打印信息
    print("SQLite3Tool.upload_sentences : new table created !")
    # 遍历
    sentences.traverse(nldb3.insert_table)
    # 关闭数据库
    nldb3.close()
    # 打印信息
    print("SQLite3Tool.upload_sentences : database closed !")

def upload_dictionary() :
    # 生成对象
    dictionary = DictionaryContent()
    # 加载文件
    if dictionary.load(json_path + "dictionary.json") <= 0 :
        # 打印信息
        print("SQLite3Tool.upload_dictionary : fail to load file !")
        return
    # 生成对象
    nldb3 = SQDictionary()
    # 打开数据库
    if not nldb3.open() :
        # 打印信息
        print("SQLite3Tool.upload_dictionary : fail to open database !")
        return
    # 删除原数据表
    nldb3.drop_table()
    # 打印信息
    print("SQLite3Tool.upload_dictionary : previous table dropped !")
    # 创建新数据表
    nldb3.create_table()
    # 打印信息
    print("SQLite3Tool.upload_dictionary : new table created !")
    # 遍历
    dictionary.traverse(nldb3.insert)
    # 关闭数据库
    nldb3.close()
    # 打印信息
    print("SQLite3Tool.upload_dictionary : database closed !")

def upload_words() :
    # 生成对象
    nldb3 = SQWords()
    # 打开数据库
    if not nldb3.open() :
        # 打印信息
        print("SQLite3Tool.upload_words : fail to open database !")
        return
    # 删除原数据表
    nldb3.drop_table()
    # 打印信息
    print("SQLite3Tool.upload_words : previous table dropped !")
    # 创建新数据表
    nldb3.create_table()
    # 打印信息
    print("SQLite3Tool.upload_words : new table created !")
    # 循环处理
    for i in range(1, 9) :
        # 设置参数
        nldb3.limit_length = i
        # 生成对象
        words = WordContent()
        # 加载文件
        if words.load(json_path + "words{}.json".format(i)) <= 0:
            # 打印信息
            print("SQLite3Tool.upload_words : fail to load file !")
            return
        # 遍历
        words.traverse(nldb3.insert_table)
    # 关闭数据库
    nldb3.close()
    # 打印信息
    print("SQLite3Tool.upload_words : database closed !")

def main() :

    # 选项
    options = \
        [
            "exit",
            "upload raw.json",
            "upload normalized.json",
            # tokens.json包含所有字符
            "upload tokens.json",
            "upload segments.json",
            "upload sentences.json",
            "upload dictionary.json",
            "upload words[1 - 8].json", # 仅包含常见中文字符
            "upload all basic json files", # 所有基础数据文件
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
            print("SQLite3Tool.main : user exit !"); break
        elif user_input == '1' :
            # 上传raw.json
            upload_raw()
        elif user_input == '2' :
            # 上传normalized.json
            upload_normalized()
        elif user_input == '3' :
            # 上传tokens.json
            upload_tokens()
        elif user_input == '4' :
            # 上传segments.json
            upload_segments()
        elif user_input == '5' :
            # 上传sentences.json
            upload_sentences()
        elif user_input == '6' :
            # 上传dictionary.json
            upload_dictionary()
        elif user_input == '7' :
            # 上传words[1-3].json
            upload_words()
        elif user_input == '8':
            # 上传normalized.json
            upload_normalized()
            # 上传sentences.json
            upload_sentences()
            # 上传segments.json
            upload_segments()
            # 上传words[1-8].json
            upload_words()
        else :
            print("SQLite3Tool.main : unknown choice !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("SQLite3Tool.main :__main__ : ", str(e))
        print("SQLite3Tool.main :__main__ : unexpected exit !")