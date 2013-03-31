#!/usr/bin/env python2

import getopt, sys, struct, cPickle, itertools, os
import nltk
from nltk.stem.porter import PorterStemmer
from utils import *
from file_ops import FileOps
from indexer import Indexer

dir_to_index = None
dict_file = None
postings_file = None
indexer = None

def main():
    """
    point of entry.
    * initialize things, get list of files to index
    * index words in all the files
    * dump the dict, postings lists to files
    """
    global indexer
    indexer = Indexer(dict_file, postings_file, dir_to_index)
    indexer.create_index()
    indexer.dump_indices_to_files()

def usage():
    print "python2 index.py -i directory-of-documents -d dictionary-file -p postings-file"

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

main()
