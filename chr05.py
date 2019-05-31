# -*- coding:utf-8 -*-  
# !/usr/bin/python 
"""
@author:yyx 
@version: 1.0
@file: chr05.py
@time: 2019/5/30 15:30
"""


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
        pass

    def travLevel(self):
        pass

    def travPre(self):
        pass

    def travIn(self):
        pass

    def travPost(self):
        pass

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


def stature(x: BinNode):
    if x:
        return x.height
    else:
        return -1


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

    def insertAsRC(self,x, e):
        self._size += 1
        x.insertAsRC(e)
        self.updateHeightAbove(x)
        return x.rc

    @staticmethod
    def attachAsLC(x, T):
        pass

    @staticmethod
    def attachAsRC(x, T):
        pass

    @staticmethod
    def remove(x):
        pass

    @staticmethod
    def secede(x):
        pass

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
            self._root.travPost()

    def __eq__(self, other):
        return self._root and other.root() and (self._root == other.root())

    def __lt__(self, other):
        return self._root and other.root() and (self._root > other.root())
