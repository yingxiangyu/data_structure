import unittest
from chr10 import PriorityQueueComplHeap


class TsetPQ(unittest.TestCase):
    def test_pq(self):
        pq = PriorityQueueComplHeap()
        pq.heapify([1, 4, 7, 9, 10, 2, 34])
        self.assertEqual(pq.get_max(), 34)
        self.assertEqual(pq.del_max(), 34)
        self.assertEqual(pq.del_max(), 10)
        pq.insert(15)
        self.assertEqual(pq.del_max(), 15)
        self.assertEqual(pq.del_max(), 9)
        self.assertEqual(pq.del_max(), 7)
        self.assertEqual(pq.del_max(), 4)
        self.assertEqual(pq.del_max(), 2)


if __name__ == '__main__':
    unittest.main()