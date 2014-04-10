from pipelines.formats.Vocabulary import *
from data_manager.OSM import *


vocfile = "/nethome/afischer/BA/components/vocabularies/training_K750.voc"

voc = object_from_file(Vocabulary, vocfile)

print len(voc), "in normal vocabulary."
print len(set(map(lambda x: x.lower(), voc))), "in lowercased vocabulary."
