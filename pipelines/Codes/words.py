from data_manager.OSM import *
import json

def words_extract(itemiterator, output_words, doc):
	for i in itemiterator:
		W = i.get_attribute(doc).split()
		S = list(W)
		i.set_attribute(output_words, json.dumps(S))
