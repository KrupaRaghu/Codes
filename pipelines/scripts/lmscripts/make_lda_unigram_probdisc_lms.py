"""
Usage:
    make_lda_unigram_fillup_lms.py [--standarduni <unigramfile>|--selecteduni <unigramext>] <folder> <ldaext> <outext>
"""
from docopt import docopt
from glob import glob
import sys, os
import shutil
import subprocess
from src.functions import get_immediate_subdirectories, make_probdisc_lm
from src.definitions import LDA_UNIGRAM_DISC_ALPHA, LDA_UNIGRAM_DISC_BETA, LDA_UNIGRAM_DISC_GAMMA, LDA_UNIGRAM_DISC_OFFSET

def process_subfolders_standardunigram(folder, ldaext, unigram, outext):
    if not folder.endswith("/"):
        folder = folder + "/"
    
    dirs = get_immediate_subdirectories(folder)
    for d in dirs:
        print "Processing folder",d
        fname = d.split("/")[-1]
        ldafile = folder+d+"/resources/"+fname+ldaext
        outname = d.split("/")[-1] + "."+outext
        outfile = folder+d+"/resources/"+outname+".lm"
#        print "fname",fname,"ldafile",ldafile,"outname",outname,"outfile",outfile
        make_probdisc_lm(fname+outext.title(), outfile, ldafile, unigram, LDA_UNIGRAM_DISC_OFFSET, LDA_UNIGRAM_DISC_ALPHA, LDA_UNIGRAM_DISC_BETA, LDA_UNIGRAM_DISC_GAMMA)
        #make_lin_lm(outname, outfile, d.split("/")[-1]+"-LDA", lmfile, "0.8", "UnigramGeneral", unigram, "0.2")

if __name__ == "__main__":
    a = docopt(__doc__, version="0.1a")
    ext = a["<outext>"]
    ldaext = a["<ldaext>"]
    if not ldaext.startswith("."):
        ldaext = "."+ldaext
    
    if a["--standarduni"]:
        process_subfolders_standardunigram(a["<folder>"], ldaext, a["<unigramfile>"], ext)
    else:
        process_subfolders_selectedunigram(a["<folder>"], ldaext, a["<unigramext>"], ext)
