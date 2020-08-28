"""
AVL树平衡条件过于苛刻，维护成本较高
伸展树：
    局部性：刚被访问过的数据极有可能很快再次被访问到，信息处理中普遍存在
    BST：下一个要访问的节点，极有可能在刚被访问节点附件
    AVL：连续查找m次需要O(mlogn)
    逐层伸展：
        节点一旦访问，就通过zig,zag旋转将访问节点转移至树根
        缺点：
            最坏情况下重构效率过低
    优化：Tarjan，逐层伸展转换成双层伸展，考察祖孙三代，
         两次旋转使节点上升两层，成为(子)树根，
         zig-zag，zag-aig，zig(p)->zag(g)。与AVL双旋等效(v,p,g)
         zig-zig，zag-zag,zig(g)->zig(p)
    折叠效果：访问坏节点时，对应路径的长度随即减半，规避最坏情况，分摊效率O(logn)
    综合评价：
        伸展树更为灵活，实现更加简单易行，优于AVL
        时间复杂度分摊O(logn)，与AVL相当
        局部性强，缓存命中率极高，访问效率可能更高，达到O(logk)，k为访问元素数
        但是不能保证单次最坏情况出现
        不适用于对效率敏感的场合
"""
from chr05 import BinNode
from chr07 import BST


def attach_as_lchild(p: BinNode, lc: BinNode) -> None:
    p.lc = lc
    if lc is not None:
        lc.parent = p


def attach_as_rchild(p: BinNode, rc: BinNode) -> None:
    p.rc = rc
    if rc is not None:
        rc.parent = p


class Splay(BST):
    def search(self, e) -> BinNode:
        # 调整搜索结果到树根，查找失败时也将_hot节点调整至树根
        p = self.serrch_in(self._root, e)
        self._root = self.splay(p if p else self._hot)
        return self._root

    def insert(self, e) -> BinNode:
        if self._root is None:  # 处理空树的情况
            self._size += 1
            self._root = BinNode(e)
            return self._root
        node = self.search(e)
        if node.data == e:  # 约定不含重复元素，已有该元素是直接返回该节点
            return self._root
        t = self._root
        if self._root.data < e:  # 判断新节点的插入位置
            t.parent = self._root = BinNode(e, None, t, t.rc)
            if t.HasRChild():
                t.rc.parent = self._root
                t.rc = None
        else:
            t.parent = self._root = BinNode(e, None, t.lc, t)
            if t.HasLChild():
                t.lc.parent = self._root
                t.lc = None
        self._size += 1
        self.updateHeight(t)
        return self._root

    def remove(self, e):
        if self._root is None or self.search(e).data != e:
            # 空树或者待删除节点不存在，则无法删除
            return False
        w = self._root
        if self._root.HasLChild():
            # 没有左子树直接删除
            self._root = self._root.rc
            if self._root is not None:
                self._root.parent = None
        elif self._root.HasRChild():
            # 没有右子树直接删除
            self._root = self._root.lc
            if self._root is not None:
                self._root.parent = None
        else:  # 两个子树都存在
            l_tree = self._root.lc
            l_tree.parent = None
            self._root.lc = None  # 暂时摘除左子树
            self._root = self._root.rc  # 右子树保留
            self._root.parent = None
            self.search(w.data)
            # 在右子树中查找原来根节点，查找失败，但是会将最小节点伸展至根节点
            # 该节点最小，故其左子树肯定是空
            self._root.lc = l_tree  # 空的左子树接入原来的左子树
            l_tree.parent = self._root
        self.size -= 1
        if self._root is not None:
            # 更新根节点高度，其他节点高度在伸展过车工中已经更新过
            self.updateHeight(self._root)
        return True

    def splay(self, v: BinNode) -> BinNode:
        # v为最近访问需要伸展的节点
        if not v:
            return None
        while v.parent and v.parent.parent:  # 短路，父节点不存在直接跳出
            # 父节点，祖父节点都存在时进行一次调整
            # 将节点v上移两层，并同时有可能缩减三个节点的高度
            p: BinNode = v.parent
            g: BinNode = p.parent
            gg: BinNode = p.parent  # 记录g的父节点，调整后接入该节点
            if v.IsLChild():
                if p.IsLChild():  # zig-zig
                    attach_as_lchild(g, p.rc)
                    attach_as_lchild(p, v.rc)
                    attach_as_rchild(p, g)
                    attach_as_rchild(v, p)
                else:  # zig-zag
                    attach_as_lchild(p, v.rc)
                    attach_as_rchild(g, v.lc)
                    attach_as_lchild(v, g)
                    attach_as_rchild(v, p)
            else:
                if p.IsRChild():  # zag-zag
                    attach_as_rchild(g, p.lc)
                    attach_as_rchild(p, v.lc)
                    attach_as_lchild(v, g)
                    attach_as_rchild(v, p)
                else:  # zag-zig
                    attach_as_rchild(p, v.lc)
                    attach_as_lchild(g, v.rc)
                    attach_as_rchild(v, g)
                    attach_as_lchild(v, p)
            if gg is None:  # gg不存在时，v为根节点
                v.parent = None
            else:  # 根据原来节点g的位置接入当前子树
                if g == gg.lc:
                    attach_as_lchild(gg, v)
                else:
                    attach_as_rchild(gg, v)
            self.updateHeight(g)  # 更新相关节点高度
            self.updateHeight(p)
            self.updateHeight(v)
        p: BinNode = v.parent
        if p is not None:
            # 上面的调整是三层一组进行调整
            # 如果v只有父节点，进行一次两层的调整
            if v.IsLChild():
                attach_as_lchild(p, v.rc)
                attach_as_rchild(v, p)
            else:
                attach_as_rchild(p, v.lc)
                attach_as_lchild(v, p)
            self.updateHeight(p)
            self.updateHeight(v)
        v.parent = None  # 调整后v为根节点
        return v
