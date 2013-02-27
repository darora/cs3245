import unittest

from skiplist import SkipList
from search import Search, MergeOperation


class TestSkipListCreation(unittest.TestCase):
    def setUp(self):
        data = range(0, 20)
        self.lst = SkipList()
        for i in data:
            self.lst.append(i)

    def test_listCreation(self):
        rt = self.lst.root
        for i in range(0, 20):
            self.assertEqual(rt.val, i)
            rt = rt.next

    def test_skipCreation(self):
        self.lst.create_skips()
        # TODO::test that skip pointers were created
        lngth = self.lst.default_skips()
        nextSkip = 0
        nd = self.lst.root
        for i in range(0, 20):
            if i == nextSkip and i + lngth < 20:
                self.assertNotEqual(len(nd.pointers),0)
                nextSkip += lngth
            else:
                self.assertIsNone(nd.pointers)
            nd = nd.next
                    

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSkipListCreation)
    unittest.TextTestRunner(verbosity=4).run(suite)
