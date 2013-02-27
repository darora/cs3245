import math

class SkipListNode:
    def __init__(self, value = None):
        self.val = value
        self.pointers = None
        self.next = None
    def appendNode(self, node):
        if hasattr(node, "pointers"):
            self.next = node
        else:
            raise "invalid node"
        
class SkipList:
    def __init__(self):
        self.root = None
        self.last = None
        self.length = 0
    def __len__(self):
        return self.length

    def __getitem__(self, index):
        if index >= self.length:
            raise "Invalid index error"
        else:
            node = self.root
            c = 0
            while c < index:
                node = node.next
                c += 1
            return node
        
    def __getslice__(self, start, end):
        """
        Take note that this method returns a standard python list.
        """
        node = self[start]
        val = []
        val.append(node.val)
        while start < end:
            node = node.next
            start += 1
            val.append(node.val)
        return val        
    
    def append(self, value):
        if self.root is None:
            self.root = SkipListNode(value)
            self.last = self.root
        else:
            node = SkipListNode(value)
            self.last.appendNode(node)
            self.last = node
        self.length += 1
    def default_skips(self):
        l = len(self)
        skip_length = math.floor(math.sqrt(l))
        return skip_length
    def gen_skips(self, skipLengthFn):
        """
        skipLengthFn: (a:SkipList) -> int
        """
        init = 1
        skip_length = skipLengthFn()
        l = len(self)
        target = init + skip_length
        while init < l and target < l:
            yield (init, target)
            init = target
            target = init + skip_length
    def create_skips(self):
        c = 1
        node = self.root
        for i,t in self.gen_skips(self.default_skips):
            while i > c:
                node = node.next
                c += 1
            target_node = node
            node.pointers = []
            while t > c:
                target_node = target_node.next
                c += 1
            node.pointers.append(target_node)
            node = target_node
