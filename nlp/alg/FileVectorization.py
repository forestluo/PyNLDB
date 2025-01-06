# -*- coding: utf-8 -*-
import os
import traceback

from widget.ProgressBar import *

from nlp.alg.WordVector import *
from nlp.content.WordContent import *
from container.file.DataContainer import *

class FileVectorization(WordVector) :
    # 文件名
    file_name = "..\\..\\db\\data.bin"

    # 初始化
    def __init__(self, dimension) :
        # 调用父类初始化
        super().__init__(dimension)
        # 打开文件
        try :
            # 数据库链接
            self.__container = DataContainer()
            # 打开文件
            # 按照缺省文件名
            self.__container.open(FileVectorization.file_name)
            # 循环处理
            for i in range(1, 9) :
                # 创建索引
                self.__container.create_index(i)
        except Exception as ex :
            traceback.print_exc()
            print("FileVectorization.__init__ : ", str(ex))
            print("FileVectorization.__init__ : unexpected exit !")

    # 析构
    def __del__(self) :
        # 调用父类函数
        super().__del__()
        # 关闭数据库连接
        self.__container.close()
        # 打印信息
        print(f"FileVectorization.__del__ : "
            f"file container has been closed !")

    @property
    def wsize(self) :
        try :
            # 计数器
            total = 0
            # 循环处理
            for i in range(1, 9) :
                # 创建索引
                count = self.__container.index_count(i)
                # 检查结果
                if not isinstance(count, int) :
                    raise Exception(f"invalid count({count}) of index({i})")
                # 求和
                total += count
            # 返回结果
            return total
        except Exception as ex :
            traceback.print_exc()
            print("FileVectorization.wsize : ", str(ex))
            print("FileVectorization.wsize : unexpected exit !")
        return -1

    # 获得计数
    def get_count(self, key) :
        try :
            # 获得长度
            length = len(key)
            # 检查
            if 1 <= length <= 8 :
                # 获得结果
                count = self.__container.\
                    load_index(length, key)
                # 返回结果
                return count if count is not None else -1
        except Exception as ex :
            traceback.print_exc()
            print("FileVectorization.get_count : ", str(ex))
            print("FileVectorization.get_count : unexpected exit !")
        return -1

    def set_count(self, key, count) :
        try :
            # 获得长度
            length = len(key)
            # 检查
            if 1 <= length <= 8 :
                # 获得结果
                self.__container.\
                    save_index(length, key, count)
        except Exception as ex :
            traceback.print_exc()
            print("FileVectorization.set_count : ", str(ex))
            print("FileVectorization.set_count : unexpected exit !")

    # 获得相关系数
    # 速度慢，但能兼容多数内容
    def get_gammas(self, error) :
        # 重建索引
        self.index_vectors()
        # 结束
        print(f"FileVectorization.get_gammas : finished reindexing vectors !")

        # 创建矩阵
        gammas = self._new_gamma()
        # 进度条
        pb = ProgressBar(self.vsize * self.vsize)
        # 开始
        pb.begin(f"FileVectorization.get_gammas : building matrix !")
        # 初始化相关系数
        for v1 in self.vectors() :
            # 检查项目
            if v1.count <= 0 :
                # 增加计数
                pb.increase(self.vsize)
                continue
            # 循环处理
            for v2 in self.vectors() :
                # 进度条
                pb.increase()
                # 检查项目
                if v2.count <= 0 : continue

                # 获得计数
                count = self.get_count(v1.content + v2.content)
                # 检查数值
                if count <= 0 : continue

                # 计算数值
                gamma = 0.5 * float(count) * \
                    (1.0 / float(v1.count) + 1.0 / float(v2.count))
                # 设置数值
                gammas[0][v1.index][v2.index] = gamma
                # 检查结果
                if gamma > error : gammas[1][v1.index][v2.index] = 1.0
        # 结束
        pb.end(f"FileVectorization.get_gammas : finished building matrix !")
        # 返回结果
        return gammas

    # 保存数据
    def save_gammas(self, file_name) :
        # 重建索引
        self.index_vectors()
        # 结束
        print(f"FileVectorization.save_gammas : finished reindexing vectors !")

        # 新建
        words = WordContent()
        # 进度条
        pb = ProgressBar(self.vsize * self.vsize)
        # 开始
        pb.begin(f"FileVectorization.save_gammas : building matrix !")
        # 初始化相关系数
        for v1 in self.vectors() :
            # 检查项目
            if v1.count <= 0 : continue
            # 循环处理
            for v2 in self.vectors() :
                # 检查项目
                if v2.count <= 0 : continue

                # 获得内容
                content = \
                    v1.content + v2.content
                # 获得计数
                count = self.get_count(content)
                # 检查数值
                if count <= 0 : continue

                # 进度条
                pb.increase()
                # 计算数值
                gamma = 0.5 * float(count) * \
                        (1.0 / float(v1.count) + 1.0 / float(v2.count))
                # 检查结果
                if content not in words :
                    # 新建项目
                    item = words.new_item(content, count)
                    # 计算数值
                    item.gamma = gamma
                    # 增加项目
                    words.add_item(item)
                else :
                    # 获得项目
                    item = words[content]
                    # 检查数值
                    if item.gamma < gamma : item.gamma = gamma
        # 结束
        pb.end(f"FileVectorization.save_gammas : finished building matrix !")
        # 保存
        words.save(file_name)
        # 结束
        print(f"FileVectorization.save_gammas : file({file_name}) was saved !")

# 测试代码
def main() :
    # 检查
    if os.path.isfile(FileVectorization.file_name) :
        # 删除原有文件
        os.remove(FileVectorization.file_name)
        # 打印
        print(f"FileVectorization.main : file({FileVectorization.file_name}) removed !")
    # 生成对象
    fv = FileVectorization(32)
    # 创建
    words = WordContent()
    # 循环处理
    for i in range(1, 3) :
        # 加载文件
        if words.load(f"..\\..\\json\\words{i}.json") <= 0 :
            print(f"FileVectorization.main : fail to load file !")
            return
        # 进度条
        pb = ProgressBar(len(words))
        # 开始
        pb.begin(f"FileVectorization.main : try to save data !")
        # 循环处理
        for item in words.values() :
            # 进度条
            pb.increase()
            # 保存数据
            fv.set_count(item.content, item.count)
        # 结束
        pb.end()

        # 进度条
        pb = ProgressBar(len(words))
        # 开始
        pb.begin(f"FileVectorization.main : try to verify data !")
        # 循环处理
        for item in words.values() :
            # 进度条
            pb.increase()
            # 保存数据
            count = fv.get_count(item.content)
            # 检查结果
            if count != item.count :
                print(f"\tincorrect item(\"{item.content}\", {item.count}) = {count}")
        # 结束
        pb.end()

        # 清理
        words.clear()

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("FileVectorization.main :__main__ : ", str(e))
        print("FileVectorization.main :__main__ : unexpected exit !")