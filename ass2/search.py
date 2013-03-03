from parser import Operation, Tree
from skiplist import SkipList
import pickle, getopt, sys

class Search:
    """
    Initialize with postings file & dictionary file.
    """
    def __init__(self, postings_file, dictionary_file):
        dct = open(dictionary_file, 'rb')
        self.dictionary = pickle.load(dct)
        dct.close()
        self.postings_file = open(postings_file, 'rb')
        
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
            lst = reduce(lambda x, y: self.merge_two_list(x, y, operation), lists[1:], lists[0])
            return lst
                
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
            return SkipList(lst)
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
            return SkipList(lst)
        elif op is Operation.NOT:
            raise Exception("TODO")
        
    # def get_next_index(*args):  # TODO::args not decided upon
    #     pass

    def build_query_tree(self, query_string):
        return Tree(query_string)

    def preprocess_query_tree(self, query_tree):
        pass

    def search_term(self, term):
        # TODO::to use file instead...
        if term in self.dictionary:
            index = self.dictionary[term][1]
            self.postings_file.seek(index)
            results = pickle.load(self.postings_file)
            return results
        else:
            return SkipList()

    def process_tree(self, query):
        if query != None and query.operator != None:
            op = query.operator
            results = None
            if op == Operation.AND or op == Operation.OR:
                resA = self.process_tree(query.left)
                resB = self.process_tree(query.right)
                results = self.merge_results(op, resA, resB)
            elif op == Operation.NOT:
                resA = self.process_tree(query.right)
                raise Exception("TODO::Not implemented yet")
            return results
        elif query.string != None:
            return self.search_term(query.string)
        raise Exception("Invalid Query Tree"+str(query))

def main():
    search = Search(postings_file, dict_file)
    query = Tree("monday OR rule")
    res = search.process_tree(query)
    print res

    print search.process_tree(Tree("he AND ha"))
    print search.process_tree(Tree("he AND ha AND other"))
    print search.process_tree(Tree("(she OR ha) AND he"))

def usage():
    print "usage info TODO"

query_file = None
dict_file = None
postings_file = None
output_file = None

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'q:d:p:o:')
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == '-q':
            query_file = a
        elif o == '-d':
            dict_file = a
        elif o == '-p':
            postings_file = a
        elif o == '-o':
            output_file = a
        else:
            assert False, "unhandled option"

    if query_file == None or dict_file == None or postings_file == None or output_file == None:
        usage()
        sys.exit(0)
else:
    # dev mode. TODO::remove, or integrate through makefile...
    query_file    = "queries"
    dict_file     = "dict.data"
    postings_file = "postings.data"
    output_file = "output"
main()
