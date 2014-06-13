from data_manager.OSM import *

from pipelines.classes.BeamSearcher import *
from pipelines.experiment_config import SENTENCE_START

W_LEN_DEFAULT = 6.0
W_LM_DEFAULT = 1.0

class DemoLMGenerator(BeamSearcher):
	def __init__(self, len_model, lm, m_lm, phrases, beam_size = BEAM_SIZE_DEFAULT, start_sentences=[[SENTENCE_START]], w_len=W_LEN_DEFAULT, w_lm = W_LM_DEFAULT):
		self.len_model = len_model
		self.lm = lm
		self.m_lm = int(m_lm)
		self.beam_size = beam_size
		self.phraselist = self.prepare_phrases(phrases)
		#Weights for scoring
		self.w_len = float(w_len)
		self.w_lm = float(w_lm)
		#Build start states
		start_states = map(self.make_node_full, map(self.prepare_phrases, start_sentences))
		start_states = map(lambda (x, T): (float("inf"), T), start_states)
		BeamSearcher.__init__(self, start_states=start_states, beam_size=beam_size)
		#print "Initialization complete."
	
	def prepare_phrases(self, phrases):
		out = []
		for phrase in phrases:
			p_out = []
			for word in phrase:
				p_out.append((word, self.lm.voc[word]))
			out.append(p_out)
		return out
	def extract_words(self, word):
		return word[0]
	def extract_indices(self, word):
		return word[1]

	def set_params(self, len_params = {},lm_params = []):
		print "Setting parameters", len_params, lm_params
		if len_params:
			self.len_model.set_params(**len_params)
		if lm_params:
			self.lm.set_updates_for_params(lm_params)
			self.lm.ReInit()

	def make_node_full(self, words):
		"""Verbosely computes a node from the given list of phrases."""
		words = []
		len_score = self.len_model(len(words))
		#print words
		lm_prob, lm_score = self.lm.AssessIndexedText(map(self.extract_indices, words), self.m_lm)
		#print "Asking LM to assess", words, "with m", self.m_lm, "starting at", 0
		return (self.w_len*len_score+self.w_lm*lm_score, (words, len(words), self.w_len*len_score, self.w_lm*lm_score))

	def expand(self, (words, length, len_score, lm_score)):
		#Try every possible phrase as expansion
		for word in self.phraselist:
			WORDS = words+word
			#Recompute the length score
			new_len = len(WORDS)
			new_len_score = self.w_len*self.len_model(new_len)
			#Compute the additional LM score
			new_words = words[max(0,len(words)-self.m_lm):]+word
			#print "Asking LM to assess", words, "with m", self.m_lm, "starting at", self.m_lm-1
			new_lmprob, add_lmscore = self.lm.AssessIndexedText(map(self.extract_indices, new_words), self.m_lm, start_at = self.m_lm-1)
			new_lm_score = lm_score + self.w_lm*add_lmscore
			yield (WORDS, new_len, new_len_score, new_lm_score)
	
	def score(self, (phrases, length, len_score, lm_score)):
		return len_score + lm_score
