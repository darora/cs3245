import nltk
from nltk.stem.porter import PorterStemmer
import xml.etree.cElementTree as ET
from blist import *
from utils import *

class Indexer(object):

    def __init__(self, dict_file, post_file, corpus_dir):
        """
        dict_file, post_file: file _object_, not a name!
        """
        super(Indexer, self).__init__()
        self.dict_file = dict_file
        self.post_file = post_file
        self.corpus_dir = corpus_dir
        self.file_counter = 0

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

