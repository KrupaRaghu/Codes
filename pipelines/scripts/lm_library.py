from ..formats.LSVLM import LSVLM

from itertools import chain

#A set of functions that allow for the generation of various language models.

def makeLinearLM(name, sublms, weights):
    out = ["# Parameters 1"]
    out.append("MainLM %s" % (name))
    out.append("# LMDefinition %d" % (2+len(sublms)*2))
    out.append("Name\t%s" % (name))
    out.append("Type\tLinear")
    for (i,lm) in enumerate(sublms):
        lmname, config, voc, lmfile = LSVLM.parse_lm_lines(lm.split("\n"))
        out.append("LM[%d]\t%s" % (i, lmname))
        out.append("Weight[%d]\t%s" % (i, weights[i]))

    for lm in sublms:
        for line in lm.split("\n"):
            if line.startswith("# Parameters 1") or line.startswith("MainLM"):
                continue
            elif line:
                out.append(line)
        
    return "\n".join(out)

def makeLoglinearLM(name, sublms, weights, noNorm=False):
    out = ["# Parameters 1"]
    out.append("MainLM %s" % (name))
    out.append("# LMDefinition %d" % (3+len(sublms)*2))
    out.append("Name\t%s" % (name))
    out.append("Type\tLogLinearLM")
    
    for (i,lm) in enumerate(sublms):
        lmname, config, voc, lmfile = LSVLM.parse_lm_lines(lm.split("\n"))
        out.append("LM[%d]\t%s" % (i, lmname))
        out.append("Weight[%d]\t%s" % (i, weights[i]))

    if noNorm:
        out.append("NoNorm\t1")
    
    for lm in sublms:
        for line in lm.split("\n"):
            if line.startswith("# Parameters 1") or line.startswith("MainLM"):
                continue
            elif line:
                out.append(line)
        
    return "\n".join(out)

def makeClassLM(name, emissionlm, predictionlm, classmapname, classmapfile):
    e_name, e_cfg, e_voc, e_file = LSVLM.parse_lm_lines(emissionlm.split("\n"))
    p_name, p_cfg, p_voc, p_file = LSVLM.parse_lm_lines(predictionlm.split("\n"))
    out = ["# Parameters 1"]
    out.append("MainLM %s" % (name))
    out.append("# LMDefinition 5")
    out.append("Name\t%s" % (name))
    out.append("Type\tClassLM")
    
    out.append("EmissionLM\t%s" % (e_name))
    out.append("ClassPredictLM\t%s" % (p_name))
    out.append("Word2ClassMap\t%s" % (classmapname))
    
    out.append("# ClassMapDefinition 2")
    out.append("%s\tClassMap" % (classmapname))
    out.append("File\t%s" % (classmapfile))
    for line in chain(emissionlm.split("\n"), predictionlm.split("\n")):
        if line.startswith("# Parameters 1") or line.startswith("MainLM"):
            continue
        elif line:
            out.append(line)
    return "\n".join(out)

def makeIncludeLM(name, includefile):
    out = ["# Parameters 1"]
    out.append("MainLM %s" % (name))
    out.append("# LMDefinition 3")
    out.append("Name\t%s" % (name))
    out.append("Type\tIncludeLM")
    from os.path import abspath
    out.append("File\t%s" % (abspath(includefile)))

    return "\n".join(out)

def makeAbsDiscLM(*args, **kwargs):
    return makeCntMGramLM(*args, **kwargs)
    
def makeCntMGramLM(name, treename, treefile, M, backofflm, disc):
    bo_name, bo_cfg, bo_voc, bo_file = LSVLM.parse_lm_lines(backofflm.split("\n"))
    
    #Remove all definitions of the tree from the backofflm
    inTree = False
    removeIdxes = []
    for i,line in enumerate(backofflm.split("\n")):
        if line.startswith("# Parameters 1") or line.startswith("MainLM"):
            removeIdxes.append(i)
        if line.startswith("# TreeDefinition 2"):
            inTree = True
        elif line.startswith("# "):
            inTree = False
        if inTree:
            if line.split()[0] == "Name" and line.split()[1] == treename:
                removeIdxes.append(i)
                removeIdxes.append(i-1)
                removeIdxes.append(i+1)
    
    bolm = [line for i,line in enumerate(backofflm.split("\n")) if i not in removeIdxes and line]

    out = ["# Parameters 1"]
    out.append("MainLM %s" % (name))
    out.append("# LMDefinition 6") 
    
    out.append("Name\t%s" % (name))
    out.append("Type\tCntMGramLM")
    out.append("Tree\t%s" % (treename))
    out.append("M\t%s" % (str(M)))
    out.append("BackOffLM\t%s" % (bo_name))
    out.append("Disc\t%s" % (str(disc)))
   
    out.extend(bolm)
    
    out.append("# TreeDefinition 2")
    out.append("Name\t%s" % (treename))
    out.append("File\t%s" % (treefile))

    return "\n".join(out)

def makeZeroLM(name, vocsize):
    out = ["# Parameters 1"]
    out.append("MainLM %s" % (name))
    out.append("# LMDefinition 3") 
    
    out.append("Name\t%s" % (name))
    out.append("Type\tZeroLM")
    out.append("VocSize\t%s" % (str(vocsize)))
    
    return "\n".join(out)

def makeDirectLM(name, probfile):
    out = ["# Parameters 1"]
    out.append("MainLM %s" % (name))
    out.append("# LMDefinition 3") 
    
    out.append("Name\t%s" % (name))
    out.append("Type\tDirectLM")
    out.append("ProbabilityFile\t%s" % (probfile))
    
    return "\n".join(out)
