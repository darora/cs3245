import nltk, string, cPickle, os
from nltk.stem.porter import PorterStemmer
# from blist import *
from collections import namedtuple, defaultdict
from utils import Utils
import indexer_targets
from file_ops import FileOps
import itertools
from citation_weight import CitationWeight

Index_file = namedtuple('Index_file', 'dictionary postings priority')

class Indexer(object):

    def __init__(self, dict_filename, post_filename, corpus_dir):
        """
        """
        super(Indexer, self).__init__()
        self.dict_file = dict_filename
        self.post_file = post_filename
        self.dictionary, self.postings = {}, []
        self.corpus_dir = corpus_dir
        self.token_counter = 0
        self.file_objects = {}
        # self.citation_weights = CitationWeight() # let's initialize
        # this when we have the file listing already.
        self.stemmer = PorterStemmer()
        self.file_counter = 0
        self.init_filenames()

    def __del__(self):
        for file_name, index_file_obj in self.file_objects.iteritems():
            index_file_obj.dictionary.close()
            index_file_obj.postings.close()
        self.dict_file.close()
        self.post_file.close()

    def dump_indices_to_files(self):
        p = self.post_file
        d = self.dict_file
        for k,v in self.dictionary.iteritems():
            self.dictionary[k] = (v, p.tell(), len(self.postings[v]))
            cPickle.dump(self.postings[v], p, 2)
        p.close()

        cPickle.dump(self.dictionary, d, 2)

        with open("./processed/FILE_COUNT", 'w') as fl_count:
            fl_count.write(str(self.file_counter))

        with open("./processed/CORPUS_DIR", 'w') as fl:
            fl.write(self.corpus_dir)

        with open("./processed/citation_weights", 'wb') as fl_citations:
            cPickle.dump(self.citation_weights.index, fl_citations, 2)

    def init_filenames(self):
        """
        Creates a bunch of files under the "processed" subdirectory to store denormalized data.
        If they already exist, they are reset to being empty.

        Also initializes the universal dictionary and postings files.
        """
        os.system("if test ! -d processed; then mkdir processed; fi")
        self.file_objects = {}
        for file_name, priority in indexer_targets.IndexFile.iteritems():
            d = open('./processed/'+file_name+'_dict', 'wb')
            p = open('./processed/'+file_name+'_post', 'w+b')
            self.file_objects[file_name] = Index_file(dictionary=d, postings=p, priority=priority)

        self.dict_file, self.post_file = open(self.dict_file, 'wb'), open(self.post_file, 'w+b')



    def index_file_tree(self, file_tree, file_name):
        """
        Arguments:
        - `file_tree`: an ElementTree that represents the file
        - `file_name`: the file name -- corresponds to the patent number
        """
        patent_number = file_name.split('.')[0]
        self.citation_weights.process_file(file_tree, patent_number)
        file_dict = defaultdict(lambda: defaultdict(int))

        for node in file_tree.iter('str'):
            self.index_node(node, file_dict)
        self.merge_into_global(file_dict, patent_number)

    def index_node(self, node, file_dict):
        name = node.get('name').lower()
        name = name.translate(string.maketrans("",""), string.punctuation)

        if name in self.file_objects:
            tokens = self.process_node(node.text)
            for token in tokens:
                file_dict[token][name] += 1
       

    def merge_into_global(self, file_dict, patent_name):
        """

        :param file_dict: a nested dictionary, of the type: {'token_category (title|abstract|author)': {'token': freq}}
        :param patent_name:
        """
        for token, token_dict in file_dict.iteritems():
            for token_type, freq in token_dict.iteritems():
                if token in self.dictionary:
                    # print token + " already in dictionary"
                    self.postings[self.dictionary[token]].append((patent_name, freq, token_type))
                else:
                    curr = self.dictionary[token] = self.token_counter
                    self.postings.insert(curr, [(patent_name, freq, token_type)])
                    self.token_counter += 1

    def process_node(self, node_text):
        """
        Takes in raw node text, returns a list of tokens ready to be indexed
        """
        sentences = nltk.sent_tokenize(node_text.lower())
        sent_words = itertools.imap(nltk.word_tokenize, sentences)
        flat_words = [word for sentence in sent_words for word in sentence]
        if not hasattr(self, 'sw'):
            self.sw = Utils.stopwords()
        filtered_words = itertools.ifilter(lambda x: x not in self.sw, flat_words)
        stemmed_words = itertools.imap(self.stemmer.stem, filtered_words)
        return stemmed_words

    def create_index(self):
        """
        Main point of entry for the class.
        """
        file_list = FileOps.get_file_list(self.corpus_dir)
        self.citation_weights = CitationWeight(dict(itertools.izip(file_list, itertools.repeat(0))))
        
        for fl in file_list:
            self.file_counter += 1
            abs_fl = FileOps.get_full_path(fl, self.corpus_dir)
            tree = FileOps.get_file_as_tree(abs_fl)
            self.index_file_tree(tree, fl)
