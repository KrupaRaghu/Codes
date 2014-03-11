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

def calc_perplexity(itemiterator, vocfile, paramfile, lm_attr, cap_attr, out_attr, visi_attr = None, cap_format="sentences", M=1):
    #Read the parameter list
    paramnames, params = read_param_file(paramfile)    

    perplexities_total = [0.0]*len(params)
    
    num_items = 0

    for item in itemiterator:
        num_items = num_items + 1
        if cap_format == "sentences":
            caption = item.get_attribute(cap_attr, Sentences).get_text(one_per_line=False).split()
        elif cap_format == "text":
            caption = item.get_attribute(cap_attr).split()
        
        if not visi_attr is None:
            visiterms = item.get_attribute(visi_attr, list)
            caption = caption + visiterms
        
	#For each item, get the LM
        lm = item.get_attribute(lm_attr, LSVLM)
        
        lm.set_vocabulary(vocfile)
        lm.set_lmfile(item.get_attribute_path(lm_attr))
        lm.start()
        perplexities = []

        for paramset in params:
            for paramname, paramval in zip(paramnames, paramset):
                lm.add_DynParam(paramname, paramval)
            lm.ReInit()
            
            perplexities.append(lm.Perplexity(caption,M))

      	item.set_attribute(out_attr, perplexities)
