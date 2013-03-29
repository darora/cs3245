import nltk
from nltk.stem.porter import PorterStemmer
import xml.etree.cElementTree as ET
from blist import *
from utils import *

Index_file = namedtuple('Index_file', 'dictionary postings')

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
        super(Indexer, self).__del__()
        
    def init_filenames(self):
        """
        Creates a bunch of files under the "processed" subdirectory to store denormalized data.
        If they already exist, they are reset to being empty.

        Also initializes the universal dictionary and postings files.
        """
        file_list = ['titles', 'abstract', 'application_data', 'publication_date', 'ipc_section', 'ipc_class', 'ipc_subclass', 'ipc_group']
        file_list.extend(['cited_by', 'cites', 'priority_country', 'priority_date', 'assignees', 'inventors'])
        proc_file_list = map(lambda x: 'processed/'+x, file_list)
        file_objects = []
        for fl in proc_file_list:
            d, p = open(fl+'_dict', 'wb'), open(fl+'_post', 'w+b')
            file_objects.append(Index_file(dictionary=d, postings=p))
        self.file_objects = dict(zip(file_list, file_objects))

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
        pass
            
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
