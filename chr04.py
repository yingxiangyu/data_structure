# -*- coding:utf-8 -*-  
# !/usr/bin/python 
"""
@author:yyx 
@version: 1.0
@file: chr04.py
@time: 2019/5/10 16:00
python内置有栈和队列的实现，有些操作的设置与书中不同，所以简单重写
"""
from chr02 import Vector


class Stack(Vector):
    def size(self):
        return self._size

    def empty(self):
        return self._size == 0

    def pop(self):
        if self._size > 0:
            t = self._elem.pop()
            self._size -= 1
            return t
        else:
            raise ValueError('元素不足')

    def push(self, e):
        self._elem.append(e)
        self._size += 1

    def top(self):
        return self._elem[-1]


def convert(n, base):  # 十进制n转base进制
    digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8',
             '9', 'A', 'B', 'C', 'D', 'E', 'F']
    S = Stack()
    while n > 0:
        remainder = n % base
        S.push(digit[remainder])
        n //= base
    s = ''
    while not S.empty():
        s += S.pop()
    return s


Catalan = [1, 1]


def count_sp(n):  # 计算栈混洗数量
    if n < len(Catalan):
        return Catalan[n]
    else:
        s = 0
        for i in range(n):
            s += count_sp(i) * count_sp(n - i - 1)
        Catalan.append(s)
        return s


def sp_check(A: Stack, B: Stack):  # 模拟进出栈判断是否为栈混洗
    s = Stack()
    c = Stack()
    while not A.empty():  # A非空时出栈
        i = 0
        s.push(A.pop())
        while not s.empty():
            if s.top() == B[i]:  # 判断S是否需要出栈，i标识出栈的次序
                c.push(s.pop())
                i += 1
            else:
                break
    return s.empty()  # 如果中间栈s非空，说明不能将A转入B中


def paren(s: str):
    check = {')': '(', ']': '[', '}': '{'}
    st = Stack()
    for i in s:
        if i in ("(", "[", "{"):
            st.push(i)
        if i in (")", "]", "}"):
            if st.top() == check[i]:
                st.pop()
            else:
                return False
    return st.empty()


def evaluate(s: str):  # 表达式求值,接受浮点数，
    temp = ''
    RPN = ''
    opnd = Stack()
    optr = Stack()
    optr.push('\0')  # 尾哨兵

    def read_number(i):
        temp = ''
        for num in range(i, len(s)):
            if s[num].isdigit() or s[num] == '.':
                temp += s[num]
            else:
                if '.' in temp:
                    return float(temp), num
                else:
                    return int(temp), num

    Operator = ["+", "-", "*", "/", "^", "!", "(", ")", "\0"]
    pri = [['>', '>', '<', '<', '<', '<', '<', '>', '>', ],
           ['>', '>', '<', '<', '<', '<', '<', '>', '>', ],
           ['>', '>', '>', '>', '<', '<', '<', '>', '>', ],
           ['>', '>', '>', '>', '<', '<', '<', '>', '>', ],
           ['>', '>', '>', '>', '>', '<', '<', '>', '>', ],
           ['>', '>', '>', '>', '>', '>', ' ', '>', '>', ],
           ['<', '<', '<', '<', '<', '<', '<', '=', ' ', ],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
           ['<', '<', '<', '<', '<', '<', '<', ' ', '=']]
    order = 0
    while not optr.empty():
        if s[order].isdigit():
            num, order = read_number(order)
            opnd.push(num)
            RPN += opnd.top()
        else:
            case = pri[Operator.index(optr.top())][Operator.index(s[order])]
            if case == '<':
                optr.push(s[order])
                order += 1
                break
            elif case == '=':
                optr.pop()
                order += 1
                break
            elif case == '>':
                pt = optr.pop()  # 处理之前已经入栈的运算符和数据、当前的运算符不处理
                RPN += pt
                if pt == '!':
                    pn = opnd.pop()
                    import math
                    opnd.push(math.factorial(pn))
                else:
                    pn2 = opnd.pop()
                    pn1 = opnd.pop()
                    if pt == '+':
                        opnd.push(pn1 + pn2)
                    elif pt == '-':
                        opnd.push(pn2 - pn1)
                    elif pt == '*':
                        opnd.push(pn1 * pn2)
                    elif pt == "/":
                        opnd.push(pn2 / pn1)
                    elif pt == '^':
                        opnd.push(pow(pn1, pn2))
                break
            else:
                import sys
                sys.exit(-1)
        return opnd.pop()


class Queen:  # 皇后类
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x or self.y == other.y or (self.x + self.y) == (other.x + other.y) or (
                self.x - self.y) == other.x - other.y

    # def __ne__(self, other):
    #     return not self == other


def placeQueens(N: int):
    import copy
    solu = Stack()
    q = Queen(0, 0)
    while q.x > 0 or q.y < N:
        if N <= solu.size() or N <= q.y:  # q超界或者解的元素个数大于等于N，则需要回溯
            q = solu.pop()
            q.y += 1  # 回溯上一行并试探下一列
        else:
            while q.y < N and solu.find(q, 0, solu.size()) >= 0:  # 在当前列寻找可摆放位置
                q.y += 1
            if q.y < N:  # 存在可摆放位置
                solu.push(copy.deepcopy(q))
                if solu.size() >= N:
                    solu.traverse()
                q.x += 1
                q.y = 0


from chr03 import List


class Queue(List):
    def enqueue(self, e):
        self.insertAsLast(e)

    def dequeue(self):
        return self.remove(self.first())

    def front(self):
        return self.first().data

    def empty(self):
        return self._size == 0

