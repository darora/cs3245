import os, sys
import xml.etree.cElementTree as ET

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
        return ET.ElementTree(file=file_path)

    
