echo 3212 | dm-reduce -r /data/corpora/CaptionGenerationCorpus -m pipelines.Codes.Caption_Generation -f generate_captions -a words_attr=words_extracted_test,beam_size=500,output_attr=captions_sample
