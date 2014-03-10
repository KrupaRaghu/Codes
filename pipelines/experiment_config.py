#Corpus rootdir and data splits
CORPUS = "/home/janno/DREENE/BA_EXPERIMENTS/corpus"
DEVSPLIT_NAME = "dev"
TESTSPLIT_NAME = "test"
TRAINSPLIT_NAME = "training"
BNCSPLIT_NAME = "BNC"
#LSVLM C wrapper paths
LSVLM_LIB_PATH="/home/janno/DREENE/lsvlm/lib/liblm.so"
LSVLM_WRAPPER_PATH="/home/janno/DREENE/BA/lsvlmc/lsvlm_c_bindings.so.1.0.1"
#Multiprocessing
CPUS = 8
#Sentence start/end tokens
SENTENCE_START = "<S_START>"
SENTENCE_END = "<S_END>"
UNKNOWN_WORD = "<UNKNOWN_WORD>"
PHRASE_DELIMITER = " "
#Default smoothing parameters
SMOOTH_EPSILON=1e-5
#k-means
K=750
KMEANS_METHOD = "K_MEANS2_SCIKIT"
KMEANS_OUTFILE = "/home/andrea/studium/BA/%d_kmeans.model" % (K)
#LDA
T=1000
LDA_OUTFILE = "/home/andrea/studium/BA/LDA_K%d_T%d.corpus" % (K,T)
#Vocabularies
FILTER_VOC_FILE = "/home/andrea/studium/BA/LDA_filter_vocabulary_K%d_T%d.voc" % (K,T)
FULL_VOC_FILE = "/home/andrea/studium/BA/vocabulary_K%d_T%d.voc" % (K,T)
#Conditional probability model(s - smoothing?)
CONDITIONAL_PROB_MODEL_FILE="/home/andrea/studium/BA/content_selection.cntfile"
#Sentence length model(s)
SENTENCE_LENGTH_MODEL_GAUSSIAN="/home/andrea/studium/BA/sentence_lengths.gaussian"
#Whether or not to use sentence start/end tokens for sentence length models
USE_TOKENS=True
#Data attribute names (for overview and central changes)
#Origins
BBC_ORIGIN = "BBC"
BNC_ORIGIN = "BNC"
#BBC documents
DOC = "html" #document start name/format
DOC_NOMARKUP = "doc"
DOC_TAGS = "doc_tagged"
DOC_TOKEN = "doc_tokenized"
DOC_LEM = "doc_lemmas"
DOC_SENT = "doc_sentences"
DOC_BOW = "doc_bow"
DOC_NVA_LEM = "doc_nva_lemmas"
DOC_NVA_WORDS = "doc_nva_words"
#BBC captions
CAP = "caption" #caption start name/format
CAP_TAGS = "caption_tagged"
CAP_TOKEN = "caption_tokenized"
CAP_LEM = "caption_lemmas"
CAP_SENT = "caption_sentences"
CAP_BOW = "caption_bow"
CAP_NVA_LEM = "caption_nva_lemmas"
CAP_NVA_WORDS = "caption_nva_words"
#BBC images
IMG = "pgm" #image start name/format
IMG_SIFT_RAW = "sift_raw"
IMG_SIFT = "sift"
IMG_VISI_KMEANS = "kmeans_visiterms_%d" % (K)
#BNC documents
BNC = "sgml" #BNC document start name/format
BNC_NOMARKUP = "BNC"
BNC_TAGS = "BNC_tagged"
BNC_TOKEN = "BNC_tokenized"
BNC_LEM = "BNC_lemmas"
BNC_SENT = "BNC_sentences"
BNC_BOW = "BNC_bow"
BNC_NVA_LEM = "BNC_nva_lemmas"
BNC_NVA_WORDS = "BNC_nva_words"