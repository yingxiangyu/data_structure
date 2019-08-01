# -*- coding:utf-8 -*-  
# !/usr/bin/python 
"""
@author:yyx 
@version: 1.0
@file: chr06.py
@time: 2019/7/26 16:41
"""
from enum import Enum
from dataclasses import dataclass
from chr02 import Vector


class VStatus(Enum):  # 顶点状态枚举类型
    UNDISCOVERED = 0
    DISCOVERED = 1
    VISITED = 2


class EType(Enum):  # 遍历树中边的类型
    UNDETERMINED = 0
    TREE = 1
    CROSS = 2
    FORWARD = 3
    BACKWARD = 4


@dataclass
class Vertex:  # 顶点对象
    data: int = 0  # 数据
    inDegree: int = 0  # 出度
    outDegree: int = 0  # 入度
    status: VStatus = VStatus.UNDISCOVERED  # 状态
    dTime: int = -1  # 时间标签
    fTime: int = -1
    parent: int = -1  # 遍历树中父节点
    priority: int = float('inf')  # 优先级数,默认最高


@dataclass
class Edge:  # 边对象
    data: int = 0  # 数据
    weight: int = 0  # 权重
    type: EType = EType.UNDETERMINED  # 类型


class GraphMatrix:
    def __init__(self, n=0, e=0):
        self.n = 0  # 顶点数
        self.e = 0  # 边数
        self._V = Vector()  # 顶点集合
        self._E = Vector()  # 边集合

    def vertex(self, i):
        return self._V[i].data

    def inDegree(self, i):
        return self._V[i].InDegree

    def outDegree(self, i):
        return self._V[i].outDegree

    def firstNbr(self, i):
        return self.nextNbr(i, self.n)

    def nextNbr(self, i, j):
        for j in range(j - 1, 0, -1):
            if self.exists(i, j):
                return j

    def exists(self, i, j):
        return 0 <= i <= self.n and 0 <= j <= self.n and self._E[i][j] is not None

    def staatus(self, i):
        return self._V[i].status

    def dTime(self, i):
        return self._V[i].dTime

    def fTime(self, i):
        return self._V[i].fTime

    def parent(self, i):
        return self._V[i].parent

    def priority(self, i):
        return self._V[i].priority

    def insertV(self, vertex: Vertex):  # 插入顶点
        for j in range(self.n):
            self._E[j].insert(None)  # 各顶点增加一个边记录位置
        self.n += 1
        self._E.insert(self.n, Vector().copyFrom([None] * self.n, 0, self.n))  # 增加新的顶点向量
        return self._V.insert(self.n, vertex)  # 增加新顶点

    def removeV(self, i):  # 删除第i个顶点及其关联的边
        for j in range(self.n):
            if self.exists(i, j):
                self._E[i][j] = None
                self._V[j].inDegree -= 1
        self._E.remove(i)
        self.n -= 1
        vBak = self.vertex(i)
        self._V.remove(i)
        for j in range(self.n):
            if self._E.remove(i):
                self._V[j].outDegree -= 1
        return vBak

    def type(self, i, j):
        return self._E[i][j].type

    def edge(self, i, j):
        return self._E[i][j].data

    def weight(self, i, j):
        return self._E[i][j].weight

    def insertE(self, edge, w, i, j):
        if self.exists(i, j): return
        self._E[i][j] = Edge(edge, w)
        self.e += 1
        self._V[i].outDegree += 1
        self._V[j].inDegree += 1

    def removeE(self, i, j):
        eBak = self.edge(i, j)
        self._E[i][j] = None
        self.e -= 1
        self._V[i].outDegree -= 1
        self._V[j].inDegree -= 1
        return eBak


class Graph:
    pass
