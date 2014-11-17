echo 3212 | dm-reduce -r /data/corpora/CaptionGenerationCorpus -m pipelines.Codes.length -f length_extract -a captions=caption_tokenized,output_attr=length_obt
