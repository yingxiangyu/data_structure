# -*- coding:utf-8 -*-  
# !/usr/bin/python 
# 二叉搜索树
# 任一节点不大于其右后代，不小于其左后代
# 假定不含重复元素
# 中序遍历单调非降（充要条件）
from chr05 import BinTree, BinNode


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
        # _hot指向命中节点的父亲节点
        return self.serrch_in(self._root, e)

    def serrch_in(self, v: BinNode, e):
        # 在节点v及其后代中寻找e
        if v is None or v.data == e:
            return v
        self._hot = v  # 记录当前节点
        if e < v.data:
            return self.serrch_in(v.lc, e)
        else:
            return self.serrch_in(v.rc, e)

    def insert(self, e):
        node = self.search(e)
        if node:
            # 约定不含重复元素，故元素重复是不做操作直接返回
            return node
        node = BinNode(data=e, parent=self._hot)  # 插入节点，空树也可正常处理
        self.updateHeightAbove(node)  # 更新x历代祖先高度
        return node

    def remove(self, e):
        node = self.search(e)
        if not node:
            # 目标不存在
            return False
        self.removeAt(node)
        self.updateHeightAbove(self._hot)
        return True

    def removeAt(self, x: BinNode):
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
