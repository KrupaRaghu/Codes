#!/bin/bash
#Preprocessing of BNC documents.
. experiment_config.sh
. functions.sh

echo "Removing HTML markup..." && \
echo 0 | map_py pipelines.maps.HTML nohtml_item ${DOC} ${DOC_NOMARKUP} && \
echo "PoS tagging with TreeTagger..." && \
echo 0 | map_cmd ${TREETAGGER} ${DOC_NOMARKUP} ${DOC_TAGS_RAW} && \
echo "Transforming raw TreeTagger output to WTLs..." && \
echo 0 | map_py pipelines.maps.TreeTagger treetagger_to_wtl_item ${DOC_TAGS_RAW} ${DOC_TAGS} && \
#Basics for LDA
#SIFT RAW
echo "Applying SIFT script..." && \
echo 0 | map_cmd ${SIFT} ${IMG} ${IMG_SIFT_RAW} && \
#SIFT
#echo "Converting raw SIFT to SIFT..." && \
#echo 0 | map_py pipelines.maps.SIFT convert_to_SIFT_item ${IMG_SIFT_RAW} ${IMG_SIFT} && \
#Delete raw SIFTs
#NVA filtering of tagged data
echo "Filtering nouns, verbs, and adjectives from tagged data..." && \
echo 0 | map_py pipelines.maps.TreeTagger filter_nva_item ${DOC_TAGS} ${DOC_NVA} && \
#Extraction of words from NVA-filtered data
echo "Extracting words from NVA-filtered data..." && \
echo 0 | map_py pipelines.maps.TreeTagger words_item ${DOC_NVA} ${DOC_NVA_WORDS} && \
#Extraction of lemmas from NVA-filtered data
echo "Extracting lemmas from NVA-filtered data..." && \
echo 0 | map_py pipelines.maps.TreeTagger lemmas_item ${DOC_NVA} ${DOC_NVA_LEM} && \
#END basics for LDA
echo "Tokenizing..." && \
echo 0 | map_py pipelines.maps.TreeTagger words_item ${DOC_TAGS} ${DOC_TOKEN} && \
echo "Applying Stanford parser..." && \
echo 0 | map_cmd "\"${STANFORD_PARSER} <(cat)\"" ${DOC_TOKEN} ${DOC_STANFORD_RAW} && \
echo "Converting raw Stanford output to StanfordDependencies..." && \
echo 0 | map_py pipelines.maps.StanfordDependencies raw_Stanford_to_Dependencies_item ${DOC_STANFORD_RAW} ${DOC_STANFORD} && \
echo "Extracting phrases from StanfordDependencies..." && \
echo 0 | map_py pipelines.maps.Sentences phrases_from_StanfordDependencies_item ${DOC_STANFORD} ${DOC_SENTS_STANFORD}
