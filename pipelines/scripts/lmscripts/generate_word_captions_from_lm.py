"""
Usage:
    generate_word_captions_from_lm.py <lmfile> <vocfile> <lengthmodel> <conditional_model> <outfolder> <documentvocabulary>
"""
from docopt import docopt
from src.word_caption_generator import WordCaptionGenerator
from src.definitions import BEAM_SIZE
from src.functions import read_file
from src.corpus_utils import read_vocabulary

def generate_word_captions(lmfile, vocfile, lengthmodel, condmodel, document, outfolder):
    doc_words = read_vocabulary(document)
    gen = WordCaptionGenerator(BEAM_SIZE, vocfile, lengthmodel, lmfile, condmodel)
    print "Generator initialized."
#    print gen.next_nodes
#    print "Document words:",doc_words
    gen.search(doc_words) 

if __name__ == "__main__":
    a = docopt(__doc__, version="0.1a")
    generate_word_captions(a["<lmfile>"], a["<vocfile>"], a["<lengthmodel>"], a["<conditional_model>"], a["<documentvocabulary>"], a["<outfolder>"])
