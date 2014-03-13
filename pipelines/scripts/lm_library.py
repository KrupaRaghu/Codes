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
    
def makeCntMGramLM(name, treename, treefile, M, backofflm, disc, ignoreTreeDef = False):
    bo_name, bo_cfg, bo_voc, bo_file = LSVLM.parse_lm_lines(backofflm.split("\n"))

    #Remove all definitions of the tree from the backofflm if not otherwise specified
    inTree = False
    removeIdxes = []
    if not ignoreTreeDef:    
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

def makeZeroLM(name):
    out = [u"# Parameters 1"]
    out.append(u"MainLM %s" % (name))
    out.append(u"# LMDefinition 3") 
    
    out.append(u"Name\t%s" % (name))
    out.append(u"Type\tZeroLM")
    
    return u"\n".join(out)

def makeDirectLM(name, probfile):
    out = [u"# Parameters 1"]
    out.append(u"MainLM %s" % (name))
    out.append(u"# LMDefinition 2") 
    
    out.append(u"Name\t%s" % (name))
    out.append(u"Type\tDirectLM")
    out.append(u"ProbabilityFile\t%s" % (probfile))
    
    return u"\n".join(out)

def makeKNTrigramWithBO(name, m3_treefile, m3_kn_treefile, m2_treefile, m2_kn_treefile, m1_treefile):
	t_m3name = name+u"_M3_tree"
	t_m3_kn_name = name+u"_M3_KNtree"
	t_m2name = name+u"_M2_tree"
	t_m2_kn_name = name+u"_M2_KNtree"
	t_m1name = name+u"_M1_tree"

	out = [u"# Parameters 1"]
	out.append(u"MainLM %s" % (name))
	#The main trigram LM definition
	out.append(u"# LMDefinition 7")
	out.append(u"Name\t%s" % (name))
	out.append(u"Type\tKN")
	out.append(u"KNTree\t%s" % (t_m3name))
	out.append(u"Tree\t%s" % (t_m3_kn_name))
	out.append(u"M\t3")
	out.append(u"BackOffLM\t%s" % (name+u"_BiGram"))	
	out.append(u"Interpolate\tFALSE")	
	#Back-off bigram definition
	out.append(u"# LMDefinition 7")
	out.append(u"Name\t%s" % (name+u"_BiGram"))
	out.append(u"Type\tKN")
	out.append(u"KNTree\t%s" % (t_m2name))
	out.append(u"Tree\t%s" % (t_m2_kn_name))
	out.append(u"M\t2")
	out.append(u"BackOffLM\t%s" % (name+u"_UniGram"))	
	out.append(u"Interpolate\tFALSE")	
	#Back-off unigram definition
	out.append(u"# LMDefinition 6")
	out.append(u"Name\t%s" % (name+u"_UniGram"))
	out.append(u"Type\tKN")
	out.append(u"KNTree\t%s" % (t_m1name))
	out.append(u"M\t1")
	out.append(u"BackOffLM\t%s" % (name+u"_ZeroGram"))	
	out.append(u"Interpolate\tFALSE")	
	#Back-off zerogram definition
	out.append(u"# LMDefinition 2")
	out.append(u"Name\t%s" % (name+u"_ZeroGram"))
	out.append(u"Type\tZero")
	#Tree definitions
	#Regular trigram tree
	out.append(u"# TreeDefinition 2")
	out.append(u"Name\t%s" % (t_m3name))
	out.append(u"File\t%s" % (m3_treefile))
	#KN trigram tree
	out.append(u"# TreeDefinition 2")
	out.append(u"Name\t%s" % (t_m3_kn_name))
	out.append(u"File\t%s" % (m3_kn_treefile))
	#Regular bigram tree
	out.append(u"# TreeDefinition 2")
	out.append(u"Name\t%s" % (t_m2name))
	out.append(u"File\t%s" % (m2_treefile))
	#KN bigram tree
	out.append(u"# TreeDefinition 2")
	out.append(u"Name\t%s" % (t_m2_kn_name))
	out.append(u"File\t%s" % (m2_kn_treefile))
	#Regular unigram tree
	out.append(u"# TreeDefinition 2")
	out.append(u"Name\t%s" % (t_m1name))
	out.append(u"File\t%s" % (m1_treefile))

	return u"\n".join(out)

def makeKNUnigramWithBO(name, m1_treefile):
	t_m1name = name+u"_M1_tree"

	out = [u"# Parameters 1"]
	out.append(u"MainLM %s" % (name))
	#Unigram definition
	out.append(u"# LMDefinition 6")
	out.append(u"Name\t%s" % (name))
	out.append(u"Type\tKN")
	out.append(u"KNTree\t%s" % (t_m1name))
	out.append(u"M\t1")
	out.append(u"BackOffLM\t%s" % (name+u"_ZeroGram"))	
	out.append(u"Interpolate\tFALSE")	
	#Back-off zerogram definition
	out.append(u"# LMDefinition 2")
	out.append(u"Name\t%s" % (name+u"_ZeroGram"))
	out.append(u"Type\tZero")
	#Regular unigram tree
	out.append(u"# TreeDefinition 2")
	out.append(u"Name\t%s" % (t_m1name))
	out.append(u"File\t%s" % (m1_treefile))

	return u"\n".join(out)

def makeLDALM(lmname, dDoc_probfile, dMix_probfile, dImg_probfile, suf="_AllLDAZero", suf_dDoc="_dDoc", suf_dMix="_dMix", suf_dImg="_dImg", suf_Zero="_Zero", w_dDoc = W_DOC_LDAZEROLM, w_dImg=W_IMG_LDAZEROLM, w_dMix=W_MIX_LDAZEROLM, w_Zero = W_ZERO_LDAZEROLM):
    for item in itemiterator:
	docname=u"".join((item.get_attribute("original_name", unicode)+name_end_dDoc.decode("utf-8")).split())
	mixname=u"".join((item.get_attribute("original_name", unicode)+name_end_dMix.decode("utf-8")).split())
	imgname=u"".join((item.get_attribute("original_name", unicode)+name_end_dImg.decode("utf-8")).split())
	zeroname=u"".join((item.get_attribute("original_name", unicode)+name_end_Zero.decode("utf-8")).split())
	lmname=u"".join((item.get_attribute("original_name", unicode)+name_end.decode("utf-8")).split())
        doclm = makeDirectLM(name=docname, probfile=item.get_attribute_path(dDoc_prob_attr))
        imglm = makeDirectLM(name=imgname, probfile=item.get_attribute_path(dImg_prob_attr))
        mixlm = makeDirectLM(name=mixname, probfile=item.get_attribute_path(dMix_prob_attr))
        zerolm = makeZeroLM(zeroname)
        return makeLinearLM(lmname, [doclm, imglm, mixlm, zerolm], [w_dDoc, w_dImg, w_dMix, w_Zero]))

def get_paramnames_for_FMALM(lmname, suf_lda, suf_tri, suf_bi, suf_uni_kn, suf_uni, suf_dDoc, suf_dMix, suf_dImg):
	#Beta is lmname::Weight[0] and must also be -lmname::Weight[1]
	yield lmname+"::Weight[0]"	
	yield lmname+"::Weight[1]"	
	#Trigram weight is constant, doesn't need to show up here.
	#LDA interpolation weights are
	#w_dDoc: ldaname::Weight[0]
	#w_dMix: ldaname::Weight[1]
	#w_dImg: ldaname::Weight[2]
	#w_Zero: ldaname::Weight[3]
	lda_name = lmname+suf_lda.decode("utf-8")
	yield lda_name+"::Weight[0]"
	yield lda_name+"::Weight[1]"
	yield lda_name+"::Weight[2]"
	yield lda_name+"::Weight[3]"
	
	#Marginal unigram discounting parameter is 
	#disc_marginal_M1: uniname::Disc
	uni_name = lmname+suf_uni.decode("utf-8")
	yield uni_name+"::Disc"

def makeFengLapataFMALM(lmname, treename, treefile_M3, treefile_M2, treefile_M1, dDoc_probfile, dMix_probfile, dImg_probfile, suf_lda="_LDA", suf_tri = "_Tri", suf_bi="_BiKN",suf_uni_kn="_UniKN", suf_uni="_Uni", suf_dDoc="_dDoc", suf_dMix="_dMix", suf_dImg="_dImg", w_dDoc=W_DOC_FMALM, w_dMix=W_MIX_FMALM, w_Img=W_IMG_FMALM, w_Zero=W_ZERO_FMALM, beta=BETA_FMALM, disc_3 = DISC_3_KNTRIGRAM, disc_2 = DISC_2_KNTRIGRAM, disc_1 = DISC_1_KNTRIGRAM):
	
	#Make backing-off trigram
	tri_name = lmname+suf_tri.decode("utf-8")
	tri_lm = makeKMsmoothedTrigramLM(tri_name, treename, treefile_M3, treefile_M2, treefile_M1, disc_3, disc_2, disc_1, suf_tri, suf_bi, suf_uni_kn)
	#Make interpolated LDA lm
	lda_name = lmname+suf_lda.decode("utf-8")
	lda_lm = makeLDALM(lda_name, dDoc_probfile, dMix_probfile, dImg_probfile, suf_lda, suf_dDoc, suf_dMix, suf_dImg, "_Zero", w_dDoc, w_dImg, w_dMix, w_Zero)
	#Make regular unigram
	uni_name = lmname+suf_uni.decode("utf-8")
	bo_uni = makeZeroLM(uni_name+u"_Zero")
	uni_lm - makeCntMGramLM(uni_name, treename, treefile_M3, 1, bo_uni, disc_1, ignoreTreeDef = True)
	
	#Combine into log-linear lm
	sublms = [lda_lm, uni_lm, tri_lm]
	weights = [float(beta), -float(beta), 1.0]
	return makeLoglinearLM(lmname, sublms, weights)
