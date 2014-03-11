from ..formats.LSVLM import LSVLM
from ..LM_WEIGHTS import *

from itertools import chain

#A set of functions that allow for the generation of various language models.

def makeLinearLM(name, sublms, weights):
    out = [u"# Parameters 1"]
    out.append(u"MainLM %s" % (name))
    out.append(u"# LMDefinition %d" % (2+len(sublms)*2))
    out.append(u"Name\t%s" % (name))
    out.append(u"Type\tLinear")
    for (i,lm) in enumerate(sublms):
        lmname, config, voc, lmfile = LSVLM.parse_lm_lines(lm.split("\n"))
        out.append(u"LM[%d]\t%s" % (i, lmname))
        out.append(u"Weight[%d]\t%s" % (i, weights[i]))

    for lm in sublms:
        for line in lm.split("\n"):
            if line.startswith(u"# Parameters 1") or line.startswith(u"MainLM"):
                continue
            elif line:
                out.append(line)
        
    return u"\n".join(out)

def makeLoglinearLM(name, sublms, weights, noNorm=False):
    out = [u"# Parameters 1"]
    out.append(u"MainLM %s" % (name))
    out.append(u"# LMDefinition %d" % (3+len(sublms)*2))
    out.append(u"Name\t%s" % (name))
    out.append(u"Type\tLogLinearLM")
    
    for (i,lm) in enumerate(sublms):
        lmname, config, voc, lmfile = LSVLM.parse_lm_lines(lm.split("\n"))
        out.append(u"LM[%d]\t%s" % (i, lmname))
        out.append(u"Weight[%d]\t%s" % (i, weights[i]))

    if noNorm:
        out.append(u"NoNorm\t1")
    
    for lm in sublms:
        for line in lm.split("\n"):
            if line.startswith(u"# Parameters 1") or line.startswith(u"MainLM"):
                continue
            elif line:
                out.append(line)
        
    return "\n".join(out)

def makeClassLM(name, emissionlm, predictionlm, classmapname, classmapfile):
    e_name, e_cfg, e_voc, e_file = LSVLM.parse_lm_lines(emissionlm.split("\n"))
    p_name, p_cfg, p_voc, p_file = LSVLM.parse_lm_lines(predictionlm.split("\n"))
    out = [u"# Parameters 1"]
    out.append(u"MainLM %s" % (name))
    out.append(u"# LMDefinition 5")
    out.append(u"Name\t%s" % (name))
    out.append(u"Type\tClassLM")
    
    out.append(u"EmissionLM\t%s" % (e_name))
    out.append(u"ClassPredictLM\t%s" % (p_name))
    out.append(u"Word2ClassMap\t%s" % (classmapname))
    
    out.append(u"# ClassMapDefinition 2")
    out.append(u"%s\tClassMap" % (classmapname))
    out.append(u"File\t%s" % (classmapfile))
    for line in chain(emissionlm.split("\n"), predictionlm.split("\n")):
        if line.startswith(u"# Parameters 1") or line.startswith("MainLM"):
            continue
        elif line:
            out.append(line)
    return u"\n".join(out)

def makeIncludeLM(name, includefile):
    out = [u"# Parameters 1"]
    out.append(u"MainLM %s" % (name))
    out.append(u"# LMDefinition 3")
    out.append(u"Name\t%s" % (name))
    out.append(u"Type\tIncludeLM")
    from os.path import abspath
    out.append(u"File\t%s" % (abspath(includefile)))

    return u"\n".join(out)

def makeAbsDiscLM(*args, **kwargs):
    return makeCntMGramLM(*args, **kwargs)
    
def makeCntMGramLM(name, treename, treefile, M, backofflm, disc):
    bo_name, bo_cfg, bo_voc, bo_file = LSVLM.parse_lm_lines(backofflm.split("\n"))
    
    #Remove all definitions of the tree from the backofflm
    inTree = False
    removeIdxes = []
    for i,line in enumerate(backofflm.split("\n")):
        if line.startswith(u"# Parameters 1") or line.startswith(u"MainLM"):
            removeIdxes.append(i)
        if line.startswith(u"# TreeDefinition 2"):
            inTree = True
        elif line.startswith(u"# "):
            inTree = False
        if inTree:
            if line.split()[0] == u"Name" and line.split()[1] == treename:
                removeIdxes.append(i)
                removeIdxes.append(i-1)
                removeIdxes.append(i+1)
    
    bolm = [line for i,line in enumerate(backofflm.split("\n")) if i not in removeIdxes and line]

    out = [u"# Parameters 1"]
    out.append(u"MainLM %s" % (name))
    out.append(u"# LMDefinition 6") 
    
    out.append(u"Name\t%s" % (name))
    out.append(u"Type\tCntMGramLM")
    out.append(u"Tree\t%s" % (treename))
    out.append(u"M\t%s" % (str(M)))
    out.append(u"BackOffLM\t%s" % (bo_name))
    out.append(u"Disc\t%s" % (str(disc)))
   
    out.extend(bolm)
    
    out.append(u"# TreeDefinition 2")
    out.append(u"Name\t%s" % (treename))
    out.append(u"File\t%s" % (treefile))

    return u"\n".join(out)

def makeZeroLM(name, vocsize):
    out = [u"# Parameters 1"]
    out.append(u"MainLM %s" % (name))
    out.append(u"# LMDefinition 3") 
    
    out.append(u"Name\t%s" % (name))
    out.append(u"Type\tZeroLM")
    out.append(u"VocSize\t%s" % (str(vocsize)))
    
    return u"\n".join(out)

def makeDirectLM(name, probfile):
    out = [u"# Parameters 1"]
    out.append(u"MainLM %s" % (name))
    out.append(u"# LMDefinition 3") 
    
    out.append(u"Name\t%s" % (name))
    out.append(u"Type\tDirectLM")
    out.append(u"ProbabilityFile\t%s" % (probfile))
    
    return u"\n".join(out)

def makeFengLapataFMALM(lmname, treename, treefile, dDoc_probfile, dMix_probfile, dImg_probfile, suf_tri = "_Tri", suf_uni="_Uni", suf_dDoc="_dDoc", suf_dMix="_dMix", suf_dImg="_dImg", w_dDoc=W_DOC_FMALM, w_dMix=W_MIX_FMALM, w_Img=W_IMG_FMALM, w_Zero=W_ZERO_FMALM, beta=BETA_FMALM):
	
	
	pass
