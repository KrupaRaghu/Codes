from random import randint, sample
from itertools import combinations_with_replacement

outdir = "/nethome/afischer/BA/demo_corpus/misc/"

vocab = ["A", "B", "C", "D", "E"]

num_sents = 10
sents = []
caps = []
min_length = 3
max_length = 10
max_len_cap = 4

for i in xrange(num_sents):
	#calc random length for content sentence 
	length = randint(min_length, max_length)
	x = sample(list(combinations_with_replacement(vocab,length)), 1)[0]
	sent = []
	for w in x:
		sent.append(w)
	sents.append(sent)
	#calc random length for caption sentence 
	length = randint(0, max_len_cap)
	x = sample(list(combinations_with_replacement(vocab,length)), 1)[0]
	sent = []
	for w in x:
		sent.append(w)
	caps.append(sent)

for i, (sent,cap) in enumerate(zip(sents, caps)):
	f_d = open(outdir+str(i)+".doc", "w")
	f_d.write(" ".join(sent))
	f_c = open(outdir+str(i)+".cap", "w")
	f_c.write(" ".join(cap))
