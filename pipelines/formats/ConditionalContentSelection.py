from math import log
from pprint import pprint
from json import dumps, loads
from collections import Counter

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
	if num_occ.__class__ != unicode:
	    num_occ = unicode(num_occ)
        cnt = self.counts.get(word, {}).get(num_occ, 0.0)
#	print self.counts.get(word, {})
        total = self.totals.get(word, 0.0)
        if not nosmooth:
            cnt = cnt + self.epsilon
            total = total + self.epsilon*self.vocab_size
#	print "Computing probability for word %s with occurrences %s: cnt=%f, total=%f, prob=%s" % (word, num_occ, cnt, total, str(float(cnt)/float(total)))
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
	p = self.prob(word, num_occ)
	if p > 0.0:
            return -log(p)
	else:
	    return float("inf")

    def score_wordlist(self, wordlist, detailed = False):
	#Make BoW/Counter representation of word list
	C = Counter(wordlist)
	scores = []
	for w,cnt in C.iteritems():
	    scores.append(self.score(w, cnt))
	if detailed:
	    return scores
	else:
	    return sum(scores)

    def score_wordlist_normalize(self, wordlist, detailed = False):
	return self.score_wordlist(self, map(lambda x:x.lower(), wordlist), detailed=detailed)

    def prob_wordlist(self, wordlist, detailed = False):
	score = self.score_wordlist(wordlist, detailed=detailed)
	if score < float("inf"):
	    return exp(-score)
	else:
	    return 0.0

    def prob_wordlist_normalize(self, wordlist, detailed = False):
	return self.prob_wordlist(self, map(lambda x:x.lower(), wordlist), detailed=detailed)

    def encode(self):
        return dumps((self.counts,self.totals))

    @staticmethod
    def decode(string):
        counts, totals = loads(string)
        return ConditionalContentSelector(counts, totals)
