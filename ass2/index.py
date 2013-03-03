#!/usr/bin/env python2

import getopt, sys, struct, pickle, itertools, os
import nltk
from nltk.stem.porter import PorterStemmer
from skiplist import SkipList

sys.setrecursionlimit(10000)

dictionary = {}
postings = []

UNIVERSAL_SET = 0
current_line = 1

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

def init_universal_set():
    dictionary["UNIVERSAL_SET"] = UNIVERSAL_SET
    postings.insert(UNIVERSAL_SET, "")
        
def main():
    init_universal_set()
    lst = get_files_list(dir_to_index)
    lst.sort(key=lambda x: int(x))
    for fl in lst:
        filePath = os.path.join(dir_to_index, fl)
        contents = postprocess_file(get_file_content(filePath))
        index_content(contents, fl)
        postings[UNIVERSAL_SET] += str(fl) + ' '
    dump_shits()
    
def dump_shits():
    fl_postings = open(postings_file, 'w+b')
    for k,v in dictionary.iteritems():
        if k != "UNIVERSAL_SET":
            postings[v].create_skips()
        dictionary[k] = (v, fl_postings.tell(), len(postings[v])) # ("line" (deprecated), indexToRead, Length)
        pickle.dump(postings[v], fl_postings, 2)
    fl_postings.close()
    # write the dictionary
    fl_dict = open(dict_file, 'wb')
    pickle.dump(dictionary, fl_dict, 2)
    fl_dict.close()

def usage():
    print "python2 index.py -i directory-of-documents -d dictionary-file -p postings-file"

dir_to_index = None
dict_file = None
postings_file = None

if __name__ == "__main__":
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
else:
    # dev mode. TODO::remove, or integrate through makefile...
    dir_to_index  = "./sample_data/"
    dict_file     = "dict.data"
    postings_file = "postings.data"
main()
