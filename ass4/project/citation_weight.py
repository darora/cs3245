from collections import namedtuple, defaultdict
from file_ops import FileOps
from itertools import imap
import string, logging
from blist import *

class CitationGraph(object):
    """
    Based off ideas from "Enhancing Patent Retrieval by Citation Analysis" by Atsushi Fujii (SIGIR 2007)
    """

    def __init__(self, dir_path):
        """

        :param dir_path:
        """
        super(CitationGraph, self).__init__()
        self.citation_weights = defaultdict(lambda: 1.0)
        self.dir_path = dir_path

    def build_graph(self):
        files = FileOps.get_file_list(self.dir_path)
        for fl in files:
            self.process_file(fl)

    def process_file(self, file_name):
        """

        :param file_name:
        """
        et = FileOps.get_file_as_tree('/'.join([self.dir_path, file_name]))
        cites = et.find('Cites')
        cites_count = et.find('Cites Count')

        if cites:
            cites = imap(string.strip, cites.split('|'))

            # TODO::debug only, remove before submission for performance
            if len(cites) != int(cites_count):
                logging.debug("Number of citations, and citation count differs! :(")

            if len(cites) > 0:
                weight = 1.0/int(cites_count)
                for citation in cites:
                    self.citation_weights[citation] += weight




