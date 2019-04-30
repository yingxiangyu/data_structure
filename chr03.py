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
        p = ListNode(data=e)
        p.succ = self.header.succ
        self.header.succ = p
        p.pred = self.header

    def insertAsLast(self, e):
        p = ListNode(data=e)
        p.pred = self.trailer.pred
        self.trailer.pred = p
        p.succ = self.trailer

    @staticmethod
    def insertAsPred(p, e):  # 作为前驱节点插入
        n = ListNode(data=e)
        n.pred = p.pred
        p.pred = n
        n.succ = p

    @staticmethod
    def insertAsSucc(p, e):  # 作为后继节点插入
        n = ListNode(data=e)
        n.succ = p.succ
        p.succ = n
        n.pred = p

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

    @staticmethod
    def remove(p):
        p.pred.succ = p.succ
        p.succ.pred = p.pred
        return p.data

    
