#Conditional content selection epsilon at vocsize = 47056
CSEL_EPSILON_OPT_DEV = 0.0005

#Phrase attachment epsilon at vocsize = 47056
PA_EPSILON_OPT_DEV = 0.0001

#LDA interpolation default parameters - taken from Feng and Lapata "Topic models for image annotation and text illustration"
W_MIX_DEFAULT=0.84
W_DOC_DEFAULT=0.12
W_IMG_DEFAULT=0.04

#Optimized unigram perplexity on captions only, dDoc + Zerogram only
W_DOC_DOCZEROLM=0.52
W_ZERO_DOCZEROLM=0.48

#Optimized unigram perplexity on captions + visiterms, full model + Zerogram
W_DOC_LDAZEROLM=0.02
W_IMG_LDAZEROLM=0.00
W_MIX_LDAZEROLM=0.95
W_ZERO_LDAZEROLM=0.03

W_DOC_FMALM=0.02
W_IMG_FMALM=0.00
W_MIX_FMALM=0.95
W_ZERO_FMALM=0.03
BETA_FMALM=0.3
