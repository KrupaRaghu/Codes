#!/bin/bash
#Preprocessing of BNC documents.
#Include experiment definitions.
. experiment_config.sh
. functions.sh
# Get BNC data split:
# dm-getsplit -r ${CORPUS} -s ${BNCSPLIT}
# get_filter_neg ${BNCSPLIT} ${BNC_NOMARKUP} 
# Keep all HAVING attribute:
# dm-itemfilterbyattr -r ${CORPUS} -a ${} --pos
# Keep all NOT HAVING attribute:
# dm-itemfilterbyattr -r ${CORPUS} -a ${} --neg
# Parallelize via "parallel [command]"
# get_filter_neg ${} ${} | map_py M F ${} ${};

#    sgml -> nosgml
#echo "Removing SGML markup...";
#echo 0 | map_py pipelines.maps.SGML nosgml_item ${BNC} ${BNC_NOMARKUP} && \
#echo "PoS tagging with TreeTagger...";
#echo 0 | map_cmd ${TREETAGGER} ${BNC_NOMARKUP} ${BNC_TAGS_RAW} && \
#echo "Transforming raw TreeTagger output to WTLs...";
#echo 0 | map_py pipelines.maps.TreeTagger treetagger_to_wtl_item ${BNC_TAGS_RAW} ${BNC_TAGS} && \
#echo "Deleting raw tag files...";
#echo 0 | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${BNC_TAGS_RAW};
#echo "Tokenizing...";
#echo 0 | map_py pipelines.maps.TreeTagger words_item ${BNC_TAGS} ${BNC_TOKEN} && \
#echo "Applying Stanford parser...";
#echo 0 | map_cmd "\"${STANFORD_PARSER} <(cat)\"" ${BNC_TOKEN} ${BNC_STANFORD_RAW} && \
echo "Converting raw Stanford output to StanfordDependencies...";
echo 0 | map_py pipelines.maps.StanfordDependencies raw_Stanford_to_Dependencies_item ${BNC_STANFORD_RAW} ${BNC_STANFORD} && \
echo "Extracting phrases from StanfordDependencies...";
echo 0 | map_py pipelines.maps.Sentences phrases_from_StanfordDependencies_item ${BNC_STANFORD} ${BNC_SENTS_STANFORD}


