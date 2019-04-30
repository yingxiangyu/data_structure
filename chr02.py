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
    def __init__(self):  # 初始化时指定向量大小
        self._size = 0
        self._elem = []

    def copyFrom(self, A, lo, hi):
        self._size = 0
        self._elem = []
        while lo < hi:
            self._elem.append(A[lo])
            self._size += 1
            lo += 1

    def size(self):
        return self._size

    def empty(self):
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

    def permute(self):  # 随机置乱向量
        for i in range(1, self._size):
            k = random.choice(range(i))
            self._elem[i], self._elem[k] = self._elem[k], self._elem[i]

    def unsort(self, lo, hi):
        for i in range(1, hi - lo):
            k = random.choice(range(i))
            self._elem[i + lo], self._elem[k + lo] = self._elem[k + lo], self._elem[i + lo]

    def find(self, e, lo, hi):
        while lo <= hi:
            hi -= 1
            if self._elem[hi] == e:
                break
        return hi

    def insert(self, r, e):
        self._elem.insert(r, e)

    def remove(self, *args):  # python不支持函数重载
        if len(args) == 1:
            if args[0] < 0 or args[0] > self._size:
                raise ValueError('索引有误')
            self.remove(args[0], args[0] + 1)
        elif len(args) == 2:
            lo, hi = args
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
        else:
            raise ValueError('参数过多')

    def deduplicate(self):
        old = self._size
        i = 1
        while i < self._size:
            if self.find(self._elem[i], 0, i) < 0:
                i += 1
            else:
                self.remove(i)
        return old - self._size

    def traverse(self, visit=print):
        for i in range(self._size):
            visit(self._elem[i])

    def disordered(self):
        n = 0  # 逆序对数
        for i in range(1, self._size):
            if self._elem[i - 1] > self._elem[i]:
                n += 1
        return n  # n=0说明有序

    def uniquify1(self):  # 有序向量去重
        old = self._size
        i = 1
        while i < self._size:
            if self._elem[i - 1] == self._elem[i]:
                self.remove(i)
            else:
                i += 1
        return old - self._size

    def uniquify(self):  # 有序向量去重
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

    @staticmethod
    def binSearch_A(A, e, lo, hi):  # 设置成静态方法,三分支
        while lo < hi:
            mi = (lo + hi) >> 1
            if A[mi] > e:
                hi = mi
            elif A[mi] < e:
                lo = mi + 1
            else:
                return mi
        return -1  # 查找失败

    @staticmethod
    def binSearch_B(A, e, lo, hi):  # 二分支
        while hi - lo > 1:
            mi = (lo + hi) >> 1
            if A[mi] > e:
                hi = mi
            else:
                lo = mi
        if A[lo] == e:
            return lo
        else:
            return -1

    @staticmethod
    def binSearch(A, e, lo, hi):
        while lo < hi:
            mi = (lo + hi) >> 1
            if A[mi] > e:
                hi = mi
            else:
                lo = mi + 1
        return lo - 1

    def bubbleSort(self, lo, hi):
        sort = False
        while not sort:
            sort = True
            for i in range(lo, hi - 1):
                if self._elem[i] > self._elem[i + 1]:
                    self._elem[i], self._elem[i + 1] = self._elem[i + 1], self._elem[i]
                    sort = False
            hi -= 1

    def selectSort(self, lo, hi):
        temp = lo
        while hi > lo:
            for i in range(lo, hi):
                if self._elem[i] > self._elem[temp]:
                    temp = i
            self._elem[temp], self._elem[hi - 1] = self._elem[hi - 1], self._elem[temp]
            hi -= 1
            temp = lo

    def mergeSort(self, lo, hi):
        if hi - lo < 2: return
        mi = (lo + hi) >> 1
        self.mergeSort(lo, mi)
        self.mergeSort(mi, hi)
        self.merge(lo, mi, hi)

    def merge(self, lo, mi, hi):
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

    def heapSort(self, lo, hi):
        pass

    def quickSort(self, lo, hi):
        pass

    def sort(self, lo, hi):
        sortes = [self.bubbleSort, self.selectSort, self.mergeSort,
                  self.heapSort, self.quickSort]
        s = random.choice(sortes)
        s(lo, hi)
