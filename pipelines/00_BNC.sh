#!/bin/bash
#Preprocessing of BNC documents.
. experiment_config.sh
. functions.sh

echo "Removing SGML markup..." && \
get_filter_neg ${BNCSPLIT} ${BNC_NOMARKUP} | map_py pipelines.maps.SGML nosgml_item ${BNC} ${BNC_NOMARKUP} && \
echo "PoS tagging with TreeTagger..." && \
get_filter_neg ${BNCSPLIT} ${BNC_TAGS_RAW} | map_cmd ${TREETAGGER} ${BNC_NOMARKUP} ${BNC_TAGS_RAW};
echo "Transforming raw TreeTagger output to WTLs..." && \
get_filter_neg ${BNCSPLIT} ${BNC_TAGS} | map_py pipelines.maps.TreeTagger treetagger_to_wtl_item ${BNC_TAGS_RAW} ${BNC_TAGS} && \
#echo "Deleting raw tag files..." && \
#get_filter_pos ${BNCSPLIT} ${BNC_TAGS} | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${BNC_TAGS_RAW} && \
echo "Tokenizing..." && \
get_filter_neg ${BNCSPLIT} ${BNC_TOKEN} | map_py pipelines.maps.TreeTagger words_item ${BNC_TAGS} ${BNC_TOKEN} && \
echo "Applying Stanford parser..." && \
get_filter_neg ${BNCSPLIT} ${BNC_STANFORD_RAW} | map_cmd "\"${STANFORD_PARSER} <(cat)\"" ${BNC_TOKEN} ${BNC_STANFORD_RAW} && \
echo "Converting raw Stanford output to StanfordDependencies..." && \
get_filter_neg ${BNCSPLIT} ${BNC_STANFORD} | map_py pipelines.maps.StanfordDependencies raw_Stanford_to_Dependencies_item ${BNC_STANFORD_RAW} ${BNC_STANFORD} && \
echo "Extracting phrases from StanfordDependencies..." && \
get_filter_neg ${BNCSPLIT} ${BNC_SENTS_STANFORD} | map_py pipelines.maps.Sentences phrases_from_StanfordDependencies_item ${BNC_STANFORD} ${BNC_SENTS_STANFORD}
