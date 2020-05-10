# -*- coding:utf-8 -*-  
# !/usr/bin/python 
# 二叉搜索树
# 任一节点不大于其右后代，不小于其左后代
# 假定不含重复元素
# 中序遍历单调非降（充要条件）
from chr05 import BinTree, BinNode, stature


class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key


class BST(BinTree):
    def __init__(self):
        super().__init__()
        self._hot = None

    def search(self, e):
        """搜索节点e并返回找到的节点"""
        # _hot指向命中节点的父亲节点
        return self.serrch_in(self._root, e)

    def serrch_in(self, v: BinNode, e):
        """在节点v及其后代中寻找e"""
        if v is None or v.data == e:
            return v
        self._hot = v  # 记录当前节点
        if e < v.data:
            return self.serrch_in(v.lc, e)
        else:
            return self.serrch_in(v.rc, e)

    def insert(self, e):
        """插入节点，返回插入后节点"""
        node = self.search(e)
        if node:
            # 约定不含重复元素，故元素重复是不做操作直接返回
            return node
        node = BinNode(data=e, parent=self._hot)  # 插入节点，空树也可正常处理
        self._size += 1
        self.updateHeightAbove(node)  # 更新x历代祖先高度
        return node

    def remove(self, e):
        """移除节点"""
        node = self.search(e)
        if not node:
            # 目标不存在
            return False
        self.removeAt(node)
        self._size -= 1
        self.updateHeightAbove(self._hot)
        return True

    def removeAt(self, x: BinNode):
        """实际移除节点方法"""
        remove_node = x  # 实际摘除的节点，初始值为x
        succ = None  # 实际被删除节点的接替者
        if not x.HasLChild():  # 没有左节点，直接用右节点代替
            succ = x = x.rc
        elif not x.HasRChild():
            succ = x = x.lc
        else:
            remove_node = remove_node.succ()  # 寻找移除节点的后继节点
            # 后继节点是当前节点右子树左侧分支的末端，一定没有左孩子
            x.data, remove_node.data = remove_node.data, x.data
            # 移除节点与后继节点交换，可以只交换数据
            # 待删除节点交换后至多只有一个右孩子
            u = remove_node.parent  # 获取后继节点的父节点
            if u == x:  # 只有当移除节点是后继节点的父节点时，删除后插入右分支
                u.rc = succ = remove_node.rc
            else:  # 其他情况都是插入左分支
                u.lc = succ = remove_node.rc
        self._hot = remove_node.parent  # 可能需要更新高度的最低节点
        if succ:  # succ不为None时需指定父节点
            succ.parent = self._hot
        del remove_node
        return succ


"""
等价BST：
    上下可变：连接关系不尽相同，承袭关系可能颠倒
    左右不乱：中序遍历序列完全一致，全局单调非降
zig(v)
zag(v)
"""


class AVL(BST):
    """
    平衡因子：左右子树高度差
    所有节点平衡因子绝对值不大于1
    """

    @staticmethod
    def blance_factory(node: BinNode):
        """获取节点的平衡因子"""
        return stature(node.lc) - stature(node.rc)

    def avl_balanced(self, node: BinNode):
        """判断节点是否满足AVL平衡条件"""
        return -2 < self.blance_factory(node) < 2

    def insert(self, e):
        # 可能导致插入节点的多个祖先节点失衡，但仅需一次调整
        # 直接调用super() 导致多执行了一次节点更新操作
        node = super().insert(e)
        g: BinNode = self._hot
        while g:  # 只会有一个节点可能失衡，调整后直接中断循环
            if not self.avl_balanced(g):
                g = self.rotate_at(g.tallerChild().tallerChild())
                break
            else:
                self.updateHeight(g)
            g = g.parent
        return node

    def remove(self, e):
        # 移除节点的父节点均有可能失衡
        # 直接调用super() 导致多执行了一次节点更新操作
        super(AVL, self).remove(e)
        g: BinNode = self._hot
        while g:  # 检测每个祖先节点，对失衡的节点进行调整
            if not self.avl_balanced(g):
                g = self.rotate_at(g.tallerChild().tallerChild())
            self.updateHeight(g)
            g = g.parent
        return True

    def connect34(self, a: BinNode, b: BinNode, c: BinNode, t0: BinNode, t1: BinNode, t2: BinNode, t3: BinNode):
        """3+4重构，根据中序遍历结果确定的顺序，直接重构子树，不进行zig，zag旋转"""
        a.lc = t0
        if t0: t0.parent = a
        a.rc = t1
        if t1: t1.parent = a; self.updateHeight(a)
        c.lc = t2
        if t2: t2.parent = c
        c.rc = t3
        if t3: t3.parent = c; self.updateHeight(c)
        b.lc = a
        a.parent = b
        b.rc = c
        c.parent = b
        self.updateHeight(b)
        return b

    def rotate_at(self, v: BinNode):
        """根据中序遍历结果确定3代节点顺序以及4棵子树顺序"""
        p: BinNode = v.parent  # 父节点
        g: BinNode = p.parent  # 祖父节点
        if p.IsLChild():
            if v.IsLChild():
                p.parent = g.parent  # 重构后子树与原来avl树连接
                return self.connect34(v, p, g, v.lc, v.rc, p.rc, g.rc)
            else:
                v.parent = g.parent
                return self.connect34(p, v, g, p.lc, v.lc, v.rc, g.rc)
        else:
            if v.IsRChild():
                p.parent = g.parent
                return self.connect34(g, p, v, g.lc, p.lc, v.lc, v.rc)
            else:
                v.parent = g.parent
                return self.connect34(g, v, p, g.lc, v.lc, v.rc, p.rc)
