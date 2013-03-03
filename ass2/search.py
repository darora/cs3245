from parser import Operation, Tree
from skiplist import SkipList
import pickle, getopt, sys
import logging
from nltk.stem.porter import PorterStemmer

class Search:
    """
    Initialize with postings file & dictionary file.
    """
    def __init__(self, postings_file, dictionary_file):
        dct = open(dictionary_file, 'rb')
        self.dictionary = pickle.load(dct)
        dct.close()
        self.postings_file = open(postings_file, 'rb')
        self.stemmer = PorterStemmer()
        self.UNIVERSAL_SET = None # will be initialized on first access
        
    def search(self):
        pass

    def merge_results(self, operation, *lists):
        """
        Arguments:
        - `operation`: Operation.OpCode
        - `*lists`: Lists to be merged over the specified "operation"
           For NOT, pass in (opcode, Empty SkipList, Actual SkipList)
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
        For NOT, it is expected that the first list is expected to be the set that the second list is to be removed from.

        For OR, AND, order doesn't matter.
        """
        if op is Operation.OR: # TODO::implement a version of the
            # merge that potentially less memory in the average case
            lst = la.get_list() + lb.get_list()
            lst = {}.fromkeys(lst).keys()
            lst.sort(key=lambda x: int(x))
            return SkipList(lst)
        elif op is Operation.AND:
            lst = []
            nodea = la.root
            nodeb = lb.root
            # TODO::skip usage!
            while nodea != None and nodeb != None:
                if nodea.val < nodeb.val:
                    if nodea.pointers != None:
                        jmp = False
                        for target in nodea.pointers:
                            if target.val <= nodeb.val:
                                nodea = target
                                jmp = True
                        if not jmp:
                            nodea = nodea.next
                    else:
                        nodea = nodea.next
                elif nodea.val > nodeb.val:
                    if nodeb.pointers != None:
                        jmp = False
                        for target in nodeb.pointers:
                            if target.val <= nodea.val:
                                nodeb = target
                                jmp = True
                        if not jmp:
                            nodeb = nodeb.next
                    else:
                        nodeb = nodeb.next
                else:
                    lst.append(nodea.val)
                    nodea = nodea.next
                    nodeb = nodeb.next
            lst = SkipList(lst)
            lst.create_skips()
            return lst
        elif op is Operation.NOT:
            # TODO::use skip list merging...
            lsta = set(self.search_term("UNIVERSAL_SET").get_list())
            lstb = set(lb.get_list())
            results = list(lsta - lstb)
            results.sort(key=lambda x: int(x))
            return SkipList(results)

    # def get_next_index(*args):  # TODO::args not decided upon
    #     pass

    def build_query_tree(self, query_string):
        return Tree(query_string)

    def preprocess_query_tree(self, query_tree):
        pass

    def search_term(self, term):
        if term != "UNIVERSAL_SET":
            term = self.stemmer.stem(term.lower())
        elif self.UNIVERSAL_SET != None:
            return self.UNIVERSAL_SET
        
        if term in self.dictionary:
            index = self.dictionary[term][1]
            self.postings_file.seek(index)
            results = pickle.load(self.postings_file)
            if term == "UNIVERSAL_SET":
                results = SkipList(results.split())
                self.UNIVERSAL_SET = results
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
                resB = self.process_tree(query.right)
                results = self.merge_results(op, SkipList(), resB)
            return results
        elif query.string != None:
            return self.search_term(query.string)
        raise Exception("Invalid Query Tree"+str(query))

def main():
    search = Search(postings_file, dict_file)
    # query = Tree("monday OR rule")
    # print search.process_tree(query)

    # # print search.process_tree(Tree("NOT ha"))
    # print search.process_tree(Tree("he AND NOT other"))
    # print search.process_tree(Tree("(she OR ha) AND NOT he"))
    # print search.process_tree(Tree("(she OR ha) AND december"))

    fd_query = open(query_file, 'r')
    fd_output = open(output_file, 'w')

    for query in fd_query.readlines():
        fd_output.write(str(search.process_tree(search.build_query_tree(query))) + '\n')
    
    fd_query.close()
    fd_output.close()
    

def manual_mode():
    search = Search(postings_file, dict_file)    
    while True:
        query = raw_input("Query:")
        if not query:
            break
        res = search.process_tree(search.build_query_tree(query))
        print res
        
    

    
def usage():
    print "python2 search.py -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

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


# main()
manual_mode()
