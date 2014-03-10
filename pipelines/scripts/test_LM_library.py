"""
Usage:
    test_LM_library.py --zero <name> <vocsize>
    test_LM_library.py --direct <name> <probfile>
    test_LM_library.py --include <name> <inclmfile>
    test_LM_library.py --linear <name> (<lmfile> <weight>)...
    test_LM_library.py --loglinear <name> (<lmfile> <weight>)...
    test_LM_library.py --class <name> <emissionlmfile> <predictionlmfile> <classmapname> <classmapfile>
    test_LM_library.py --absdisc <name> <treename> <treefile> <M> <backofflmfile> <disc>
"""
from docopt import docopt
from LM_LIBRARY import *

def main():
    a = docopt(__doc__, version="0.1a")
    if a["--zero"]:
        #Test makeZeroLM
        print makeZeroLM(a["<name>"], int(a["<vocsize>"]))

    if a["--direct"]:
        from os.path import isfile 
        #Test makeDirectLM
        if not isfile(a["<probfile>"]):
            raise TypeError("Error: probfile is not an existing file!")
        print makeDirectLM(a["<name>"], a["<probfile>"])
    
    if a["--include"]:
        from os.path import isfile 
        #Test makeIncludeLM
        if not isfile(a["<inclmfile>"]):
            raise TypeError("Error: lmfile does not exist!")
        print makeIncludeLM(a["<name>"], a["<inclmfile>"])

    if a["--linear"] or a["--loglinear"]:
        #Test makeLinearLM
        #Test makeLogLinearLM
        sublms = []
        weights = []
        for lm,w_raw in zip(a["<lmfile>"], a["<weight>"]):
            with open(lm, "r") as f:
                sublms.append(f.read())
            weights.append(float(w_raw))
        if a["--linear"]:
            print makeLinearLM(a["<name>"], sublms, weights)
        if a["--loglinear"]:
            print makeLoglinearLM(a["<name>"], sublms, weights)

    if a["--class"]:
        #Test makeClassLM
        emissionlm = ""
        with open(a["<emissionlmfile>"], "r") as f:
            emissionlm = f.read()
        predictionlm = ""
        with open(a["<predictionlmfile>"], "r") as f:
            predictionlm = f.read()
        
        print makeClassLM(a["<name>"], emissionlm, predictionlm, a["<classmapname>"], a["<classmapfile>"])

#Test makeAbsDiscLM
    if a["--absdisc"]:
        bolm = ""
        with open(a["<backofflmfile>"], 'r') as f:
            bolm = f.read()
        print makeAbsDiscLM(a["<name>"], a["<treename>"], a["<treefile>"], int(a["<M>"]), bolm, float(a["<disc>"]))

if __name__ == "__main__":
    main()
