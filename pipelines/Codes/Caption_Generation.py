from data_manager.OSM import object_from_file
from pipelines.Codes.Caption_Generator import *
from pipelines.formats.Sentences1 import *



def generate_captions(itemiterator, beam_size, words_attr, output_attr, use_words=False):


	for item in itemiterator:

		#Instantiate for words

		words = item.get_attribute(words_attr, list)
		word = set([])
		print words
		if use_words:
			word.append((words,))
		word = map(list, word)
#		print word

		C = CaptionGenerator(word, beam_size=int(beam_size))
		captions = C.search
		print captions
