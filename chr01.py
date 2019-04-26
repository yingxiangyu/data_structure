# -*- coding:utf-8 -*-  
# !/usr/bin/python 
"""
@author:yyx 
@version: 1.0
@file: chr01.py
@time: 2019/4/25 9:54
"""


# 起泡排序
def bubblesort1A(n: int, A: list):
    sorte = False  # 标识整体是否有序
    while not sorte:
        sorte = True
        for i in range(n - 1):
            if A[i] > A[i + 1]:
                A[i], A[i + 1] = A[i + 1], A[i]
                sorte = False
        n -= 1


# Fibonacci数：二分递归
def fib(n: int):
    if n < 0:
        raise ValueError('n为负')
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


# Fibonacci数：迭代
def fibI(n: int):
    f = 0
    g = 1
    while n > 0:
        g += f
        f = g - f
        n -= 1
    return f
