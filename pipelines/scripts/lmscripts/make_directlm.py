"""
Usage:
    make_directlm.py <probfile> <name> <outfile>
"""
from docopt import docopt
from src.functions import sentences_to_file

def make_lm(probfile, name, outfile):
    out = [["# Parameters 1"]]
    out.append(["MainLM %s" % (name)])
    out.append(["# LMDefinition 3"])
    out.append(["Name   %s" % (name)])
    out.append(["Type   DirectLM"])
    out.append(["ProbabilityFile    %s" % (probfile)])

    sentences_to_file(outfile, out)


if __name__ == "__main__":
    a = docopt(__doc__, version="0.1a")
    make_lm(a["<probfile>"], a["<name>"], a["<outfile>"])
