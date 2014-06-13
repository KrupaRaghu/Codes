from data_manager.OSM import object_from_file

from pipelines.classes.CaptionGenerator import *

from pipelines.reduces.ParameterOptimization import read_param_file

from pipelines.formats.LengthModels import *
from pipelines.formats.ConditionalContentSelection import *
from pipelines.formats.PhraseAttachments import *
from pipelines.formats.Sentences import *
from pipelines.formats.LSVLM import *
from pipelines.formats.Vocabulary import *
from pipelines.LM_WEIGHTS import *

from time import time, localtime, asctime

#The items in phrase_attr must be in Sentences format to enable phrasing. If use_words is set, then phrasing will be ignored.
def generate_captions(itemiterator, voc_file, m_lm, csel_file, len_file, beam_size, lm_attr, phrase_attr, out_attr, pa_file = None, use_words = False, lowercased_csel=False, csel_vocsize=None):
	voc = object_from_file(Vocabulary, voc_file)
	#Instantiate content selection component
	csel_model = object_from_file(ConditionalContentSelector, csel_file)
	csel_model.set_epsilon(CSEL_EPSILON_OPT_DEV)
	if lowercased_csel:
		csel_model.set_vocab_size(int(csel_vocsize))
	else:
		csel_model.set_vocab_size(len(voc))
	#Instantiate length model
	len_model_object = object_from_file(GaussianLengthModel, len_file)
	len_model = lambda x: len_model_object.score(x)
	#Instantiate the phrase attachment component, if available
	pa_model = None
	if not pa_file is None:
		pa_model = object_from_file(PhraseAttachmentModel, pa_file)
		pa_model.set_epsilon(PA_EPSILON_OPT_DEV)
		pa_model.set_vocab_size(len(voc))
	#Do the generation for each item
	for item in itemiterator:
		#Instantiate and start LM
		T0 = time()
		lm = object_from_file(LSVLM, item.get_attribute_path(lm_attr))
		lm.set_vocabulary(voc_file)
		lm.set_lmfile(item.get_attribute_path(lm_attr))
		lm.start()
		#Get the basic units
		T_postlm = time()
		sents = item.get_attribute(phrase_attr, Sentences)
		phrases = set([])
		for sent in sents:
			for phrase in sent:
				if use_words:
					for word in phrase:
						phrases.add((word,))
				else:
					phrases.add(tuple(phrase))
		phrases = map(list, phrases)
		#Build the caption generator
		C = CaptionGenerator(len_model=len_model, csel_model=csel_model, lm=lm, m_lm=int(m_lm), phrases=phrases, beam_size=int(beam_size), pa_model=pa_model)
		T = time()
		caption = C.search()
		T2 = time()
		#print caption, T2 - T
		item.set_attribute(out_attr, [caption, "LM setup: "+str(T_postlm - T0), "Generation: "+str(T2-T), "Total: "+str(T2-T0)])

def generate_captions_for_LM_parameters(itemiterator, paramfile, voc_file, m_lm, csel_file, len_file, beam_size, lm_attr, phrase_attr, out_attr, pa_file = None, use_words = False, lowercased_csel=False, csel_vocsize=None):
	paramnames, params = read_param_file(paramfile)
	voc = object_from_file(Vocabulary, voc_file)
	#Instantiate content selection component
	csel_model = object_from_file(ConditionalContentSelector, csel_file)
	csel_model.set_epsilon(5e-4)
	if lowercased_csel:
		csel_model.set_vocab_size(int(csel_vocsize))
	else:
		csel_model.set_vocab_size(len(voc))
	#Instantiate length model
	len_model_object = object_from_file(GaussianLengthModel, len_file)
	len_model = lambda x: len_model_object.score(x)
	#Instantiate the phrase attachment component, if available
	pa_model = None
	if not pa_file is None:
		pa_model = object_from_file(PhraseAttachmentModel, pa_file)
		pa_model.set_epsilon(6e-7)
		pa_model.set_vocab_size(len(voc))
	#Do the generation for each item
	for item in itemiterator:
		#Instantiate and start LM
		lm = object_from_file(LSVLM, item.get_attribute_path(lm_attr))
		lm.set_vocabulary(voc_file)
		lm.set_lmfile(item.get_attribute_path(lm_attr))
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
		phrases = map(list, phrases)
		captions = ["Used paramfile %s for generation at %s." % (paramfile, asctime(localtime()))]
		name = item.get_attribute("original_name")
		for pars in params:
			#stderr.write("using params"+str(pars))
			lm.set_updates(zip(map(lambda x: name+x, paramnames), pars))
			lm.ReInit()
			C = CaptionGenerator(len_model=len_model, csel_model=csel_model, lm=lm, m_lm=int(m_lm), phrases=phrases, beam_size=int(beam_size), pa_model=pa_model)
			#captions.append([zip(paramnames,pars), C.search()])
			res = C.search()
			caption = []
			for score, answer in res:
#				print score, answer
				caption.append([score, map(lambda x: map(lambda y: C.extract_wo(y), x), answer[0])])
			captions.append(caption)
		item.set_attribute(out_attr, captions)


