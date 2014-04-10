from ..formats.ConditionalContentSelection import *
from ..formats.Sentences import *
from ..formats.BoW import *
from ..experiment_config import *
from data_manager.OSM import *
from math import sqrt, exp
from pprint import pprint

#Format should be either "text", "BoW", or "sentences"
def estimate_caption_if_document(itemiterator, doc_attr = None, cap_attr = None, content_format="text", silent = False):
    doc_bows = []
    cap_bows = []
    voc = set([])
    #Read all information
    for item in itemiterator:
        if content_format == "text":
            c_doc = BoW(item.get_attribute(doc_attr).split())
            c_cap = BoW(item.get_attribute(cap_attr).split())
            doc_bows.append(c_doc)
            cap_bows.append(c_cap)
            voc.update(c_doc.keys())
        elif content_format == "sentences":
            c_doc = BoW(item.get_attribute(doc_attr, Sentences).get_text(SENTENCE_START, SENTENCE_END).split())
            c_cap = BoW(item.get_attribute(cap_attr, Sentences).get_text(SENTENCE_START, SENTENCE_END).split())
            doc_bows.append(c_doc)
            cap_bows.append(c_cap)
            voc.update(c_doc.keys())
        elif content_format == "BoW":
            c_doc = item.get_attribute(doc_attr, BoW)
            c_cap = item.get_attribute(cap_attr, BoW)
            doc_bows.append(c_doc)
            cap_bows.append(c_cap)
            voc.update(c_doc.keys())
    #Parse all information.
    #Register which documents contain which words
    doc_occs = {w:[] for w in voc}
    for (i,B) in enumerate(doc_bows):
        for w in B.keys():
            doc_occs[w].append(i)
    #Then count how many of the relevant captions also contain the word how many times.
    w_occs = {w:[] for w in voc}
    #For each word
    for w in voc:
        #Go through all documents that contain the word
        for i in doc_occs[w]:
            w_occs[w].append(cap_bows[i].get(w,0))
            #Record the number of times the word occurs in the corresponding caption

    #Make probability model from these occurrences
    totals = {w:len(w_occs[w]) for w in voc}
    counts = {w:Counter(w_occs[w]) for w in voc}
    model = ConditionalContentSelector(counts, totals)
    if not silent:
        print model.encode()
    return model

def compute_scores_for_caption_words(itemiterator, modelfile, epsilon, vocsize, cap_attr="caption_sentences_stanford", cap_format="sentences", lowercased = False, probs=False):
	model = object_from_file(ConditionalContentSelector, modelfile)
	model.set_vocab_size(int(vocsize))
	model.set_epsilon(float(epsilon))
	for item in itemiterator:
		cap = []
		if cap_format=="sentences":
			cap = item.get_attribute(cap_attr, Sentences).get_text().split()
		else:
			cap = item.get_attribute(cap_attr).split()
		if lowercased:
			cap = map(lambda x:x.lower(), cap)
		for word in cap:
			if probs:
				print model.prob(word)
			else:
				print model.score(word)

def compute_average_score_for_captions(itemiterator, modelfile, out_attr, epsilon, vocsize, cap_attr="caption_sentences_stanford", cap_format="sentences", lowercased = False, probs=False):
	
	model = object_from_file(ConditionalContentSelector, modelfile)
	model.set_vocab_size(int(vocsize))
	model.set_epsilon(float(epsilon))
	totals = []
	for item in itemiterator:
		cap = []
		if cap_format=="sentences":
			cap = item.get_attribute(cap_attr, Sentences).get_text().split()
		else:
			cap = item.get_attribute(cap_attr).split()
		if lowercased:
			cap = map(lambda x:x.lower(), cap)
		item.set_attribute(out_attr, [model.score_phrase(cap)/len(cap), list(model.score_phrase_detailed(cap))])
		totals.append(model.score_phrase(cap)/len(cap))
		if probs:
			print exp(-model.score_phrase(cap)/len(cap))
		else:
			print model.score_phrase(cap)/len(cap)
	if probs:
		print exp(-sum(totals)/len(totals))
	else:
		print sum(totals)/len(totals)
