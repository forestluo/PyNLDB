# -*- coding: utf-8 -*-

class SizeOf :
    byte = 1
    short = 2
    integer = 4
    long = 8
    float = 4
    double = 8

# 页面类型
class SizeType :
    # Killo Bytes
    # 1 KB = 1024 Bytes
    _kb = 1024
    _mb = 1024 * _kb
    # Total Types
    _total_types = 21

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
        return SizeType._total_types

    @staticmethod
    def is_valid(size_type) :
        # 返回结果
        return 0 <= size_type <= 21

    @staticmethod
    def get_type(size) :
        # Check result.
        if size <= SizeType._kb / 4 / 4 : return SizeType.qqkb
        elif size <= SizeType._kb / 4 / 2 : return SizeType.hqkb
        elif size <= SizeType._kb / 4 : return SizeType.qkb
        elif size <= SizeType._kb / 2 : return SizeType.hkb
        elif size <= 1 * SizeType._kb : return SizeType.kb1
        elif size <= 2 * SizeType._kb : return SizeType.kb2
        elif size <= 4 * SizeType._kb : return SizeType.kb4
        elif size <= 8 * SizeType._kb : return SizeType.kb8
        elif size <= 16 * SizeType._kb : return SizeType.kb16
        elif size <= 32 * SizeType._kb : return SizeType.kb32
        elif size <= 64 * SizeType._kb : return SizeType.kb64
        elif size <= 128 * SizeType._kb : return SizeType.kb128
        elif size <= 256 * SizeType._kb : return SizeType.kb256
        elif size <= 512 * SizeType._kb : return SizeType.kb512
        elif size <= 1 * SizeType._mb : return SizeType.mb1
        elif size <= 2 * SizeType._mb : return SizeType.mb2
        elif size <= 4 * SizeType._mb : return SizeType.mb4
        elif size <= 8 * SizeType._mb : return SizeType.mb8
        elif size <= 16 * SizeType._mb : return SizeType.mb16
        elif size <= 32 * SizeType._mb : return SizeType.mb32
        elif size <= 64 * SizeType._mb : return SizeType.mb64
        else : raise Exception(f"unsupported size({size})")

    @staticmethod
    def get_size(size_type) :
        # 获得数值
        if size_type <= 0 :
            raise Exception(f"unknown size type({size_type})")
        elif size_type <= 4 :
            return 64 << (size_type - 1)
        elif size_type <= 14 :
            return 1024 << (size_type - 5)
        elif size_type <= 21 :
            return 1048576 << (size_type - 15)
        else :
            raise Exception(f"unknown size type({size_type})")

class PageOffset :
    invalid = -1

    @staticmethod
    def l2i(value) :
        if value == -1 :
            return 0xFFFFFFFF
        return (value & 0xFFFFFFFFFFFFFFFF) >> 6

    @staticmethod
    def i2l(value) :
        if value == 0xFFFFFFFF : return -1
        return (value & 0xFFFFFFFFFFFFFFFF) << 6

    @staticmethod
    def check_offset(offset, data_size) :
        if offset != -1 :
            if (offset > data_size) or (offset & 0x3F) != 0 :
                raise Exception(f"invalid offset({offset})")

# 页面类型
class PageType :
    invalid = 0
    head_page = 1
    free_page = 2
    root_page = 3
    data_page = 4
    queue_page = 5
    queue_element = 6
    index_page = 7
    index_element = 8

    @staticmethod
    def is_valid(page_type) :
        # 返回结果
        return 0 <= page_type <= 8

    @staticmethod
    def get_default(page_type) :
        # 检查
        if page_type == PageType.head_page :
            return SizeType.hqkb
        elif page_type == PageType.free_page :
            return SizeType.hqkb
        elif page_type == PageType.root_page :
            return SizeType.hqkb
        elif page_type == PageType.data_page :
            return SizeType.qqkb
        elif page_type == PageType.queue_page :
            return SizeType.qqkb
        elif page_type == PageType.queue_element :
            return SizeType.qqkb
        elif page_type == PageType.index_page :
            return SizeType.mb1
        elif page_type == PageType.index_element :
            return SizeType.kb1
        else :
            raise Exception(f"unsupported page type({page_type})")

    @staticmethod
    def check_default(page_type, size_type) :
        # 检查
        if page_type == PageType.invalid :
            pass
        elif page_type == PageType.head_page :
            if size_type != SizeType.hqkb :
                raise Exception(f"invalid size type({size_type})")
        elif page_type == PageType.free_page :
            if size_type != SizeType.hqkb :
                raise Exception(f"invalid size type({size_type})")
        elif page_type == PageType.root_page :
            if size_type != SizeType.hqkb :
                raise Exception(f"invalid size type({size_type})")
        elif page_type == PageType.data_page :
            if not SizeType.is_valid(size_type) :
                raise Exception(f"invalid size type({size_type})")
        elif page_type == PageType.queue_page:
            if size_type != SizeType.qqkb :
                raise Exception(f"invalid size type({size_type})")
        elif page_type == PageType.queue_element :
            if size_type != SizeType.qqkb :
                raise Exception(f"invalid size type({size_type})")
        elif page_type == PageType.index_page :
            if not (SizeType.mb1 <= size_type <= SizeType.mb64) :
                raise Exception(f"invalid size type({size_type})")
        elif page_type == PageType.index_element :
            if not (SizeType.kb1 <= size_type <= SizeType.kb512) :
                raise Exception(f"invalid size type({size_type})")
        else :
            raise Exception(f"invalid page type({page_type})")
