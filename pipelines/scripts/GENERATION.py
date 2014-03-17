from ..experiment_config import *
from ..formats.Sentences import *
from bisect import insort_left
from pprint import pprint
#Functions for generating captions.

BEAM_SIZE = 500

class CaptionGenerator(object):
    def __init__(self, lang_model, m_lang_model, len_model, csel_model, pa_model = None, beam_size = BEAM_SIZE):
        self.lang_model = lang_model
	self.m_lm = m_lang_model
        self.len_model = len_model
        self.csel_model = csel_model
        self.pa_model = pa_model
	self.captions = []
	self.current_candidates = [(float("inf"), [[SENTENCE_START]])]
	self.next_candidates = []
	self.beam_size = beam_size
	print "Setup complete."
    
    def score_sentence(self, sentence, verbose = False):
	"""Completely scores a sentence."""
        words = []
	for phrase in sentence:
	    words.extend(phrase)
	lm_prob, lm_score = self.lang_model.AssessText(words, self.m_lm)
	cond_score = self.csel_model(words)
        len_score = self.len_model(len(words))
        phrase_score = 0.0
        if not self.pa_model is None:
            for i in xrange(len(sentence)-1):
                phrase_score = self.pa_model(sentence[i], sentence[i+1])
        if verbose:
            return lm_score, cond_score, len_score, phrase_score
        else:
            return lm_score + cond_score + len_score + phrase_score

    def score_sentence_delta(self, old_sentence, new_addition, verbose = False):
	"""Computes the change in score after adding a new element to the sentence."""
        words_old = []
	for phrase in old_sentence:
	    words_old.extend(phrase)
	lm_sent = old_sentence[len(words_old)-self.m_lm+1:] + new_addition
        lm_prob, lm_score_new = self.lang_model.AssessText(lm_sent, self.m_lm)
	len_score_old = self.len_model(len(words_old))
        len_score_new = self.len_model(len(words_old) + len(new_addition))
	d_len_score = len_score_new - len_score_old
        phrase_score_new = 0.0
	if old_sentence and not self.pa_model is None:
	    phrase_score_new = self.pa_model(old_sentence[-1], new_addition)
        #Conditional scores cannot be computed incrementally - recompute fully instead.
	#To get CHANGE in score, also need the old score.
	cond_score_old = self.csel_model(words_old)
	cond_score_new = self.csel_model(words_old+new_addition)
        if verbose:
            return lm_score_new, cond_score_new - cond_score_old, d_len_score, phrase_score_new
        else:
            return lm_score_new + cond_score_new - cond_score_old + d_len_score + phrase_score_new

    def expand_sentence(self, (score, sentence), expansionlist):
	"""Expands the given sentence using all expansions from the given list."""
	for exp in expansionlist:
	    new_sent = sentence[:]
	    new_sent.append(exp)
	    #if score < float("inf"):
	    #    new_score = score+self.score_sentence_delta(sentence, exp)
	    #else:
	    new_score=self.score_sentence(new_sent)
	    self.insert((new_score, new_sent), self.next_candidates)
	return self.insert((score, sentence), self.captions)

    def expand_current(self, expansionlist):
	found_one = False
	for (score, sentence) in self.current_candidates:
	    if self.expand_sentence((score, sentence), expansionlist):
		found_one = True
	return found_one

    def step(self, expansionlist):
	#print "current candidates:"
	#print self.current_candidates
	found_one = self.expand_current(expansionlist)
	print "next candidates:"
	pprint(zip(map(lambda (s, x): self.score_sentence(x, verbose=True), self.next_candidates), self.next_candidates))
	self.current_candidates = self.next_candidates
	self.next_candidates = []
	return found_one
    
    #NOT TESTED, PROBABLY DOES NOT WORK!
    #TODO: TEST & FIX
    def search_grid(self, expansionlist, maxlength):
	beam_tmp = self.beam_size
	self.beam_size = float("inf")
	self.captions = []
	self.current_candidates = [(float("inf"), [[SENTENCE_START]])]
	self.next_candidates = []
	for i in xrange(maxlength):
	    self.step(expansionlist)	
	self.beam_size = beam_tmp
	print self.captions[0], self.score_sentence(self.captions[1], verbose=True)	
	pprint(self.captions[1:10])
	

    def search_beam(self, expansionlist, detailed=False):
	print "Searching for captions using the basic units"
	pprint(expansionlist)
	self.captions = []
	self.current_candidates = [(float("inf"), [[SENTENCE_START]])]
	self.next_candidates = []
	steps = 0
	while self.step(expansionlist):
	    steps = steps + 1
	    print "Completed iteration %d." % (steps)
	print "Done."
	pprint(self.captions)
        words = []
	for phrase in self.captions[0][1]:
	    words.extend(phrase)
	print words
	print "The best caption is:"
	print self.captions[0]
	print "csel component:"
        print map(lambda x: self.csel_model(x), words)
	print "length model:"
	print map(lambda x:self.len_model(x), (i+1 for i in xrange(len(words))))
	print "language model:"
	print self.lang_model.AssessText(words, self.m_lm, verbose=True)

    def insert(self, new_elem, lim_list):
	#If we have space left in the limited list or the new element is better than the worst old element, add it
	if len(lim_list) < self.beam_size:
	    insort_left(lim_list, new_elem)
	    return True
	else:
	    #Do this 'if' to circumvent the case where lim_list is empty.
	    if lim_list[-1] > new_elem:
		del lim_list[-1]
	    	insort_left(lim_list, new_elem)
		return True
	return False
