from math import log, exp
from json import dumps, loads

class PhraseAttachmentModel(object):
    def __init__(self, counts, left_counts = None, right_counts = None, epsilon = 0.0, vocab_size = 0.0):
        """vocab_size must be the UNIGRAM vocabulary size, i.e. the number of different words in existence."""
        if counts:
            if counts.keys()[0].__class__ == tuple:
                self.counts = self._convert_tuple_counts(counts)
            else:
                self.counts = counts
        else:
            self.counts = {}
        if left_counts is None:
            self.left_counts = self._make_left_counts(self.counts)
        else:
            self.left_counts = left_counts
        if right_counts is None:
            self.right_counts = self._make_right_counts(self.counts)
        else:
            self.right_counts = right_counts
        self.epsilon = epsilon
        self.vocab_size = vocab_size

    def encode(self):
        return dumps(self.counts)

    @staticmethod
    def decode(string):
        return PhraseAttachmentModel(loads(string))

    def score(self, left_phrase, right_phrase):
        return sum(self.score_detailed(left_phrase, right_phrase))

    def score_detailed(self, left_phrase, right_phrase):
        for wl in left_phrase:
            for wr in right_phrase:
                yield self.score_words(wl,wr)

    def prob(self, left_phrase, right_phrase):
        return exp(-self.score(left_phrase, right_phrase))

    def prob_detailed(self, left_phrase, right_phrase):
        for wl in left_phrase:
            for wr in right_phrase:
                yield self.prob_words(wl,wr)

    def prob_words(self, left_word, right_word):
        return 0.5*(self.left_prob(left_word, right_word) + self.right_prob(left_word, right_word))

    def score_words(self, left_word, right_word):
        return -log(self.prob_words(left_word, right_word))

    def left_prob(self, left_word, right_word):
        return float(self.count(left_word, right_word)+self.epsilon)/(self.left_count(left_word)+self.epsilon*self.vocab_size*self.vocab_size)
    
    def right_prob(self, left_word, right_word):
        return float(self.count(left_word, right_word)+self.epsilon)/(self.right_count(right_word)+self.epsilon*self.vocab_size*self.vocab_size)

    def count(self, left_word, right_word):
        return self.counts[self._join_words(left_word, right_word)]

    def left_count(self, word):
        return self.left_counts[word]

    def right_count(self, word):
        return self.right_counts[word]

    def _join_words(self, wl, wr):
        return wl+"||"+wr

    def _split_words(self, string):
        return string.split("||")

    def _make_left_counts(self, counts):
        leftcounts = {}
        for wstring, cnt in counts.iteritems():
            wl, wr = self._split_words(wstring)
            leftcounts[wl] = leftcounts.get(wl, 0) + cnt
        return leftcounts

    def _make_right_counts(self, counts):
        rightcounts = {}
        for wstring, cnt in counts.iteritems():
            wl, wr = self._split_words(wstring)
            rightcounts[wl] = rightcounts.get(wl, 0) + cnt
        return rightcounts

    def _convert_tuple_counts(self, tcounts):
        out = {}
        for (wl,wr), cnt in tcounts.iteritems():
            out[self._join_words(wl,wr)] = cnt
        return out
