#!/bin/bash
#Preprocessing of BNC documents.
. experiment_config.sh
. functions.sh

echo "Applying Stanford parser..." && \
get_filter_neg BNC ${BNC_STANFORD_RAW} | map_cmd "\"${STANFORD_PARSER} <(cat)\"" ${BNC_TOKEN} ${BNC_STANFORD_RAW}
#get_filter_neg BNC_rest_dreene ${BNC_STANFORD_RAW} | map_cmd "\"${STANFORD_PARSER} <(cat)\"" ${BNC_TOKEN} ${BNC_STANFORD_RAW}
#&& \
#echo "Converting raw Stanford output to StanfordDependencies..." && \
#get_filter_neg BNC_1 ${BNC_STANFORD} | map_py pipelines.maps.StanfordDependencies raw_Stanford_to_Dependencies_item ${BNC_STANFORD_RAW} ${BNC_STANFORD} && \
#echo "Extracting phrases from StanfordDependencies..." && \
#get_filter_neg BNC_1 ${BNC_SENTS_STANFORD} | map_py pipelines.maps.Sentences phrases_from_StanfordDependencies_item ${BNC_STANFORD} ${BNC_SENTS_STANFORD}
