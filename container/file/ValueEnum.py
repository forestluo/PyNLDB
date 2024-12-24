# -*- coding: utf-8 -*-

from enum import Enum

class SizeOf(Enum) :
    byte = 1
    short = 2
    integer = 4
    long = 8
    float = 4
    double = 8

# 页面类型
class PageType(Enum) :
    invalid = 0
    head_page = 1
    free_page = 2
    root_page = 3
    data_page = 4
    queue_page = 5
    queue_element = 6
    index_page = 7
    index_element = 8

# Killo Bytes
# 1 KB = 1024 Bytes
_kb = 1024
_mb = 1024 * _kb
# Total Types
_total_types = 21

# 页面类型
class SizeType(Enum) :
    invalid = 0
    qqkb = 1
    hqkb = 2
    qkb = 3
    hkb = 4
    kb1 = 5
    kb2 = 6
    kb4 = 7
    kb8 = 8
    kb16 = 9
    kb32 = 10
    kb64 = 11
    kb128 = 12
    kb256 = 13
    kb512 = 14
    mb1 = 15
    mb2 = 16
    mb4 = 17
    mb8 = 18
    mb16 = 19
    mb32 = 20
    mb64 = 21

    @staticmethod
    def total_types() :
        # 返回结果
        return _total_types

    @staticmethod
    def get_type(size) :
        # Check result.
        if size <= _kb / 4 / 4 : return SizeType.qqKB
        elif size <= _kb / 4 / 2 : return SizeType.hqkb
        elif size <= _kb / 4 : return SizeType.qkb
        elif size <= _kb / 2 : return SizeType.hkb
        elif size <= 1 * _kb : return SizeType.kb1
        elif size <= 2 * _kb : return SizeType.kb2
        elif size <= 4 * _kb : return SizeType.kb4
        elif size <= 8 * _kb : return SizeType.kb8
        elif size <= 16 * _kb : return SizeType.kb16
        elif size <= 32 * _kb : return SizeType.kb32
        elif size <= 64 * _kb : return SizeType.kb64
        elif size <= 128 * _kb : return SizeType.kb128
        elif size <= 256 * _kb : return SizeType.kb256
        elif size <= 512 * _kb : return SizeType.kb512
        elif size <= 1 * _mb : return SizeType.mb1
        elif size <= 2 * _mb : return SizeType.mb2
        elif size <= 4 * _mb : return SizeType.mb4
        elif size <= 8 * _mb : return SizeType.mb8
        elif size <= 16 * _mb : return SizeType.mb16
        elif size <= 32 * _mb : return SizeType.mb32
        elif size <= 64 * _mb : return SizeType.mb64
        else : return None

    @staticmethod
    def get_size(size_type) :
        # 检查
        assert isinstance(size_type, SizeType)
        # 获得数值
        value = size_type.value
        # 获得数值
        if value <= 0 :
            raise Exception(f"unknown size type({size_type})")
        elif value <= 4 :
            return 64 << (value - 1)
        elif value <= 14 :
            return 1024 << (value - 5)
        elif value <= 21 :
            return 1048576 << (value - 15)
        else :
            raise Exception(f"unknown size type({size_type})")

class PageOffset(Enum) :
    none = 0xFFFFFFFF

    @staticmethod
    def e2v(value) :
        if value != PageOffset.none :
            return (value >> 6) & 0xFFFFFFFF
        return PageOffset.none.value

    @staticmethod
    def v2e(value) :
        if value == PageOffset.none.value :
            return PageOffset.none
        return (value & 0xFFFFFFFFFFFFFFFF) << 6

class Capacity(Enum) :
    without_limit = 0xFFFFFFFF

    @staticmethod
    def e2v(value) :
        if value == Capacity.without_limit :
            return Capacity.without_limit.value
        return value

    @staticmethod
    def v2e(value) :
        if value == Capacity.without_limit.value :
            return Capacity.without_limit
        return value

class OccupiedSize(Enum) :
    full = 0xFFFFFFFF

    @staticmethod
    def e2v(value) :
        if value == OccupiedSize.full :
            return OccupiedSize.full.value
        return value

    @staticmethod
    def v2e(value) :
        if value == OccupiedSize.full.value :
            return OccupiedSize.full
        return value

class SafelyClosed(Enum) :
    closed = 0
    opened = 1

    @staticmethod
    def e2v(value) :
        if value == SafelyClosed.closed :
            return SafelyClosed.closed.value
        elif value == SafelyClosed.opened :
            return SafelyClosed.opened.value
        raise Exception(f"invalid safely closed({value})")

    @staticmethod
    def v2e(value) :
        if value == SafelyClosed.closed.value :
            return SafelyClosed.closed
        elif value == SafelyClosed.opened.value :
            return SafelyClosed.opened
        raise Exception(f"invalid safely closed({value})")
