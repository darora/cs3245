#!/usr/bin/env python2

import getopt, sys, struct, pickle, itertools, os
import nltk
from nltk.stem.porter import PorterStemmer
from skiplist import SkipList

sys.setrecursionlimit(10000)    # My SkipList is a recursive
# LinkedList (sort of), so need to increase this here in order to
# pickle successfully.


dictionary = {}
postings = []
file_count = 0

UNIVERSAL_SET = 0
current_line = 1

stemmer = PorterStemmer()

def get_files_list(dir_path):
    try:
        return os.listdir(dir_path)
    except OSError:
        print "Invalid directory path encountered"
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
    """
    Remove the newlines that each line read in contains, and join them using a single space instead.
    """
    contents = contents[0]
    return " ".join(map(lambda x: x.strip(), contents))

def index_content(file_contents, docId):
    """
    Tokenizes the contents of the file.
    Next, carries out case-folding and stemming.
    Creates a file-specific dictionary of the term frequencies, that is merged into the global dictionary using another method.
    """
    sentences = nltk.sent_tokenize(file_contents)
    words = map(nltk.word_tokenize, sentences)
    words = map(lambda x: [stemmer.stem(y.lower()) for y in x], words) # case-folding, stemming

    words = [x for y in words for x in y] # non-unique list of terms, flattened.
    
    file_dict = {}
    for word in words:
        if word in file_dict:
            file_dict[word] += 1
        else:
            file_dict[word] = 1
    merge_file_term_counts(file_dict, docId)

def merge_file_term_counts(file_dict, docId):
    global current_line
    for k, v in file_dict.iteritems():
        if k in dictionary:
            postings[dictionary[word]].append((docId, v))
        else:
            dictionary[word] = current_line
            lst = SkipList()
            lst.append((docId,v))
            postings.insert(current_line, lst)
            current_line += 1
        
def main():
    """
    point of entry.
    * initialize things, get list of files to index
    * index words in all the files
    * dump the dict, postings lists to files
    """
    # init_universal_set()
    lst = get_files_list(dir_to_index)
    lst.sort(key=lambda x: int(x))
    for fl in lst:
        file_count += 1
        filePath = os.path.join(dir_to_index, fl)
        contents = postprocess_file(get_file_content(filePath))
        index_content(contents, fl)
        # postings[UNIVERSAL_SET] += str(fl) + ' '
    dump_files()
    
def dump_files():
    """
    * create skips for all but the universal set
    * pickle the postings lists & the dictionary
    * the dictionary now contains tuples of (id, postingListIndexLocation, postingListLength)
      - note that the last member is the document frequency df
    """
    fl_postings = open(postings_file, 'w+b')
    for k,v in dictionary.iteritems():
        # if k != "UNIVERSAL_SET":
        postings[v].create_skips()
        dictionary[k] = (v, fl_postings.tell(), len(postings[v]))
        pickle.dump(postings[v], fl_postings, 2)
    fl_postings.close()
    # write the dictionary
    fl_dict = open(dict_file, 'wb')
    pickle.dump(dictionary, fl_dict, 2)
    fl_dict.close()

    # the count of files being indexed
    fl_count = open("FILE_COUNT", 'w')
    fl_count.write(file_count)
    fl_count.close()

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
