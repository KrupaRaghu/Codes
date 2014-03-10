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
echo "PoS tagging with TreeTagger..." && \
dm-getsplit -r ${CORPUS} -s ${BNCSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${BNC_TAGS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c ${TREETAGGER} -a ${BNC_NOMARKUP} -o ${BNC_TAGS_RAW} --print-reasons && \
echo "Done."

