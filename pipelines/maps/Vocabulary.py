from ..formats.Vocabulary import Vocabulary

def bow_to_vocabulary(bow):
    """Builds a vocabulary from a bag of words."""
    return Vocabulary(bow)

def preprocess_by_vocabulary(voc, text):
    """Filters the text, replacing all unknown words with an unknown word token."""
    out = []
    for sent in text.split("\n"):
        out_sent = []
        for word in sent.split():
            if word in voc:
                out_sent.append(word)
            else:
                out_sent.append(UNKNOWN_WORD)
        out.append(" ".join(out_send))
    return "\n".join(out)


def filter_by_vocabulary(voc, bow):
    """Returns the bag of words filtered to only include words from the given vocabulary."""
    return bow.filter_by_vocabulary(lambda x: x in voc)
