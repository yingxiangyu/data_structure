# -*- coding:utf-8 -*-  
# !/usr/bin/python 
"""
@author:yyx 
@version: 1.0
@file: chr03.py
@time: 2019/4/30 16:20
"""


class ListNode:
    def __init__(self, data=None, pred=None, succ=None):
        self.data = data
        self.pred = pred  # 前
        self.succ = succ  # 后


class List:
    def __init__(self):
        self.header = ListNode()  # 创建头部哨兵节点
        self.trailer = ListNode()  # 创建尾部哨兵节点
        self.header.succ = self.trailer
        self.header.pred = None
        self.trailer.pred = self.header
        self.trailer.succ = None
        self._size = 0

    def first(self):
        if self._size:
            return self.header.succ
        else:
            return None

    def last(self):
        if self._size:
            return self.trailer.pred
        else:
            return None

    def insertAsFirst(self, e):
        self.insertAsSucc(self.header, e)

    def insertAsLast(self, e):
        self.insertAsPred(self.trailer, e)

    def insertAsPred(self, p, e):  # 作为前驱节点插入
        if p not in self:
            raise ValueError('p not in List')
        n = ListNode(data=e, pred=p.pred, succ=p)
        p.pred.succ = n
        p.pred = n
        self._size += 1

    def insertAsSucc(self, p, e):  # 作为后继节点插入
        if p not in self:
            raise ValueError('p not in List')
        n = ListNode(data=e, pred=p, succ=p.succ)
        p.succ.pred = n
        p.succ = n
        self._size += 1

    def __contains__(self, item):
        p = self.header.succ
        while p != self.trailer:
            if p == item:
                return True
            else:
                p = p.succ
        return False

    def __getitem__(self, r):
        p = self.first()
        if not 0 <= r < self._size - 1:
            raise ValueError('index error')
        while r > 0:
            p = p.succ
            r -= 1
        return p.data

    def __len__(self):
        return self._size

    def size(self):
        return self._size

    def remove(self, p):
        if p not in self:
            raise ValueError('p not in List')

        p.pred.succ = p.succ
        p.succ.pred = p.pred
        self._size-=1
        return p.data

    def disordered(self):  # 逆序对
        n = 0
        p = self.header.succ
        for i in range(self._size):
            if p.succ.data >= p.data:
                n += 1
            p = p.succ
        return 0

    def find(self, e, n, p):  # 在无序列表内节点p（可能是trailer）的n个（真）前驱中，找到等于e的最后者
        while n > 0 and p != self.header:
            if p.data == e:
                return p
            else:
                p = p.pred
                n -= 1
        return None

    def copyNodes(self, p, n):
        self.trailer.pred = self.header
        self.header.succ = self.trailer
        self._size = 0
        while n:
            self.insertAsLast(p.data)
            if p.succ.succ :
                p = p.succ
            else:
                import warnings
                warnings.warn('节点数量不足', DeprecationWarning)
                break
            n -= 1

    def clear(self):
        self.trailer.pred = self.header
        self.header.succ = self.trailer
        self._size = 0

