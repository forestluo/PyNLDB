# -*- coding: utf-8 -*-
import traceback

from container.file.ValueEnum import *

class BytesBuffer :
    # 初始化
    def __init__(self) :
        # 位置
        self._position = 0
        # 数组
        self._bytes = bytearray()

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

    def put_int(self, sizeof, value, signed = False) :
        # 检查参数
        assert isinstance(sizeof, SizeOf)
        # 挪动位置
        self._position += sizeof.value
        # 加入字节
        self._bytes.extend(value.to_bytes(sizeof.value, "big", signed = signed))

    def get_int(self, sizeof, signed = False) :
        # 检查参数
        assert isinstance(sizeof, SizeOf)
        # 开始位置
        start = self._position
        # 结束位置
        end = self._position + sizeof.value
        # 设置新位置
        self._position = end
        # 检查
        if end > len(self._bytes) :
            raise Exception(f"end position({end}) overflow")
        # 返回结果
        return int.from_bytes(self._bytes[start : end], "big", signed = signed)

    def put_str(self, value) :
        # 检查参数
        if value is None or len(value) <= 0 :
            self.put_int(SizeOf.short, 0)
            #self._bytes.extend("".encode("utf-8"))
        else :
            value = value.encode("utf-8"); length = len(value)
            # 检查
            if length > 65535 :
                raise Exception(f"string length({length}) overflow")
            self.put_int(SizeOf.short, length); self._bytes.extend(value)

    def get_str(self) :
        # 获得长度
        length = self.get_int(SizeOf.short)
        # 检查长度
        if length == 0 : return ""
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
        return self._bytes[start : end].decode("utf-8")

    def put_buffer(self, value) :
        # 检查参数
        if value is None or len(value) <= 0 :
            self.put_int(SizeOf.integer, 0)
        else :
            length = len(value)
            # 检查
            if length > SizeType.get_size(SizeType.mb64) :
                raise Exception(f"bytes length({length}) overflow")
            self.put_int(SizeOf.integer, length); self._bytes.extend(value)

    def get_buffer(self) :
        # 获得长度
        length = self.get_int(SizeOf.integer)
        # 检查长度
        if length == 0 : return []
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


def main() :
    # 新建
    buffer = BytesBuffer()
    # 增加
    buffer.put_int(SizeOf.byte,0x01)
    buffer.put_int(SizeOf.short,0x0203)
    buffer.put_int(SizeOf.integer,0x04050607)
    buffer.put_int(SizeOf.long,0x08090a0b0c0d0e0f)
    buffer.put_int(SizeOf.integer, -1, True)
    buffer.put_str("")
    buffer.put_str("你好！Hello World !")
    # 设置位置
    buffer.pos = 0
    # 获得
    print(f"0x{buffer.get_int(SizeOf.byte):02x}")
    print(f"0x{buffer.get_int(SizeOf.short):04x}")
    print(f"0x{buffer.get_int(SizeOf.integer):08x}")
    print(f"0x{buffer.get_int(SizeOf.long):016x}")
    print(f"{buffer.get_int(SizeOf.integer, True)}")
    print(f"{buffer.get_str()}")
    print(f"{buffer.get_str()}")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("BytesBuffer.main :__main__ : ", str(e))
        print("BytesBuffer.main :__main__ : unexpected exit !")