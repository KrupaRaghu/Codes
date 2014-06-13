from ..experiment_config import *
from ..formats.Sentences import *
from bisect import insort_left
from pprint import pprint
from time import time

#Functions for generating captions.

BEAM_SIZE_DEFAULT = 500

class BeamSearcher(object):
	def __init__(self, start_states, beam_size = BEAM_SIZE_DEFAULT):
		"""
			start_states: list of start states
		"""
		self.start_states = start_states[:]
		self.beam_size = beam_size

	def expand(self, node):
		raise NotImplementedError

	def score(self, node):
		raise NotImplementedError

	def search(self, verbose=False, return_time = False):
		start_time = time()
		self.expanded = []
		self.next_candidates = []
		self.current_candidates = self.start_states[:]
		steps = 0
		#print "Start states:"
		#pprint(self.start_states)
		while self.step():
	    		steps = steps + 1
	    		if verbose:
				print "Completed iteration %d." % (steps)
				print len(self.expanded), len(self.current_candidates)
				pprint(self.expanded)
				print "Candidates for next round:"
				pprint(self.current_candidates)
		end_time = time()
		duration = end_time - start_time
		if verbose:
			print "Search completed. The best result is:", self.expanded[0]	
		#return self.expanded[0]
		if return_time:
			return self.expanded, duration
		else:
			return self.expanded

	def step(self):
		found_one = self.expand_current()
		self.current_candidates = self.next_candidates
		self.next_candidates = []
		return found_one
	
	def expand_current(self):
		found_one = False
		for (score, state) in self.current_candidates:
			if self.expand_state(state):
				found_one = True
		return found_one

	def expand_state(self, state):
		for new_state in self.expand(state):
	    		self.insert((self.score(new_state), new_state), self.next_candidates)
		return self.insert((self.score(state), state), self.expanded)
    
	def insert(self, new_elem, lim_list):
		if len(lim_list) < self.beam_size:
			#If we have space left in the limited list, add the new element.
	    		insort_left(lim_list, new_elem)
	    		return True
		else:
			#Otherwise, the new element must be better than the worst old element.
	    		if lim_list[-1] > new_elem:
				del lim_list[-1]
				insort_left(lim_list, new_elem)
				return True
		return False
