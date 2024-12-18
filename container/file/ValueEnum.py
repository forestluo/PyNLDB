# -*- coding: utf-8 -*-

from enum import Enum

class NextPage(Enum) :
    none = 0xFFFFFFFF

class Capacity(Enum) :
    without_limit = -1

class SafelyClosed(Enum) :
    closed = 0
    opened = 1

    @staticmethod
    def is_valid(value) :
        if isinstance(value, SafelyClosed) :
            return True
        # 返回结果
        return 0 <= value <= 1

    @staticmethod
    def get_type(value) :
        if value == SafelyClosed.closed.value :
            return SafelyClosed.closed
        elif value == SafelyClosed.opened.value :
            return SafelyClosed.opened
        return None

class OccupiedSize(Enum) :
    full = 0xFFFFFFFF

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
    data_page = 3
    queue_page = 4
    queue_element = 5
    index_page = 6
    index_element = 7

    @staticmethod
    def is_valid(page_type) :
        # 返回结果
        return 1 <= page_type.value <= 7

# Killo Bytes
# 1 KB = 1024 Bytes
__kb = 1024
__mb = 1024 * __kb

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

    __total_types = 21

    @staticmethod
    def total_types() :
        # 返回结果
        return SizeType.__total_types

    @staticmethod
    def is_valid(size_type) :
        # 返回结果
        return 1 <= size_type.value <= 21

    @staticmethod
    def get_type(size) :
        # Check result.
        if size <= __kb / 4 / 4 : return SizeType.qqKB
        elif size <= __kb / 4 / 2 : return SizeType.hqkb
        elif size <= __kb / 4 : return SizeType.qkb
        elif size <= __kb / 2 : return SizeType.hkb
        elif size <= 1 * __kb : return SizeType.kb1
        elif size <= 2 * __kb : return SizeType.kb2
        elif size <= 4 * __kb : return SizeType.kb4
        elif size <= 8 * __kb : return SizeType.kb8
        elif size <= 16 * __kb : return SizeType.kb16
        elif size <= 32 * __kb : return SizeType.kb32
        elif size <= 64 * __kb : return SizeType.kb64
        elif size <= 128 * __kb : return SizeType.kb128
        elif size <= 256 * __kb : return SizeType.kb256
        elif size <= 512 * __kb : return SizeType.kb512
        elif size <= 1 * __mb : return SizeType.mb1
        elif size <= 2 * __mb : return SizeType.mb2
        elif size <= 4 * __mb : return SizeType.mb4
        elif size <= 8 * __mb : return SizeType.mb8
        elif size <= 16 * __mb : return SizeType.mb16
        elif size <= 32 * __mb : return SizeType.mb32
        elif size <= 64 * __mb : return SizeType.mb64
        else : return None

    @staticmethod
    def get_size(size_type) :
        assert isinstance(size_type, SizeType)
        # 获得数值
        value = size_type.value
        # 获得数值
        if value <= 0 :
            raise Exception(f"unknown type({size_type})")
        elif value <= 4 :
            return 64 << (value - 1)
        elif value <= 14 :
            return 1024 << (value - 5)
        elif value <= 21 :
            return 1048576 << (value - 15)
        else :
            raise Exception(f"unknown type({size_type})")
