import unittest

from chr02 import Vector


class VectorTest(unittest.TestCase):
    def test_find(self):
        t = Vector()
        t.copyFrom([5, 4, 3, 2, 1, 5], 0, 6)
        self.assertEqual(t.find(5), 0)
        self.assertEqual(t.find(10), -1)
        self.assertEqual(t.find(5, 1, t.size()), 5)

    def test_disordered(self):
        t = Vector()
        t.copyFrom([5, 4, 3, 2, 1], 0, 5)
        self.assertEqual(t.disordered(), 4)

    def test_insert(self):
        t = Vector()
        t.insert(0, 1)
        t.insert(0, 3)
        t.insert(1, 5)
        t.insert(5, 10)
        self.assertEqual(t[:], [3, 5, 1, 10])

    def test_remove_range(self):
        t = Vector()
        t.copyFrom([0, 1, 2, 3, 4, 5, 6], 0, 7)
        t.remove_range(3, 5)
        self.assertEqual(t[:], [0, 1, 2, 5, 6])
        t.remove(0)
        self.assertEqual(t[:], [1, 2, 5, 6])

    def test_deduplicate(self):
        t = Vector()
        t.copyFrom([0, 1, 1, 3, 1, 3, 6], 0, 7)
        s = t.deduplicate()
        self.assertEqual(set(t[:]), {0, 1, 3, 6})
        self.assertEqual(s, 3)

    def test_uniquify(self):
        t = Vector()
        t.copyFrom([0, 1, 1, 2, 3, 4, 5, 5], 0, 8)
        s = t.uniquify()
        self.assertEqual(t[:], [0, 1, 2, 3, 4, 5])
        self.assertEqual(s, 2)

    def test_bin_search(self):
        t = Vector()
        t.copyFrom([0, 1, 2, 3, 4, 5, 6], 0, 7)
        self.assertEqual(t.binSearch(0), 0)
        self.assertEqual(t.binSearch(3), 3)
        self.assertEqual(t.binSearch(6), 6)
        self.assertEqual(t.binSearch_A(0), 0)
        self.assertEqual(t.binSearch_A(4), 4)
        self.assertEqual(t.binSearch_A(6), 6)

    def test_sort(self):
        t = Vector()
        t.copyFrom([0, 1, 2, 3, 4, 5, 6], 0, 7)
        t.permute()
        t._bubbleSort()  # 冒泡排序
        self.assertEqual(t[:], list(range(7)))
        t.permute()
        t._selectSort()  # 选择排序
        self.assertEqual(t[:], list(range(7)))
        t.permute()
        t._mergeSort()  # 归并排序
        self.assertEqual(t[:], list(range(7)))
        t.permute()
        t.quickSort()  # 快速排序
        self.assertEqual(t[:], list(range(7)))


if __name__ == '__main__':
    unittest.main()
