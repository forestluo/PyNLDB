# -*- coding: utf-8 -*-
from nlp.item.ContentItem import *
from nlp.item.DictionaryItem import *
from nlp.content.ContentGroup import *

class DictionaryContent(ContentGroup) :
    # 新对象
    def new_item(self, content = None, count = 1) :
        # 返回结果
        return DictionaryItem(content, count)

    # 增加项目
    # 用于traverse函数
    def count_item(self, item, need_split = True) :
        # 检查参数
        assert isinstance(item, ContentItem)
        # 生成内容
        segments = ['$' + item.content]
        # 检查标志位
        if need_split :
            # 拆分内容
            segments = SplitTool.split(item.content)
        # 循环处理
        for segment in segments :
            # 检查结果
            if segment[0] != '$' : continue
            # 获得内容
            content = segment[1 : ]
            # 循环处理
            for i in range(len(content)) :
                # 循环处理
                for length in range(1, 1 + self.max_length) :
                    # 长度限定在当前长度
                    if i + length > len(content) : break
                    # 获得子字符串
                    value = content[i : i + length]
                    # 检查结果
                    if value in self : self[value].count += item.count

    # 加载数据
    @staticmethod
    def load_dict(file_name) :
        # 检查文件名
        assert isinstance(file_name, str)
        # 检查文件是否存在
        if not os.path.isfile(file_name):
            # 打印信息
            print("DictionaryContent.load_dict : invalid file(\"%s\") !" % file_name)
            return -1
        # 打开文件
        json_file = open(file_name, "r", encoding = "utf-8")
        # 打印信息
        print("DictionaryContent.load_dict : file(\"%s\") opened !" % file_name)
        # 检查文件
        assert json_file is not None

        # 进度条
        pb = None
        # 总数
        total = 0
        # 创建对象
        dictionary = DictionaryContent()

        try:
            # 按行读取
            line = json_file.readline()
            # 循环处理
            while line :
                # 剪裁字符串
                line = line.strip()
                # 检查结果
                if len(line) <= 0:
                    # 读取下一行
                    line = json_file.readline()
                    continue

                # 检查计数器
                if pb is None :
                    # 获得数据总数
                    total = int(line)
                    # 检查结果
                    if total <= 0 :
                        # 打印信息
                        print("DictionaryContent.load_dict : invalid total(\"%s\") !" % line)
                        break
                    # 进度条
                    pb = ProgressBar(total)
                    # 打印数据总数
                    pb.begin(f"DictionaryContent.load_dict : try to load {total} row(s) !")
                else:
                    # 按照json格式解析
                    item = json.loads(line)
                    # 进度条
                    if pb is not None : pb.increase()
                    # 获得内容
                    content = item["content"]
                    # 检查数据
                    if content not in dictionary :
                        # 生成数据对象
                        new_item = dictionary.new_item(content)
                        # 设置计数
                        new_item.count = item["count"]
                        # 设置来源
                        new_item.add_source(item["source"], item["remark"])
                        # 设置数据对象
                        dictionary[content] = new_item
                    else :
                        # 检查来源
                        if isinstance(item["source"], str) :
                            # 增加来源
                            dictionary[content].add_source(item["source"], item["remark"])
                # 读取下一行
                line = json_file.readline()
            # 打印信息
            pb.end()
        except Exception as e:
            traceback.print_exc()
            print("DictionaryContent.load_dict : ", str(e))
            print("DictionaryContent.load_dict : unexpected exit !")
        # 关闭文件
        json_file.close()
        # 打印信息
        print("DictionaryContent.load_dict : file(\"%s\") closed !" % file_name)
        print("DictionaryContent.load_dict : %d item(s) loaded !" % len(dictionary))
        # 更新数据
        dictionary.update_max_length()
        # 打印信息
        print("DictionaryContent.load_dict : max length(%d) !" % dictionary.max_length)
        return dictionary
