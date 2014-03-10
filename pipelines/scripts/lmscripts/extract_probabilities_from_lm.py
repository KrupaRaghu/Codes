"""
Usage:
    extract_probabilities_from_lm.py <vocfile> <lmfile> <outfile>

"""
from docopt import docopt
from src.corpus_utils import read_vocabulary
from src.functions import sentences_to_file
from src.lm_wrapper import LSVLM

def write_lm_probabilities_to_file(vocfile, lmfile, outfile):
    voc = read_vocabulary(vocfile)
    lm = LSVLM(lmfile, vocfile)

    probs = []

    for (idx, w) in enumerate(voc):
        p = lm.Prob([idx],1)
        probs.append([w, str(p)])
    
    sentences_to_file(outfile, probs)

if __name__ == "__main__":
    a = docopt(__doc__, version="0.1a")
    write_lm_probabilities_to_file(a["<vocfile>"], a["<lmfile>"], a["<outfile>"])
