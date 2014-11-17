from data_manager.OSM import *

from pipelines.Codes.Beam_Searcher import *
from pipelines.exp_config import SENTENCE_START

class CaptionGenerator(BeamSearcher):

	def __init__(self, words, beam_size = BEAM_SIZE_DEFAULT, start_sentences=[[SENTENCE_START]]):

		#Build start states
		start_states = start_sentences
		#start_states = map(self.make_node_full, map(self.prepare_phrases, start_sentences))
		#start_states = map(lambda (x, T): (float("inf"), T), start_states)
		print "start_states: ", start_states
		print "beam_size: ", beam_size

		BeamSearcher.__init__(self, start_states, beam_size)				
		
		self.wordlist = self.prepare_wordlist(words)
		print "wordslist", self.wordlist
	
	def prepare_wordlist(self, words):
		out = []
		for word in words:
			w_out = []
			for word in words:
				w_out.append((word,))
			out.append(w_out)
		return out


	def expand(self, words):
		for word in self.wordlist:
			new_words = word+[words]
			word = []
			for word in new_words:
				word.extend(word)
		return next_candidates+word
			
	def score(self, word):
		return 0
