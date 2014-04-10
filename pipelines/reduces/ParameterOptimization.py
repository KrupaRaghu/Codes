
from ..formats.Sentences import *
from ..formats.LSVLM import LSVLM
from data_manager.OSM import object_from_file

#For caption generation
from pipelines.scripts.CaptionGenerator import *
from pipelines.formats.LengthModels import *
from pipelines.formats.ConditionalContentSelection import *
from pipelines.formats.PhraseAttachments import *
from pipelines.formats.Sentences import *
from pipelines.formats.LSVLM import *
from pipelines.scripts.TER import *

#Scripts for optimizing the parameters of LMs.

def read_param_file(paramfile):
    paramnames = []
    params = []
    with open(paramfile, "r") as f:
        paramnames = f.readline().split()
        for line in f.readlines():
            params.append(map(float, line.split()))
    return paramnames, params

def pick_best_parameters_by_total(itemiterator, paramfile, perp_attr, num_lms = 240):
    #Read the parameter list
    paramnames, params = read_param_file(paramfile)    
    perp_totals = [0.0]*len(params)

    for item in itemiterator:
	perps = item.get_attribute(perp_attr, list)
	for i, p in enumerate(perps):
	    perp_totals[i] = perp_totals[i] + p
    
    best = min(zip(perp_totals, params))
    print "Total perplexities of all data:"
    for p,pars in sorted(zip(perp_totals, params)):
    	print p, float(p)/num_lms, pars
    print "The best parameter set is:"
    print best

def calc_perplexity(itemiterator, vocfile, lm_attr, cap_attr, out_attr, paramfile = None, visi_attr = None, cap_format="sentences", M=1, global_lm = False):
    if not paramfile is None:
	#Read the parameter list
    	paramnames, params = read_param_file(paramfile)    
    else:
	paramnames = None
	params = None

    perplexities_total = [0.0]*len(params)
    
    num_items = 0
    lm = None
    
    if global_lm:
	lm = object_from_file(LSVLM, lm_attr)
	lm.set_vocabulary(vocfile)
    	lm.set_lmfile(lm_attr)
    	lm.start()

    for item in itemiterator:
        num_items = num_items + 1
        if cap_format == "sentences":
            caption = item.get_attribute(cap_attr, Sentences).get_text(one_per_line=False).split()
        elif cap_format == "text":
            caption = item.get_attribute(cap_attr).split()
        
        if not visi_attr is None:
            visiterms = item.get_attribute(visi_attr, list)
            caption = caption + visiterms
        if not global_lm:
	#For each item, get the LM
            lm = item.get_attribute(lm_attr, LSVLM)
            lm.set_vocabulary(vocfile)
            lm.set_lmfile(item.get_attribute_path(lm_attr))
            lm.start()

        perplexities = []
	caption_idxes = lm.voc.index_words(caption)
        if not paramfile is None:
	    for paramset in params:
                for paramname, paramval in zip(paramnames, paramset):
                    lm.add_DynParam(paramname, paramval)
             	lm.ReInit()
            
            perplexities.append(lm.Perplexity_idxes(caption_idxes,M))
	else:
            perplexities.append(lm.Perplexity_idxes(caption_idxes,M))

      	item.set_attribute(out_attr, perplexities)

def score_csel_epsilon(itemiterator, voc_size, csel_file, cap_attr, out_attr, content_format="sentences", lowercased = False):
	epses = [0.0001, 0.0005, 0.001, 0.002, 0.003, 0.004, 0.0045, 0.005, 0.0055, 0.006, 0.007, 0.008, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3]
	#Instantiate content selection component
	csel_model = object_from_file(ConditionalContentSelector, csel_file)
	total_scores = [0.0]*len(epses)
	for item in itemiterator:
		scores = []	
		cnt = []
		if content_format == "sentences":
			cnt = item.get_attribute(cap_attr, Sentences).get_text().split()
		else:
			cnt = item.get_attribute(cap_attr).split()
		if lowercased:
			cnt = map(lambda x: x.lower(), cnt)
		for i,eps in enumerate(epses):
			csel_model.set_params(**{"epsilon": eps, "vocab_size":int(voc_size)})
			S = csel_model.score_wordlist_normalize(map(lambda x: x.lower(), cnt))
			scores.append((eps, voc_size, S))
			total_scores[i] = total_scores[i]+S
		item.set_attribute(out_attr, scores)

	print "Conditional content selection epsilon optimization for voc_size =", voc_size
	print sorted(zip(total_scores, epses))

def score_pA_epsilon(itemiterator, voc_size, pA_file, cap_attr, out_attr, content_format="sentences"):
	epses = [1e-5, 2e-5, 3e-5, 4e1-5, 0.00005, 0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.001, 0.002, 0.003]
	#, 0.004, 0.0045, 0.005, 0.0055, 0.006, 0.007, 0.008, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
	#Instantiate content selection component
	pA_model = object_from_file(PhraseAttachmentModel, pA_file)
	total_scores = [0.0]*len(epses)
	for item in itemiterator:
		scores = []	
		cnt = item.get_attribute(cap_attr, Sentences).get_text().split()
		
		for i,eps in enumerate(epses):
			pA_model.set_params(**{"epsilon": eps, "vocab_size":int(voc_size)})
			S_tot = 0.0
			for sentence in cnt:
				S = pA_model.score_sentence(sentence)
				S_tot = S_tot + S
			scores.append((eps, voc_size, S_tot))
			total_scores[i] = total_scores[i]+S_tot
		item.set_attribute(out_attr, scores)
	print "Phrase attachment epsilon optimization for voc_size =", voc_size
	print sorted(zip(total_scores, epses))

def extract_sentences(L):
	sentences = []
	for line in L:
		sentences.append(line[2])
	return sentences

#sent_attr must be the list of generated best captions for the parameters in paramfile
#after, each item has an out_attr containing the TER scores for each best sentence in sent_attr
def rank_params_by_TER(itemiterator, sent_attr, cap_attr, out_attr, paramfile, cap_format="sentences", print_totals = False, print_best = False):
	paramnames, params = read_param_file(paramfile)
	totals = [0.0]*len(params)
	for item in itemiterator:
		sents_raw = item.get_attribute(sent_attr, list)
		sents = []
		for resline in sents_raw[1:]:
			sents.append(" ".join(map(lambda x: " ".join(x), resline[0][1])).split())
		cap = []
		if cap_format == "sentences":
			cap = item.get_attribute(cap_attr, Sentences).get_text().split()
		else:
			#Assuming that format is raw text now
			cap = item.get_attribute(sent_attr).split()
		out = []
		for i,sent in enumerate(sents):
			T = TER(sent, cap)
			totals[i] = totals[i]+T
			out.append(T)
		item.set_attribute(out_attr, out)
	if print_totals:
		print sorted(zip(totals, params))
	if print_best and not print_totals:
		print sorted(zip(totals,params))[0]

def analyze_TERs_for_parameters(itemiterator, paramfile, TER_attr, doc_attr=None, cap_attr=None, formats="sentences"):
	paramnames, params = read_param_file(paramfile)
	totals_nosubset = [0.0]*len(params)
	totals_subset = [0.0]*len(params)
	num_subset = 0
	num_nosubset = 0
	for item in itemiterator:
		TERs = item.get_attribute(TER_attr, list)
		cap = set([])
		doc = set([])
		if not doc_attr is None and not cap_attr is None:
			if formats == "sentences":
				cap = set(item.get_attribute(cap_attr, Sentences).get_text().split()) 
				doc = set(item.get_attribute(doc_attr, Sentences).get_text().split()) 
			else:
				cap = set(item.get_attribute(cap_attr).split()) 
				doc = set(item.get_attribute(doc_attr).split()) 
		if cap.issubset(doc):
			num_subset = num_subset + 1
			for i,T in enumerate(TERs):
				totals_subset[i] = totals_subset[i] + T
		else:
			num_nosubset = num_nosubset + 1
			for i,T in enumerate(TERs):
				totals_nosubset[i] = totals_nosubset[i] + T
	print "Out of", num_subset+num_nosubset, "document-caption pairs, in", num_subset, "cases is the caption a subset of the document, and in", num_nosubset, "cases is it not a subset."
	print "TERs across all data: (total, average)"
	for x in sorted(zip(zip(map(lambda (a,b): a+b, zip(totals_nosubset, totals_subset)),map(lambda (a,b): (a+b)/(num_subset+num_nosubset), zip(totals_nosubset, totals_subset))), params)):
		print x
	print "TER where cap subset doc: (total, average)"
	for x in zip(totals_subset, zip(map(lambda x:x/num_subset, totals_subset),params)):
		print x
	print "TER where cap NOT subset doc: (total, average)"
	for x in zip(totals_nosubset, zip(map(lambda x:x/num_nosubset, totals_nosubset), params)):
		print x


#The items in phrase_attr must be in Sentences format to enable phrasing. If use_words is set, then phrasing will be ignored.
def optimize_length_attenuation_parameter(itemiterator, paramfile, voc_file, m_lm, csel_file, len_file, beam_size, lm_attr, phrase_attr, out_attr, pa_file = None, use_words = False):
	#Instantiate content selection component
	csel_model = object_from_file(ConditionalContentSelector, csel_file)
	#Instantiate length model
	len_model_object = object_from_file(GaussianLengthModel, len_file)
	len_model = lambda x: len_model_object.score(len(x))
	#Instantiate the phrase attachment component, if available
	pa_model = None
	if not pa_file is None:
		pa_model = object_from_file(PhraseAttachmentModel, pa_file)
	
    	#Read parameters
	paramnames, params = read_param_file(paramfile)
 
	#Do the generation for each item
	for item in itemiterator:
		#Instantiate and start LM
		lm = object_from_file(LSVLM, item.get_attribute_path(lm_attr))
		lm.set_vocabulary(voc_file)
		lm.set_lmfile(tri_file)
		lm.start()
		#Get the basic units
		sents = item.get_attribute(phrase_attr, Sentences)
		phrases = set([])
		for sent in sents:
			for phrase in sent:
				if use_words:
					for word in phrase:
						phrases.add((word,))
				else:
					phrases.add(tuple(phrase))
		#Build the caption generator
		generated = []
		for att in params:
			C = CaptionGenerator(len_model=len_model, csel_model=csel_model, lm=lm, m_lm=str(m_lm), phrases=phrases, beam_size=beam_size, pa_model=pa_model, w_len=att[0])
			generated.append((att[0], C.search()))
		item.set_attribute(out_attr, generated)
