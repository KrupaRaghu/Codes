from ..formats.WTL import *

#PoS tagging with TreeTagger

#The command to be called in order to call TreeTagger
#TREETAGGER_COMMAND = "treetagger"
TREETAGGER_COMMAND = "/home/andrea/studium/BA/treetagger/cmd/tree-tagger-english"

#POSTPROCESSING

def treetagger_to_wtl_item(item, in_attr="tagged_raw", out_attr="tagged"):
    cont = item.get_attribute(in_attr).decode("latin")
    wtl = treetagger_output_to_wtl(cont)
    item.set_attribute(out_attr, wtl)

def filter_nva_item(item, in_attr="tagged", out_attr="nva"):
    wtl = item.get_attribute(in_attr, WTL)
    item.set_attribute(out_attr, nva(wtl))

def words_item(item, in_attr="tagged", out_attr="nva"):
    wtl = item.get_attribute(in_attr, WTL)
    item.set_attribute(out_attr, words(wtl))

def lemmas_item(item, in_attr="tagged", out_attr="nva"):
    wtl = item.get_attribute(in_attr, WTL)
    item.set_attribute(out_attr, lemmas(wtl))



def treetagger_output_to_wtl(text):
    """Transforms some text, which is assumed to be output from the TreeTagger script, into a WTL."""
    return WTL.from_text(text)

def nva(wtl):
    """Filters and keeps only those tags which fall into the noun, verb, or adjective category. Returns string. Intended for use with apply_pyfunc or in pipelines."""
    return list(filter_nva(wtl))

def words(wtl):
    """Extracts the words from all TreeTagger word-tag-lemma tuples. Intended for use with apply_pyfunc."""
    return " ".join(extract_words(wtl))

def lemmas(wtl):
    """Extracts the lemmas from all TreeTagger word-tag-lemma tuples. Intended for use with apply_pyfunc."""
    return " ".join(extract_lemmas(wtl))

#The TreeTagger PoS tags that count as nouns, verbs, and adjectives.
NVA_TAGS = ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NP', 'NPS', 'MD', 'VB', 'VBN', 'VBG', 'VBZ', 'VBP']
#Additionally with the SENT tag
NVA_SENT_TAGS = ['SENT'] + NVA_TAGS

def filter_nva(wtl):
    """
    Returns only the nouns, verbs, and adjectives from wtl. Returns list of words.
    """
    return keep_by_tags(NVA_TAGS, wtl)

def remove_by_tags(tags, wtl):
    """
    Filters the word-tag-lemma list wtl to include only tuples tagged NOT with one of the tag set tags.
    """
    for l in wtl:
        if not l:
            continue
        if l[1] in tags:
            continue
        yield l    

def keep_by_tags(tags, wtl):
    """
    Filters the word-tag list wtl to include only tuples tagged with one of the tag set tags.
    """
    for l in wtl:
        if not l:
            continue
        if len(l) < 3:
            continue
        if l[1] not in tags:
            continue
        yield l

def extract_lemmas(wtl):
    """
    Returns the lemmas from the list of tuples wtl. Returns list of words.
    """
    for l in wtl:
        if not l:
            continue
        yield (l[2] if l[2] != "<unknown>" else l[0])

def extract_words(wtl):
    """
    Returns the words from the list of tuples wtl. Returns list of words.
    """
    for l in wtl:
        if not l:
            continue
        yield l[0]
