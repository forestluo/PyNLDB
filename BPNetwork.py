# -*- coding: utf-8 -*-

import os
import math
import random
import traceback

from ContentTool import *

class Neuron :
    # 初始化
    def __init__(self, input_count = 2, output_count = 1, hidden_count = 2, learning_rate = 0.008) :
        # 检查参数
        assert 0.000001 <= learning_rate <= 1.0
        assert input_count > 1 and output_count > 0 and hidden_count > 1

        # 学习率
        # 范围一般在0.000001至1.0之间
        self.__learning_rate = learning_rate

        # 输入层
        self.__input_count = input_count
        self.__inputs = [0.0] * input_count
        # 输出层
        self.__output_count = output_count
        self.__outputs = [0.0] * output_count
        # 隐藏层
        self.__hidden_count = hidden_count
        self.__hiddens = [0.0] * hidden_count

        # 误差数据
        self.__errors = [0.0] * output_count
        self.__deltas = [0.0] * output_count

        # 偏置数据
        self.__input_biases = [0.0] * hidden_count
        # 权重数据
        self.__input_weights = \
            [[0.0 for i in range(input_count)] for j in range(hidden_count)]

        # 偏置数据
        self.__output_biases = [0.0] * output_count
        # 权重数据
        self.__output_weights = \
            [[0.0 for i in range(hidden_count)] for j in range(output_count)]

        # 随机给定一个初始值
        for i in range(input_count) :
            self.__inputs[i] = random.random()
        for i in range(output_count) :
            self.__outputs[i] = random.random()
        for i in range(hidden_count) :
            for j in range(input_count) :
                self.__input_weights[i][j] = random.random()
        for i in range(output_count) :
            for j in range(hidden_count) :
                self.__output_weights[i][j] = random.random()

    @property
    def input_count(self) :
        # 返回结果
        return self.__input_count

    @property
    def output_count(self) :
        # 返回结果
        return self.__output_count

    @property
    def hidden_count(self) :
        # 返回结果
        return self.__hidden_count

    @property
    def learning_rate(self) :
        # 返回结果
        return self.__learning_rate

    @learning_rate.setter
    def learning_rate(self, value) :
        # 检查参数
        assert 0.000001 <= value <= 1.0
        # 设置数值
        self.__learning_rate = value

    @property
    def inputs(self) :
        # 返回结果
        return self.__inputs.copy()

    @inputs.setter
    def inputs(self, values) :
        # 检查参数
        assert isinstance(values, list)
        assert len(values) == self.__input_count
        # 拷贝参数
        for i in range(self.__input_count) : self.__inputs[i] = values[i]

    @property
    def outputs(self) :
        # 返回结果
        return self.__outputs.copy()

    @outputs.setter
    def outputs(self, values) :
        # 检查参数
        assert isinstance(values, list)
        assert len(values) == self.__output_count
        # 计算误差
        for i in range(self.__output_count) : self.__errors[i] = values[i] - self.__outputs[i]

    @property
    def error(self) :
        # 结果
        result = 0.0
        # 循环处理
        for i in range(self.__output_count) : result += 0.5 * self.__errors[i] ** 2
        # 返回结果
        return result

    def set_input_paras(self, input_biases, input_weights) :
        # 检查参数
        assert input_biases is not None
        assert len(input_biases) == self.__input_count
        assert input_weights is not None
        assert len(input_weights) == self.__hidden_count
        for i in range(len(input_weights)) :
            assert len(input_weights[i]) == self.__input_count
        # 设置输入参数
        self.__input_biases = input_biases
        self.__input_weights = input_weights

    def set_output_paras(self, output_biases, output_weights) :
        # 检查参数
        assert output_biases is not None
        assert len(output_biases) == self.__output_count
        assert output_weights is not None
        assert len(output_weights) == self.__output_count
        for i in range(len(output_weights)) :
            assert len(output_weights[i]) == self.__hidden_count
        # 设置输入参数
        self.__output_biases = output_biases
        self.__output_weights = output_weights

    # 向前传播
    def forward(self) :
        # 计算隐藏层数据
        for i in range(self.__hidden_count) :
            # 数值
            value = 0.0
            # 循环处理
            for j in range(self.__input_count) :
                value += self.__input_weights[i][j] * self.__inputs[j]
            # 设置输出值
            self.__hiddens[i] = Neuron.__sigmoid__(value + self.__input_biases[i])

        # 计算输出层数据
        for i in range(self.__output_count) :
            # 数值
            value = 0.0
            # 循环处理
            for j in range(self.__hidden_count) :
                value += self.__output_weights[i][j] * self.__hiddens[j]
            # 设置输出值
            self.__outputs[i] = Neuron.__sigmoid__(value + self.__output_biases[i])

    # 后向传播
    def backward(self) :
        # 计算隐层
        for i in range(self.__output_count) :
            # 链式反应
            delta = - self.__errors[i]
            # 链式反应
            delta *= Neuron.__delta_sigmoid__(self.__outputs[i])
            # 设置误差
            self.__deltas[i] = delta
            # 设置新的偏置
            # 与学习率有关
            self.__output_biases[i] -= self.__learning_rate * delta
            # 循环处理
            for j in range(self.__hidden_count) :
                # 设置新的权重
                # 与学习率有关
                self.__output_weights[i][j] -= self.__learning_rate * delta * self.__hiddens[j]

        # 计算输入层
        for i in range(self.__hidden_count) :
            # 链式反应
            delta = 0.0
            # 循环处理
            for j in range(self.__output_count) :
                # 链式反应
                delta += self.__output_weights[j][i] * self.__deltas[j]
            # 链式反应
            delta *= Neuron.__delta_sigmoid__(self.__hiddens[i])
            # 与学习率有关
            # 设置新的偏置
            self.__input_biases[i] -= self.__learning_rate * delta
            # 循环处理
            for j in range(self.__input_count) :
                # 设置新的权重
                # 与学习率有关
                self.__input_weights[i][j] -= self.__learning_rate * delta * self.__inputs[j]

    def save(self, file_name):
        # 检查文件名
        if file_name is None:
            file_name = "neuron.json"
        # 打开文件
        json_file = open(file_name, "w", encoding = "utf-8")
        # 打印信息
        print("Neuron.save : file(\"%s\") opened !" % file_name)
        # 检查文件
        assert json_file is not None
        # 数据项
        item = \
            {
                "learning_rate" : self.__learning_rate,
                "input_count" : self.__input_count,
                "output_count" : self.__output_count,
                "hidden_count" : self.__hidden_count,
                "input_biases" : self.__input_biases,
                "input_weights" : self.__input_weights,
                "output_biases" : self.__output_biases,
                "output_weights" : self.__output_weights,
            }
        # 写入文件
        json_file.write(json.dumps(item, ensure_ascii = False))
        json_file.write("\n")
        # 关闭文件
        json_file.close()
        # 打印信息
        print("Neuron.save : file(\"%s\") closed !" % file_name)

    # 加载数据
    def load(self, file_name):
        # 检查文件名
        if file_name is None:
            file_name = "neuron.json"
        # 检查文件是否存在
        if not os.path.isfile(file_name):
            # 打印信息
            print("Neuron.load : invalid file(\"%s\") !" % file_name)
            return -1
        # 打开文件
        json_file = open(file_name, "r", encoding = "utf-8")
        # 打印信息
        print("Neuron.load : file(\"%s\") opened !" % file_name)
        # 检查文件
        assert json_file is not None

        try:
            # 按行读取
            line = json_file.readline()
            # 剪裁字符串
            line = line.strip()
            # 检查结果
            if len(line) <= 0: return False
            # 按照json格式解析
            item = json.loads(line)
            # 设置参数
            self.__learning_rate = item["learning_rate"]
            self.__input_count = item["input_count"]
            self.__inputs = [0.0] * self.__input_count
            self.__output_count = item["output_count"]
            self.__outputs = [0.0] * self.__output_count
            self.__hidden_count = item["hidden_count"]
            self.__hiddens = [0.0] * self.__hidden_count
            self.__input_biases = item["input_biases"]
            self.__input_weights = item["input_weights"]
            self.__output_biases = item["output_biases"]
            self.__output_weights = item["output_weights"]
        except Exception as e:
            traceback.print_exc()
            print("Neuron.load : ", str(e))
            print("Neuron.load : unexpected exit !")
        # 关闭文件
        json_file.close()
        # 打印信息
        print("Neuron.load : file(\"%s\") closed !" % file_name)

    def dump(self) :
        # 检查参数
        assert self.__errors is not None
        assert self.__deltas is not None
        assert self.__inputs is not None
        assert self.__outputs is not None
        assert self.__hiddens is not None
        assert self.__input_biases is not None
        assert self.__input_weights is not None
        assert self.__output_biases is not None
        assert self.__output_weights is not None

        print("Neuron.dump : print properties !")
        print("\t", end = "")
        print("__input_count = %d" % self.__input_count)
        print("\t", end = "")
        print("__output_count = %d" % self.__output_count)
        print("\t", end = "")
        print("__hidden_count = %d" % self.__hidden_count)
        print("\t", end = "")
        print("__learning_rate = %f" % self.__learning_rate)
        # 打印输入端数据
        for i in range(self.__hidden_count) :
            print("\t", end = "")
            print("__input_biases[%d] = %f" % (i, self.__input_biases[i]))
        for i in range(self.__hidden_count) :
            for j in range(self.__input_count) :
                print("\t", end = "")
                print("__input_weights[%d][%d] = %f" % (i,j, self.__input_weights[i][j]))
        # 打印输出端数据
        for i in range(self.__output_count) :
            print("\t", end = "")
            print("__output_biases[%d] = %f" % (i, self.__output_biases[i]))
        for i in range(self.__output_count) :
            for j in range(self.__hidden_count) :
                print("\t", end = "")
                print("__output_weights[%d][%d] = %f" % (i, j, self.__output_weights[i][j]))

    @staticmethod
    def __delta_sigmoid__(x) :
        # 计算数值
        value = Neuron.__sigmoid__(x)
        # 返回结果
        return value * (1.0 - value)

    @staticmethod
    def __sigmoid__(x) :
        # 防止溢出
        if x > 20 : return 1.0
        if x < -20 : return 0.0
        # 返回结果
        return 1.0 / (1.0 + math.exp(-x))

    # 设置缺省数值，用于标定程序
    @staticmethod
    def example_case() :
        # 设置输入参数
        input_biases = [0.55, 0.56]
        input_weights = [[0.1, 0.2],[0.3, 0.4]]
        # 设置输出权重
        output_biases = [0.66, 0.67]
        output_weights = [[0.5, 0.6],[0.7, 0.8]]
        # 生成对象
        neuron = Neuron(2, 2, 2, 0.5)
        # 设置输入
        neuron.set_input_paras(input_biases, input_weights)
        # 设置输出
        neuron.set_output_paras(output_biases, output_weights)

        # 设置标定用数值
        inputs = [0.1, 0.2]
        expects = [0.01, 0.99]

        # 设置输入值
        neuron.inputs = inputs
        # 计算一次正向传播
        neuron.forward()
        # 获得输出值
        outputs = neuron.outputs

        # 打印信息
        print("BPNetwork.example_case : print results !")
        # 打印输出值
        # outputs[0] = 0.7989476413779711
        # outputs[1] = 0.8390480283342561
        print("\t", end = "")
        print("outputs[0] = %f" % outputs[0])
        print("\t", end = "")
        print("outputs[1] = %f" % outputs[1])
        # 设置预期数值
        neuron.outputs = expects
        # 打印误差
        # error = 0.3226124392928197
        print("\t", end = "")
        print("error = %f" % neuron.error)
        # 计算一次反向传播
        neuron.backward()
        # 打印信息
        # neuron.dump()
        """
        Neuron.dump : print properties !
            __input_count = 2
            __output_count = 1
            __hidden_count = 2
            __learning_rate = 0.008000
            __input_biases[0] = 0.000000
            __input_biases[1] = 0.000000
            __input_weights[0][0] = 0.093242
            __input_weights[0][1] = 0.060770
            __input_weights[1][0] = 0.966417
            __input_weights[1][1] = 0.869598
            __output_biases[0] = 0.000000
            __output_weights[0][0] = 0.033377
            __output_weights[0][1] = 0.693605
        """

def main() :

    # 创建对象
    neuron = Neuron()
    # 执行标定例程
    neuron.example_case()
    # 打印信息
    neuron.dump()

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("OperateData.main :__main__ : ", str(e))
        print("OperateData.main :__main__ : unexpected exit !")
