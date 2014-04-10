from data_manager.OSM import *

from pipelines.formats.LSVLM import LSVLM

tri_file = "/nethome/afischer/BA/components/Ngrams/trigram_SRI.lm"
lda_file = "/nethome/afischer/BA/corpus/data/08/02155/dDocZeroLM"
voc_file = "/nethome/afischer/BA/components/vocabularies/training_K750.voc"
m = 3

lm2 = object_from_file(LSVLM, lda_file)
lm2.set_vocabulary(voc_file)
lm2.set_lmfile(lda_file)
lm2.start()

lm2.CollectParams()

lm = object_from_file(LSVLM, tri_file)
lm.set_vocabulary(voc_file)
lm.set_lmfile(tri_file)
lm.start()

lm.CollectParams()
