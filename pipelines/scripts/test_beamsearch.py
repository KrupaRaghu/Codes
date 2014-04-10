from pipelines.scripts.BeamSearcher import BeamSearcher
from data_manager.OSM import *

from pipelines.formats.LengthModels import *
from pipelines.formats.ConditionalContentSelection import *
from pipelines.formats.LSVLM import LSVLM

from pipelines.experiment_config import SENTENCE_START

S = [1]

def expand((score, L)):
	for x in xrange(10):
		yield (score+x, L+[x])

def expand2(L):
	for x in xrange(10):
		yield L+[x]

def score((score, L)):
	return max([0,100-score])

def score2(L):
	return max([0,100-sum(L)])

BS = 5

print "Search:"
searcher2 = BeamSearcher([(score2(S), S)], expand2, score2, beam_size = BS)
print searcher2.search(verbose=False)


# CAPTION GENERATION TEST PART
tri_file = "/nethome/afischer/BA/components/Ngrams/trigram_SRI.lm"
voc_file = "/nethome/afischer/BA/components/vocabularies/training_K750.voc"
m_lm = 3
csel_file = "/nethome/afischer/BA/components/conditional_content_selection/training.content_selector"
len_file = "/nethome/afischer/BA/components/sentence_lengths/training_captions.gaussian"
wordfile="/nethome/afischer/BA/misc/words"

len_model_object = object_from_file(GaussianLengthModel, len_file)
len_model = lambda x: len_model_object.score(x)
csel_model = object_from_file(ConditionalContentSelector, csel_file)
lm = object_from_file(LSVLM, tri_file)
lm.set_vocabulary(voc_file)
lm.set_lmfile(tri_file)
lm.start()

def make_node_full(phrases):
	"""Verbosely computes a node from the given list of phrases."""
	words = []
	for phrase in phrases:
		for word in phrase:
			words.append(word)
	len_score = len_model(len(words))
	lm_prob, lm_score = lm.AssessText(words, m_lm)
	cond_score = csel_model.score_phrase(words)
	pa_score = 0.0
	if not pa_model is None:
		pa_score = pa_model.score_sentence(phrases)
	return (phrases, len(words), len_score, lm_score, cond_score, pa_score)

def make_caption_expander(phraselist):
	def expand((phrases, length, len_score, lm_score, cond_score, pa_score)):
		#Try every possible phrase as expansion
		for phrase in phraselist:
			new_phrases = phrases+[phrase]
			words = []
			for phrase in new_phrases:
				for word in phrase:
					words.append(word)
			#Recompute the length score
			new_len = length + len(phrase) 
			new_len_score = len_model(new_len)
			#Compute the additional LM score
			new_words = phrases[-1][len(phrases[-1])-m_lm:]+phrase
			new_lm_score = lm_score + lm.AssessText(words, m_lm, start_at = m_lm-1)
			#Recompute the conditional score
			new_cond_score = csel_model(words)
			#Compute the additional phrase attachment score
			new_pa_score = pa_score
			if not pa_model is None:
				new_pa_score = new_pa_score + pa_model(phrases[-1], phrase)	
			yield (new_phrases, new_len, new_len_score, new_lm_score, new_cond_score, new_pa_score)
	return expand

def score((phrases, len_score, lm_score, cond_score, pa_score)):
	return len_score + lm_score + cond_score + pa_score

start_state = make_node_full([[SENTENCE_START]])

expand = make_caption_expander(map(str, [1,2,3,4,"and", "the", "muffins", "I"]))
for x in expand(start_state):
	print x

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

    def set_params(self, m_len, csel_eps, phrase_eps, beta_FMA, w_dDoc, w_dImg, w_dMix, w_Zero):
	#Set mean sentence length to m_len
	self.len_model.mean = m_len
	#Set conditional content selection epsilon to csel_eps
	self.csel_model.set_epsilon(csel_eps)
	#Set phrase attachment model epsilon to phrase_eps, if it exists
	#Also set vocabulary size to the LM's vocabulary size
	if not self.pa_model is None and phrase_eps > 0.0:
	    self.pa_model.epsilon = phrase_eps
	    self.pa_model.vocab_size = len(self.lang_model.voc)
	#Set the LM parameters
	params = [beta_FMA, w_dDoc, w_dImg, w_dMix, w_Zero]
   	self.lang_model.set_updates_for_params(params)
 
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
