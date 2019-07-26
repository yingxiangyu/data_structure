# -*- coding:utf-8 -*-  
# !/usr/bin/python 
"""
@author:yyx 
@version: 1.0
@file: chr05.py
@time: 2019/5/30 15:30
"""
from chr04 import Stack, Queue


class BinNode:
    def __init__(self, data=None, parent=None, lc=None, rc=None, height=0, color='R'):
        self.data = data
        self.parent = parent
        self.lc = lc
        self.rc = rc
        self.height = height
        self.npl = height
        self.color = color

    def size(self):
        pass

    def insertAsLC(self, e):
        self.lc = BinNode(data=e, parent=self)

    def insertAsRc(self, e):
        self.rc = BinNode(data=e, parent=self)

    def succ(self):
        s = self
        if s.rc:
            s = s.rc
            while s.HasLChild():
                s = s.lc
        else:
            while s.IsRChild():
                s = s.parent
            s = s.parent
        return s

    def travLevel(self, visit=print):
        Q = Queue()
        Q.enqueue(self)
        while Q.size() != 0:
            x = Q.dequeue()
            visit(x.data)
            if x.HasLChild(): Q.enqueue(x.lc)
            if x.HasRChild(): Q.enqueue(x.rc)

    def travPre(self, visit=print):  # 递归版本先序遍历
        S = Stack()
        x = self
        while True:
            while x:
                visit(x.data)
                S.push(x.rc)
                x = x.lc
            if S.empty(): break
            x = S.pop()

    def travPreR(self, visit=print):  # 递归版本先序遍历
        if not self: return
        visit(self.data)
        if self.lc:
            self.lc.travPreR(visit)
        if self.rc:
            self.rc.travPreR(visit)

    def travIn(self, visit=print):  # 递归版中序遍历
        S = Stack()
        x = self
        while True:
            while x:
                S.push(x)
                x = x.lc
            if S.empty(): break
            x = S.pop()
            visit(x.data)
            x = x.rc

    def travIn2(self, visit=print):  # 递归版中序遍历
        S = Stack()
        x = self
        while True:
            if x:
                S.push(x)
                x = x.lc
            elif not S.empty():
                x = S.pop()
                visit(x.data)
                x = x.rc
            else:
                break

    def travIn3(self, visit=print):  # 递归版中序遍历
        backtrack = False  # 标识是否需要回退
        x = self
        while True:
            if not backtrack and x.HasLChild():  # 一直往左
                x = x.lc
            else:
                visit(x.data)
                if x.HasRChild():
                    x = x.rc
                    backtrack = False
                else:
                    x = x.succ()
                    if not x: break
                    backtrack = True

    def travInR(self, visit=print):  # 递归版本中序遍历
        if not self: return
        if self.lc:
            self.lc.travInR(visit)
        visit(self.data)
        if self.rc:
            self.rc.travInR(visit)

    def travPost(self, visit=print):  # 递归版本后序遍历
        S = Stack()
        x = self
        if x:
            S.push(x)
        while not S.empty():
            if x.parent and S.top() != x.parent:
                x = S.top()
                while x:
                    if x.HasLChild:
                        if x.HasRChild: S.push(x.rc)
                        S.push(x.lc)
                    else:
                        S.push(x.rc)
                    x = S.top()
                S.pop()
            x = S.pop()
            visit(x.data)

    def travPostR(self, visit=print):  # 递归版本后序遍历
        if not self: return
        if self.lc:
            self.lc.travPostR(visit)
        if self.rc:
            self.rc.travPostR(visit)
        visit(self.data)

    def __lt__(self, other):
        return self.data > other.data

    def __eq__(self, other):
        return self.data == other.data

    def IsRoot(self):
        return not self.parent

    def IsLChild(self):
        return not self.IsRoot() and (self == self.parent.lc)

    def IsRChild(self):
        return not self.IsRoot() and (self == self.parent.rc)

    def HasParent(self):
        return not self.IsRoot()

    def HasLChild(self):
        return self.lc

    def HasRChild(self):
        return self.rc

    def HasChild(self):
        return self.HasLChild() or self.HasRChild()

    def HasBothChild(self):
        return self.HasLChild() and self.HasRChild()

    def IsLead(self):
        return not self.HasChild()

    def sibling(self):
        return self.parent.rc if self.IsLChild() else self.parent.lc

    def uncle(self):
        return self.parent.parent.rc if self.parent.IsLChild() else self.parent.parent.lc

    def FromParentTo(self):
        if self.IsRoot():
            return self
        else:
            if self.IsLChild():
                return self.parent.lc
            else:
                return self.parent.rc


class BinTree:
    def __init__(self):
        self._size = 0
        self._root = None

    @staticmethod
    def stature(x: BinNode):
        if x:
            return x.height
        else:
            return -1

    @staticmethod
    def updateHeight(x: BinNode):
        x.height = 1 + max(BinTree.stature(x.lc), BinTree.stature(x.rc))
        return x.height

    @staticmethod
    def updateHeightAbove(x: BinNode):
        while x:
            old = x.height
            n = BinTree.updateHeight(x)
            if old == n:  # 节点高度无变化则该节点的父节点不再需要更新
                break
            x = x.parent

    def size(self):
        return self._size

    def empty(self):
        return not self._root

    def root(self):
        return self._root

    def insertAsRoot(self, e):
        self._size = 1
        self._root = BinNode(data=e)
        return self._root

    def insertAsLC(self, x: BinNode, e):  # 假设x的lc为空
        self._size += 1
        x.insertAsLC(e)
        self.updateHeightAbove(x)
        return x.lc

    def insertAsRC(self, x, e):
        self._size += 1
        x.insertAsRc(e)
        self.updateHeightAbove(x)
        return x.rc

    def attachAsLC(self, x: BinNode, T):
        x.lc = T.root()
        x.lc.parent = x
        self._size += T.size()
        self.updateHeightAbove(x)
        T._root = None
        return x

    def attachAsRC(self, x, T):
        x.rc = T.root()
        x.rc.parent = x
        self._size += T.size()
        self.updateHeightAbove(x)
        T._root = None
        return x

    def remove(self, x: BinNode):
        if x.IsRoot():
            x = None
        else:
            if x.IsLChild():
                x.parent.lc = None
            else:
                x.parent.rc = None
        self.updateHeightAbove(x.parent)
        n = self.removeAt(x)
        self._size -= n
        return n

    @staticmethod
    def removeAt(x):  # 计算删除的节点数
        if not x:
            return 0
        n = 1 + BinTree.removeAt(x.lc) + BinTree.removeAt(x.rc)
        return n

    def secede(self, x):
        if x.IsRoot():
            x = None
        else:
            if x.IsLChild():
                x.parent.lc = None
            else:
                x.parent.rc = None
        self.updateHeightAbove(x.parent)
        S = BinTree()
        S._root = x
        x.parent = None
        S._size = x.size()
        self._size -= S._size
        return S

    def travLevel(self):
        if self._root:
            self._root.travLevel()

    def travPre(self):
        if self._root:
            self._root.travPre()

    def travIn(self):
        if self._root:
            self._root.travIn()

    def travPost(self):
        if self._root:
            self._root.travPostR()

    def __eq__(self, other):
        return self._root and other.root() and (self._root == other.root())

    def __lt__(self, other):
        return self._root and other.root() and (self._root > other.root())


def test():
    bt = BinTree()
    bt.insertAsRoot(1)
    lc = bt.insertAsLC(bt.root(), 2)
    lc = bt.insertAsLC(lc, 7)
    rc = bt.insertAsRC(bt.root(), 3)
    rc = bt.insertAsRC(rc, 3)
