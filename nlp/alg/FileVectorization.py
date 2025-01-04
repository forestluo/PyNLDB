# -*- coding: utf-8 -*-
import traceback

from widget.ProgressBar import *

from nlp.alg.WordVector import *
from nlp.content.WordContent import *
from container.file.DataContainer import *

class FileVectorization(WordVector) :
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
            self.__container.open("..\\..\\db\\data.bin")
            # 创建索引
            self.__container.create_index(1)
        except Exception as ex :
            traceback.print_exc()
            print("FileVectorization.__init__ : ", str(e))
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
            # 获得结果
            count = self.__container.index_count(1)
            # 返回结果
            return count if count is not None else -1
        except Exception as ex :
            traceback.print_exc()
            print("FileVectorization.wsize : ", str(e))
            print("FileVectorization.wsize : unexpected exit !")
        return -1

    # 获得计数
    def get_count(self, key) :
        try :
            # 获得结果
            count = self.__container.\
                load_index(1, key)
            # 返回结果
            return count if count is not None else -1
        except Exception as ex :
            traceback.print_exc()
            print("FileVectorization.get_count : ", str(e))
            print("FileVectorization.get_count : unexpected exit !")
        return -1

    def set_count(self, key, count) :
        try :
            # 获得结果
            count = self.__container.\
                save_index(1, key, count)
        except Exception as ex :
            traceback.print_exc()
            print("FileVectorization.set_count : ", str(e))
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

    # 生成对象
    fv = FileVectorization(32)
    # 检查数量
    if fv.wsize <= 0 :
        # 创建
        words = WordContent()
        # 循环处理
        for i in range(8) :
            # 加载文件
            if words.load(f"..\\..\\json\\words{i + 1}.json") <= 0 :
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
    # 选项
    # 加载数据
    if fv.load_vectors("..\\..\\json\\vectors.json", False) <= 0 :
        # 打印信息
        print("FileVectorization.main : fail to load vectors.json !")
        return
    """
    # 加载数据
    if fv.load_vectors("..\\..\\json\\cores.json", False) <= 0 :
        # 打印信息
        print("FileVectorization.main : fail to load cores.json !")
        return
    """
    # 打印信息
    print("FileVectorization.main : successfully loaded !")
    # 获得求解器
    solution = fv.get_solution("cupy.l2")
    # 检查结果
    if solution is None :
        # 打印信息
        print("FileVectorization.main : fail to get solution !")
        return
    # 启动
    solution.start()
    # 打印信息
    print("FileVectorization.main : successfully start solving !")
    # 等待输入
    input()
    # 结束线程
    solution.stop()
    # 打印信息
    print("FileVectorization.main : successfully stopped solving !")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("FileVectorization.main :__main__ : ", str(e))
        print("FileVectorization.main :__main__ : unexpected exit !")