from pipelines.scripts.GENERATION import *
from data_manager.OSM import *

from pipelines.formats.LengthModels import *
from pipelines.formats.ConditionalContentSelection import *
from pipelines.formats.LSVLM import LSVLM

tri_file = "/nethome/afischer/BA/components/Ngrams/trigram_SRI.lm"
voc_file = "/nethome/afischer/BA/components/vocabularies/training_K750.voc"
m = 3
csel_file = "/nethome/afischer/BA/components/conditional_content_selection/training.content_selector"
len_file = "/nethome/afischer/BA/components/sentence_lengths/training_captions.gaussian"
wordfile="/nethome/afischer/BA/misc/words"

dummy_csel = lambda x: 0.0
len_model = object_from_file(GaussianLengthModel, len_file)
csel_model = object_from_file(ConditionalContentSelector, csel_file)
lm = object_from_file(LSVLM, tri_file)
lm.set_vocabulary(voc_file)
lm.set_lmfile(tri_file)
lm.start()

words = ["I", "to", "from"]
with open(wordfile, "r") as f:
	words = f.read().split()

C.search_beam(map(lambda x: [x], words))
#C.search_grid(map(lambda x: [x], words), 11)

