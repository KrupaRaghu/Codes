from ..formats.LengthModels import *
from ..formats.Sentences import *
from ..experiment_config import *
from math import sqrt
from pprint import pprint

def estimate_Gaussian(lengths):
    num = len(lengths)
    mu = float(sum(lengths))/num
    var = 0.0
    for l in lengths:
        var = var + (l-mu)**2
    var = var / (num - 1)
    return mu, var

def get_sentence_lengths_for_latex(itemiterator, doc_attr = None, cap_attr = None):
	lengths = []
	for item in itemiterator:
		if doc_attr:
			lengths.extend(item.get_attribute(doc_attr, Sentences).get_sentence_lengths())	
		if cap_attr:
			lengths.extend(item.get_attribute(cap_attr, Sentences).get_sentence_lengths())	
	for l in lengths:
		print l

def plot_sentence_lengths(itemiterator, doc_attr = None, cap_attr = None, name = "Sentence lengths", maxval=None):
    lengths = []
    for item in itemiterator:
        if doc_attr:
            sentlens = item.get_attribute(doc_attr, Sentences).get_sentence_lengths()
            for l in sentlens:
                lengths.append(l)
        if cap_attr:
            sentlens = item.get_attribute(cap_attr, Sentences).get_sentence_lengths()
            for l in sentlens:
                lengths.append(l)
    import pylab as PLT
    PLT.figure()
    if maxval is None:
        upper = max(lengths)+1
    else:
        lengths = filter(lambda x: x <= int(maxval), lengths)
        upper = int(maxval)
    print "Number of sentences:", len(lengths)
    print "Maximum sentence length:", max(lengths)
    PLT.hist(lengths, xrange(upper), normed=1, rwidth=0.8, align='mid', facecolor="green", color="green")
#    mu, var = estimate_Gaussian(sorted(lengths)[0:upper])
    mu, var = estimate_Gaussian(lengths)
    lengthmodel = GaussianLengthModel(mu, sqrt(var))

    print "Mean of Gaussian:", mu
    print "Variance of Gaussian:", var
    print "Standard deviation:", sqrt(var)

    PLT.plot(xrange(upper), [lengthmodel.prob(x) for x in xrange(upper)], color='red', linewidth=2.5)
    
    PLT.title(name)
    PLT.show()

def train_Gaussian_length_model(itemiterator, doc_attr = None, cap_attr = None):
    lengths = []
    for item in itemiterator:
        if doc_attr:
            sentlens = item.get_attribute(doc_attr, Sentences).get_sentence_lengths()
            for l in sentlens:
                lengths.append(l)
        if cap_attr:
            sentlens = item.get_attribute(cap_attr, Sentences).get_sentence_lengths()
            for l in sentlens:
                lengths.append(l)
    mu, var = estimate_Gaussian(lengths)
    lengthmodel = GaussianLengthModel(mu, sqrt(var))
    print lengthmodel.encode()
    
