#!/bin/bash
#Tools/commands
TREETAGGER=/home/andrea/studium/tools/treetagger/cmd/tree-tagger-english
SIFT=/home/andrea/studium/tools/siftDemoV4/sift
STANFORD_PARSER=/home/andrea/studium/tools/stanford-parser/lexparser.sh
#Corpus rootdir and data splits
CORPUS=/home/andrea/studium/BA_EXPERIMENTS/corpus
TESTSPLIT="test"
DEVSPLIT="dev"
TRAINSPLIT="training"
BNCSPLIT="BNC"
#Multiprocessing
CPUS=8
#Sentence start/end tokens
SENTENCE_START="<S_START>"
SENTENCE_END="<S_END>"
#Default smoothing parameters
SMOOTH_EPSILON=1e-5
#k-means
K=750
KMEANS_METHOD=K_MEANS2_SCIKIT
KMEANS_OUTFILE=/home/andrea/studium/BA/${K}_kmeans.model
#LDA
T=1000
LDA_OUTFILE=/home/andrea/studium/BA/LDA_K${K}_T${T}.corpus
#Vocabularies
FILTER_VOC_FILE=/home/andrea/studium/BA/LDA_filter_vocabulary_K${K}_T${T}.voc
FULL_VOC_FILE=/home/andrea/studium/BA/vocabulary_K${K}_T${T}.voc
#Conditional probability model(s - smoothing?)
CONDITIONAL_PROB_MODEL_FILE=/home/andrea/studium/BA/content_selection.cntfile
#Sentence length model(s)
SENTENCE_LENGTH_MODEL_GAUSSIAN=/home/andrea/studium/BA/sentence_lengths.gaussian
#Whether or not to use sentence start/end tokens for sentence length models
USE_TOKENS=True
#Data attribute names (for overview and central changes)
#Origins
BBC_ORIGIN="BBC"
BNC_ORIGIN="BNC"
#BBC documents
DOC="html" #document start name/format
DOC_NOMARKUP="doc"
DOC_TAGS_RAW="doc_tagged_raw"
DOC_TAGS="doc_tagged"
DOC_TOKEN="doc_tokenized"
DOC_LEM="doc_lemmas"
DOC_SENTS_RAW="doc_sentences_raw"
DOC_SENTS_STANFORD="doc_sentences_stanford"
DOC_BOW="doc_bow"
DOC_NVA="doc_nva"
DOC_NVA_WORDS="doc_nva_words"
DOC_NVA_LEM="doc_nva_lemmas"
DOC_STANFORD_RAW=doc_stanford_raw
DOC_STANFORD=doc_stanford
#BBC captions
CAP="txt" #caption start name/format
CAP_TAGS_RAW="caption_tagged_raw"
CAP_TAGS="caption_tagged"
CAP_TOKEN="caption_tokenized"
CAP_LEM="caption_lemmas"
CAP_SENTS_RAW="caption_sentences_raw"
CAP_SENTS_STANFORD="caption_sentences_stanford"
CAP_BOW="caption_bow"
CAP_NVA="caption_nva"
CAP_NVA_WORDS="caption_nva_words"
CAP_NVA_LEM="caption_nva_lemmas"
CAP_STANFORD_RAW=caption_stanford_raw
CAP_STANFORD=caption_stanford
#BBC images
IMG="pgm" #image start name/format
IMG_SIFT_RAW="sift_raw"
IMG_SIFT="sift"
IMG_VISI_KMEANS="kmeans_visiterms_${K}"
#BNC documents
BNC="sgml" #BNC document start name/format
BNC_NOMARKUP="BNC"
BNC_TAGS_RAW="BNC_tagged_raw"
BNC_TAGS="BNC_tagged"
BNC_TOKEN="BNC_tokenized"
BNC_LEM="BNC_lemmas"
BNC_SENTS_RAW="BNC_sentences_raw"
BNC_SENTS_STANFORD="BNC_sentences_stanford"
BNC_BOW="BNC_bow"
BNC_NVA="BNC_nva"
BNC_NVA_LEM="BNC_nva_lemmas"
BNC_STANFORD_RAW=BNC_stanford_raw
BNC_STANFORD=BNC_stanford
BNC_TYPDEP=BNC_typed_dependencies
