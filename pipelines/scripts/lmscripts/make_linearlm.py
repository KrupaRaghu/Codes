"""
Usage:
    make_linearlm.py <name> <outfile> (<lmname> <lmfile> <weight>)...
"""
from docopt import docopt
from src.functions import sentences_to_file

def make_lm(name, outfile, lms, lmfiles, weights):
    #print "name", name
    #print "outfile", outfile
    #print "lms", lms
    #print "lmfiles", lmfiles
    #print "weights", weights
    out = [["# Parameters 1"]]
    out.append(["MainLM %s" % (name)])
    out.append(["# LMDefinition %d" % (2+len(lms)*2)])
    out.append(["Name\t%s" % (name)])
    out.append(["Type\tLinear"])
    
    lmlines = []

    for (i,lm) in enumerate(lms):
        out.append(["LM[%d]\t%s" % (i, lm)])
        out.append(["Weight[%d]\t%s" % (i, weights[i])])
        lmlines.append(["# LMDefinition 3"])
        lmlines.append(["Name\t%s" % (lm)])
        lmlines.append(["Type\tInclude"])
        lmlines.append(["File\t%s" % (lmfiles[i])])

    out = out + lmlines
    sentences_to_file(outfile, out)

if __name__ == "__main__":
    a = docopt(__doc__, version="0.1a")
    make_lm(a["<name>"], a["<outfile>"], a["<lmname>"], a["<lmfile>"], a["<weight>"])
