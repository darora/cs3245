from collections import namedtuple, defaultdict
from file_ops import FileOps
from itertools import imap
import string, logging
from blist import *

class CitationWeight(object):
    """
    Based off ideas from "Enhancing Patent Retrieval by Citation Analysis" by Atsushi Fujii (SIGIR 2007)
    """

    def __init__(self):
        """

        :param dir_path:
        """
        super(CitationWeight, self).__init__()
        self.index = {}

    def process_file(self, file_tree):
        """

        :param file_tree:
        """
        cites = file_tree.find('Cites')
        cites_count = file_tree.find('Cites Count')

        if cites:
            cites = imap(string.strip, cites.split('|'))

            # TODO::debug only, remove before submission for performance
            if len(cites) != int(cites_count):
                logging.debug("Number of citations, and citation count differs! :(")

            if len(cites) > 0:
                weight = 1.0/int(cites_count)
                for citation in cites:
                    if citation in self.index:
                        self.index[citation] += weight
                    else:
                        self.index[citation] = 1 + weight
            
