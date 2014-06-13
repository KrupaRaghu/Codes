#Defines a vocabulary class which allows to get either the i-th word or the index of a word via []-access.
from json import loads,dumps
from meta import *
from BoW import BoW
from ..experiment_config import UNKNOWN_WORD

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
	    try:
            	return self.index(item)
	    except ValueError as v:
		return self.index(self.unknown)
		# return list.__getitem__(self,self.index(self.unknown))

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

    def index_words(self, words, unknown = None):
        idxes = []
	if not unknown is None:
       	    self.unknown = unknown
        for word in words:
	   # print "indexing",word
            try:
                idxes.append(self[word])
	#	print "found index", self[word]
            except ValueError as e:
	#	print "using unknown word",UNKNOWN_WORD
	#	print "found index", self[UNKNOWN_WORD]
                idxes.append(self[UNKNOWN_WORD])
        return idxes

    def words2indices(self, words, unknown = UNKNOWN_WORD):
	return self.index_words(words, unknown)
    def indices2words(self, indices):
	words = []
	for index in indices:
	    words.append(self[index])
	return words
