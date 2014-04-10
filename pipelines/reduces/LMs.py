from data_manager.templates import fill
from pipelines.experiment_config import TEMPLATE_DIR

def make_FMA_cheating_LMs(itemiterator, cap_cnt_attr, w_cap_cnt, w_zero, beta, uni_file, tri_file, out_attr):
	FMA_template = TEMPLATE_DIR+"FL_FMA_lm.template"
	lm_uni_template = TEMPLATE_DIR+"absdisc_lm.template"
	tree_template = TEMPLATE_DIR+"tree.template"
	#Names in the LM are equal to regular FMA FL LM, for simplicity.
	for item in itemiterator:
		name = item.get_attribute("original_name").strip()
		uni_name = name+"_AllLDAZero"
		tree_name = name+"_caption_Uni_tree"
		zero_name = name+"_Zero"
		zero_def = fill(TEMPLATE_DIR+"zero_lm.template", name=zero_name).strip()
		tree_def = fill(tree_template, tree_name=tree_name, tree_file=item.get_attribute_path(cap_cnt_attr)).strip()
		uni_def = fill(lm_uni_template, name=uni_name, tree=tree_name, tree_def=tree_def, M=1, backoff_name=zero_name, backoff_def=zero_def, disc=0).strip()
		FMA_def = fill(FMA_template, name=name, lda_def=uni_def, uni_file=uni_file, tri_file=tri_file, beta=beta).strip()
		item.set_attribute(out_attr, FMA_def)

def make_FMA_FL_LMs(itemiterator, dDoc_attr, w_dDoc, dImg_attr, w_dImg, dMix_attr, w_dMix, w_Zero, beta, tri_file, uni_file, out_attr):
	LDA_template = TEMPLATE_DIR+"LDA_full_nomain.template"
	FMA_template = TEMPLATE_DIR+"FL_FMA_lm.template"
	
	for item in itemiterator:
		name = item.get_attribute("original_name")
		def_lda = fill(LDA_template, name=name, w_dDoc=w_dDoc, w_dImg=w_dImg, w_dMix=w_dMix, w_Zero=w_Zero, dDoc_file=item.get_attribute_path(dDoc_attr), dImg_file=item.get_attribute_path(dImg_attr), dMix_file=item.get_attribute_path(dMix_attr))
		def_fma = fill(FMA_template, name=name, beta=beta, lda_def=def_lda.strip(), uni_file=uni_file, tri_file=tri_file)
		item.set_attribute(out_attr, def_fma)
