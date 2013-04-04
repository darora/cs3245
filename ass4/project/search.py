# import line_profiler
import math
import nltk
import cPickle, getopt, sys
from nltk.stem.porter import PorterStemmer
from itertools import groupby, ifilter, imap
from indexer_targets import IndexFile
from file_ops import FileOps
from nltk.corpus import stopwords

class Search(object):
    """
    Initialize with postings file & dictionary filenames.
    Also initialize the number of files that were indexed.
    Use cPickle for greater speed.
    """
    # @profile
    def __init__(self, postings_file, dictionary_file):
        with open(dictionary_file, 'rb') as fl:
            self.dictionary = cPickle.load(fl)
        
        self.postings_file = open(postings_file, 'rb')
        self.stemmer = PorterStemmer()
        
        with open('./processed/FILE_COUNT', 'r') as fl:
            self.FILE_COUNT = int(fl.readline().strip())

        with open('./processed/citation_weights', 'rb') as fl:
            self.citation_weights = cPickle.load(fl)

    # @profile
    def process_query(self, query):
        """
        query: an elementTree representing the query file. Contains two children ("title", "description")
        """
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
                    scores[doc[0]] += self.get_log_tf(doc[1]) * wt * IndexFile[doc[2]]
                else:
                    scores[doc[0]] = self.get_log_tf(doc[1]) * wt * IndexFile[doc[2]]

        for doc,score in scores.iteritems():
            if doc in self.citation_weights:
                # print doc +',' + str(self.citation_weights[doc]) + ' --> '+str(score)
                scores[doc] = score * self.citation_weights[doc]
            # else:
            #     print doc +' --> '+str(score)    
        h = []
        for docId, score in scores.iteritems():
            h.append((score, docId))
        h.sort(key=lambda x: x[0], reverse=True)

        return map(lambda x: x[1], h)

    # @profile
    def preprocess_query(self, query):
        """
        Perform weight calculation for the terms of the query.
        This involves first tokenizing the query, and then for each token--
        * calculate tf
        * calculate idf
        * calculate weight as a product of the two
        * normalize the weights
        
        Return a dictionary with this information.
        """
        sw = stopwords.words('english')
        
        title = query.find('title')
        desc = query.find('description')
        if title is None:
            print "No title in the query file."
            return None
        # Note: Description _can_ be None!

        def process_words(words, weight=1.0, denom=0, dct={}):
            # case-folding, stemming the query
            terms = nltk.word_tokenize(words)
            terms = ifilter(lambda x: x not in sw, terms)
            terms = imap(lambda x: self.stemmer.stem(x.lower()), terms)

            # calculate tf
            for term in terms:
                if term not in dct:
                    dct[term] = 1
                else:
                    dct[term] += 1

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
                dct[k] = wt * weight
            denom = math.sqrt(denom)
            return (dct, denom)
        dct, denom = process_words(title.text, weight=2.0)
        # if desc is not None:
        #     dct, denom = process_words(desc.text, denom=denom, dct=dct)
            
        if denom == 0:
            return []
        
        # normalization
        for k, wt in dct.iteritems():
            dct[k] = wt/denom

        return dct

    def str_results(self, lst):
        """
        Used to print out the results in the expected format.
        """
        return "\n".join([str(i) for i in lst])
    
    def get_idf(self, term):
        """
        Returns the inverted document frequency for a term.
        """
        if term in self.dictionary:
            # freq = self.dictionary[term][2]
            plist = self.search_term(term)
            plist = groupby(plist, lambda x: x[0]) # get patent name
            l = 0
            for k, g in plist:
                l += len(list(g))
            return math.log10(self.FILE_COUNT/float(l))
        else:
            return 0

    def get_log_tf(self, freq):
        if freq == 0:
            return 0
        else:
            return 1 + math.log10(freq)

    # @profile
    def search_term(self, term):
        """
        Returns the postings list for a term.
        """
        if term in self.dictionary:
            index = self.dictionary[term][1]
            self.postings_file.seek(index)
            results = cPickle.load(self.postings_file)
            return results
        else:
            return []
def main():
    """
    Main entry point for the file.
    """
    search = Search(postings_file, dict_file)

    query_tree = FileOps.get_query_as_tree(query_file)
    fd_output = open(output_file, 'w')

    res = search.process_query(query_tree)
    fd_output.write(search.str_results(res) + '\n')
    
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


main()
# manual_mode()
