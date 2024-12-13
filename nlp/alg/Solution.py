# -*- coding: utf-8 -*-
import traceback

from threading import Thread

class Solution(Thread) :
    # 初始化
    def __init__(self) :
        # 调用父类初始化
        super().__init__()
        # 主动中断循环
        self._break_loop = False

    def start(self) :
        # 启动线程
        if not self.is_alive() :
            # 启动线程
            super().start()
            # 打印信息
            print(f"Solution.start : thread startup !")
        else :
            # 打印信息
            print(f"Solution.start : fail to startup thread !")

    def stop(self) :
        # 检查参数
        if self.is_alive() :
            # 设置标记
            self._break_loop = True
            # 打印信息
            print(f"Solution.stop : flag was set !")
            # 等待结束
            self.wait()
            # 打印信息
            print(f"Solution.stop : finish waiting !")
        else :
            # 打印信息
            print(f"Solution.stop : thread already stopped !")

    # 等待线程结束
    def wait(self) :
        # 尝试
        try :
            # 检查线程
            if self.is_alive() :
                # 等待线程结束
                self.join()
                # 设置标记
                self._break_loop = False
                # 打印信息
                print(f"Solution.wait : thread stopped !")
            else :
                # 打印信息
                print(f"Solution.wait : thread not running !")
        except Exception as e:
            traceback.print_exc()
            print("Solution.run : ", str(e))
            print("Solution.run : unexpected exit !")

    # 执行函数
    def _run(self) :
        # 设置标记
        self._break_loop = True
        # 打印信息
        print(f"Solution._run : do nothing !")

    # 执行函数
    def run(self) :
        # 异常处理
        try :
            # 打印信息
            print(f"Solution.run : thread is running !")
            # 调用函数
            self._run()
            # 打印信息
            print(f"Solution.run : thread finished running !")
        except Exception as e :
            traceback.print_exc()
            print("Solution.run : ", str(e))
            print("Solution.run : unexpected exit !")
        # 设置标记
        self._break_loop = False
        # 打印信息
        print(f"Solution.run : thread has been stopped !")

