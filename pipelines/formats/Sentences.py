#A class to abstract sentences. Actually, simply a list of lists of lists of words (list of sentences -> lists of phrases -> lists of words).
from json import dumps, loads
from meta import *
from ..experiment_config import *

class Sentences(list):
    __metaclass__ = FormatMeta
    def __init__(self, iterable = None):
        list.__init__(self, iterable)
        for i,x in enumerate(self):
            if x.__class__ == str:
                self[i] = x.encode("utf-8")

    @conversion(str)
    def from_str(string):
        return Sentences.from_text(string)

    @staticmethod
    def from_text(string):
        return Sentences(map(lambda x: x.split(), string.split(u"\n")))

    @staticmethod
    def decode(text):
        return Sentences(loads(text))

    def encode(self):
        return dumps(self)

    def get_sentence(self, i, start_token = SENTENCE_START, end_token = SENTENCE_END, phrase_delimiter = " "):
        """Returns the i-th sentence as string."""
        words = map(lambda y:u" ".join(y),self[i])
        if start_token:
            words.insert(0, start_token)
        if end_token:
            words.append(end_token)
        return phrase_delimiter.join(words)
    
    def get_sentences(self, start_token=SENTENCE_START, end_token=SENTENCE_END, phrase_delimiter = u" "):
        """Returns an iterator over all sentences."""
        for i in xrange(len(self)):
            yield self.get_sentence(i, start_token, end_token, phrase_delimiter)

    def get_text(self, start_token = SENTENCE_START, end_token = SENTENCE_END, one_per_line = True, phrase_delimiter = u" "):
        """Returns all sentences represented as text following a specific format."""
        sent_delim = u"\n"
        if not one_per_line:
            sent_delim = u" "
        return sent_delim.join(self.get_sentences(start_token, end_token, phrase_delimiter))

    def get_sentence_length(self, i, use_tokens = True):
        """Returns the length of the i-th sentence."""
        if use_tokens:
            return sum(map(len, self[i])) + 2
        else:
            return sum(map(len, self[i]))

    def get_sentence_lengths(self, use_tokens = True):
        """Returns all sentence lengths iteratively."""
        for i in xrange(len(self)):
            yield self.get_sentence_length(i, use_tokens)
