class Search:
    """
    Initialize with postings file & dictionary file.
    """
    def __init__(self, postings_file, dictionary_file):
        self.postings = postings_file
        self.dictionary = dictionary_file
        
    def search():
        pass

    def merge_results(*lists):
        if len(lists) is 0:
            raise "You can't merge less than 1 list!"
        elif len(lists) is 1:
            return lists[0]
        else:
            lists.sort(key=len)
            pass

    def merge_two_list(la, lb, op):
        if op is MergeOperation.OR: # TODO::implement a version of the
            # merge that potentially less memory in the average case
            lst = la + lb
            lst = {}.fromkeys(lst).keys()
            lst.sort()
            return lst
        elif op is MergeOperation.AND:
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
        
class MergeOperation:
    AND = 0
    OR  = 1
