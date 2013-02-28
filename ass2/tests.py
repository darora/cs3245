import random
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
        # TODO::test that the *right* skip pointers were created, i.e.
        # test the targets for the skips!
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

class TestSkipListMerging(unittest.TestCase):
    def get_skipList(self, length):
        lst = SkipList()
        data = sorted([random.randint(0, length*4) for i in range(0, length)])
        for i in range(0, length):
            lst.append(data[i])
        return lst

    def setUp(self):
        self.la = self.get_skipList(10)
        self.lb = self.get_skipList(20)
        self.lc = self.get_skipList(20)
        postings_file = {}      # TODO::create stub
        dictionary_file = {}    # TODO::create stub
        self.search = Search(postings_file, dictionary_file)

    def list_equality(self, lsta, lstb):
        self.assertEqual(lsta, lstb)

    def test_mergingSingleListShouldReturnTheList(self):
        """
        A single skip list should just be casted into a simple list and returned
        """
        lsts = [self.la]
        results = self.search.merge_results(MergeOperation.AND, lsts)
        self.list_equality(self.la.get_list(), results)

    def test_mergingTwoListsORshouldReturnUnion(self):
        lsts = [self.la, self.lb]
        results = self.search.merge_results(MergeOperation.OR, lsts)
        la = self.la.get_list()
        la.extend(self.lb.get_list())
        la = list(set(la))
        la.sort()
        self.list_equality(results, la)

    def test_mergingTwoListsOverANDshouldReturnIntersection(self):
        lsts = [self.la, self.lb]
        results = self.search.merge_results(MergeOperation.OR, lsts)
        la = set(self.la.get_list())
        lb = set(self.lb.get_list())
        ls = la & lb
        ls = list(ls)
        ls.sort()
        self.list_equality(results, ls)
        


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSkipListCreation)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSkipListMerging)
    unittest.TextTestRunner(verbosity=2).run(suite)
