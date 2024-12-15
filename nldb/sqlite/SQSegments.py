# -*- coding: utf-8 -*-

from nldb.sqlite.SQContent import *

class SQSegments(SQContent) :
    # 初始化函数
    def __init__(self) :
        # 调用父类函数
        super().__init__("segments")