import random
import unittest
import logging
import sys

from skiplist import SkipList
from search import Search
from parser import Operation, Tree

# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

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
        lngth = self.lst.default_skip_length()
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
            lst.append(data[i]) # TODO:swap out with SkipList(data)
        return lst

    def setUp(self):
        self.la = self.get_skipList(10)
        self.lb = self.get_skipList(20)
        self.lc = self.get_skipList(20)
        postings_file = "dev_postings.data"
        dictionary_file = "dev_dict.data"
        self.search = Search(postings_file, dictionary_file)

    def list_equality(self, lsta, lstb):
        try:
            self.assertEqual(len(lsta), len(lstb))
            self.assertEqual(lsta.get_list(), lstb.get_list())
        except AssertionError as e:
            logging.info(lsta)
            logging.info(lstb)
            print lsta
            print lstb
            raise e

    def test_mergingSingleListShouldReturnTheList(self):
        """
        A single skip list should just be casted into a simple list and returned
        """
        results = self.search.merge_results(Operation.AND, self.la)
        self.list_equality(self.la, results)

    def test_mergingTwoListsORshouldReturnUnion(self):
        results = self.search.merge_results(Operation.OR, self.la, self.lb)
        # results = self.search.merge_two_list(self.la, self.lb, Operation.OR)
        la = self.la.get_list()
        la.extend(self.lb.get_list())
        la = list(set(la))
        la.sort()
        self.list_equality(results, SkipList(la))

    def test_mergingTwoListsOverANDshouldReturnIntersection(self):
        results = self.search.merge_results(Operation.AND, self.la, self.lb)
        # results = self.search.merge_two_list(self.la, self.lb, Operation.AND)
        la = set(self.la.get_list())
        lb = set(self.lb.get_list())
        ls = la & lb
        ls = list(ls)
        ls.sort()
        self.list_equality(results, SkipList(ls))
        
class TestQueryParsing(unittest.TestCase):

    def checkEquality(self, tree1, tree2):
        right = False
        left = False
        base = False

        if tree1.right == None and tree2.right == None:
            right = True
        elif tree1.right != None and tree2.right != None:
            right = self.checkEquality(tree1.right, tree2.right)

        if tree1.left == None and tree2.left == None:
            left = True
        elif tree1.left != None and tree2.left != None:
            left = self.checkEquality(tree1.left, tree2.left)

        if tree1.operator == None and tree2.operator == None:
            if tree1.string != None and tree2.string != None:
                base = tree1.string == tree2.string
        elif tree1.operator != None and tree2.operator != None:
            base = tree1.operator == tree2.operator

        if not left:
            logging.debug("Left##########")
            logging.debug(tree1.left)
            logging.debug(tree2.left)
        if not right:
            logging.debug("Right####################")
            logging.debug(tree1.right)
            logging.debug(tree2.right)
        if not base:
            logging.debug("Base##########")
            logging.debug(tree1.operator)
            logging.debug(tree2.operator)
            logging.debug(tree1.string)
            logging.debug(tree2.string)
        if not (base and right and left):
            # logging.debug("#################### Trees")
            # logging.debug(tree1)
            # logging.debug(tree2)
            raise Exception("Failed checks") # Let's not pollute the
        # output if we know that we've failed already
        return base and right and left
        
    
    def test_creatingAND(self):
        first = Tree("hello AND world")
        b = Tree()
        b.operator = Operation.AND
        l = Tree("hello")
        r = Tree("world")
        b.right = r
        b.left = l
        self.assertTrue(self.checkEquality(first, b))
        logging.debug(first)

    def test_creatingOR(self):
        second = Tree("hello OR world")
        b = Tree()
        b.operator = Operation.OR
        l = Tree("hello")
        r = Tree("world")
        b.right = r
        b.left = l
        self.assertTrue(self.checkEquality(second, b))
        logging.debug(second)

    def test_creatingAND_NOT(self):
        third = Tree("hello AND NOT world")
        b = Tree()
        b.operator = Operation.AND
        l = Tree("hello")
        r = Tree("world")
        r_base = Tree()
        r_base.operator = Operation.NOT
        r_base.right = r
        b.right = r_base
        b.left = l
        self.assertTrue(self.checkEquality(third, b))
        
        logging.debug(third)

    def test_creatingNOT_OR(self):
        fourth = Tree("NOT hello OR world")

        b = Tree()
        b.operator = Operation.OR
        l = Tree("hello")
        l_base = Tree()
        l_base.operator = Operation.NOT
        l_base.right = l
        r = Tree("world")
        b.right = r
        b.left = l_base

        self.assertTrue(self.checkEquality(fourth, b))

    def test_creating_AND_OR_AND_NOT(self):
        fifth = Tree("hello AND world OR hello AND NOT world") # TODO::test optimizations

        b = Tree()
        b.operator = Operation.OR

        l_1 = Tree()
        l_1.operator = Operation.AND
        l_1_l = Tree("hello")
        l_1_r = Tree("world")
        l_1.left = l_1_l
        l_1.right = l_1_r

        r_1 = Tree()
        r_1.operator = Operation.AND
        r_1_r = Tree()
        r_1_r.operator = Operation.NOT
        r_1_r_r = Tree("world")
        r_1_r.right = r_1_r_r
        r_1_l = Tree("hello")
        r_1.right = r_1_r
        r_1.left = r_1_l

        b.right = r_1
        b.left = l_1

        self.assertTrue(self.checkEquality(fifth, b))

    def test_creating_paran1(self):
        first = Tree("(hello AND world)")
        b = Tree("hello AND world")
        self.assertTrue(self.checkEquality(first, b))
        
    def test_creating_paran2(self):
        second = Tree("(hello OR world) AND earth")
        b = Tree()
        b.operator = Operation.AND
        bl, br = Tree("hello OR world"), Tree("earth")
        b.left = bl
        b.right = br
        self.assertTrue(self.checkEquality(second, b))

    def test_creating_paran3(self):
        third = Tree("earth AND (hello OR world)")
        b = Tree()
        b.operator = Operation.AND
        br, bl = Tree("hello OR world"), Tree("earth")
        b.left = bl
        b.right = br
        self.assertTrue(self.checkEquality(third, b))


    def test_creating_paran4(self):
        tr = Tree("earth AND NOT (hello OR world)")
        b = Tree()
        b.operator = Operation.AND
        bl = Tree("earth")
        br = Tree()
        br.operator = Operation.NOT
        brr = Tree("hello OR world")
        br.right = brr
        
        b.left = bl
        b.right = br

        self.assertTrue(self.checkEquality(tr, b))

    
    def test_creating_paran4_5(self):
        tr = Tree("NOT (hello OR world)")
        b = Tree()
        b.operator = Operation.NOT
        br = Tree("hello OR world")
        
        b.right = br

        self.assertTrue(self.checkEquality(tr, b))

    
        
    def test_creating_paran5(self):
        tr = Tree("earth AND NOT (hello OR world) OR mars")

        b = Tree()
        b.operator = Operation.OR
        br = Tree("mars")
        bl = Tree("earth AND NOT (hello OR world)")
        
        b.left = bl
        b.right = br
        
        self.assertTrue(self.checkEquality(tr, b))

    def test_creating_paran6(self):
        tr = Tree("earth AND NOT (hello OR world) OR (mars AND jupiter)")

        b = Tree()
        b.operator = Operation.OR
        br = Tree("(mars AND jupiter)")
        bl = Tree("earth AND NOT (hello OR world)")
        
        b.left = bl
        b.right = br

        self.assertTrue(self.checkEquality(tr, b))

    def test_creating_paran7(self):
        tr = Tree("(computer AND terminal)")
        b = Tree("computer AND terminal")
        self.assertTrue(self.checkEquality(tr, b))

    def test_creating_paran8(self):
        tr = Tree("(computer AND terminal) OR (soybean AND crush)")
        b = Tree()
        b.operator = Operation.OR
        br = Tree("soybean AND crush")
        bl = Tree("computer AND terminal")
        b.right = br
        b.left = bl
        self.assertTrue(self.checkEquality(tr, b))

        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSkipListCreation)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSkipListMerging)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQueryParsing)
    unittest.TextTestRunner(verbosity=2).run(suite)
