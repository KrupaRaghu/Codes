from ..formats.Sentences import Sentences
from ..formats.StanfordDependencies import *

OPENNLP_SENTENCE_DETECTOR="sent-detect"

def phrases_from_StanfordDependencies_item(item, in_attr="stanford", out_attr="stanford_sentences"):
    deps = item.get_attribute(in_attr, StanfordDependencies)
    item.set_attribute(out_attr, phrased_sentences_from_StanfordDependencies(deps))

def phrased_sentences_from_StanfordDependencies(dependencies):
    phrases = make_phrases(dependencies)
    sents = []
    for P in phrases:
        phrases = []
        for w in P:
            phrase = []
            for x in sorted(w):
                phrase.append(x[1])
            phrases.append(phrase)
        sents.append(phrases)
    return Sentences(sents)

def make_phrases(DEPS):
    all_phrases = []
    for D in DEPS:
        #Get all phrases - this list can contain duplicates!
        phrases_tmp = map(lambda x: make_phrase(x,D), D)
        phrases = []
        #Join the phrases together (as make_phrase can yield lists of phrases)
        for p in phrases_tmp:
            for phrase in p:
                if len(phrase) > 0:
                    phrases.append(list(set(phrase)))
        phrases.sort(key=lambda x:len(x), reverse=True)
        not_taken = set([])
        for p in phrases:
            for w in p:
                not_taken.add(w[0])
        selected = []
        #Choose the longest phrases. Single words fill the gaps.

        for P in phrases:
            available = True
            for p in P:
                if len(p) <= 0:
                    continue
                if p[0] not in not_taken:
                    available = False
            if available:
                selected.append(P)
                for p in P:
                    not_taken.remove(p[0])
        all_phrases.append(sorted(selected))
    return all_phrases

def add(phrase, cur_dep, all_deps, ALLOWED_TAGS = ALLOWED_TAGS_CONT):
    if len(all_deps) < 3:
        pass
    #Do not add prepositional objects that do not follow right after
    #This is done to limit the size of certain phrases, as pobjs that
    #do not follow right after usually contain a few words.
    if cur_dep[0] == "pobj":
        if abs(cur_dep[1]- cur_dep[2]) > 1:
            return
    cand = all_deps[cur_dep[2]-1]
#    print "POSSIBLY ADDING", cand
    try:
        if cand[1] in ALLOWED_TAGS and cand[0] not in phrase:
            phrase.append(cand[0])
            for dep in cand[2]:
                add(phrase, dep, all_deps, ALLOWED_TAGS)
    except RuntimeError as E:
        print "tried to make phrase in ADD for", cand
def make_phrase(D, all_deps):

    deps = D[2]
    tag = D[1]
    word = D[0][1]
    i = D[0][0]
    phrase = []
    phrase = [D[0]]
    try:
        if D[1] not in VERBS:
            for dep in deps:
                add(phrase, dep, all_deps)
        else:
            #Verbs may only be followed by other verbs.
            for dep in deps:
                add(phrase, dep, all_deps, VERBS)
    except RuntimeError as e:
        print "tried to make phrase from", D
        print "with all_deps"
        pprint(all_deps)
    phrase = sorted(phrase)
    #Split phrases with "gaps" in them into multiple phrases.
    first = 0
    cur = 0
    last = phrase[0][0]
    for w in phrase:
        if last + 1 < w[0]:
            yield phrase[first:cur]
            first = cur
        last = w[0]
        cur = cur + 1
    yield phrase[first:]

def tokens_to_Sentences_item(item, in_attr="text", out_attr="sentences"):
    text = item.get_attribute(in_attr, Sentences)
    item.set_attribute(out_attr,Sentences.from_str(text))

def raw_sentences_to_Sentences(text):
    return Sentences.from_str(text)

def add_sentence_tokens_to_sentence(sent, allow_repeats = False):
    if not sent:
        pass
    if allow_repeats or sentence[0] != SENTENCE_START_TOKEN:
        sent.insert(0, SENTENCE_START_TOKEN)
    if allow_repeats or sentence[-1] != SENTENCE_END_TOKEN:
        sent.append(SENTENCE_END_TOKEN)
