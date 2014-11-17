from pipelines.reduces.BoW import compute_joint_BoW
from pipelines.formats.Vocabulary1 import Vocabulary
from pipelines.exp_config import *
FILTER_VOC_ATTRIBUTES=[DOC_NVA_WORDS, CAP_NVA_WORDS]
FULL_VOC_ATTRIBUTES=[DOC_NVA_WORDS, CAP_NVA_WORDS, DOC_TOKEN, CAP_TOKEN]

def build_vocabulary_items(itemiterator, doc_attr = None, cap_attr = None, content_format="text", K = 0, sent_start = SENTENCE_START, sent_end = SENTENCE_END, unknown_word = UNKNOWN_WORD, silent = False):
    attrs = []
    if not doc_attr is None:
        attrs.append(doc_attr)
    if not cap_attr is None:
        attrs.append(cap_attr)
    addwords = [make_kmeans_visiterm(x) for x in xrange(int(K))]
    if not sent_start is None:
        addwords.append(sent_start)
    if not sent_end is None:
        addwords.append(sent_end)
    if not unknown_word is None:
        addwords.append(unknown_word)
    voc = build_vocabulary(itemiterator, attrs, content_format, addwords)
    if not silent:
        print voc
    return voc

def build_filter_vocabulary(itemiterator, attributes, threshold = 4):
    bow = compute_joint_BoW(itemiterator, attributes)
    bow = bow << threshold
    words = bow.iterkeys()
    return Vocabulary(sorted(list(words)))

def build_vocabulary_full(itemiterator, k):
    return build_vocabulary(itemiterator, FULL_VOC_ATTRIBUTES, [make_kmeans_visiterm(x) for x in xrange(k)]+[SENT_START, SENT_END, UNKNOWN_WORD])

def build_vocabulary(itemiterator, attributes, content_format = "text", additional_words = []):
    bow = compute_joint_BoW(itemiterator, attributes, content_format)
    words = list(set(list(bow.iterkeys()) + additional_words))
    return Vocabulary(sorted(words))
                                                                                            
