from ..scripts.lm_library import *
from ..LM_WEIGHTS import *

def make_LDA_dDoc_lms(item, vocsize, dDoc_prob_attr, out_attr, name_end="_dDocZero", name_end_dDoc="_dDoc", name_end_Zero="_Zero", w_dDoc = W_DOC_DOCZEROLM, w_Zero = W_ZERO_DOCZEROLM):
    ldalm = makeDirectLM(name=item.get_attribute("original_name")+name_end_dDoc, probfile=item.get_attribute_path(dDoc_prob_attr))
    zerolm = makeZeroLM(item.get_attribute("original_name")+name_end_Zero, vocsize)
    item.set_attribute(out_attr, makeLinearLM(item.get_attribute("original_name")+name_end, [ldalm, zerolm], [w_dDoc, w_Zero]))

def make_LDA_all_lms(item, vocsize, dDoc_prob_attr, dMix_prob_attr, dImg_prob_attr, out_attr, name_end="_AllLDAZero", name_end_dDoc="_dDoc", name_end_dMix="_dMix", name_end_dImg="_dImg", name_end_Zero="_Zero", w_dDoc = W_DOC_LDAZEROLM, w_dImg=W_IMG_LDAZEROLM, w_dMix=W_MIX_LDAZEROLM, w_Zero = W_ZERO_LDAZEROLM):
    doclm = makeDirectLM(name=item.get_attribute("original_name")+name_end_dDoc, probfile=item.get_attribute_path(dDoc_prob_attr))
    imglm = makeDirectLM(name=item.get_attribute("original_name")+name_end_dImg, probfile=item.get_attribute_path(dImg_prob_attr))
    mixlm = makeDirectLM(name=item.get_attribute("original_name")+name_end_dMix, probfile=item.get_attribute_path(dMix_prob_attr))
    zerolm = makeZeroLM(item.get_attribute("original_name")+name_end_Zero, vocsize)
    item.set_attribute(out_attr, makeLinearLM(item.get_attribute("original_name")+name_end, [doclm, imglm, mixlm, zerolm], [w_dDoc, w_dImg, w_dMix, w_Zero]))
