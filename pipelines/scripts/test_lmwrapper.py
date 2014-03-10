"""
Usage:
    test_lmwrapper.py --instantiate <lmfile> [<vocfile>] [-v]

"""
from docopt import docopt
from pprint import pprint
from ..formats.LSVLM import *

def main():
    a = docopt(__doc__, version="0.1a")
    
    if a["--instantiate"]:
        if a["<vocfile>"]:
            vf = a["<vocfile>"]
            if a["-v"]:
                print "Vocabulary file %s was given." % (vf)
            lm = LSVLM(lmfile=a["<lmfile>"], vocfile=vf)
        else:
            if a["-v"]:
                print "No vocabulary given."
            lm = LSVLM(lmfile=a["<lmfile>"])
        if a["-v"]:
            print "DIR(LM):"
            print dir(lm)
            print "Vocfile:", lm.vocfile
            print "LMfile:", lm.lmfile
            print "LM config:"
            pprint(lm.config)
        lm.start()
if __name__ == "__main__":
    main()
