import os, sys
import xml.etree.cElementTree as ET
from itertools import imap

__author__ = 'darora'

class FileOps(object):
    @staticmethod
    def get_file_list(dir_path):
        """
        dir_path: path to dir
        returns: *just* the file names
        """
        try:
            return os.listdir(dir_path)
        except OSError:
            print "Invalid directory path encountered"
            sys.exit(-1)

    @staticmethod
    def get_full_path(filename, dir_path):
        return '/'.join([dir_path, filename])

    @staticmethod
    def get_file_contents(file_path):
        with open(file_path, 'r') as fl:
            content = fl.readlines()
            return content

    @staticmethod
    def get_file_as_tree(file_path):
        """
        Returns an etree representing the file.
        
        Note::the query files are malformed XML, with multiple top-level nodes. To parse queries, use the ``get_query_as_tree'' method instead.
        
        TODO: catch ET.ParseError and return an empty tree, with a logged error
        """
        return ET.ElementTree(file=file_path)

    @staticmethod
    def get_query_as_tree(file_path):
        """
        Wraps the contents of a query file in a phony 'data' tag, so that etree doesn't die on the multiple top-level nodes.
        """
        content = []
        with open(file_path, 'r') as fl:
            content.append(fl.readline()) # read the <xml> decl line
            content.append('<data>')
            content.extend(fl.readlines())
            content.append('</data>')
            text = imap(lambda x: x.strip('\n'), content)
            text = ' '.join(text)
            tree = ET.fromstring(text)
            return tree

    
