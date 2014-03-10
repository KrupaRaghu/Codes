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
echo "Applying Stanford parser...";
echo 0 | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c "\"${STANFORD_PARSER} <(cat)\"" -a ${BNC_TOKEN} -o ${BNC_STANFORD_RAW} --print-reasons --overwrite
#echo 0 | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c '"/home/andrea/studium/tools/stanford-parser/lexparser.sh <(cat)"' -a ${BNC_TOKEN} -o ${BNC_STANFORD_RAW} --print-reasons --overwrite
