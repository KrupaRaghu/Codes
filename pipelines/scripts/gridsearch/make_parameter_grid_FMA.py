#Weight[0]: Weight of LDA model	    = beta
#Weight[1]: Weight of Unigram model = -beta
#Weight[2]: Weight of Trigram model = const 1

paramnames = ["Weight[0]", "Weight[1]", "Weight[2]"]
print " ".join(paramnames)

maxrange = 250
#Resolution: 1%
for b in xrange(maxrange+1):
	print float(b)/100, -float(b)/100, 1.0
