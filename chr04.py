# -*- coding:utf-8 -*-  
# !/usr/bin/python 
"""
@author:yyx 
@version: 1.0
@file: chr04.py
@time: 2019/5/10 16:00
python内置有栈和队列的实现，有些操作的设置与书中不同，所以简单重写
"""


class Stack:
    def __init__(self):
        self._elem = []
        self._size = 0

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
    s=''
    while not S.empty():
        s+=S.pop()
    return s