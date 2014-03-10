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


from ..scripts.lm_library import *
from ..LM_WEIGHTS import *

def make_LDA_dDoc_lms(itemiterator, vocsize, dDoc_prob_attr, out_attr, name_end="_dDocZero", name_end_dDoc="_dDoc", name_end_Zero="_Zero", w_dDoc = W_DOC_DOCZEROLM, w_Zero = W_ZERO_DOCZEROLM):
    for item in itemiterator:
        ldalm = makeDirectLM(name=item.get_attribute("original_name")+name_end_dDoc, probfile=item.get_attribute_path(dDoc_prob_attr))
        zerolm = makeZeroLM(item.get_attribute("original_name")+name_end_Zero, vocsize)
        item.set_attribute(out_attr, makeLinearLM(item.get_attribute("original_name")+name_end, [ldalm, zerolm], [w_dDoc, w_Zero]))

def make_LDA_all_lms(itemiterator, vocsize, dDoc_prob_attr, dMix_prob_attr, dImg_prob_attr, out_attr, name_end="_AllLDAZero", name_end_dDoc="_dDoc", name_end_dMix="_dMix", name_end_dImg="_dImg", name_end_Zero="_Zero", w_dDoc = W_DOC_LDAZEROLM, w_dImg=W_IMG_LDAZEROLM, w_dMix=W_MIX_LDAZEROLM, w_Zero = W_ZERO_LDAZEROLM):
    for item in itemiterator:
        doclm = makeDirectLM(name=item.get_attribute("original_name")+name_end_dDoc, probfile=item.get_attribute_path(dDoc_prob_attr))
        imglm = makeDirectLM(name=item.get_attribute("original_name")+name_end_dImg, probfile=item.get_attribute_path(dImg_prob_attr))
        mixlm = makeDirectLM(name=item.get_attribute("original_name")+name_end_dMix, probfile=item.get_attribute_path(dMix_prob_attr))
        zerolm = makeZeroLM(item.get_attribute("original_name")+name_end_Zero, vocsize)
        item.set_attribute(out_attr, makeLinearLM(item.get_attribute("original_name")+name_end, [doclm, imglm, mixlm, zerolm], [w_dDoc, w_dImg, w_dMix, w_Zero]))
