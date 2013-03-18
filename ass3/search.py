# import line_profiler
import math
import nltk
from parser import Operation, Tree
import cPickle, getopt, sys, logging
from nltk.stem.porter import PorterStemmer

class Search:
    """
    Initialize with postings file & dictionary filenames.
    """
    # @profile
    def __init__(self, postings_file, dictionary_file):
        dct = open(dictionary_file, 'rb')
        self.dictionary = cPickle.load(dct)
        dct.close()
        self.postings_file = open(postings_file, 'rb')
        self.stemmer = PorterStemmer()
        t = open('FILE_COUNT', 'r')
        self.FILE_COUNT = int(t.readline().strip())
        t.close()

    # @profile
    def process_query(self, query):
        query = self.preprocess_query(query)
        scores = {}
        
        if not query:
            return []
        
        for term, wt in query.iteritems():
            if wt == 0:
                continue
            postings_lst = self.search_term(term)
            for doc in postings_lst:
                if doc[0] in scores:
                    scores[doc[0]] += self.get_log_tf(doc[1]) * wt
                else:
                    scores[doc[0]] = self.get_log_tf(doc[1]) * wt


        def comparator(x, y):
            if x[0] > y[0]:
                return -1
            elif x[0] < y[0]:
                return 1
            elif x[1] > y[1]:
                return 1
            else:
                return -1
                    
        h = []
        for docId, score in scores.iteritems():
            h.append((score, int(docId)))
        h.sort(comparator)

        # for i in h[:10]:
        #     print i
        return map(lambda x: x[1], h[:10])

    # @profile
    def preprocess_query(self, query):
        dct = {}
        # case-folding, stemming the query
        terms = nltk.word_tokenize(query)
        terms = map(lambda x: self.stemmer.stem(x.lower()), terms)
        
        # calculate tf
        for term in terms:
            if term not in dct:
                dct[term] = 1
            else:
                dct[term] += 1
        denom = 0

        # calculate wt
        for k, v in dct.iteritems():
            tf = self.get_log_tf(v)
            idf = self.get_idf(k)
            # print str(idf)+k
            wt = tf * idf
            # dis-regard low wt terms from the query, when idf is at
            # most less than 1.0
            # if wt < 1.0:
            #     dct[k] = 0
            # else:
            denom += wt**2
            dct[k] = wt
        denom = math.sqrt(denom)

        if denom == 0:
            return []
        
        # normalization
        for k, wt in dct.iteritems():
            dct[k] = wt/denom
        return dct

    def str_results(self, lst):
        return " ".join([str(i) for i in lst])
    
    def get_idf(self, term):
        """
        Returns the inverted document frequency for a term.
        """
        if term in self.dictionary:
            freq = self.dictionary[term][2]
            return math.log10(self.FILE_COUNT/freq)
        else:
            return 0

    def get_log_tf(self, freq):
        if freq == 10:
            return 0
        else:
            return 1 + math.log10(freq)

    # @profile
    def search_term(self, term):
        if term in self.dictionary:
            index = self.dictionary[term][1]
            self.postings_file.seek(index)
            results = cPickle.load(self.postings_file)
            return results
        else:
            return []
def main():
    search = Search(postings_file, dict_file)

    fd_query = open(query_file, 'r')
    fd_output = open(output_file, 'w')

    for query in fd_query.readlines():
        res = search.process_query(query)
        fd_output.write(search.str_results(res) + '\n')
    fd_query.close()
    fd_output.close()
    

def manual_mode():
    """
    A driver for a CLI, rather than file-based. If this is used instead of main(), the -q and -o flags are "ignored" in that they don't do anything. You'll still have to pass them in, though. Why? Because lazy.
    """
    search = Search(postings_file, dict_file)    
    while True:
        query = raw_input("Query:")
        if not query:
            break
        # res = search.process_tree(search.build_query_tree(query))
        # print res
        res = search.process_query(query)
        print search.str_results(res)
        
    

    
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


main()
# manual_mode()
