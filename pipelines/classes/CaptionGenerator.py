from data_manager.OSM import *

from pipelines.classes.BeamSearcher import *
from pipelines.experiment_config import SENTENCE_START

W_LEN_DEFAULT = 15.0
W_LM_DEFAULT = 1.0
W_COND_DEFAULT = 1.0
W_PA_DEFAULT = 1.0

class CaptionGenerator(BeamSearcher):
	def __init__(self, len_model, csel_model, lm, m_lm, phrases, beam_size = BEAM_SIZE_DEFAULT, pa_model = None, start_sentences=[[[SENTENCE_START]]], w_len=W_LEN_DEFAULT, w_lm = W_LM_DEFAULT,w_cond = W_COND_DEFAULT,w_pa=W_PA_DEFAULT, csel_lowercased = False):
		self.len_model = len_model
		self.csel_model = csel_model
		self.csel_lowercased = csel_lowercased
		self.lm = lm
		self.m_lm = int(m_lm)
		self.beam_size = beam_size
		self.pa_model = pa_model
		self.phraselist = self.prepare_phrases(phrases)
		print "phraselist", self.phraselist
		#Weights for scoring
		self.w_len = float(w_len)
		self.w_cond = float(w_cond)
		self.w_lm = float(w_lm)
		self.w_pa = float(w_pa)
		#Build start states
		start_states = map(self.make_node_full, map(self.prepare_phrases, start_sentences))
		start_states = map(lambda (x, T): (float("inf"), T), start_states)
		print "start_states", start_states
		BeamSearcher.__init__(self, start_states=start_states, beam_size=beam_size)
		print "Initialization complete."
	
	def prepare_phrases(self, phrases):
		out = []
		for phrase in phrases:
			p_out = []
			for word in phrase:
				p_out.append((word, word.lower(), self.lm.voc[word], self.lm.voc[word.lower()]))
			out.append(p_out)
		return out
	def extract_wo(self, word):
		return word[0]
	def extract_wl(self, word):
		return word[1]
	def extract_io(self, word):
		return word[2]
	def extract_il(self, word):
		return word[3]

	def set_params(self, len_params = {}, csel_params = {}, phrase_params = {}, lm_params = []):
		print "Setting parameters", len_params, csel_params, phrase_params, lm_params
		if len_params:
			self.len_model.set_params(**len_params)
		if csel_params:
			self.csel_model.set_params(**len_params)
		if phrase_params and not self.pa_model is None:
			self.pa_model.set_params(**len_params)
		if lm_params:
			self.lm.set_updates_for_params(lm_params)
			self.lm.ReInit()

	def make_node_full(self, phrases):
		"""Verbosely computes a node from the given list of phrases."""
		words = []
		for phrase in phrases:
			for word in phrase:
				words.append(word)
		len_score = self.len_model(len(words))
		#print words
		lm_prob, lm_score = self.lm.AssessIndexedText(map(self.extract_io, words), self.m_lm)
		#print "Asking LM to assess", words, "with m", self.m_lm, "starting at", 0
		if self.csel_lowercased:
			cond_score = self.csel_model.score_wordlist(map(self.extract_wl, words))
		else:
			cond_score = self.csel_model.score_wordlist(map(self.extract_wo, words))
		pa_score = 0.0
		if not self.pa_model is None:
			pa_score = self.pa_model.score_sentence(map(lambda x: map(self.extract_wo, x), phrases))
		return (self.w_len*len_score+self.w_lm*lm_score+self.w_cond*cond_score+self.w_pa*pa_score, (phrases, len(words), self.w_len*len_score, self.w_lm*lm_score, self.w_cond*cond_score, self.w_pa*pa_score))

	def expand(self, (phrases, length, len_score, lm_score, cond_score, pa_score)):
		#Try every possible phrase as expansion
		for phrase in self.phraselist:
			new_phrases = phrases+[phrase]
			words = []
			for phrase in new_phrases:
				words.extend(phrase)
			#Recompute the length score
			new_len = length + len(phrase) 
			new_len_score = self.w_len*self.len_model(new_len)
			#Compute the additional LM score
			new_words = phrases[-1][len(phrases[-1])-self.m_lm:]+phrase
			#print "Asking LM to assess", words, "with m", self.m_lm, "starting at", self.m_lm-1
			new_lmprob, add_lmscore = self.lm.AssessIndexedText(map(self.extract_io, words), self.m_lm, start_at = self.m_lm-1)
			new_lm_score = lm_score + self.w_lm*add_lmscore
			#Recompute the conditional score
			if self.csel_lowercased:
				new_cond_score = self.w_cond*self.csel_model.score_wordlist(map(self.extract_wl, words))
			else:
				new_cond_score = self.w_cond*self.csel_model.score_wordlist(map(self.extract_wo, words))
			#Compute the additional phrase attachment score
			new_pa_score = pa_score
			if not self.pa_model is None:
				new_pa_score = new_pa_score + self.w_pa*self.pa_model.score(map(self.extract_wo, phrases[-1]), map(self.extract_wo, phrase))
			yield (new_phrases, new_len, new_len_score, new_lm_score, new_cond_score, new_pa_score)
	
	def score(self, (phrases, length, len_score, lm_score, cond_score, pa_score)):
		return len_score + lm_score + cond_score + pa_score
