"""
优先级队列  priority queue
    维护偏序关系，替代全序关系，降低顺序性的维护成本，并保证获取最高级数据的效率
    完全二叉堆：
        逻辑结构等同于完全二叉树，线性存储该完全二叉树的层次遍历结果,每个节点都不大于其父节点
        向量中任意元素均满足，完全二叉树中节点在向量中秩为i的节点
            左孩子：2i+1
            右孩子：2i+2
            父节点： (i-1)>>1
    左式堆：实现堆的快速合并
        完全二叉堆合并两个堆需要将较小的堆逐一取出加入较大堆，效率O(m*log(n+m))，效率低
        弗洛伊德建堆算法可以只将将两堆合并后建堆，效率O(n+m),但是没有使用原有堆的偏序性

        增加新条件：单测倾斜：节点分布偏于左侧  控制右侧高度O(logn)
                           合并操作只涉及右侧
        空节点路径长度：Null Path Length (npl)
                      引入外部节点，将堆转化成完全二叉堆
                      消除一度节点，转化成真二叉树
                      0)npl(NUll) = 0
                      1)npl(x) = 1+ min( npl(lc(x)),npl((rc(x)) )
                  npl(x) = x到外部节点的最近距离
                  npl(x) = 以x为根的最大满子树高度
        左倾： 任一内部节点x npl(lc(x)) >= npl(rc(x))
        推论： 任一内部节点x ，npl(x)=1+npl(rc(x))
        满足左倾性的堆即为左式堆
        左式堆的子堆也是左式堆
    右侧链：节点x出发，一直沿右分支前进， rChain(x)
        rChain(root)的终点是全堆中最浅的外部节点
        npl(r) === |rChain(r)| = d
        存在一颗以r为根，高度为d的满子树
        右侧链长度为d的左式堆，至少包含 2^d-1个内部节点，2^(d+1)-1个节点
        包含n个节点的左式堆，右侧链长度d满足：d<= log2(n+1)取整 -1 = O(logn)
"""
from abc import ABC, abstractmethod

from chr05 import BinTree


class PriorityQueue(ABC):
    @abstractmethod
    def size(self):
        """获取队列规模"""

    @abstractmethod
    def insert(self, data):
        """插入数据"""

    @abstractmethod
    def get_max(self):
        """获取优先级最高的数据"""

    @abstractmethod
    def del_max(self):
        """删除优先级最高的数据"""


def left_child(i): return 2 * i + 1  # 左孩子


def right_child(i): return 2 * i + 2  # 右孩子


def parent(i): return (i - 1) >> 1  # 当前节点的父节点


def parent_valid(i): return i > 0  # 当前节点是否有父节点


class PriorityQueueComplHeap(PriorityQueue):
    def __init__(self):
        self._element = []

    def size(self):
        return len(self._element)

    def insert(self, data):
        self._element.append(data)
        self.percolate_up(self.size() - 1)

    def get_max(self):
        return self[0]

    def del_max(self):
        max_elem = self[0]
        self[0] = self[self.size() - 1]
        self._element = self._element[:-1]
        self.percolate_down(0)
        return max_elem

    def heapify(self, data: list):
        """Floyd建堆算法"""
        self._element = data
        i = self.last_internal()
        # 规避掉最下层的叶结点，完全二叉树中叶结点较多，n/2个
        while self.in_heap(i):  # 自底而上，依次下滤各个内部节点
            self.percolate_down(i)
            i -= 1
        # 节点较多的底层节点需要下滤的深度低
        # 时间复杂度O(n)

    def __getitem__(self, item):
        return self._element[item]

    def __setitem__(self, key, value):
        self._element[key] = value

    def percolate_up(self, i):
        """上滤指定元素"""
        while parent_valid(i):  # 节点没有父节点，即达到堆顶时终止
            j = parent(i)
            if self[j] > self[i]: break  # 父子节点不再逆序时终止
            self[i], self[j] = self[j], self[i]  # 交换节点值，考察上一层
            i = j
        return i

    def percolate_up_a(self, i):
        # 存储需要上滤的元素的值，每次上滤只将上层值下移，找到最终位置后再将上滤元素上移
        # 降低交换的复制操作数有3次减少到1次
        temp = self[i]  # 存储i的值
        while parent_valid(i):  # 节点没有父节点，即达到堆顶时终止
            j = parent(i)
            if self[j] > temp: break  # 父子节点不再逆序时终止
            self[i] = self[j]  # 交换节点值，考察上一层
            i = j
        self[i] = temp
        return i

    def percolate_up_b(self, i):
        # 任一节点确定后其祖先节点也已经确定，可以将其祖先节点视为静态查找表
        # 对该表进行二分查找确定节点的插入位置，降低比较次数到O(loglogn)
        pass

    def percolate_down(self, i):
        """下滤指定元素"""
        while True:
            j = self.proper_parent(i)
            if i == j:
                break
            else:
                self[i], self[j] = self[j], self[i]
                i = j
        # 元素下滤方向不确定，不能二分加速，可以参考上滤减少复制的交换次数
        return i

    def in_heap(self, i):
        """判断坐标i是否合法，n为堆大小"""
        return -1 < i < self.size()

    def left_child_valid(self, i):
        """判断i是否有左孩子"""
        return self.in_heap(left_child(i))

    def right_child_valid(self, i):
        """判断i是否有右孩子"""
        return self.in_heap(right_child(i))

    def last_internal(self):
        """最后一个内部节点，即末节点的父亲"""
        return parent(self.size())

    def proper_parent(self, i):
        """取父子三者中的最大者"""
        if self.right_child_valid(i):  # 有右孩子必有左孩子
            return max(i, left_child(i), right_child(i), key=lambda x: self[x])
        elif self.left_child_valid(i):
            return max(i, left_child(i), key=lambda x: self[x])
        else:
            return i


class LeftHeapPriorityQueue(PriorityQueue, BinTree):
    def insert(self, data):
        pass

    def get_max(self):
        return self._root.data

    def del_max(self):
        pass


if __name__ == '__main__':
    pq = PriorityQueueComplHeap()
    pq.heapify([1, 4, 7, 9, 10, 2, 34])
    print(pq.del_max())
    print(pq.del_max())
    print(pq.del_max())
    pq.insert(15)
    print(pq.del_max())
    print(pq.del_max())
    print(pq.del_max())
    print(pq.del_max())
