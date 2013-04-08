from collections import namedtuple, defaultdict
from file_ops import FileOps
from itertools import imap
import string, logging
# from blist import *
from utils import Config

class CitationWeight(object):
    """
    Based off ideas from "Enhancing Patent Retrieval by Citation Analysis" by Atsushi Fujii (SIGIR 2007)
    """

    def __init__(self, file_dict):
        """
        Doesn't do much. Stores the file_dict with the names of all the files internally, though.
        It'll be used to figure out which patents are within our corpus.
        
        :param dir_path:
        """
        super(CitationWeight, self).__init__()
        self.index = {}
        self.file_dict = file_dict

    def process_file(self, file_tree, patent_number):
        """

        Award vote to patents cited by the current file.
        Award vote to current patent for the patents that cite it but aren't within our corpus.
        
        :param file_tree: an elementTree representing the file being processed
        :param patent_number: the patent number for the file being processed
        """
        cites = file_tree.find('./str[@name="Cites"]')
        cites_count = file_tree.find('./str[@name="Cites Count"]')
        cited_by = file_tree.find('./str[@name="Cited By"]')

        # if the cited_by doc is not present in our corpus, this
        # patent will never recieve it's vote. Therefore, use a
        # default vote score instead.
        cited_by_score = 0
        if cited_by is not None:
            cited_by = imap(lambda x: string.strip(x)+'.xml', cited_by.text.split('|'))
            for patent in cited_by:
                if patent not in self.file_dict:
                    cited_by_score += Config['DEFAULT_CITATION_VOTE']

        # We prefer to use the count given within the file. But if it
        # isn't present, we'll fallback to using the list's length
        # instead. Ideally, they shouldn't differ anyway.
        c_count = None
        if cites_count is not None:
            c_count = int(cites_count.text)
            
        if cites is not None:
            cites = map(string.strip, cites.text.split('|'))
            if c_count is None:
                c_count = len(cites)

            # add in the default votes that we calc'ed earlier
            if patent_number in self.index:
                self.index[patent_number] += cited_by_score
            else:
                self.index[patent_number] = 1 + cited_by_score

            # give this patent's vote to all the ones it cites.
            if len(cites) > 0:
                weight = 1.0/c_count
                for citation in cites:
                    if citation in self.index:
                        self.index[citation] += weight
                    else:
                        self.index[citation] = 1 + weight
            
