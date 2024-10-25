import traceback

from NLDB3Raw import *
from RawContent import *
from WordContent import *
from TokenContent import *
from SentenceTool import *
from SentenceContent import *
from SentenceTemplate import *

def main() :

    # 生成对象
    nldb3 = NLDB3Raw()
    # 打开数据库链接
    nldb3.open()
    # 加载数据
    nldb3.save("raw.json")
    # 关闭数据库链接
    nldb3.close()

    # 生成对象
    raw = RawContent()
    # 加载数据
    raw.load("raw.json")
    # 遍历
    raw.traverse(ContentTool.normalize_item)
    # 保存数据
    raw.save("normalized.json")

    # 生成对象
    tokens = TokenContent()
    # 遍历
    raw.traverse(tokens.add)
    # 保存文件
    tokens.save("tokens.json")
    # 抛弃内存数据
    tokens.clear()

    # 设置缺省数值
    SentenceTemplate.set_default()
    # 保存文件
    SentenceTemplate.save("templates.json")

    # 加载模板文件
    count = SentenceTemplate.load("templates.json")
    # 检查结果
    if count <= 0 :
        # 设置缺省模板
        SentenceTemplate.clear(); SentenceTemplate.set_default()

    # 生成对象
    sentences = SentenceContent()
    # 遍历提取
    raw.traverse(sentences.extract_item)
    # 保存数据
    sentences.save("sentences.json")
    # 抛弃内存数据
    sentences.clear()

    # 生成对象
    words = WordContent()
    # 循环处理
    for i in range(1, 8) :
        # 设置参数值
        words.length = i
        # 打印信息
        print("GenerateData.main : word length = %d !" % i)

        # 加载数据
        raw.traverse(words.add)
        # 打印信息
        print("GenerateData.main : %d row(s) added !" % len(words))

        # 打印信息
        print("GenerateData.main : clear useless word !")
        # 清理项目
        words.clear_useless(1)

        # 保存中间过程数据
        words.save("words{}.json".format(i))
        # 打印信息
        print("GenerateData.main : %d row(s) saved !" % len(words))

        # 清理数据
        words.clear()
        # 打印信息
        print("GenerateData.main : words cleared !")

    # 加载所有数据
    for i in range(1, 8) :
        # 加载数据
        words.load("words{}.json".format(i))
    # 打印信息
    print("GenerateData.main : %d row(s) loaded !" % len(words))

    # 清理数据
    raw.clear()
    # 打印信息
    print("GenerateData.main : clear raw data !")

    # 更新Gamma数值
    words.update_gammas()
    # 保存文件
    words.save("words.json")
    # 打印信息
    print("GenerateData.main : %d word(s) saved !" % len(words))

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("GenerateData.main :__main__ : ", str(e))
        print("GenerateData.main :__main__ : unexpected exit !")