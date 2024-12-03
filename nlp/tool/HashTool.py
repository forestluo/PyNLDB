# -*- coding: utf-8 -*-
import hashlib

class HashTool :
    # 质数表
    __primes = \
    [
        107, 109, 113, 127, 131, 137, 139, 149, 151, 157,
        163, 167, 173, 179, 181, 191, 193, 197, 199, 211,
        217, 223, 227, 229, 233, 239, 241, 247, 251, 253,
        255, 256
    ]

    # 字符串哈希（FNV-1）
    @staticmethod
    def hash64(content) :
        # 检查参数
        assert isinstance(content, str)
        # 初始值
        value = 0x811c9dc5
        # 循环处理
        for token in content :
            value = (value * 16777619) ^ ord(token)
        # 返回结果
        return value

    # sha256
    @staticmethod
    def sha256(content) :
        # 返回结果
        return hashlib.sha256(content.encode("utf-8"))

    # hash256
    @staticmethod
    def hash256(content) :
        # 余数序列
        residues = []
        # 循环处理
        for prime in HashTool.__primes :
            # 余数
            residue = 0
            # 循环处理
            for token in content :
                # 求余数
                residue = (ord(token) + (residue << 16)) % prime
            # 扩展序列
            residues.append(residue)
        # 返回结果
        return bytes(residues)
