# -*- coding: utf-8 -*-
import traceback

from container.file.ValueEnum import *

class BytesBuffer :
    # 初始化
    def __init__(self, size) :
        # 位置
        self._position = 0
        # 数组
        self._bytes = bytearray(size)

    @property
    def size(self) :
        # 返回结果
        return len(self._bytes)

    @property
    def bytes(self) :
        # 返回结果
        return self._bytes

    @bytes.setter
    def bytes(self, value) :
        # 设置数值
        self._bytes = value

    @property
    def pos(self) :
        # 返回结果
        return self._position

    @pos.setter
    def pos(self, pos) :
        # 检查参数
        assert 0 <= pos <= len(self._bytes)
        # 设置数值
        self._position = pos

    @staticmethod
    def create(size_type) :
        # 返回结果
        return BytesBuffer(SizeType.get_size(size_type))

    def put_int(self, sizeof, value, signed = False) :
        # 开始位置
        start = self._position
        # 结束位置
        end = self._position + sizeof
        # 挪动位置
        self._position = end
        # 检查
        if end > len(self._bytes) :
            raise Exception(f"end position({end}) overflow")
        # 设置数值
        self._bytes[start : end] = \
            value.to_bytes(sizeof, "big", signed = signed)

    def get_int(self, sizeof, signed = False) :
        # 开始位置
        start = self._position
        # 结束位置
        end = self._position + sizeof
        # 设置新位置
        self._position = end
        # 检查
        if end > len(self._bytes) :
            raise Exception(f"end position({end}) overflow")
        # 返回结果
        return int.from_bytes(self._bytes[start : end], "big", signed = signed)

    def put_str(self, value) :
        # 编码
        self.put_buffer(value.encode("utf-8"))

    def get_str(self) :
        # 获得字节
        return self.get_buffer().decode("utf-8")

    def put_buffer(self, value) :
        # 检查参数
        if value is None or len(value) <= 0 :
            # 保存长度
            self.put_int(SizeOf.integer, 0); return
        # 获得长度
        length = len(value)
        # 检查
        if length > SizeType.get_size(SizeType.mb64) :
            raise Exception(f"length({length}) overflow")
        # 保存长度
        self.put_int(SizeOf.integer, length)
        # 输入
        self.put_raw(value, length)

    def get_buffer(self) :
        # 获得长度
        length = self.get_int(SizeOf.integer)
        # 检查长度
        if length <= 0 : return bytearray()
        # 检查
        if length > SizeType.get_size(SizeType.mb64) :
            raise Exception(f"length({length}) overflow")
        # 返回结果
        return self.get_raw(length)

    def put_raw(self, value, length) :
        # 开始位置
        start = self._position
        # 结束位置
        end = self._position + length
        # 设置新位置
        self._position = end
        # 检查
        if end > len(self._bytes) :
            raise Exception(f"end position({end}) overflow")
        # 设置数值
        self._bytes[start : end] = value

    def get_raw(self, length) :
        # 开始位置
        start = self._position
        # 结束位置
        end = self._position + length
        # 检查
        if end > len(self._bytes) :
            raise Exception(f"end position({end}) overflow")
        # 设置新位置
        self._position = end
        # 获得字节
        return self._bytes[start : end]

    def dump(self) :
        print(f"BytesBuffer.dump : show properties !")
        print(f"\tlength = {len(self._bytes)}")
        print(f"\tposition = {self._position}")
        print(f"\tbytes = {self._bytes.hex()}")
