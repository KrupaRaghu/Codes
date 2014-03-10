from ..formats.BoW import BoW
from BoW import join_BoWs, compute_joint_BoW
from sys import stdout
from ..formats.LDA import *
from ..formats.Vocabulary import Vocabulary
from Vocabulary import *
from ..maps.Vocabulary import filter_by_vocabulary
from ..experiment_config import *
from itertools import tee
from data_manager.OSM import object_from_file

LDA_ATTRIBUTES=[CAP_NVA_WORDS, DOC_NVA_WORDS]

def inf_to_prob(itemiterator, modelfile, out_attr, inf_attr):
    model = object_from_file(pLDAModel, modelfile)
    for item in itemiterator:
        topics = item.get_attribute(inf_attr, pLDADocument).get_topic_distribution()
        assert len(topics) == model.get_num_topics(), "Number of topics in model %d does not match number of topics in infered data %d!" % (model.get_num_topics(), len(topics))
        out = []
        for word in model.t_dict.iterkeys():
            x = sum(map(lambda (a,b):a*b, zip(topics,model.get_word_dist_over_topics(word))))
            if x > 0.0:
                out.append(word+u"\t%s" % (str(x)))
        item.set_attribute(out_attr, u"# Probabilities %d\n" % (len(out)) + u"\n".join(out))

def make_inference_corpora_dDoc(itemiterator, out_attr, doc_attr = None, cap_attr = None):
    for item in itemiterator:
        bow = BoW([])
        if not doc_attr is None:
            bow.update(BoW(item.get_attribute(doc_attr).split()))
        if not cap_attr is None:
            bow.update(BoW(item.get_attribute(cap_attr).split()))
        item.set_attribute(out_attr, pLDACorpus([bow]))
    
def make_inference_corpora_dImg(itemiterator, out_attr, img_attr):
    for item in itemiterator:
        item.set_attribute(out_attr, pLDACorpus([BoW(item.get_attribute(img_attr, list))])) 

def make_inference_corpora_dMix(itemiterator, out_attr, img_attr, doc_attr = None, cap_attr = None):
    if doc_attr is None and cap_attr is None:
        print "Error: Document or caption attribute must be set!"
        return
    for item in itemiterator:
        bow = BoW(item.get_attribute(img_attr, list))
        if not doc_attr is None:
            bow.update(BoW(item.get_attribute(doc_attr).split()))
        if not cap_attr is None:
            bow.update(BoW(item.get_attribute(cap_attr).split()))
        item.set_attribute(out_attr, pLDACorpus([bow]))

def make_pLDA_corpus_from_attr(itemiterator, attr, silent = False):
    voc_it, bow_it = tee(itemiterator)
    voc = build_filter_vocabulary(voc_it, [attr], 5)
    entries = []
    for item in bow_it:
        item_bow = BoW(item.get_attribute(attr).split())
        entries.append(item_bow.filter_by_vocabulary(voc))
    corpus = pLDACorpus(entries)
    if not silent:
        stdout.write(corpus.encode())
    return corpus

def pLDA_corpus_dDoc(itemiterator, doc_attr = None, cap_attr = None, print_list = False):
    attrs = []
    if doc_attr is not None:
        attrs.append(doc_attr)
    if cap_attr is not None:
        attrs.append(cap_attr)
    return make_pLDA_corpus(itemiterator, attrs, print_list = print_list)

def pLDA_filtervoc(itemiterator, doc_attr = None, cap_attr = None, threshold = 5, silent = False, print_list = False):
    attrs = []
    if not doc_attr is None:
        attrs.append(doc_attr)
    if not cap_attr is None:
        attrs.append(cap_attr)
    if attrs:
        voc = build_filter_vocabulary(itemiterator, attrs, threshold)
    else:
        voc = Vocabulary([])
    if not silent:
        print voc
    return voc

def pLDA_corpus_dImg(itemiterator, visi_attr):
    return make_pLDA_corpus(itemiterator, [visi_attr], print_list = print_list)

def pLDA_corpus_dMix(itemiterator, visi_attr, doc_attr = None, cap_attr = None, print_list = False):
    attrs = [visi_attr]
    if doc_attr is not None:
        attrs.append(doc_attr)
    if cap_attr is not None:
        attrs.append(cap_attr)
    return make_pLDA_corpus(itemiterator, [visi_attr] + LDA_ATTRIBUTES, print_list = print_list)

def make_pLDA_corpus(itemiterator, attrs = LDA_ATTRIBUTES, threshold = 5, silent = False, print_list = False):
    """Builds a pLDA corpus from all given attributes of all given items and prints its text representation to stdout (unless silent = True)."""
    voc_it, bow_it = tee(itemiterator)
    voc = build_filter_vocabulary(voc_it, attrs, threshold)
    entries = []
    datalist = []
    for item in bow_it:
        item_bow = BoW([])
        datalist.append(item.get_attribute("original_name"))
        for attr in attrs:
            item_bow.update(BoW(item.get_attribute(attr).split()))
        entries.append(item_bow.filter_by_vocabulary(voc))
    corpus = pLDACorpus(entries)
    if not silent:
        stdout.write(corpus.encode())
    if not silent and print_list:
        for entry in datalist:
            stdout.write(entry)
    return corpus, datalist
    
