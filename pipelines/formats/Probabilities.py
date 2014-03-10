from json import dumps, loads
from math import log, exp
from meta import *
#A class for probabilities computed from counts via MLE.
#Can be used to model conditional probabilities, too, if they have been fully computed already and their components will not be needed later.

def CountProbability(object):
    def __init__(self, counts, totals):
        self.counts = counts
        self.totals = totals
    def encode(self):
        return dumps(self.counts)+"\n\n"+dumps(self.totals)
    @staticmethod
    def decode(text):
        c = loads(text.split("\n\n")[0])
        T = loads(text.split("\n\n")[1])
        return CountProbability(c, T)
    def prob_word(self, word):
        cnt_w = self.counts.get(word,0)
        cnt_T = self.totals.get(word,0)
        if cnt_T > 0:
            return float(cnt_w)/cnt_T
        else:
            return 0.0
    def score_word(self, word):
        return -log(self.prob_word(word))
    def score_phrase(self, phrase):
        score = 0
        for word in phrase:
            score = score + self.score_word(word)
        return score
    def prob_phrase(self, phrase):
        return exp(-self.score_phrase(phrase))

def CountProbabilityAddeps(CountProbability):
    def __init__(self, counts, totals, epsilon, vocabsize):
        CountProbability.__init__(self, counts, totals)
        self.epsilon = epsilon
        self.vocabsize = vocabsize
    def encode(self):
        return str(self.epsilon)+" "+str(self.vocabsize)+"\n\n"+CountProbability.encode(self)
    @staticmethod
    def decode(text):
        t0 = text.split("\n\n")
        eps = float(t0[0].split()[0])
        vsize = int(t0[0].split()[1])
        c = loads(t0[1])
        T = loads(t0[2])
        return CountProbability(c, T, eps, vsize)
    def prob_word(self, word):
        cnt_w = self.counts.get(word,0) + self.epsilon
        cnt_T = self.totals.get(word,0) + self.epsilon*self.vocabsize
        return float(cnt_w)/cnt_T
