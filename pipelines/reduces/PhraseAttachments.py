from ..formats.Sentences import *
from ..formats.PhraseAttachments import *
from json import dumps

def extract_adjacent_phrases(sentences):
    for sentence in sentences:
        if len(sentence) > 1:
            for p in zip(sentence[0:-1], sentence[1:]):
                yield p

def estimate_phrase_attachments(itemiterator, doc_attr = None, cap_attr = None, silent = False):
    counts = {}
    for item in itemiterator:
        if not doc_attr is None:
            for x in extract_adjacent_phrases(item.get_attribute(doc_attr, Sentences)):
                lp = x[0]
                rp = x[1]
                for wl in lp:
                    for wr in rp:
                        counts[(wl,wr)] = counts.get((wl,wr),0)+1
        if not cap_attr is None:
            for (lp,rp) in extract_adjacent_phrases(item.get_attribute(cap_attr, Sentences)):
                for wl in lp:
                    for wr in rp:
                        counts[(wl,wr)] = counts.get((wl,wr),0)+1
    print dumps(PhraseAttachmentModel._convert_tuple_counts(counts))
    #pAmodel = PhraseAttachmentModel(counts)
    #if not silent:
    #    print pAmodel.encode()
    #return pAmodel
