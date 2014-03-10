#!/bin/bash
#Preprocessing of BNC documents.
. experiment_config.sh
. functions.sh

echo "Removing HTML markup..." && \
get_filter_neg ${TRAINSPLIT} ${DOC_NOMARKUP} | map_py pipelines.maps.HTML nohtml_item ${DOC} ${DOC_NOMARKUP} && \
get_filter_neg ${TESTSPLIT} ${DOC_NOMARKUP} | map_py pipelines.maps.HTML nohtml_item ${DOC} ${DOC_NOMARKUP} && \
get_filter_neg ${DEVSPLIT} ${DOC_NOMARKUP} | map_py pipelines.maps.HTML nohtml_item ${DOC} ${DOC_NOMARKUP} && \
echo "PoS tagging with TreeTagger..." && \
get_filter_neg ${TRAINSPLIT} ${DOC_TAGS_RAW} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TAGS} --neg | map_cmd ${TREETAGGER} ${DOC_NOMARKUP} ${DOC_TAGS_RAW} && \
get_filter_neg ${TESTSPLIT} ${DOC_TAGS_RAW} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TAGS} --neg | map_cmd ${TREETAGGER} ${DOC_NOMARKUP} ${DOC_TAGS_RAW} && \
get_filter_neg ${DEVSPLIT} ${DOC_TAGS_RAW} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TAGS} --neg | map_cmd ${TREETAGGER} ${DOC_NOMARKUP} ${DOC_TAGS_RAW} && \
get_filter_neg ${TRAINSPLIT} ${CAP_TAGS_RAW} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TAGS} --neg | map_cmd ${TREETAGGER} ${CAP} ${CAP_TAGS_RAW} && \
get_filter_neg ${TESTSPLIT} ${CAP_TAGS_RAW} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TAGS} --neg | map_cmd ${TREETAGGER} ${CAP} ${CAP_TAGS_RAW} && \
get_filter_neg ${DEVSPLIT} ${CAP_TAGS_RAW} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TAGS} --neg | map_cmd ${TREETAGGER} ${CAP} ${CAP_TAGS_RAW} && \
echo "Transforming raw TreeTagger output to WTLs..." && \
get_filter_neg ${TRAINSPLIT} ${DOC_TAGS} | map_py pipelines.maps.TreeTagger treetagger_to_wtl_item ${DOC_TAGS_RAW} ${DOC_TAGS} && \
get_filter_neg ${TESTSPLIT} ${DOC_TAGS} | map_py pipelines.maps.TreeTagger treetagger_to_wtl_item ${DOC_TAGS_RAW} ${DOC_TAGS} && \
get_filter_neg ${DEVSPLIT} ${DOC_TAGS} | map_py pipelines.maps.TreeTagger treetagger_to_wtl_item ${DOC_TAGS_RAW} ${DOC_TAGS} && \
get_filter_neg ${TRAINSPLIT} ${CAP_TAGS} | map_py pipelines.maps.TreeTagger treetagger_to_wtl_item ${CAP_TAGS_RAW} ${CAP_TAGS} && \
get_filter_neg ${TESTSPLIT} ${CAP_TAGS} | map_py pipelines.maps.TreeTagger treetagger_to_wtl_item ${CAP_TAGS_RAW} ${CAP_TAGS} && \
get_filter_neg ${DEVSPLIT} ${CAP_TAGS} | map_py pipelines.maps.TreeTagger treetagger_to_wtl_item ${CAP_TAGS_RAW} ${CAP_TAGS} && \
#echo "Deleting raw tag files..." && \
#get_filter_pos ${TRAINSPLIT} ${DOC_TAGS} | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${DOC_TAGS_RAW} && \
#get_filter_pos ${TESTSPLIT} ${DOC_TAGS} | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${DOC_TAGS_RAW} && \
#get_filter_pos ${DEVSPLIT} ${DOC_TAGS} | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${DOC_TAGS_RAW} && \
#get_filter_pos ${TRAINSPLIT} ${CAP_TAGS} | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${CAP_TAGS_RAW} && \
#get_filter_pos ${TESTSPLIT} ${CAP_TAGS} | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${CAP_TAGS_RAW} && \
#get_filter_pos ${DEVSPLIT} ${CAP_TAGS} | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${CAP_TAGS_RAW} && \
#Basics for LDA
#SIFT RAW
echo "Applying SIFT scrips..." && \
get_filter_neg ${TRAINSPLIT} ${IMG_SIFT_RAW} | map_cmd ${SIFT} ${IMG} ${IMG_SIFT_RAW} && \
get_filter_neg ${TESTSPLIT} ${IMG_SIFT_RAW} | map_cmd ${SIFT} ${IMG} ${IMG_SIFT_RAW} && \
get_filter_neg ${DEVSPLIT} ${IMG_SIFT_RAW} | map_cmd ${SIFT} ${IMG} ${IMG_SIFT_RAW} && \
#SIFT
echo "Converting raw SIFT to SIFT..." && \
get_filter_neg ${TRAINSPLIT} ${DOC_SIFT} | map_py pipelines.maps.SIFT convert_to_SIFT_item ${IMG_SIFT_RAW} ${IMG_SIFT} && \
get_filter_neg ${TESTSPLIT} ${DOC_SIFT} | map_py pipelines.maps.SIFT convert_to_SIFT_item ${IMG_SIFT_RAW} ${IMG_SIFT} && \
get_filter_neg ${DEVSPLIT} ${DOC_SIFT} | map_py pipelines.maps.SIFT convert_to_SIFT_item ${IMG_SIFT_RAW} ${IMG_SIFT} && \
#Delete raw SIFTs
#echo "Deleting raw SIFTs..." && \
#get_filter_pos ${TRAINSPLIT} ${IMG_SIFT} | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${IMG_SIFT_RAW} && \
#get_filter_pos ${TESTSPLIT} ${IMG_SIFT} | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${IMG_SIFT_RAW} && \
#get_filter_pos ${DEVSPLIT} ${IMG_SIFT} | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${IMG_SIFT_RAW} && \
#NVA filtering of tagged data
echo "Filtering nouns, verbs, and adjectives from tagged data..." && \
get_filter_neg ${TRAINSPLIT} ${DOC_NVA} | map_py pipelines.maps.TreeTagger filter_nva_item ${DOC_TAGS} ${DOC_NVA} && \
get_filter_neg ${TESTSPLIT} ${DOC_NVA} | map_py pipelines.maps.TreeTagger filter_nva_item ${DOC_TAGS} ${DOC_NVA} && \
get_filter_neg ${DEVSPLIT} ${DOC_NVA} | map_py pipelines.maps.TreeTagger filter_nva_item ${DOC_TAGS} ${DOC_NVA} && \
get_filter_neg ${TRAINSPLIT} ${CAP_NVA} | map_py pipelines.maps.TreeTagger filter_nva_item ${CAP_TAGS} ${CAP_NVA} && \
get_filter_neg ${TESTSPLIT} ${CAP_NVA} | map_py pipelines.maps.TreeTagger filter_nva_item ${CAP_TAGS} ${CAP_NVA} && \
get_filter_neg ${DEVSPLIT} ${CAP_NVA} | map_py pipelines.maps.TreeTagger filter_nva_item ${CAP_TAGS} ${CAP_NVA} && \
#Extraction of words from NVA-filtered data
echo "Extracting words from NVA-filtered data..." && \
get_filter_neg ${TRAINSPLIT} ${DOC_NVA_WORDS} | map_py pipelines.maps.TreeTagger words_item ${DOC_NVA} ${DOC_NVA_WORDS} && \
get_filter_neg ${TESTSPLIT} ${DOC_NVA_WORDS} | map_py pipelines.maps.TreeTagger words_item ${DOC_NVA} ${DOC_NVA_WORDS} && \
get_filter_neg ${DEVSPLIT} ${DOC_NVA_WORDS} | map_py pipelines.maps.TreeTagger words_item ${DOC_NVA} ${DOC_NVA_WORDS} && \
get_filter_neg ${TRAINSPLIT} ${CAP_NVA_WORDS} | map_py pipelines.maps.TreeTagger words_item ${CAP_NVA} ${CAP_NVA_WORDS} && \
get_filter_neg ${TESTSPLIT} ${CAP_NVA_WORDS} | map_py pipelines.maps.TreeTagger words_item ${CAP_NVA} ${CAP_NVA_WORDS} && \
get_filter_neg ${DEVSPLIT} ${CAP_NVA_WORDS} | map_py pipelines.maps.TreeTagger words_item ${CAP_NVA} ${CAP_NVA_WORDS} && \
#Extraction of lemmas from NVA-filtered data
#echo "Extracting lemmas from NVA-filtered data..." && \
#get_filter_neg ${TRAINSPLIT} ${DOC_NVA_LEM} | map_py pipelines.maps.TreeTagger lemmas_item ${DOC_NVA} ${DOC_NVA_LEM} && \
#get_filter_neg ${TESTSPLIT} ${DOC_NVA_LEM} | map_py pipelines.maps.TreeTagger lemmas_item ${DOC_NVA} ${DOC_NVA_LEM} && \
#get_filter_neg ${DEVSPLIT} ${DOC_NVA_LEM} | map_py pipelines.maps.TreeTagger lemmas_item ${DOC_NVA} ${DOC_NVA_LEM} && \
#get_filter_neg ${TRAINSPLIT} ${CAP_NVA_LEM} | map_py pipelines.maps.TreeTagger lemmas_item ${CAP_NVA} ${CAP_NVA_LEM} && \
#get_filter_neg ${TESTSPLIT} ${CAP_NVA_LEM} | map_py pipelines.maps.TreeTagger lemmas_item ${CAP_NVA} ${CAP_NVA_LEM} && \
#get_filter_neg ${DEVSPLIT} ${CAP_NVA_LEM} | map_py pipelines.maps.TreeTagger lemmas_item ${CAP_NVA} ${CAP_NVA_LEM} && \
##END basics for LDA
echo "Tokenizing..." && \
get_filter_neg ${TRAINSPLIT} ${DOC_TOKEN} | map_py pipelines.maps.TreeTagger words_item ${DOC_TAGS} ${DOC_TOKEN} && \
get_filter_neg ${TESTSPLIT} ${DOC_TOKEN} | map_py pipelines.maps.TreeTagger words_item ${DOC_TAGS} ${DOC_TOKEN} && \
get_filter_neg ${DEVSPLIT} ${DOC_TOKEN} | map_py pipelines.maps.TreeTagger words_item ${DOC_TAGS} ${DOC_TOKEN} && \
get_filter_neg ${TRAINSPLIT} ${CAP_TOKEN} | map_py pipelines.maps.TreeTagger words_item ${CAP_TAGS} ${CAP_TOKEN} && \
get_filter_neg ${TESTSPLIT} ${CAP_TOKEN} | map_py pipelines.maps.TreeTagger words_item ${CAP_TAGS} ${CAP_TOKEN} && \
get_filter_neg ${DEVSPLIT} ${CAP_TOKEN} | map_py pipelines.maps.TreeTagger words_item ${CAP_TAGS} ${CAP_TOKEN} && \
echo "Applying Stanford parser..." && \
get_filter_neg ${TRAINSPLIT} ${DOC_STANFORD_RAW} | map_cmd "\"${STANFORD_PARSER} <(cat)\"" ${DOC_TOKEN} ${DOC_STANFORD_RAW} && \
get_filter_neg ${TESTSPLIT} ${DOC_STANFORD_RAW} | map_cmd "\"${STANFORD_PARSER} <(cat)\"" ${DOC_TOKEN} ${DOC_STANFORD_RAW} && \
get_filter_neg ${DEVSPLIT} ${DOC_STANFORD_RAW} | map_cmd "\"${STANFORD_PARSER} <(cat)\"" ${DOC_TOKEN} ${DOC_STANFORD_RAW} && \
get_filter_neg ${TRAINSPLIT} ${CAP_STANFORD_RAW} | map_cmd "\"${STANFORD_PARSER} <(cat)\"" ${CAP_TOKEN} ${CAP_STANFORD_RAW} && \
get_filter_neg ${TESTSPLIT} ${CAP_STANFORD_RAW} | map_cmd "\"${STANFORD_PARSER} <(cat)\"" ${CAP_TOKEN} ${CAP_STANFORD_RAW} && \
get_filter_neg ${DEVSPLIT} ${CAP_STANFORD_RAW} | map_cmd "\"${STANFORD_PARSER} <(cat)\"" ${CAP_TOKEN} ${CAP_STANFORD_RAW} && \
echo "Converting raw Stanford output to StanfordDependencies..." && \
get_filter_neg ${TRAINSPLIT} ${DOC_STANFORD} | map_py pipelines.maps.StanfordDependencies raw_Stanford_to_Dependencies_item ${DOC_STANFORD_RAW} ${DOC_STANFORD} && \
get_filter_neg ${TESTSPLIT} ${DOC_STANFORD} | map_py pipelines.maps.StanfordDependencies raw_Stanford_to_Dependencies_item ${DOC_STANFORD_RAW} ${DOC_STANFORD} && \
get_filter_neg ${DEVSPLIT} ${DOC_STANFORD} | map_py pipelines.maps.StanfordDependencies raw_Stanford_to_Dependencies_item ${DOC_STANFORD_RAW} ${DOC_STANFORD} && \
get_filter_neg ${TRAINSPLIT} ${CAP_STANFORD} | map_py pipelines.maps.StanfordDependencies raw_Stanford_to_Dependencies_item ${CAP_STANFORD_RAW} ${CAP_STANFORD} && \
get_filter_neg ${TESTSPLIT} ${CAP_STANFORD} | map_py pipelines.maps.StanfordDependencies raw_Stanford_to_Dependencies_item ${CAP_STANFORD_RAW} ${CAP_STANFORD} && \
get_filter_neg ${DEVSPLIT} ${CAP_STANFORD} | map_py pipelines.maps.StanfordDependencies raw_Stanford_to_Dependencies_item ${CAP_STANFORD_RAW} ${CAP_STANFORD} && \
echo "Extracting phrases from StanfordDependencies..." && \
get_filter_neg ${TRAINSPLIT} ${DOC_SENTS_STANFORD1} | map_py pipelines.maps.Sentences phrases_from_StanfordDependencies_item ${DOC_STANFORD} ${DOC_SENTS_STANFORD} && \
get_filter_neg ${TESTSPLIT} ${DOC_SENTS_STANFORD1} | map_py pipelines.maps.Sentences phrases_from_StanfordDependencies_item ${DOC_STANFORD} ${DOC_SENTS_STANFORD} && \
get_filter_neg ${DEVSPLIT} ${DOC_SENTS_STANFORD1} | map_py pipelines.maps.Sentences phrases_from_StanfordDependencies_item ${DOC_STANFORD} ${DOC_SENTS_STANFORD} && \
get_filter_neg ${TRAINSPLIT} ${CAP_SENTS_STANFORD1} | map_py pipelines.maps.Sentences phrases_from_StanfordDependencies_item ${CAP_STANFORD} ${CAP_SENTS_STANFORD} && \
get_filter_neg ${TESTSPLIT} ${CAP_SENTS_STANFORD1} | map_py pipelines.maps.Sentences phrases_from_StanfordDependencies_item ${CAP_STANFORD} ${CAP_SENTS_STANFORD} && \
get_filter_neg ${DEVSPLIT} ${CAP_SENTS_STANFORD1} | map_py pipelines.maps.Sentences phrases_from_StanfordDependencies_item ${CAP_STANFORD} ${CAP_SENTS_STANFORD}
