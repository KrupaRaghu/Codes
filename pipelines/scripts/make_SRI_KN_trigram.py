from data_manager.templates import fill
from pipelines.experiment_config import TEMPLATE_DIR

basefile = "/nethome/afischer/BA/components/Ngrams/training_background.%s.cnt"

m3_reg = basefile % ("M3")
m2_reg = basefile % ("M2")
m1_reg = basefile % ("M1")

m3_kn = basefile % ("M3.kn")
m2_kn = basefile % ("M2.kn")

print fill(TEMPLATE_DIR+"SRI_trigram.template", name="trigram_background_full", tree_name="trigram_background_full_tree", kn_tree_m3_file=m3_kn, kn_tree_m2_file=m2_kn, tree_m3_file=m3_reg, tree_m2_file=m2_reg, tree_m1_file=m1_reg)
