# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from TokenContent import *

def main():

    # 建立数据库链接
    tokenContent = TokenContent()
    # 加载文件
    tokenContent.load("tokens.json")

    # 获得所有数据项
    tokenItems = tokenContent.token_items()
    # 排序
    sorted(tokenItems, key = lambda item : item.unicode)

    # 宽度
    _width = 1920
    # 高度
    _height = 1080
    # 统计数据
    _tokens = []
    _counts = []
    # 循环处理
    for token in tokenItems :
        # 增加统计数据
        _counts.append(token.count)
        """
        # 检查数据
        if token.unicode < 0 :
            token.unicode += 65536
        """
        # 增加数据标识
        _tokens.append(token.unicode)
    # 归一化处理
    maxToken = max(_tokens); maxCount = max(_counts)
    for i in range(0, len(_tokens)) :
        _tokens[i] = _tokens[i] / maxToken * float(_width)
    for i in range(0, len(_counts)) :
        _counts[i] = _counts[i] / maxCount * float(_height)
    # 设置图形数据
    plt.bar(x = _tokens,data = _counts, height = _height, width = _width)
    # 设置图表属性
    plt.title('Tokens')
    plt.xlabel('Unicode')
    plt.ylabel('Frequency')
    # 显示图表
    plt.show()

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("TokenBar.main :__main__ : ", str(e))
        print("TokenBar.main :__main__ : unexpected exit !")