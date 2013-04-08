from contextlib import contextmanager
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
__author__ = 'darora'

@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass
        
class Utils:
    @staticmethod
    def stopwords():
        stemmer = PorterStemmer()
        sw = stopwords.words('english')
        sw.extend(string.punctuation)
        sw.extend(["a", "has", "such", "accordance", "have", "suitable", "according", "having", "than", "all", "herein", "that", "also", "however", "the", "an", "if", "their", "and", "in", "then", "another", "into", "there", "are", "invention", "thereby", "as", "is", "therefore", "at", "it", "thereof", "be", "its", "thereto", "because", "means", "these", "been", "not", "they", "being", "now", "this", "by", "of", "those", "claim", "on", "thus", "comprises", "onto", "to", "corresponding", "or", "use", "could", "other", "various", "described", "particularly", "was", "desired", "preferably", "were", "do", "preferred", "what", "does", "present", "when", "each", "provide", "where", "embodiment", "provided", "whereby", "fig", "provides", "wherein", "figs", "relatively", "which", "for", "respectively", "while", "from", "said", "who", "further", "should", "will", "generally", "since", "with", "had", "some", "would"])
        sw = map(stemmer.stem, sw)
        sw = set(sw)
        return sw
    
Config = {
    'DEFAULT_CITATION_VOTE': 0.25,
    'DOCUMENT_PERCENTILE': 0.2,
    'TERM_PERCENTILE': 0.2,
    'QUERY_EXPANSION_PERCENTILE' : 0.7
}
