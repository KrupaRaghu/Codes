from ..formats.Vocabulary import *
from ..formats.BoW import *
from ..formats.Sentences import *
from data_manager.OSM import *
from ..experiment_config import *

def process_unknown_words(itemiterator, vocabfile, in_attr, out_attr, content_format="text"):
    voc = object_from_file(Vocabulary, vocabfile)
    for item in itemiterator:
        if content_format == "text":
            text = item.get_attribute(in_attr).decode("utf-8")
            out = []
            sents = text.split("\n")
            for sent in sents:
                out_loc = []
                for w in sent.split():
                    if w in voc:
                        out_loc.append(w)
                    else:
                        out_loc.append(UNKNOWN_WORD)
                out.append(" ".join(out_loc))
            item.set_attribute(out_attr, "\n".join(out))
        elif content_format == "sentences":
            sentences = item.get_attribute(in_attr, Sentences)
            for sent in sentences:
                for phrase in sent:
                    for i,word in enumerate(phrase):
                        if word not in voc:
                            phrase[i] = UNKNOWN_WORD
            item.set_attribute(out_attr)
        elif content_format == "BoW" or content_format == "bow":
            bow = item.get_attribute(in_attr, BoW)
            for word, count in bow.iteritems():
                if word not in voc:
                    del bow[word]
                    bow[UNKNOWN_WORD] = bow.get(UNKNOWN_WORD, 0) + count
            item.set_attribute(out_attr, bow)

