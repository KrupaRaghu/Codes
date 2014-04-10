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

#print "Search:"
#searcher2 = BeamSearcher([(score2(S), S)], expand2, score2, beam_size = BS)
#print searcher2.search(verbose=False)

# CAPTION GENERATION TEST PART
#Test content selection
csel_file = "/nethome/afischer/BA/components/conditional_content_selection/training.content_selector"
csel_model = object_from_file(ConditionalContentSelector, csel_file)

words = ["1,809", "blast-off", "1,800", "gah", "sonja", "woods", "cooking", "crouch"]
#"1,809": {"0": 1}, "blast-off": {"0": 1}, "1,800": {"0": 8}, "gah": {"0": 3}, "sonja": {"1": 1}, "askew": {"0": 2}, "woods": {"1": 6, "0": 14}, "spiders": {"0": 4}, "hanging": {"0": 20}, "trawling": {"0": 1}, "localized": {"0": 6}, "disobeying": {"0": 2}, "hennings": {"0": 3}, "spot-kicks": {"0": 1},
def expand_csel(old_words):
	for w in words:
		yield old_words+[w]

def score_csel(old_words):
	return csel_model.score_phrase(old_words)

#print "Conditional component test:"
#searcher_csel = BeamSearcher([(float("inf"), ["test"])], expand_csel, score_csel, 3)
#print searcher_csel.search(verbose=False)

#Test length model
len_file = "/nethome/afischer/BA/components/sentence_lengths/training_captions.gaussian"
len_model_object = object_from_file(GaussianLengthModel, len_file)
len_model = lambda x: len_model_object.score(len(x))

def expand_len(old_words):
	for w in words:
		yield old_words + [w]

#print "Length model test:"
#searcher_len = BeamSearcher([(len_model(["test"]), ["test"])], expand_len, len_model, 50)
#print searcher_len.search(verbose=False)
#print "Length of best result:", len(searcher_len.expanded[0][-1])

#Test LM
tri_file = "/nethome/afischer/BA/components/Ngrams/trigram_SRI.lm"
voc_file = "/nethome/afischer/BA/components/vocabularies/training_K750.voc"
m_lm = 3
lm = object_from_file(LSVLM, tri_file)
lm.set_vocabulary(voc_file)
lm.set_lmfile(tri_file)
lm.start()

pa_model = None
len_model = lambda x: len_model_object.score(x)

def make_node_LM(phrases):
	words = []
	for phrase in phrases:
		for word in phrase:
			words.append(word)
	lm_prob, lm_score = lm.AssessText(words, m_lm)
	return lm_score, (phrases, lm_score)

def make_expander_LM(phraselist):
	#print "LM expander with list:"
	pprint(phraselist)
	def expand((phrases, lm_score)):
		#print "Expanding", phrases
		#Try every possible phrase as expansion
		for phrase in phraselist:
			new_phrases = phrases+[phrase]
			words = []
			for phrase in new_phrases:
				for word in phrase:
					words.append(word)
			#Compute the additional LM score
			new_words = phrases[-1][len(phrases[-1])-m_lm:]+phrase
			#print "New words for the LM (with history) should be", new_words
			new_lmprob, add_lmscore = lm.AssessText(words, m_lm, start_at = m_lm-1)
			new_lm_score = lm_score + add_lmscore
			yield (new_phrases, new_lm_score)
	return expand

expand_LM = make_expander_LM(map(lambda x:[str(x)], [1,2,3,4,"and", "the", "muffins", "I"]))

def score_LM((phrases, old_score)):
	words = []
	for phrase in phrases:
		for word in phrase:
			words.append(word)
	#Compute the additional LM score
	#print "Full score"
	lm_prob, lm_score = lm.AssessText(words, m_lm)
	return lm_score

#start_state_LM = make_node_LM([[SENTENCE_START]])
#print "LM test"
#print "Start state:", start_state_LM

#searcher_LM = BeamSearcher([start_state_LM], expand_LM, score_LM, beam_size = 3)
#searcher_LM.search(verbose=True)

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
	return (len_score+lm_score+cond_score+pa_score, (phrases, len(words), len_score, lm_score, cond_score, pa_score))

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
			new_lmprob, add_lmscore = lm.AssessText(words, m_lm, start_at = m_lm-1)
			new_lm_score = lm_score + add_lmscore
			#Recompute the conditional score
			new_cond_score = csel_model.score_phrase(words)
			#Compute the additional phrase attachment score
			new_pa_score = pa_score
			if not pa_model is None:
				new_pa_score = new_pa_score + pa_model.score(phrases[-1], phrase)	
			yield (new_phrases, new_len, new_len_score, new_lm_score, new_cond_score, new_pa_score)
	return expand

def score((phrases, length, len_score, lm_score, cond_score, pa_score)):
	return len_score + lm_score + cond_score + pa_score

wordfile="/nethome/afischer/BA/misc/words"

start_state = make_node_full([[SENTENCE_START]])
print "Full test"
print "Start state:", start_state
expand = make_caption_expander(map(lambda x:[str(x)], [1,2,3,4,"and", "the", "muffins", "I"]))

searcher_full = BeamSearcher([start_state], expand, score, beam_size = 3)
searcher_full.search(verbose=True)
