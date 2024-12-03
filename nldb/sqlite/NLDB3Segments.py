# -*- coding: utf-8 -*-

from nldb.sqlite.NLDB3Content import *

class NLDB3Segments(NLDB3Content) :
    # 初始化函数
    def __init__(self) :
        # 调用父类函数
        super().__init__("segments")