# -*- coding: utf-8 -*-
import sqlite3
import traceback

from Content import *
from ContentTool import *
from QuantityTool import *
from SentenceTool import *

json_path = ".\\json\\"

# 数据项目
raw_items = []
# 生成对象
raw = RawContent()
# 加载数据
if raw.load(json_path + "raw.json") > 0 :
    # 获得所有项目
    raw_items = [item for item in raw.values()]
else :
    print("OperateData.random_quantity : fail to load file !")

def random_quantity() :
    # 清理输入项目
    user_input = ""
    # 循环处理
    while user_input.lower() != '0':
        # 获得随机数
        index = random.randint(0, len(raw_items))
        # 获得内容
        original = raw_items[index].content
        #original = "中国奥运代表团旗手仍定男篮 王治郅易建联２选１"
        normalized = ContentTool.normalize_content(original)
        # 打印结果
        print("OperateData.random_quantity : normalized result !")
        print("\t", end = ""); print("original   =\"%s\"" % original)
        print("\t", end = ""); print("normalized =\"%s\"" % normalized)
        # 提取数量词
        group = QuantityTemplate.extract(normalized)
        # 检查结果
        if group is not None :
            # 打印信息
            group.dump()
        else :
            # 打印信息
            print("OperateData.random_quantity : no matched !")
        # 继续选择输入
        user_input = input("Enter '0' to exit : ")

def random_sentence() :
    # 清理输入项目
    user_input = ""
    # 循环处理
    while user_input.lower() != '0':
        # 获得随机数
        index = random.randint(0, len(raw_items))
        # 获得内容
        original = raw_items[index].content
        normalized = ContentTool.normalize_content(original)
        # 打印结果
        print("OperateData.random_sentence : normalized result !")
        print("\t", end = ""); print("original   =\"%s\"" % original)
        print("\t", end = ""); print("normalized =\"%s\"" % normalized)
        # 打散和标记
        segments = SentenceTool.split(normalized)
        # 打印结果
        print("OperateData.random_sentence : split result !")
        # 打印结果
        for segment in segments: print("\t%s" % segment)
        # 合并
        segments = SentenceTool.merge(segments)
        # 打印结果
        print("OperateData.random_sentence : merged result !")
        # 打印结果
        for segment in segments: print("\t%s" % segment)
        # 继续选择输入
        user_input = input("Enter '0' to exit : ")

def update_core_gammas() :
    # 生成对象
    cores = CoreContent()
    # 加载数据
    if cores.load(json_path + "cores.json") <= 0 :
        print("OperateData.update_core_gammas : fail to load file !")
    # 更新数据
    cores.update_gammas()
    # 保存数据
    cores.save(json_path + "cores.json")

def upload_words_to_sqlite3() :
    try:
        # 链接数据库
        dbConn = sqlite3.connect("nldb3.db")
        # 打开数据库
        dbCursor = dbConn.cursor()
        # 打印信息
        print("OperateData.upload_words_to_sqlite3 : database connected !")
        # 循环加载
        for i in range(1, 9):
            # 生成对象
            words = WordContent()
            # 加载数据
            if words.load(json_path + "words{}.json".format(i)) <= 0:
                print("OperateData.get_gamma_by_words : fail to load words{}.json !".format(i))
                break

            # 计数器
            count = 0
            # 获得总数
            total = len(words)
            # 百分之一
            percent = 0
            one_percent = total / 100.0
            # 循环处理
            for item in words.values() :
                # 计数器加1
                count = count + 1
                # 将数据插入数据库
                dbCursor.execute("INSERT INTO words (content, count, length) " + \
                    "VALUES (\"{0}\", {1}, {2})".format(item.content, item.count, item.length))
                # 检查结果
                if (count - 1) >= (percent + 1) * one_percent:
                    # 增加百分之一
                    percent = percent + 1
                    # 打印进度条
                    print("\r", end = "")
                    print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                    sys.stdout.flush()
            print("")
            print("OperateData.get_gamma_by_words : words{}.json loaded !".format(i))
        # 关闭数据库
        dbCursor.close()
        dbConn.close()
        # 打印信息
        print("OperateData.upload_words_to_sqlite3 : database closed !")
    except Exception as e:
        traceback.print_exc()
        print("OperateData.upload_words_to_sqlite3 : ", str(e))
        print("OperateData.upload_words_to_sqlite3 : unexpected exit !")

def main() :
    # 选项
    options = \
        [
            "exit",
            "random quantity",
            "random sentence",
            "update core gammas",
            "upload words to sqlite3",
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
            print("OperateData.main : user exit !"); break
        elif user_input == '1' :
            # 随机选择一条内容，提取数量词
            random_quantity()
        elif user_input == '2' :
            # 随机选择一条内容，拆分成句子
            random_sentence()
        elif user_input == '3' :
            # 更新Gamma数值
            update_core_gammas()
        elif user_input == '4' :
            # 获得Gamma数值
            upload_words_to_sqlite3()
        else :
            print("OperateData.main : unknown choice !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("OperateData.main :__main__ : ", str(e))
        print("OperateData.main :__main__ : unexpected exit !")