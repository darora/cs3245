class Search:
    """
    Initialize with postings file & dictionary file.
    """
    def __init__(self, postings_file, dictionary_file):
        self.postings = postings_file
        self.dictionary = dictionary_file
        
    def search():
        pass

    def merge_results(operation, *lists):
        """
        
        Arguments:
        - `operation`: Operation.OpCode
        - `*lists`: Lists to be merged over the specified "operation"
        """
        

        if len(lists[1]) is 0:
            raise "You can't merge less than 1 list!"
        elif len(lists[1]) is 1:
            return lists[1][0].get_list()
        else:
            lst_lists = list(lists[1:])
            lst_lists.sort(key=len)
            pass

    def merge_two_list(la, lb, op):
        if op is Operation.OR: # TODO::implement a version of the
            # merge that potentially less memory in the average case
            lst = la + lb
            lst = {}.fromkeys(lst).keys()
            lst.sort()
            return lst
        elif op is Operation.AND:
            lst = []
            nodea = la.root
            nodeb = lb.root
            
            while nodea != None and nodeb != None:
                if nodea.val < nodeb.val:
                    pass
                elif nodea.val > nodeb.val:
                    pass
                else:           # found in both lists, add to results
                    lst.append(nodea.val)
                    nodea = nodea.next
                    nodeb = nodeb.next

            while nodea != None:
                lst.append(nodea.val)
                nodea = nodea.next
            while nodeb != None:
                lst.append(nodeb.val)
                nodeb = nodeb.next
            return lst

    def get_next_index(*args):  # TODO::args not decided upon
        pass
