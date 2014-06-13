from data_manager.OSM import object_from_file

from pipelines.classes.DemoLMGenerator import *

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
def generate_captions_for_LM(itemiterator, voc_file, m_lm, len_file, beam_size, lmfile, phrase_attr, out_attr, global_lm = False):
	voc = object_from_file(Vocabulary, voc_file)
	#Instantiate length model
	len_model_object = object_from_file(GaussianLengthModel, len_file)
	len_model = lambda x: len_model_object.score(x)
	if global_lm:
		#Instantiate and start LM
		lm = object_from_file(LSVLM, lmfile)
		lm.set_vocabulary(voc_file)
		lm.set_lmfile(lmfile)
		lm.start()
	#Do the generation for each item
	for item in itemiterator:
		T0 = time()
		#Get the basic units
		
		if not global_lm:
			#Instantiate and start LM
			lm = object_from_file(LSVLM, item.get_attribute_path(lmfile))
			lm.set_vocabulary(voc_file)
			lm.set_lmfile(item.get_attribute_path(lmfile))
			lm.start()
		T_postlm = time()
		sents = item.get_attribute(phrase_attr, Sentences)
		phrases = set([])
		for sent in sents:
			for phrase in sent:
				for word in phrase:
					phrases.add((word,))
		phrases = map(list, phrases)
		#Build the caption generator
		C = DemoLMGenerator(len_model=len_model, lm=lm, m_lm=int(m_lm), phrases=phrases, beam_size=int(beam_size))
		T = time()
		caption = C.search()
		T2 = time()
		#print caption, T2 - T
		item.set_attribute(out_attr, [caption, "LM setup: "+str(T_postlm - T0), "Generation: "+str(T2-T), "Total: "+str(T2-T0)])
