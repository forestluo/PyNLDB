# -*- coding: utf-8 -*-
import hashlib

from container.file.ValueEnum import *
from container.file.PageBuffer import *

class IndexData :
    ##################################################
    #
    # Offsets.
    #
    # Key             [long] * 2 = 128bit
    # Data Value      [int]
    # Subnode Offset  [int]
    #
    ##################################################
    size = 2 * SizeOf.long + 2 * SizeOf.integer

    # 初始化
    def __init__(self) :
        # 设置参数
        # 临时参数
        self.offset = -1

        # 设置关键字
        self.key = None
        # 设置数据偏移量
        self.data_value = -1
        # 设置子节点偏移量
        self.subnode_offset = -1

    def has_key(self, key) :
        # 返回结果
        return self.valid and self.key == key

    @property
    def valid(self) :
        # 检查
        if self.key is None : return False
        # 返回结果
        return False \
            if self.key == IndexTool.invalid_key else True

    def wrap(self, buffer) :
        # 检查
        if self.key is not None :
            buffer.put_raw(self.key, 16)
        else :
            buffer.put_raw(IndexTool.invalid_key, 16)
        buffer.put_int(SizeOf.integer, self.data_value, True)
        buffer.put_int(SizeOf.integer, PageOffset.l2i(self.subnode_offset))

    def unwrap(self, buffer) :
        # 获得数据
        self.key = buffer.get_raw(16)
        # 检查
        if self.key == IndexTool.invalid_key : self.key = None
        self.data_value = buffer.get_int(SizeOf.integer, True)
        self.subnode_offset = PageOffset.i2l(buffer.get_int(SizeOf.integer))

    def check_valid(self, data_size) :
        PageOffset.check_offset(self.subnode_offset, data_size)

    def dump(self) :
        print(f"IndexData.dump : show properties !")
        if self.key is not None :
            print(f"\tkey = 0x{self.__key.hex()}")
        print(f"\tdata_value = {self.data_value}")
        print(f"\tsubnode_offset = {self.subnode_offset}")

class IndexTool :
    # Invalid Key
    invalid_key = bytearray(b'\xFF' * 16)

    @staticmethod
    def get_int(key) :
        # 返回结果
        return int.from_bytes(key,"big")

    @staticmethod
    def md5(value) :
        # 检查
        if not isinstance(value, str) :
            # 转换为字符串
            value = str(value)
        # 设置数值
        _md5 = hashlib.md5(value.encode("utf-8"))
        # 返回字节
        return bytearray.fromhex(_md5.hexdigest())

    @staticmethod
    def get_reminder(key, prime) :
        # 返回结果
        return int.from_bytes(key, "big") % prime

    @staticmethod
    def get_size_type(level) :
        # 返回结果
        return SizeType.kb1 + level

    @staticmethod
    def get_data_index(key, level) :
        # 尺寸类型
        size_type = \
            IndexTool.get_size_type(level)
        # 返回结果
        return IndexTool.get_index(key, size_type)

    @staticmethod
    def get_data_offset(key, level) :
        # 返回结果
        return PageBuffer.description_size + SizeOf.integer + \
            IndexTool.get_data_index(key, level) * IndexData.size

    @staticmethod
    def get_subnode_count(size_type) :
        # Index Element Page
        # 检查
        if size_type == SizeType.kb1 :
            return 41 # 空余30
        elif size_type == SizeType.kb2 :
            return 83 # 空余46
        elif size_type == SizeType.kb4 :
            return 167 # 空余78
        elif size_type == SizeType.kb8 :
            return 337 # 空余94
        elif size_type == SizeType.kb16 :
            return 667 # 空余126
        elif size_type == SizeType.kb32 :
            return 1361 # 空余94
        elif size_type == SizeType.kb64 :
            return 2729 # 空余30
        elif size_type == SizeType.kb128 :
            return 5449 # 空余286
        elif size_type == SizeType.kb256 :
            return 10909 # 空余318
        elif size_type == SizeType.kb512 :
            return 21841 # 空余94
        # Index Buffer Page
        # 检查
        if size_type == SizeType.mb1 :
            return 43689 # 3 * 14563
        elif size_type == SizeType.mb2 :
            return 87380 # 2 * 2 * 5 * 17
        elif size_type == SizeType.mb4 :
            return 174761
        elif size_type == SizeType.mb8 :
            return 349524 # 2 * 2 * 3 * 3 * 7 * 19 * 73
        elif size_type == SizeType.mb16 :
            return 699049 # 13 * 53773
        elif size_type == SizeType.mb32 :
            return 1398100 # 2 * 2 * 5 * 5 * 11 * 31 * 41
        elif size_type == SizeType.mb64 :
            return 2796201 # 3 * 3 * 3 * 3 * 3 * 37 * 311
        # 抛出异常
        raise Exception(f"unsupported size type({size_type})")

    @staticmethod
    def get_index(key, size_type) :
        # 返回结果
        return IndexTool.get_int(key) % IndexTool.get_subnode_count(size_type)
