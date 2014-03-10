"""
Usage:
    make_trigramlm.py <name> <counttree> <outfile>
"""
from docopt import docopt
from src.functions import sentences_to_file

def make_lm(name, outfile, ctree):
    out = [["# Parameters 1"]]
    out.append(["MainLM Trigram%s" % (name)])

    out.append(["# LMDefinition 7"])
    out.append(["Name\tTrigram%s" % (name)])
    out.append(["Type\tCntMGramLM"])
    out.append(["Tree\tTrigramTree"])
    out.append(["M\t3"])
    out.append(["BackOffLM\tBigram%s" % (name)])
    out.append(["Disc\t0.0"])
    out.append(["SentBeg\t<UNKNOWN_WORD>"])
    
    out.append(["# LMDefinition 7"])
    out.append(["Name\tBigram%s" % (name)])
    out.append(["Type\tCntMGramLM"])
    out.append(["Tree\tTrigramTree"])
    out.append(["M\t2"])
    out.append(["BackOffLM\tUnigram%s" % (name)])
    out.append(["Disc\t0.0"])
    out.append(["SentBeg\t<UNKNOWN_WORD>"])
   
    out.append(["# LMDefinition 7"])
    out.append(["Name\tUnigram%s" % (name)])
    out.append(["Type\tCntMGramLM"])
    out.append(["Tree\tTrigramTree"])
    out.append(["M\t1"])
    out.append(["BackOffLM\tZeroGram%s" % (name)])
    out.append(["Disc\t0.0"])
    out.append(["SentBeg\t<UNKNOWN_WORD>"])

    out.append(["# LMDefinition 2"])
    out.append(["Name\tZeroGram%s"%(name)])
    out.append(["Type\tZero"])
    
    out.append(["# TreeDefinition 2"])
    out.append(["Name\tTrigramTree"])
    out.append(["File\t%s" % (ctree)])

    sentences_to_file(outfile, out)

if __name__ == "__main__":
    a = docopt(__doc__, version="0.1a")
    make_lm(a["<name>"], a["<outfile>"], a["<counttree>"])
