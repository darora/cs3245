from parser import Operation

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
            return lists[0].get_list()
        else:
            lists.sort(key=len)
            lst = reduce(lambda x, y: self.merge_two_list(x, y, operation), lst_lists[1:], lst_lists[0])
            return lst
                

    def merge_two_list(self, la, lb, op):
        if op is Operation.OR: # TODO::implement a version of the
            # merge that potentially less memory in the average case
            lst = la.get_list() + lb.get_list()
            lst.sort()
            lst = {}.fromkeys(lst).keys()
            return lst
        elif op is Operation.AND:
            lst = []
            nodea = la.root
            nodeb = lb.root
            
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

            return lst

    def get_next_index(*args):  # TODO::args not decided upon
        pass
