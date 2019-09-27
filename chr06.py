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
from chr03 import List
from chr04 import Queue


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
    etype: EType = EType.UNDETERMINED  # 类型

# 使用nametuple实现c的结构体，3.7版本可以设置默认值
# from collections import namedtuple
#
# Vertex = namedtuple('Vertex', ['data', 'inDegree', 'outDegree', 'status', 'dTime', 'fTime', 'parent', 'priority'],
#                     defaults=[0, 0, 0, VStatus.UNDISCOVERED, -1, -1, float('inf')])
# Edge = namedtuple('Edge', ['data', 'weight', 'type'], defaults=[0, 0, EType.UNDETERMINED])
#

class GraphMatrix:  # 基于向量，邻接矩阵实现图
    def __init__(self):
        self.n = 0  # 顶点数
        self.e = 0  # 边数
        self.__V = Vector()  # 顶点集合
        self.__E = Vector()  # 边集合

    def reset(self):
        for i in range(self.n):
            self.vertex(i).status = VStatus.UNDISCOVERED
            self.vertex(i).dTime = -1
            self.vertex(i).fTime = -1
            self.vertex(i).parent = -1
            self.vertex(i).priority = float('inf')
            for j in range(self.n):
                if self.exists(i, j):
                    self.__E[i][j].type = EType.UNDETERMINED

    def vertex(self, i):
        return self.__V[i]

    def vertex_data(self, i):
        return self.__V[i].data

    def inDegree(self, i):
        return self.__V[i].InDegree

    def outDegree(self, i):
        return self.__V[i].outDegree

    def firstNbr(self, i):
        return self.nextNbr(i, self.n)

    def nextNbr(self, i, j):
        for j in range(j - 1, 0, -1):
            if self.exists(i, j):
                return j
        return -1

    def exists(self, i, j):  # i到j的边是否存在
        return 0 <= i <= self.n and 0 <= j <= self.n and self.__E[i][
            j] is not None

    def status(self, i):
        return self.__V[i].status

    def dTime(self, i):
        return self.__V[i].dTime

    def fTime(self, i):
        return self.__V[i].fTime

    def parent(self, i):
        return self.__V[i].parent

    def priority(self, i):
        return self.__V[i].priority

    def insertV(self, vertex: Vertex):  # 插入顶点
        for j in range(self.n):
            self.__E[j].insert(None)  # 各顶点增加一个边记录位置
        self.n += 1
        self.__E.insert(self.n, Vector().copyFrom([None] * self.n, 0,
                                                  self.n))  # 增加新的顶点向量
        return self.__V.insert(self.n, vertex)  # 增加新顶点

    def removeV(self, i):  # 删除第i个顶点及其关联的边
        for j in range(self.n):  # 所有出边
            if self.exists(i, j):  # 存在
                self.__E[i][j] = None  # 删除出边，可选，后续删除整条边
                self.__V[j].inDegree -= 1  # 顶点J入度-1
        self.__E.remove(i)  # 删除i的边数据
        self.n -= 1
        vBak = self.vertex(i)  # 需要删除的顶点备份
        self.__V.remove(i)  # 删除顶点
        for j in range(self.n):
            if not self.__E[j][i] is None:  # 判断第j的顶点是否有到i的边
                self.__E[j][i] = None  # 有边时删除
                self.__V[j].outDegree -= 1  # 出度减1
        return vBak

    def type(self, i, j):
        return self.__E[i][j].etype

    def edge(self, i, j):  # 方便后续程序修改值，将边对象直接返回
        return self.__E[i][j]

    def edge_data(self, i, j):
        return self.__E[i][j].data

    def weight(self, i, j):
        return self.__E[i][j].weight

    def insertE(self, edge: Edge, i, j):  # 插入i到j的边
        if self.exists(i, j): return  # 边存在则不做任何处理）
        self.__E[i][j] = edge
        self.e += 1
        self.__V[i].outDegree += 1
        self.__V[j].inDegree += 1

    def removeE(self, i, j):  # 移除i到j的边
        eBak = self.edge(i, j)
        self.__E[i][j] = None
        self.e -= 1
        self.__V[i].outDegree -= 1
        self.__V[j].inDegree -= 1
        return eBak

    def __getitem__(self, item: int):
        return self.__V[item]

@dataclass
class GraphEdge(Edge):  # 邻接表边对象
    vertex: Vertex = Vertex()  # 关联的顶点

class Graph:  # 邻接表实现图
    def __init__(self):
        self.n = 0  # 顶点数
        self.e = 0  # 边数
        self.__L = list()  # 邻接矩阵的集合

    def reset(self):
        for v in self.__L:
            v[0].status = VStatus.UNDISCOVERED
            v[0].dTime = v[0].fTime = -1
            v[0].parent = -1
            v[0].priority = float('inf')
            for e in v[1:]:
                e.type = EType.UNDETERMINED

    def vertex(self, i) -> Vertex:  # 直接返回节点对象，方便后续程序修改
        return self.__L[i][0]

    def vertex_data(self, i):
        return self.__L[i][0].data

    def inDegree(self, i):
        return self.__L[i][0].InDegree

    def outDegree(self, i):
        return self.__L[i][0].outDegree

    def firstNbr(self, i):  # 返回下一个邻居顶点的索引
        return self.nextNbr(i, self.n)

    def nextNbr(self, i, j):
        for j in range(j - 1, 0, -1):
            if self.exists(i, j):
                return j
        return -1

    def exists(self, i, j):  # i到j的边是否存在
        for e in self.__L[i][1:]:
            if e.vertex == self.__L[j][0]:
                return True
        return False

    def status(self, i):
        return self.__L[i][0].status

    def dTime(self, i):
        return self.__L[i][0].dTime

    def fTime(self, i):
        return self.__L[i][0].fTime

    def parent(self, i):
        return self.__L[i][0].parent

    def priority(self, i):
        return self.__L[i][0].priority

    def insertV(self, vertex: Vertex):  # 插入顶点
        self.__L.append(List().insertAsFirst(vertex))
        self.n += 1

    def removeV(self, i):  # 删除第i个顶点及其关联的边
        for e in self.__L[i][1:]:  # 遍历与i相连的顶点
            e.vertex.inDegree -= 1  # 入度-1
        vBak = self.__L[i][0]  # 需要删除的顶点备份
        self.__L.remove(i)  # 删除i
        self.n -= 1
        for v in self.__L:  # 遍历剩余顶点
            for p in v[1:]:  # 遍历每个顶点的边
                if p.vertex == vBak:  # 与i相连时删除
                    v[0].outDegree -= 1
                    v.remove(p)
                    continue
        return vBak

    def type(self, i, j):
        for p in self.__L[i][1:]:
            if p.vertex == self.__L[j][0]:
                return p.etype

    def edge(self, i, j):  # 直接返回边对象，方便后续程序修改
        for p in self.__L[i][1:]:
            if p.vertex == self.__L[j][0]:
                return p
        return None

    def edge_data(self, i, j):
        for p in self.__L[i][1:]:
            if p.vertex == self.__L[j][0]:
                return p.data

    def weight(self, i, j):
        for p in self.__L[i][1:]:
            if p.vertex == self.__L[j][0]:
                return p.weight

    def insertE(self, edge: Edge, i, j):  # 插入i到j的边
        if self.exists(i, j): self.removeE(i, j)  # 边存在则移除
        e = GraphEdge(vertex=self.__L[j][0], data=edge.data, weight=edge.weight
                      , etype=edge.etype)
        self.__L[i].insertAsLast(e)
        self.e += 1
        self.__L[i][0].outDegree += 1
        self.__L[j][0].inDegree += 1

    def removeE(self, i, j):  # 移除i到j的边
        eBak = self.edge(i, j)
        for p in self.__L[i][1:]:
            if p.vertex == self.__L[j][0]:
                self.__L[i].remove(p)
        self.e -= 1
        self.__L[i][0].outDegree -= 1
        self.__L[j][0].inDegree -= 1
        return eBak

    def __getitem__(self, item: int):
        return self.__L[item][0]

def bfs(graph: Graph):  # 全图BFS算法
    graph.reset()  # 初始化、重置图状态
    clock = 0

    def BFS(i: int):  # 第i个节点的BFS算法
        nonlocal clock
        Q = Queue()  # 辅助队列
        vertex = graph.vertex(i)  # 获取初始化顶点
        vertex.status = VStatus.DISCOVERED  # 标记为discovered
        Q.enqueue(i)  # 初始顶点入队
        while not Q.empty():
            v = Q.dequeue()  # 处理队列首节点
            vertex = graph[v]
            vertex.dTime = clock
            clock += 1
            u = graph.firstNbr(v)
            while True:
                nbr_vertex = graph[u]
                if nbr_vertex.status == VStatus.UNDISCOVERED:
                    nbr_vertex.status = VStatus.DISCOVERED
                    Q.enqueue(u)
                    nbr_vertex.parent = v
                    graph.insertE(Edge(etype=EType.TREE), u, v)
                else:
                    graph.insertE(Edge(etype=EType.CROSS), u, v)
                vertex.status = VStatus.VISITED
                u = graph.nextNbr(v, u)
                if u == -1:
                    break

    for index in range(graph.n):
        if graph[index].status == VStatus.UNDISCOVERED:
            BFS(index)

def dfs(graph: Graph):  # 全图BFS算法
    graph.reset()  # 初始化、重置图状态
    clock = 0

    def DFS(v: int):  # 第i个节点的BFS算法
        nonlocal clock
        vertex = graph.vertex(v)  # 获取初始化顶点
        vertex.status = VStatus.DISCOVERED  # 标记为discovered
        vertex.dTime = clock
        clock += 1
        u = graph.firstNbr(v)
        while True:
            nbr_vertex = graph[u]
            if nbr_vertex.status == VStatus.UNDISCOVERED:
                nbr_vertex.parent = v
                graph.insertE(Edge(etype=EType.TREE), u, v)
                DFS(u)
            elif nbr_vertex.status == VStatus.DISCOVERED:
                graph.insertE(Edge(etype=EType.BACKWARD), u, v)
            else:
                if vertex.dTime < nbr_vertex.dTime:
                    graph.insertE(Edge(etype=EType.FORWARD), u, v)
                else:
                    graph.insertE(Edge(etype=EType.CROSS), u, v)
            vertex.status = VStatus.VISITED
            vertex.fTime = clock
            clock += 1
            u = graph.nextNbr(v, u)
            if u == -1:
                break

    for index in range(graph.n):
        if graph[index].status == VStatus.UNDISCOVERED:
            DFS(index)
