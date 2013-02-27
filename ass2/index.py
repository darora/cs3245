#!/usr/bin/env python2

import getopt
import sys
import nltk
import os
import math
import itertools
from nltk.stem.porter import PorterStemmer

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
            while t > c:
                target_node = target_node.next
                c += 1
            node.pointers.append(target_node)

dictionary = {}
postings = []

current_line = 0

stemmer = PorterStemmer()


def get_files_list(dir_path):
    try:
        return os.listdir(dir_path)
    except OSError:
        print "Invalid directory path encountered: " + dir_path
        sys.exit(-1)

def get_file_content(filePath):
    try:
        f = open(filePath, 'r')
        content = f.readlines()
        f.close()
        return (content, filePath)
    except IOError:
        print "Invalid filePath encountered: " + filePath
        sys.exit(-1)

def postprocess_file(contents):
    contents = contents[0]
    return " ".join(map(lambda x: x.strip(), contents))

def index_content(file_contents, docId):
    sentences = nltk.sent_tokenize(file_contents)
    words = map(nltk.word_tokenize, sentences)
    words = map(lambda x: [stemmer.stem(y.lower()) for y in x], words) # case-folding, stemming
    words = {}.fromkeys([x for y in words for x in y]).keys() # the
# fastest method to make a list unique, benchmarks by
# http://www.peterbe.com/plog/uniqifiers-benchmark. Also note that I'm
# flattening the list here.
    
    for word in words:
        index_word(word, docId)

def index_word(word, docId):
    global current_line
    if word not in dictionary:
        dictionary[word] = current_line
        lst = SkipList()
        lst.append(docId)
        postings.insert(current_line, lst)
        current_line += 1
    else:
        postings[dictionary[word]].append(docId)
    
    




def main():
    lst = get_files_list(dir_to_index)
    for fl in lst:
        filePath = os.path.join(dir_to_index, fl)
        contents = postprocess_file(get_file_content(filePath))
        index_content(contents, os.path.basename(filePath))
    # for k,v in dictionary.iteritems():
    #     print str(len(postings[v])) + " is the frequency for " + k



        



def usage():
    print "usage info TODO"




dir_to_index = None
dict_file = None
postings_file = None
    
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        dir_to_index = a
    elif o == '-d':
        dict_file = a
    elif o == '-p':
        postings_file = a
    else:
        assert False, "unhandled option"
        
if dir_to_index == None or dict_file == None or postings_file == None:
    usage()
    sys.exit(0)

main()
