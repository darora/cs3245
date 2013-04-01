from contextlib import contextmanager

__author__ = 'darora'

@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


Config = {
    'DEFAULT_CITATION_VOTE': 0.4
}
