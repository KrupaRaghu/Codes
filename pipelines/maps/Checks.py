from data_manager.OSM import object_from_file
from pipelines.formats.Vocabulary import *
from pipelines.formats.Sentences import *
from pipelines.experiment_config import UNKNOWN_WORD

def check_caption_subset_of_doc(item, cap_attr, doc_attr, attr_formats="sentences"):
	cap = []
	doc = []
	if attr_formats == "sentences":
		cap = item.get_attribute(cap_attr, Sentences).get_text().split()
		doc = item.get_attribute(doc_attr, Sentences).get_text().split()
	else:
		cap = item.get_attribute(in_attr).split()
		doc = item.get_attribute(doc_attr).split()
	cap = set(cap)
	doc = set(doc)
	return cap.issubset(doc)

def check_for_unknown_words(item, vocfile, in_attr, attr_format="sentences"):
	"""Returns true if at least one of the words in the item's attribute are unknown to the vocabulary."""
	if not hasattr(check_for_unknown_words, "voc"):
		check_for_unknown_words.voc = object_from_file(Vocabulary, vocfile)
	else: 
		text = []
		if attr_format == "sentences":
			text = item.get_attribute(in_attr, Sentences).get_text().split()
		else:
			text = item.get_attribute(in_attr).split()
		idxed = check_for_unknown_words.voc.index_words(text)
		u_idx = check_for_unknown_words.voc[UNKNOWN_WORD]
		
		return u_idx in idxed
