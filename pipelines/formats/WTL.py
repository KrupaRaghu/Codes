#Word-tag-lemma lists (TreeTagger output)
from meta import *
import json

class WTL(list):
    __metaclass__ = FormatMeta
    """A class representing word-text-lemma lists."""
    def __init__(self, *args, **kwargs):
        return list.__init__(self, *args, **kwargs) 

    @staticmethod
    def decode(buf):
        return (json.loads(buf))
    
    def encode(self):
        return json.dumps(self)

    @staticmethod
    def from_text(string):
        return WTL(map(lambda x: x.split(), string.split("\n")))

    @conversion(str)
    def from_str(string):
        return WTL.from_text(string)
