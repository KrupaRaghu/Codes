#Defines a vocabulary class which allows to get either the i-th word or the index of a word via []-access.
from json import loads,dumps
from meta import *
from BoW import BoW

class Vocabulary(list):
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        for i,x in enumerate(self):
            if x.__class__ == str:
                self[i] = x.decode("utf-8")

    def __getitem__(self, item):
        try:
            return list.__getitem__(self, item)
        except TypeError as e:
            return self.index(item)

    @conversion(BoW)
    def from_BoW(bow):
        return Vocabulary.from_bow(bow)

    @staticmethod
    def from_bow(bow):
        return Vocabulary([a for (a,o) in bow.iteritems() if o > 0])

    @staticmethod
    def decode(text):
        text = text.split("\n", 1)[1]
        return Vocabulary(text.split("\n"))

    def encode(self):
        return (u'# Vocabulary %d\n' % (len(self) - 1) + u'\n'.join(self)).encode("utf-8")
    
    def __repr__(self):
        return self.encode()

    def index_words(self, words):
        idxes = []
        for word in words:
            idxes.append(self[word])
        return idxes

