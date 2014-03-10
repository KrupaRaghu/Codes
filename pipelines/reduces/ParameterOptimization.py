from ..formats.Sentences import *
from ..formats.LSVLM import LSVLM


#Scripts for optimizing the parameters of LMs.

def read_param_file(paramfile):
    paramnames = []
    params = []
    with open(paramfile, "r") as f:
        paramnames = f.readline().split()
        for line in f.readlines():
            params.append(map(float, line.split()))
    return paramnames, params

def optimize_parameters(itemiterator, vocfile, paramfile, lm_attr, cap_attr, out_attr = None, visi_attr = None, cap_format="sentences", M=1, print_optimum = True, print_all = True):
    """paramnames: list of parameters names. paramlist: list of tuples containing parameter values."""
    
    #Read the parameter list
    paramnames, params = read_param_file(paramfile)    

    scores_total = [0.0]*len(params)
    perplexities_total = [0.0]*len(params)
    
    num_items = 0

    for item in itemiterator:
        num_items = num_items + 1
        #For each item, get the LM
        if cap_format == "sentences":
            caption = item.get_attribute(cap_attr, Sentences).get_text(one_per_line=False).split()
        elif cap_format == "text":
            caption = item.get_attribute(cap_attr).split()
        
        if not visi_attr is None:
            visiterms = item.get_attribute(visi_attr, list)
            caption = caption + visiterms
        lm = item.get_attribute(lm_attr, LSVLM)
        
        lm.set_vocabulary(vocfile)
        lm.set_lmfile(item.get_attribute_path(lm_attr))
        lm.start()
        scores = []
        perplexities = []

        for paramset in params:
            for paramname, paramval in zip(paramnames, paramset):
                lm.add_DynParam(paramname, paramval)
            lm.ReInit()
            
            scores.append(lm.AssessText(caption, M)[1])
            perplexities.append(lm.Perplexity(caption,M))

        if not out_attr is None:
            item.set_attribute(out_attr, scores)
   
        for i,score in enumerate(scores):
            scores_total[i] = scores_total[i] + score
            perplexities_total[i] = perplexities_total[i] + perplexity[i]

    if print_all:
        print paramnames, "Score"
        for paramset, (score, perp) in zip(params,zip(scores_total, perplexities)):
            print paramset, score

    if print_optimum:
        print "Best parameters BY SCORE (disregarding sentence lengths!):"
        best_score = min(zip(scores_total, params))
        print best_score[0], zip(paramnames, best_score[1])
        print "Best parameters BY PERPLEXITY:"
        best_perp = min(zip(perplexities_total, params))
        print "Total perplexity:",best_perp[0], "- Average perplexity:",best_perp[0]/num_items, "- Parameters:", zip(paramnames, best_perp[1])

