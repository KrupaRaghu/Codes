from math import log
from pprint import pprint
from json import dumps, loads

class ConditionalContentSelector(object):
    def __init__(self, counts, totals, epsilon = 0.0, vocab_size = 0):
        self.counts = counts
        self.totals = totals
        self.epsilon = epsilon
        self.vocab_size = vocab_size

    def set_epsilon(self, eps):
        self.epsilon = eps

    def set_vocab_size(self, vocsize):
        self.vocab_size = vocsize

    def prob(self, word, num_occ = 1, nosmooth = False):
        cnt = self.counts.get(word, {}).get(num_occ, 0.0)
        total = self.totals.get(word, 0.0)
        if not nosmooth:
            cnt = cnt + self.epsilon
            total = total + self.epsilon*self.vocab_size
        if cnt == 0.0:
            return 0.0
        elif total == 0.0:
            raise ValueError(cnt, total)
        return float(cnt)/float(total)

    def prob_phrase(self, phrase):
        """A convenience method. Returns the overall probability of a phrase."""
        return exp(-self.score_phrase(phrase))
    
    def prob_phrase_detailed(self, phrase):
        for word in phrase:
            yield self.prob(word)

    def score_phrase(self, phrase):
        return sum(self.score_phrase_detailed(phrase))

    def score_phrase_detailed(self, phrase):
        for word in phrase:
            yield self.score(word)

    def score(self, word, num_occ = 1):
        return -log(self.prob(word, num_occ))

    def encode(self):
        return dumps((self.counts,self.totals))

    @staticmethod
    def decode(string):
        counts, totals = loads(string)
        return ConditionalContentSelector(counts, totals)
