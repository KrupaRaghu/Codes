from ..experiment_config import SENTENCE_START, SENTENCE_END, PHRASE_DELIMITER
from ..formats.Sentences import *

#Sensible choices for content_format are "text" and "sentences"
def make_LSVLM_Ngram_corpus(itemiterator, doc_attr=None, cap_attr=None, silent=False, data_only = False, print_IDs = False, content_format = "text", sent_start = SENTENCE_START, sent_end = SENTENCE_END, phrase_delim = PHRASE_DELIMITER):
    out = []
    outnames = []
    for item in itemiterator:
        item_out = []
        if not doc_attr is None:
            if content_format == "text":
                item_out.append(item.get_attribute(doc_attr))
            elif content_format == "sentences":
                item_out.append(item.get_attribute(doc_attr, Sentences))
        if not cap_attr is None:
            if content_format == "text":
                item_out.append(item.get_attribute(cap_attr))
            elif content_format == "sentences":
                item_out.append(item.get_attribute(cap_attr, Sentences))
        out.append(item_out)
        if not doc_attr is None or not cap_attr is None:
            if print_IDs:
                outnames.append(item.ID)
            else:
                outnames.append(item.get_attribute("original_name"))
    for item in out:
        if content_format == "text":
            print u" ".join(item).encode("utf-8")
        elif content_format == "sentences":
            print u" ".join(map(lambda x: x.get_text(start_token = sent_start, end_token = sent_end, phrase_delimiter=phrase_delim, one_per_line = False), item)).encode("utf-8")
    if not data_only:
        for item in outnames:
            print item
