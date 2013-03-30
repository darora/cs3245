import nltk, string
from nltk.stem.porter import PorterStemmer
import xml.etree.cElementTree as ET
from blist import *
from collections import namedtuple
from utils import *
import indexer_targets

Index_file = namedtuple('Index_file', 'dictionary postings priority')

class Indexer(object):

    def __init__(self, dict_filename, post_filename, corpus_dir):
        """
        """
        super(Indexer, self).__init__()
        self.dict_file = dict_filename
        self.post_file = post_filename
        self.corpus_dir = corpus_dir
        self.file_counter = 0
        self.file_objects = {}

    def __del__(self):
        for fname, fobj in self.file_objects.iteritems():
            fobj.close()
        self.dict_file.close()
        self.post_file.close()
        super(Indexer, self).__del__() # TODO:check if this is necessary.
        
    def init_filenames(self):
        """
        Creates a bunch of files under the "processed" subdirectory to store denormalized data.
        If they already exist, they are reset to being empty.

        Also initializes the universal dictionary and postings files.
        """
        self.file_objects = {}
        for file_name, priority in indexer_targets.IndexFile.iteritems():
            d = open('processed/'+file_name+'_dict', 'wb')
            p = open('processed/'+file_name+'_post', 'w+b')
            self.file_objects[file_name] = Index_file(dictionary=d, postings=p, priority=priority)

        self.dict_file = open(self.dict_file, 'wb')
        self.post_file = open(self.post_file, 'w+b')

    def get_file_list(self, dir_path):
        try:
            return os.listdir(dir_path)
        except OSError:
            print "Invalid directory path encountered"
            sys.exit(-1)

    def get_file_as_tree(self, file_path):
        return ET.ElementTree(file=file_path)

    def index_file_tree(self, file_tree, file_name):
        """
        Arguments:
        - `file_tree`: an ElementTree that represents the file
        - `file_name`: the file name -- corresponds to the patent number
        """
        for node in file_tree:
            self.index(node, file_name)

    def index_node(self, node, file_name):
        name = node.get('name').lower()
        name = name.translate(string.maketrans("",""), string.punctuation)

        if name in self.file_objects:
            # to index
            value = node.text
        
        raise Exception("not implemented")
            
    def postprocess_file(self, contents):
        """
        Remove the newlines that each line read in contains, and join them using a single space instead.
        :param contents: the contents of a single file
        """
        contents = contents[0]
        return " ".join(map(lambda x: x.strip(), contents))

    def create_index(self):
        """
        Main point of entry for the class.
        """
        pass
