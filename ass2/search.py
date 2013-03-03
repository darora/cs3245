from parser import Operation
from skiplist import SkipList

class Search:
    """
    Initialize with postings file & dictionary file.
    """
    def __init__(self, postings_file, dictionary_file):
        self.postings = postings_file
        self.dictionary = dictionary_file
        
    def search(self):
        pass

    def merge_results(self, operation, *lists):
        """
        Arguments:
        - `operation`: Operation.OpCode
        - `*lists`: Lists to be merged over the specified "operation"
        """
        if len(lists) is 0:
            raise "You can't merge less than 1 list!"
        elif len(lists) is 1:
            return lists[0]
        else:
            lists = list(lists)
            lists.sort(key=len)
            lst = reduce(lambda x, y: self.merge_two_list(x, y, operation), lists[1:], lists[0]) # TODO::this would cause problems with > 2 lists, as the method still expects skip lists as input, whereas we'd have simple []
            return SkipList(lst)
                
    # TODO::make these methods return SkipLists as well, in order to
    # resolve nested queries efficiently...
    def merge_two_list(self, la, lb, op):
        """
        TODO::modify merge_results for NOT.
        For NOT, it is expected that the first list is expected to be the set that the second list is to be removed from.

        For OR, AND, order doesn't matter.
        """
        if op is Operation.OR: # TODO::implement a version of the
            # merge that potentially less memory in the average case
            lst = la.get_list() + lb.get_list()
            lst = {}.fromkeys(lst).keys()
            lst.sort()
            return lst
        elif op is Operation.AND:
            lst = []
            nodea = la.root
            nodeb = lb.root
            # TODO::skip usage!
            while nodea != None and nodeb != None:
                if nodea.val < nodeb.val:
                    nodea = nodea.next
                elif nodea.val > nodeb.val:
                    nodeb = nodeb.next
                else:
                    # found in both lists, add to results
                    lst.append(nodea.val)
                    nodea = nodea.next
                    nodeb = nodeb.next
            # lst.create_skips()
            return lst
        elif op is Operation.NOT:
            raise Exception("TODO")
        
    def get_next_index(*args):  # TODO::args not decided upon
        pass

    def build_query_tree(self, query_string):
        pass

    def preprocess_query_tree(self, query_tree):
        pass

    def search_term(self, term):
        pass

    def process_tree(self, query):
        if query != None and query.operator != None:
            op = query.operator
            results = None
            if op == Operation.AND or op == Operation.OR:
                resA = self.process_tree(query.left)
                resB = self.process_tree(query.right)
                results = merge_results(op, resA, resB)
            elif op == Operation.NOT:
                resA = self.process_tree(query.right)
                raise Exception("TODO::Not implemented yet")
            return results
        raise Exception("Invalid Query Tree"+str(query))
