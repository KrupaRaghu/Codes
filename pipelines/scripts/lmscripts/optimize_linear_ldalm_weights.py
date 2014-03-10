"""
Usage:
    optimize_linear_ldalm_weights.py -t <vocfile> <infolder> <cpus>
    optimize_linear_ldalm_weights.py -c <vocfile> <infolder> <captfolder> <captext> <cpus>
    optimize_linear_ldalm_weights.py <vocfile> <cpus> (<doclm> <mixlm> <imglm> <corpusfile> <outfile>)...
"""

from docopt import docopt
import subprocess
import re
from glob import glob
import sys, os
from src.functions import get_immediate_subdirectories, make_linear_lm, text_from_file, compute_perplexity
from pprint import pprint
from multiprocessing import Pool, cpu_count

#Need functions
def calc_perp_for_weights((ID, folder, dirs, vocfile, alpha,beta,gamma)):
    perp = {}
#    print "calculating perp for",(alpha,beta,gamma)
    for d in dirs:
        if not d:
            continue
        mixcorp = folder+d+"/"+d+".mix.dev_file"
        
        doclm = folder+d+"/resources/"+d+".doc.lm"
        mixlm = folder+d+"/resources/"+d+".mix.lm"
        imglm = folder+d+"/resources/"+d+".img.lm"
        
        tmpfile = folder+d+"/temporary/"+d+"_linear_weights_"+str(ID)+".tmp.lm"

        make_linear_lm(d+"_optimization_tmp", tmpfile, ["optimization_tmp_doc", "optimization_tmp_mix", "optimization_img_mix"], [doclm, mixlm, imglm], [alpha, beta, gamma])
        (pp, score) = compute_perplexity(vocfile, tmpfile, mixcorp)
        perp[d] = (pp, score)
    return ((alpha, beta, gamma), perp)

#def ldalm_grid_search(vocfile, lmfiles, corpusfiles):
def ldalm_grid_search_devfiles(vocfile, folder, cpus):
    """Uses one vocabulary and a list of language models and corresponding corpora for perplexity calculation."""
    if not folder.endswith("/"):
        folder = folder + "/"
    dirs = get_immediate_subdirectories(folder)
    
    for d in dirs:
        try:
            os.makedirs(folder+"/"+d+"/temporary/")
        except:
            pass

    jobs = []
    ID = 0
    for a in range(0,101,1):
        for b in range(0,101-a,1):
            alpha = float(a)/100.0
            beta = float(b)/100.0
            gamma = float(100-a-b)/100.0
            jobs.append((ID, folder, dirs, vocfile, alpha,beta,gamma))
            ID = ID + 1
#    print "Initialized jobs..."
    p = Pool(cpus)
    res = dict(p.map(calc_perp_for_weights, jobs))
#    pprint(res)
    totals = []
    for ((alpha,beta,gamma), d) in res.iteritems():
        tot = 0.0
        for (doc, (pp, score)) in d.iteritems():
            tot = tot+score 
        totals.append((tot, (alpha,beta,gamma)))

    pprint(sorted(totals))

    return res#, totals

if __name__ == "__main__":
    a = docopt(__doc__, version="0.1a")
    #compute_perplexity(a["<vocfile>"], a["<lmfile>"], a["<corpusfile>"])
    if a["-t"]:
        ldalm_grid_search_devfiles(a["<vocfile>"], a["<infolder>"], int(a["<cpus>"]))
    else:
        ldalm_grid_search_captions(a["<vocfile>"], a["<infolder>"], int(a["<cpus>"]), a["<captfolder>"], a["<captext>"])
#    ldalm_grid_search(a["<vocfile>"], a["<doclm>"], a["<mixlm>"], a["<imglm>"], a["<corpusfile>"], a["<outfile>"])
