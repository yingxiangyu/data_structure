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
        n = ListNode(data=e, pred=p.pred, succ=p)
        p.pred.succ = n
        p.pred = n
        self._size += 1

    def insertAsSucc(self, p, e):  # 作为后继节点插入
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
        self._size -= 1
        return p.data

    def disordered(self):  # 逆序对
        n = 0
        p = self.header.succ
        while p != self.trailer.pred:
            if p.succ.data >= p.data:
                n += 1
            p = p.succ
        return n

    def find(self, e, n, p):  # 在无序列表内节点p（可能是trailer）的n个真前驱中，找到等于e的最后者
        p = p.pred
        while n > 0 and p != self.header:
            if p.data == e:
                return p
            else:
                p = p.pred
                n -= 1
        return None

    def copyNodes(self, p, n):  # 从p节点开始，往后复制n个节点
        self.trailer.pred = self.header
        self.header.succ = self.trailer
        self._size = 0
        while n:
            if p.succ is None:  # p为尾哨兵则退出
                import warnings
                warnings.warn('节点数量不足', DeprecationWarning)
                break
            self.insertAsLast(p.data)
            p = p.succ
            n -= 1

    def clear(self):
        self.trailer.pred = self.header
        self.header.succ = self.trailer
        self._size = 0

    def deduplicate(self):  # 无序链表去重
        if self._size < 2:
            return 0
        old_size = self._size
        p = self.header.succ
        r = 0
        while p != self.trailer:
            q = self.find(p.data, r, p)
            if q:
                self.remove(q)
            else:
                r += 1
            p = p.succ
        return old_size - self._size

    def traverse(self, visit=print):  # 遍历
        p = self.header.succ
        while p != self.trailer:
            visit(p.data)
            p = p.succ

    def uniquify(self):  # 有序链表去重
        if self._size < 2:
            return 0
        oldsize = self._size
        p = self.first()
        q = p.succ
        while q != self.trailer:
            if p.data != q.data:
                p = q
            else:
                self.remove(q)
            q = p.succ
        return oldsize - self._size

    def search(self, e, n, p):  # 在有序列表内节点p（可能是trailer）的n个（真）前驱中，找到不小于e的最后者
        assert 0 <= n < self._size
        p = p.pred
        while n >= 0:
            if p == self.header:
                break
            if p.data <= e:
                break
            else:
                p = p.pred
                n -= 1
        return p

    def sort(self, p, n):
        import random
        s = [self.insertionSort, self.selectionSort, self.mergeSort]
        f = random.choice(s)
        f(p, n)

    def insertionSort(self, p, n):  # 对起始于位置p的n个元素排序
        r = 0
        assert 0 <= n <= self._size
        while r < n:
            temp = self.search(p.data, r, p)
            self.insertAsSucc(temp, p.data)
            p = p.succ
            self.remove(p.pred)
            r += 1

    def seleectMax(self, p, n):  # 从起始于位置p的n个元素中选出最大者
        max_p = p
        cur = p
        while n > 0:
            if cur == self.trailer:
                break
            if cur.data > max_p.data:
                max_p = cur
            cur = cur.succ
            n -= 1
        return max_p

    def selectionSort(self, p, n):  # ：对起始于位置p癿n个元素排序
        assert 0 <= n <= self._size
        head = p.pred
        tail = p
        for i in range(n):
            tail = tail.succ
        while n > 0:
            max_p = self.seleectMax(head.succ, n)
            print(max_p.data, n)
            self.insertAsPred(tail, self.remove(max_p))
            tail = tail.pred
            n -= 1

    def merge(self, p, n, q, m):  # 当前列表中自p起的n个元素，与列表中自q起的m个元素归并
        pp = p.pred
        while m > 0:
            if n > 0 and p.data <= q.data:  # p较小，则当前p位置不需要调整，直接后移到下一位置
                p = p.succ
                if q == p:  # 前列表耗尽，直接退出
                    break
                n -= 1
            else:
                q = q.succ  # q较小，需要将q插入到p之前，q后移
                self.insertAsPred(p, self.remove(q.pred))
                if q.succ is None:  # q到哨兵节点则退出
                    break

                m -= 1
        return pp.succ

    def mergeSort(self, p, n):  # 节点位置变化，直接按节点、节点数量去调用会导致排序失败，每次归并后更新节点位置，会多一个返回值，暂时不处理
        if n < 2: return p
        m = n >> 1
        q = p
        for i in range(m):
            q = q.succ
        p = self.mergeSort(p, m)
        q = self.mergeSort(q, n - m)
        return self.merge(p, m, q, n - m)


