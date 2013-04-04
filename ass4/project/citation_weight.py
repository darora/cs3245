from collections import namedtuple, defaultdict
from file_ops import FileOps
from itertools import imap
import string, logging
from blist import *
from utils import Config

class CitationWeight(object):
    """
    Based off ideas from "Enhancing Patent Retrieval by Citation Analysis" by Atsushi Fujii (SIGIR 2007)
    """

    def __init__(self, file_dict):
        """

        :param dir_path:
        """
        super(CitationWeight, self).__init__()
        self.index = {}
        self.file_dict = file_dict

    def process_file(self, file_tree, patent_number):
        """

        :param file_tree:
        """
        cites = file_tree.find('./str[@name="Cites"]')
        cites_count = file_tree.find('./str[@name="Cites Count"]')
        cited_by = file_tree.find('./str[@name="Cites By"]')
        
        cited_by_score = 0
        if cited_by is not None:
            cited_by = imap(lambda x: string.strip(x)+'.xml', cited_by.text.split('|'))
            for patent in cited_by:
                if patent not in self.file_dict:
                    # let's be kind and award 0.4 per patent.
                    cited_by_score += Config['DEFAULT_CITATION_VOTE']

        c_count = None
        if cites_count is not None:
            c_count = int(cites_count.text)
            
        if cites is not None:
            cites = map(string.strip, cites.text.split('|'))
            if c_count is None:
                c_count = len(cites)
            # TODO::debug only, remove before submission for performance
            elif len(cites) != c_count:
                print "Number of citations, and citation count differs! :("

            if patent_number in self.index:
                self.index[patent_number] += cited_by_score
            else:
                self.index[patent_number] = 1 + cited_by_score
                
            if len(cites) > 0:
                weight = 1.0/c_count
                for citation in cites:
                    if citation in self.index:
                        self.index[citation] += weight
                    else:
                        self.index[citation] = 1 + weight
            
