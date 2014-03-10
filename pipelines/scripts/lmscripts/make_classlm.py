"""
Usage:
    make_classlm.py <name> <outfile> <classmap> <emitlm> <predictlm>
"""
from docopt import docopt
from src.functions import sentences_to_file

def make_class_lm(name, outfile, classmap, emitlm, predictlm):
    out = [["# Parameters 1"]]
    out.append(["MainLM %s" % (name)])
    out.append(["# LMDefinition 5"])
    out.append(["Name\t%s" % (name)])
    out.append(["Type\tClassLM"])
    out.append(["EmissionLM\t%sEmission" % (name)])
    out.append(["ClassPredictLM\t%sPrediction" % (name)])
    out.append(["Word2ClassMap\t%sClassMap" % (name)])

    #Add ClassMapDefinition
    out.append(["# ClassMapDefinition 2"])
    out.append(["Name\t%sClassMap" % (name)])
    out.append([classmap])

    #Add EmissionLM
    out.append(["# LMDefinition 3"])
    out.append(["Name\t%sEmission" % (name)])
    out.append(["Type\tInclude"])
    out.append(["File\t%s" % (emitlm)])
    
    #Add PredictionLM
    out.append(["# LMDefinition 3"])
    out.append(["Name\t%sPrediction" % (name)])
    out.append(["Type\tInclude"])
    out.append(["File\t%s" % (predictlm)])

    sentences_to_file(outfile, out)

if __name__ == "__main__":
    a = docopt(__doc__, version="0.1a")
    make_lm(a["<name>"], a["<outfile>"], a["<lmname>"], a["<lmfile>"], a["<weight>"])
