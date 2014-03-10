#!/bin/bash
#Preprocessing of BNC documents.
#Include experiment definitions.
. experiment_config.sh
# Get BNC data split:
# dm-getsplit -r ${CORPUS} -s ${BNCSPLIT}
# Keep all HAVING attribute:
# dm-itemfilterbyattr -r ${CORPUS} -a ${} --pos
# Keep all NOT HAVING attribute:
# dm-itemfilterbyattr -r ${CORPUS} -a ${} --neg
# Parallelize via "parallel [command]"

#    sgml -> nosgml
echo "Removing SGML markup..." && \
dm-getsplit -r ${CORPUS} -s ${BNCSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${BNC_NOMARKUP} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.SGML -f nosgml_item -a in_attr=${BNC},out_attr=${BNC_NOMARKUP} && \
echo "Done." && \
#    nosgml -> tagged_raw
echo "PoS tagging with TreeTagger..." && \
dm-getsplit -r ${CORPUS} -s ${BNCSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${BNC_TAGS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c ${TREETAGGER} -a ${BNC_NOMARKUP} -o ${BNC_TAGS_RAW} --print-reasons && \
echo "Done." && \
#    remove nosgml (optional)
#echo "Deleting NOSGML files..." && \
#dm-getsplit -r ${CORPUS} -s ${BNCSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${BNC_NOMARKUP} --pos | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${BNC_NOMARKUP} && \
#echo "Done." && \
#    tagged_raw -> tagged
echo "Transforming raw TreeTagger output to WTLs..." && \
dm-getsplit -r ${CORPUS} -s ${BNCSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${BNC_TAGS} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f treetagger_to_wtl_item -a in_attr=${BNC_TAGS_RAW},out_attr=${BNC_TAGS} && \
echo "Done." && \
#    remove tagged_raw
echo "Deleting raw tag files..." && \
dm-getsplit -r ${CORPUS} -s ${BNCSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${BNC_TAGS_RAW} --pos | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${BNC_TAGS_RAW}
echo "Done." && \
#    tagged -> tokenized
echo "Tokenizing..." && \
dm-getsplit -r ${CORPUS} -s ${BNCSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${BNC_TOKEN} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f words_item -a in_attr=${BNC_TAGS},out_attr=${BNC_TOKEN} && \
echo "Done." && \
#    tokenized -> sentences_nophrase
echo "Extracting basic sentences from tokens..." && \
dm-getsplit -r ${CORPUS} -s ${BNCSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${BNC_SENTS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.Sentences -f tokens_to_Sentences_item -a in_attr=${BNC_TOKEN},out_attr=${BNC_SENTS_RAW} && \
echo "Done." && \
#    tokenized -> stanford_raw
map_files ${STANFORD_PARSER} ${CORPUS} ${BNC_TOKEN} ${BNC_STANFORD_RAW}

#    typed_dependencies_raw -> typed_dependencies

#    remove typed_dependencies_raw (optional)
# dm-itemdelattr -r ${CORPUS} -a ${BNC_NOMARKUP}

#    typed_dependencies -> phrases

