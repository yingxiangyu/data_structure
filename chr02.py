# -*- coding:utf-8 -*-  
# !/usr/bin/python 
"""
@author:yyx 
@version: 1.0
@file: chr02.py
@time: 2019/4/26 11:19
使用列表管理数据，去除了向量容量的限制
"""
import random


class Vector:
    def __init__(self):
        self._size = 0
        self._elem = []

    def copyFrom(self, A, lo, hi):
        """复制向量A的区间lo到hi，通过复制初始化向量"""
        self._size = 0
        self._elem = []
        if len(A) < hi: raise IndexError
        while lo < hi:
            self._elem.append(A[lo])
            self._size += 1
            lo += 1

    def size(self):
        """返回数组当前规模"""
        return self._size

    def empty(self):
        """判断数组是否为空"""
        return self._size == 0

    def __getitem__(self, item):
        return self._elem[item]

    def __setitem__(self, key, value):
        self._elem[key] = value

    def __eq__(self, other):
        self.copyFrom(other, 0, other.size())
        return self

    def __len__(self):
        return self._size

    def permute(self):
        """随机置乱向量"""
        for i in range(1, self._size):
            k = random.choice(range(i))
            self._elem[i], self._elem[k] = self._elem[k], self._elem[i]

    def find(self, data, lo=None, hi=None):
        """查找指定元素，返回找到的第一个元素索引，不指定区间默认全向量查找"""
        if lo is None and hi is None:  # 不指定查找区间时在整个数组查找
            return self.find(data, 0, self._size)
        while lo < hi:
            if self._elem[lo] == data:
                break
            lo += 1
        return lo if lo != hi else -1

    def disordered(self):
        """返回向量的逆序对数"""
        n = 0  # 逆序对数
        for i in range(1, self._size):
            if self._elem[i - 1] > self._elem[i]:
                n += 1
        return n  # n=0说明有序

    def insert(self, index: int, data):
        """与列表的插入语义保持一致，index超出范围时不报错，插入到最后"""
        self._elem.insert(index, data)
        self._size += 1

    def remove_range(self, lo: int, hi: int):
        """区间删除"""
        if lo < 0 or lo > self._size:
            raise ValueError('索引有误')
        if hi < 0 or hi > self._size:
            raise ValueError('索引有误')
        if lo == hi:
            return 0
        while hi < self._size:
            self._elem[lo] = self._elem[hi]
            lo += 1
            hi += 1
        self._elem = self._elem[:lo]
        self._size = lo
        return hi - lo

    def remove(self, index):
        """删除指定位置的元素"""
        if index < 0 or index > self._size:
            raise ValueError('索引有误')
        return self.remove_range(index, index + 1)

    def deduplicate(self) -> int:
        """无序向量去重，返回重复元素个数"""
        old = self._size
        i = 1
        while i < self._size:
            if self.find(self._elem[i], 0, i) < 0:
                i += 1
            else:
                self.remove(i)
        return old - self._size

    def traverse(self, visit=print):
        """遍历向量，默认打印"""
        for i in range(self._size):
            visit(self._elem[i])

    def uniquify(self):
        """有序向量去重"""
        old = self._size
        i = 0
        for j in range(1, self._size):
            if self._elem[i] == self._elem[j]:
                pass
            else:
                i += 1
                self._elem[i] = self._elem[j]
        self._size = i + 1
        self._elem = self._elem[:i + 1]
        return old - self._size

    def binSearch_A(self, e, lo=0, hi=None):
        """三分支二分查找"""
        # bisect.bisect_left 实现该方法
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = self._size
        while lo < hi:
            mi = (lo + hi) >> 1
            if self._elem[mi] > e:
                hi = mi
            elif self._elem[mi] < e:
                lo = mi + 1
            else:
                return mi
        return -1  # 查找失败

    def binSearch(self, e, lo=0, hi=None):
        """二分支"""
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = self._size
        while hi - lo > 1:
            mi = (lo + hi) >> 1
            if self._elem[mi] > e:
                hi = mi
            else:
                lo = mi
        if self._elem[lo] == e:
            return lo
        else:
            return -1

    def _bubbleSort(self, lo=0, hi=None):
        """冒泡排序"""
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = self._size
        sort = False
        while not sort:
            sort = True
            for i in range(lo, hi - 1):
                if self._elem[i] > self._elem[i + 1]:
                    self._elem[i], self._elem[i + 1] = self._elem[i + 1], self._elem[i]
                    sort = False
            hi -= 1

    def _selectSort(self, lo=0, hi=None):
        """选择排序"""
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = self._size
        temp = lo
        while hi > lo:
            for i in range(lo, hi):
                if self._elem[i] > self._elem[temp]:
                    temp = i
            self._elem[temp], self._elem[hi - 1] = self._elem[hi - 1], self._elem[temp]
            hi -= 1
            temp = lo

    def _mergeSort(self, lo=0, hi=None):
        """归并排序"""
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = self._size
        if hi - lo < 2: return
        mi = (lo + hi) >> 1
        self._mergeSort(lo, mi)
        self._mergeSort(mi, hi)
        self._merge(lo, mi, hi)

    def _merge(self, lo, mi, hi):
        """归并排序算法"""
        A = self._elem[lo:mi]
        B = self._elem[mi:hi]
        i = j = 0
        k = lo
        while k < hi:
            if i < len(A) and (not (j < len(B)) or A[i] < B[j]):
                self._elem[k] = A[i]
                i += 1
                k += 1
            if j < len(B) and (not (i < len(A)) or B[j] <= A[i]):
                self._elem[k] = B[j]
                j += 1
                k += 1

    def partition(self, lo, hi):
        t = self._elem[lo]
        i = lo
        j = lo
        for k in range(lo + 1, hi):
            if self._elem[k] <= t:
                self._elem[k], self._elem[i + 1] = self._elem[i + 1], self._elem[k]
                j += 1
                i += 1
            else:
                j += 1
        self._elem[lo], self._elem[i] = self._elem[i], self._elem[lo]
        return i

    def quickSort(self, lo=0, hi=None):
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = self._size
        if lo >= hi:
            return
        t = self.partition(lo, hi)
        self.quickSort(lo, t)
        self.quickSort(t + 1, hi)

    def sort(self, lo, hi):
        self.quickSort(lo, hi)
