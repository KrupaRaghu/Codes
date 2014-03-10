#Bag-of-words representation as a Counter subclass
from collections import Counter
from json import dumps, loads
from meta import *

class BoW(Counter):
    __metaclass__ = FormatMeta
    """A class representing bags of words."""
    def __init__(self, *args, **kwargs):
        return Counter.__init__(self, *args, **kwargs) 

    @conversion(str)
    def from_str(string):
        if string.__class__ == str:
            string = string.decode("utf-8")
        return BoW(string.split())

    @staticmethod
    def decode(buf):
        return Counter(loads(buf))
    
    def encode(self):
        return dumps(self)

    def below_threshold(self, val):
        D = {x:o for (x,o) in self.iteritems() if o < val}
        if not D:
            D = {}
        return BoW(D)

    def __rshift__(self, val):
        """Returns the BoW with all values increased by val."""
        D = {x:o+val for (x,o) in self.iteritems()}
        if not D:
            D = {}
        return BoW(D)

    def __lshift__(self, val):
        """Returns the BoW with all values diminished by val."""
        D = {x:o-val for (x,o) in self.iteritems() if o > val}
        if not D:
            D = {}
        return BoW(D)

    def filter(self, f):
        """Returns a BoW that contains only those key-value tuples for which f(k,v) returned true."""
        D = {x:o for (x,o) in self.iteritems() if f((x,o))}
        if not D:
            D = {}
        return BoW(D)

    def filter_by_vocabulary(self, voc):
        return self.filter(lambda (x, o): x in voc)

    def __add__(self, other):
        """Returns the summation of both BoWs."""
        x = BoW(self)
        return x.update(other) 
