#!/bin/bash
#Preprocessing of BBC documents.
#Include experiment definitions.
. experiment_config.sh
# Get BBC data split: split into test, dev, train. Handle each split separately.
# dm-getsplit -r ${CORPUS} -s ${DEVSPLIT}
# dm-getsplit -r ${CORPUS} -s ${TESTSPLIT}
# dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT}
# Keep all HAVING attribute:
# dm-itemfilterbyattr -r ${CORPUS} -a ${} --pos
# Keep all NOT HAVING attribute:
# dm-itemfilterbyattr -r ${CORPUS} -a ${} --neg
# Parallelize via
# parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r /home/andrea/studium/BA_EXPERIMENTS/corpus -m pipelines.maps.SGML -f nosgml_item -a in_attr=data,out_attr=BNC

#    html -> nohtml on test, training, and dev
echo "Removing HTML from documents..." && \
dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_NOMARKUP} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.HTML -f nohtml_item -a in_attr=${DOC},out_attr=${DOC_NOMARKUP} && \
 dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_NOMARKUP} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.HTML -f nohtml_item -a in_attr=${DOC},out_attr=${DOC_NOMARKUP} && \
 dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_NOMARKUP} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.HTML -f nohtml_item -a in_attr=${DOC},out_attr=${DOC_NOMARKUP} && \
#    nohtml -> tagged_raw on test, training, and dev
echo "Applying TreeTagger to documents..." && \
 dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TAGS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c ${TREETAGGER} -a ${DOC_NOMARKUP} -o ${DOC_TAGS_RAW} --print-reasons && \
 dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TAGS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c ${TREETAGGER} -a ${DOC_NOMARKUP} -o ${DOC_TAGS_RAW} --print-reasons && \
 dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TAGS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c ${TREETAGGER} -a ${DOC_NOMARKUP} -o ${DOC_TAGS_RAW} --print-reasons && \
#   captions -> tagged_raw on test, training, and dev
echo "Applying TreeTagger to captions..." && \
 dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TAGS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c ${TREETAGGER} -a ${CAP_NOMARKUP} -o ${CAP_TAGS_RAW} --print-reasons && \
 dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TAGS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c ${TREETAGGER} -a ${CAP_NOMARKUP} -o ${CAP_TAGS_RAW} --print-reasons && \
 dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TAGS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c ${TREETAGGER} -a ${CAP_NOMARKUP} -o ${CAP_TAGS_RAW} --print-reasons && \
#    remove nohtml (optional)
#echo "Removing NOHTML versions..." && \
# dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_NOMARKUP} --pos | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${DOC_NOMARKUP} && \
# dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_NOMARKUP} --pos | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${DOC_NOMARKUP} && \
# dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_NOMARKUP} --pos | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${DOC_NOMARKUP} && \
#    tagged_raw -> tagged for docs on test, train, and dev
echo "Transforming raw tagger output to WTLs..." && \
dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TAGS} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f treetagger_to_wtl_item -a in_attr=${DOC_TAGS_RAW},out_attr=${DOC_TAGS} && \
dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TAGS} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f treetagger_to_wtl_item -a in_attr=${CAP_TAGS_RAW},out_attr=${CAP_TAGS} && \
dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TAGS} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f treetagger_to_wtl_item -a in_attr=${DOC_TAGS_RAW},out_attr=${DOC_TAGS} && \
dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TAGS} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f treetagger_to_wtl_item -a in_attr=${CAP_TAGS_RAW},out_attr=${CAP_TAGS} && \
dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TAGS} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f treetagger_to_wtl_item -a in_attr=${DOC_TAGS_RAW},out_attr=${DOC_TAGS} && \
dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TAGS} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f treetagger_to_wtl_item -a in_attr=${CAP_TAGS_RAW},out_attr=${CAP_TAGS} && \
#    remove tagged_raw (optional)
#echo "Removing raw tagged output..." && \
# dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TAGS_RAW} --pos | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${DOC_TAGS_RAW} && \
# dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TAGS_RAW} --pos | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${DOC_TAGS_RAW} && \
# dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TAGS_RAW} --pos | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${DOC_TAGS_RAW} && \
# dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TAGS_RAW} --pos | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${CAP_TAGS_RAW} && \
# dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TAGS_RAW} --pos | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${CAP_TAGS_RAW} && \
# dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TAGS_RAW} --pos | parallel --progress -N 1 --pipe --round-robin -j 8 dm-itemdelattr -r ${CORPUS} -a ${CAP_TAGS_RAW} && \
#    tagged -> tokenized on captions and documents for test, train, and split
echo "Tokenizing..." && \
dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TOKEN} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f words_item -a in_attr=${DOC_TAGS},out_attr=${DOC_TOKEN} && \
dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TOKEN} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f words_item -a in_attr=${DOC_TAGS},out_attr=${DOC_TOKEN} && \
dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_TOKEN} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f words_item -a in_attr=${DOC_TAGS},out_attr=${DOC_TOKEN} && \
dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TOKEN} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f words_item -a in_attr=${CAP_TAGS},out_attr=${CAP_TOKEN} && \
dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TOKEN} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f words_item -a in_attr=${CAP_TAGS},out_attr=${CAP_TOKEN} && \
dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_TOKEN} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f words_item -a in_attr=${CAP_TAGS},out_attr=${CAP_TOKEN} && \
# Filter nouns, verbs, and adjectives from training (and dev?) set
echo "Filtering nouns, verbs, and adjectives" && \
dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_NVA} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f filter_nva_item -a in_attr=${CAP_TAGS},out_attr=${CAP_NVA} && \
dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_NVA} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f filter_nva_item -a in_attr=${CAP_TAGS},out_attr=${CAP_NVA} && \
dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_NVA} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f filter_nva_item -a in_attr=${DOC_TAGS},out_attr=${DOC_NVA} && \
dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_NVA} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f filter_nva_item -a in_attr=${DOC_TAGS},out_attr=${DOC_NVA} && \
# Extract lemmas from NVA-filtered data
echo "Extracting lemmas from NVA-filtered data..." && \
dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_NVA_LEM} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f lemmas_item -a in_attr=${CAP_NVA},out_attr=${CAP_NVA_LEM} && \
dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_NVA_LEM} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f lemmas_item -a in_attr=${CAP_NVA},out_attr=${CAP_NVA_LEM} && \
dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_NVA_LEM} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f lemmas_item -a in_attr=${DOC_NVA},out_attr=${DOC_NVA_LEM} && \
dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_NVA_LEM} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.TreeTagger -f lemmas_item -a in_attr=${DOC_NVA},out_attr=${DOC_NVA_LEM} && \
#    tokenized -> sentences_nophrase
echo "Building simple sentences from tokenization..." && \
dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${DOC_SENTS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.Sentences -f tokens_to_Sentences_item -a in_attr=${DOC_TOKEN},out_attr=${DOC_SENTS_RAW} && \
dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_SENTS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.Sentences -f tokens_to_Sentences_item -a in_attr=${CAP_TOKEN},out_attr=${CAP_SENTS_RAW} && \
dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_SENTS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.Sentences -f tokens_to_Sentences_item -a in_attr=${CAP_TOKEN},out_attr=${CAP_SENTS_RAW} && \
dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${CAP_SENTS_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.Sentences -f tokens_to_Sentences_item -a in_attr=${CAP_TOKEN},out_attr=${CAP_SENTS_RAW} && \
# Preprocess the images
#    pgm -> raw_SIFT on train, test, dev
echo "Extracting raw SIFT from images..." && \
 dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${IMG_SIFT_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c ${SIFT} -a ${IMG} -o ${IMG_SIFT_RAW} --print-reasons && \
 dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${IMG_SIFT_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c ${SIFT} -a ${IMG} -o ${IMG_SIFT_RAW} --print-reasons && \
 dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${IMG_SIFT_RAW} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c ${SIFT} -a ${IMG} -o ${IMG_SIFT_RAW} --print-reasons && \
#    raw_SIFT -> SIFT on train, test, dev
echo "Transforming raw SIFT into SIFT..." && \
dm-getsplit -r ${CORPUS} -s ${TRAINSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${IMG_SIFT} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.SIFT -f convert_to_SIFT_item -a in_attr=${IMG_SIFT_RAW},out_attr=${IMG_SIFT} && \
dm-getsplit -r ${CORPUS} -s ${TESTSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${IMG_SIFT} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.SIFT -f convert_to_SIFT_item -a in_attr=${IMG_SIFT_RAW},out_attr=${IMG_SIFT} && \
dm-getsplit -r ${CORPUS} -s ${DEVSPLIT} | dm-itemfilterbyattr -r ${CORPUS} -a ${IMG_SIFT} --neg | parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m pipelines.maps.SIFT -f convert_to_SIFT_item -a in_attr=${IMG_SIFT_RAW},out_attr=${IMG_SIFT} && \
echo "Done." && \
#    tokenized -> stanford_raw
#map_files ${STANFORD_PARSER} ${CORPUS} ${CAP_TOKEN} ${CAP_STANFORD_RAW} && \
#map_files ${STANFORD_PARSER} ${CORPUS} ${DOC_TOKEN} ${DOC_STANFORD_RAW}
get_filter_neg ${TRAINSPLIT} ${DOC_STANFORD_RAW} | map_cmd "${STANFORD_PARSER} <(cat)" ${DOC_TOKEN} ${DOC_STANFORD_RAW}

# TRANSFORMATIONS NOT IMPLEMENTED YET
#    typed_dependencies_raw -> typed_dependencies

#    remove typed_dependencies_raw (optional)
# dm-itemdelattr -r ${CORPUS} -a ${BNC_NOMARKUP}

#    typed_dependencies -> phrases
