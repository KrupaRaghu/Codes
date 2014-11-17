dm-getsplit -r /data/corpora/CaptionGenerationCorpus -s dev | dm-reduce -r /data/corpora/CaptionGenerationCorpus -m pipelines.reduces.LM_ttd -f LMs_FMA -a cnt_tree1=indextocnt1_dev.cnt,cnt_tree2=indextocnt2_dev.cnt,cnt_tree3=indextocnt3_dev.cnt,KNM2_tree=KN.M2_dev.cnt,KNM3_tree=KN.M3_dev.cnt,out_attr=output_dev





