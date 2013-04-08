# import line_profiler
import math
import nltk
import cPickle, getopt, sys
from nltk.stem.porter import PorterStemmer
from itertools import groupby, ifilter, imap, chain
from indexer_targets import IndexFile
from file_ops import FileOps
from utils import Utils, ignored, Config

from socket import gethostname  # used to select output mechanism

class Search(object):
    """
    Initialize with postings file & dictionary filenames.
    Also initialize the number of files that were indexed, alongwith a dictionary of weights for each file based on citation analysis (ref:citation_weight.py)
    Use cPickle for greater speed.
    """
    def __init__(self, postings_file, dictionary_file):
        with open(dictionary_file, 'rb') as fl:
            self.dictionary = cPickle.load(fl)
        
        self.postings_file = open(postings_file, 'rb')
        self.stemmer = PorterStemmer()
        
        with open('./processed/FILE_COUNT', 'r') as fl:
            self.FILE_COUNT = int(fl.readline().strip())

        with open('./processed/citation_weights', 'rb') as fl:
            self.citation_weights = cPickle.load(fl)

        with open('./processed/CORPUS_DIR', 'r') as fl:
            self.corpus_dir = fl.readline().strip()


    def process_query_core(self, query, threshold):
        """
        query: a dictionary of the form {term: weight}
        """
        scores = {}
        
        for term, wt in query.iteritems():
            if wt == 0:
                continue
            postings_lst = self.search_term(term)
            if verbose_mode:
                print term.ljust(10) + " has " + str(len(postings_lst)) + " docs"
            for doc in postings_lst:
                if doc[0] in scores:
                    scores[doc[0]] += self.get_log_tf(doc[1]) * wt * IndexFile[doc[2]]
                else:
                    scores[doc[0]] = self.get_log_tf(doc[1]) * wt * IndexFile[doc[2]]

        # citation weightings muxed in
        for doc,score in scores.iteritems():
            if doc in self.citation_weights:
                scores[doc] = score * self.citation_weights[doc]

        scores = self.filter_out_lowers(self.calculate_percentile_index(scores, threshold), scores)
        
        return scores
            
    def process_query(self, query):
        """
        query: an elementTree representing the query file. Contains two children ("title", "description")
        Each matching term, in addition to standard tf-idf weighting, is also weighted by which section of the patent it appeared in. For instance, a title occurance is valued more than one in the abstract or the description.
        The exact ratios are in indexer_targets.py
        Lastly, the documents are also, if present, weighted by their citation analysis.
        """
        query = self.preprocess_query(query)
                
        scores = self.process_query_core(query, 0.80)

        queries = []
        for docId, score in scores.iteritems():
            et = FileOps.get_file_as_tree(self.corpus_dir + docId + '.xml')
            title = et.find('./str[@name="Title"]')
            abstract = et.find('./str[@name="Abstract"]')
            queries.append(self.preprocess_core(title, abstract))
            
        all_terms = chain(*imap(lambda x: x.iteritems(), queries))

        query = {}
        for k,v in all_terms:
            if k in query:
                query[k] += v
            else:
                query[k] = v
            
        scores = self.process_query_core(query, doc_percentile)
        
        h = []
        for docId, score in scores.iteritems():
            h.append((score, docId))
        h.sort(key=lambda x: x[0], reverse=True)
        
        # with open('./queries/q2-qrels+ve.txt') as results:
        #     results = results.readlines()
        #     results = set(map(string.strip, results))
        #     for v,k in h:
        #         if not verbose_mode:
        #             continue
        #         if k in results:
        #             print k + ' ---> ' + str(v)
        #         else:
        #             print k + ' !!!> ' + str(v)

        return map(lambda x: x[1], h)

    def preprocess_core(self, title=None, description=None):
        sw = Utils.stopwords()

        if title is None:
            print "Can't process a query without a title"
            sys.exit(2)

        def process_words(words, weight=1.0, denom=0, dct={}):
            terms = nltk.word_tokenize(words)
            terms = imap(lambda x: self.stemmer.stem(x.lower()), terms)
            terms = ifilter(lambda x: x not in sw, terms)

            counts = {}
            # calculate tf
            for term in terms:
                if term not in counts:
                    counts[term] = 1
                else:
                    counts[term] += 1

            # calculate wt
            for k, v in counts.iteritems():
                tf = self.get_log_tf(v)
                idf = self.get_idf(k)
                wt = tf * idf
                denom += wt**2
                if k in dct:
                    dct[k] += wt * weight
                else:
                    dct[k] = wt * weight

            denom = math.sqrt(denom)
            return (dct, denom)

        dct, denom = process_words(title.text, weight=2.0)
        
        if description is not None:
            dct, denom = process_words(description.text, denom=denom, dct=dct, weight=1.8)
            
        if denom == 0:
            return []
        
        # normalization
        for k, wt in dct.iteritems():
            dct[k] = wt/denom

        # discard the lowest ranked terms.
        # can be configured through CLI options
        dct = self.filter_out_lowers(self.calculate_percentile_index(dct, term_percentile), dct)
        
        return dct

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
        title = query.find('title')
        desc = query.find('description')
        return self.preprocess_core(title, desc)

    def calculate_percentile_index(self, dct, percentile):
        """
        Returns the value of the given percentile.
        dct: of the form {label: numericScore}
        percentile: numeric in range [0,1]
        """
        scores = []
        for k,v in dct.iteritems():
            scores.append(v)
        scores.sort()
        ith = math.floor(percentile * len(scores) + 0.5)
        if verbose_mode:
            print str(ith) + " is the first quartile, which comes to: " + str(scores[int(ith)])
        return scores[int(ith)]

    def filter_out_lowers(self, threshold, dct):
        """
        Returns the dct with all elements with a score below the threshold deleted.
        dct must be of the form {label: numericScore}
        """
        to_del = []
        for k,v in dct.iteritems():
            if v < threshold:
                to_del.append(k)
        for k in to_del:
            del dct[k]
        return dct


    def str_results(self, lst):
        """
        Used to print out the results in the expected format.
        """
        if gethostname().find('div') != -1:
            return "\n".join([str(i) for i in lst])
        else:
            return ' '.join([str(i) for i in lst])
    
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

    with ignored(IOError):
        query_tree = FileOps.get_query_as_tree(query_file)
        with open(output_file, 'w') as fd_output:
            res = search.process_query(query_tree)
            fd_output.write(search.str_results(res) + '\n')
    
def usage():
    print "python2 search.py -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

query_file = None
dict_file = None
postings_file = None
output_file = None

# new options
verbose_mode = False
term_percentile = None
doc_percentile = None


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'q:d:p:o:', ["verbose", "term-percentile=", "doc-percentile="])
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
        elif o == '--verbose':
            verbose_mode = True
        elif o == '--term-percentile':
            term_percentile = float(a)
        elif o == '--doc-percentile':
            doc_percentile = float(a)        
        else:
            assert False, "unhandled option"

    if query_file == None or dict_file == None or postings_file == None or output_file == None:
        usage()
        sys.exit(0)
    if term_percentile is None:
        term_percentile = Config['TERM_PERCENTILE']
    if doc_percentile is None:
        doc_percentile = Config['DOCUMENT_PERCENTILE']

main()
