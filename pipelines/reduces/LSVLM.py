from ..experiment_config import SENTENCE_START, SENTENCE_END, PHRASE_DELIMITER
from ..formats.Sentences import *

#Sensible choices for content_format are "text" and "sentences"
def make_LSVLM_Ngram_corpus(itemiterator, doc_attr=None, cap_attr=None, silent=False, data_only = False, print_IDs = False, content_format = "text", sent_start = SENTENCE_START, sent_end = SENTENCE_END, phrase_delim = PHRASE_DELIMITER):
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
        if content_format == "text":
            print u" ".join(item_out).encode("utf-8")
        elif content_format == "sentences":
            print u" ".join(map(lambda x: x.get_text(start_token = sent_start, end_token = sent_end, phrase_delimiter=phrase_delim, one_per_line = False), item_out)).encode("utf-8")
        if not doc_attr is None or not cap_attr is None:
            if print_IDs:
                outnames.append(item.ID)
            else:
                outnames.append(item.get_attribute("original_name", unicode))
    if not data_only:
        for item in outnames:
            print item

from ..scripts.lm_library import *
from ..LM_WEIGHTS import *

def make_LDA_dDoc_lms(itemiterator, vocsize, dDoc_prob_attr, out_attr, name_end="_dDocZero", name_end_dDoc="_dDoc", name_end_Zero="_Zero", w_dDoc = W_DOC_DOCZEROLM, w_Zero = W_ZERO_DOCZEROLM):
    for item in itemiterator:
	ldaname=u"".join((item.get_attribute("original_name", unicode)+name_end_dDoc.decode("utf-8")).split())
	zeroname=u"".join((item.get_attribute("original_name", unicode)+name_end_Zero.decode("utf-8")).split())
        ldalm = makeDirectLM(name=ldaname, probfile=item.get_attribute_path(dDoc_prob_attr))
        zerolm = makeZeroLM(zeroname, vocsize)
	lmname=u"".join((item.get_attribute("original_name", unicode)+name_end.decode("utf-8")).split())
        item.set_attribute(out_attr, makeLinearLM(lmname, [ldalm, zerolm], [w_dDoc, w_Zero]).encode("utf-8"))

def make_LDA_all_lms(itemiterator, vocsize, dDoc_prob_attr, dMix_prob_attr, dImg_prob_attr, out_attr, name_end="_AllLDAZero", name_end_dDoc="_dDoc", name_end_dMix="_dMix", name_end_dImg="_dImg", name_end_Zero="_Zero", w_dDoc = W_DOC_LDAZEROLM, w_dImg=W_IMG_LDAZEROLM, w_dMix=W_MIX_LDAZEROLM, w_Zero = W_ZERO_LDAZEROLM):
    for item in itemiterator:
	docname=u"".join((item.get_attribute("original_name", unicode)+name_end_dDoc.decode("utf-8")).split())
	mixname=u"".join((item.get_attribute("original_name", unicode)+name_end_dMix.decode("utf-8")).split())
	imgname=u"".join((item.get_attribute("original_name", unicode)+name_end_dImg.decode("utf-8")).split())
	zeroname=u"".join((item.get_attribute("original_name", unicode)+name_end_Zero.decode("utf-8")).split())
	lmname=u"".join((item.get_attribute("original_name", unicode)+name_end.decode("utf-8")).split())
        doclm = makeDirectLM(name=docname, probfile=item.get_attribute_path(dDoc_prob_attr))
        imglm = makeDirectLM(name=imgname, probfile=item.get_attribute_path(dImg_prob_attr))
        mixlm = makeDirectLM(name=mixname, probfile=item.get_attribute_path(dMix_prob_attr))
        zerolm = makeZeroLM(zeroname, vocsize)
        item.set_attribute(out_attr, makeLinearLM(lmname, [doclm, imglm, mixlm, zerolm], [w_dDoc, w_dImg, w_dMix, w_Zero]).encode("utf-8"))


def make_FMA_all_lms(itemiterator, treefile, vocsize, LDA_lm_attr, out_attr, name_end="_FMA", name_end_LDA="_LDA", name_end_dTri="_Tri", name_end_Uni="_Uni", beta=BETA_FMALM, w_doc=W_DOC_FMALM, w_img=W_IMG_FMALM,w_mix=W_MIX_FMALM,w_zero=W_ZERO_FMALM):
