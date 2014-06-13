from data_manager.templates import fill
from pipelines.experiment_config import TEMPLATE_DIR,SENTENCE_START

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

from ..LM_WEIGHTS import *

def make_LDA_dDoc_lms(itemiterator, dDoc_prob_attr, out_attr, w_dDoc = W_DOC_DOCZEROLM, w_Zero = W_ZERO_DOCZEROLM):
	LDA_template = TEMPLATE_DIR+"LDA_dDocZero.template"
    	for item in itemiterator:
		print item.ID, item.get_attribute_path(dDoc_prob_attr)
		LM_def = fill(LDA_template, name=item.get_attribute("original_name", unicode).strip(), w_dDoc=w_dDoc, w_Zero=w_Zero, probfile=item.get_attribute_path(dDoc_prob_attr))
		item.set_attribute(out_attr, LM_def)

def make_LDA_all_lms(itemiterator, dDoc_prob_attr, dMix_prob_attr, dImg_prob_attr, out_attr, w_dDoc = W_DOC_LDAZEROLM, w_dImg=W_IMG_LDAZEROLM, w_dMix=W_MIX_LDAZEROLM, w_Zero = W_ZERO_LDAZEROLM):
	LDA_template = TEMPLATE_DIR+"LDA_full.template"
	for item in itemiterator:
		def_lda = fill(LDA_template, name=item.get_attribute("original_name", unicode).strip(), w_dDoc=w_dDoc, w_dImg=w_dImg, w_dMix=w_dMix, w_Zero=w_Zero, dDoc_file=item.get_attribute_path(dDoc_prob_attr), dImg_file=item.get_attribute_path(dImg_prob_attr), dMix_file=item.get_attribute_path(dMix_prob_attr))
		item.set_attribute(out_attr, def_lda)

def make_trigram_caption_lms(itemiterator, cnt_attr, out_attr):
	tree_template = TEMPLATE_DIR+"tree.template"
	LM_template = TEMPLATE_DIR+"absdisc_lm.template"
	zero_template = TEMPLATE_DIR+""
	for item in itemiterator:
		tri_name = item.get_attribute("original_name").strip()+"_CaptionTrigram"

		treefile = item.get_attribute_path(cnt_attr)
		tree_name = item.get_attribute("original_name").strip()+"_CaptionTree"
		tree_def = fill(tree_template, tree_name=tree_name, tree_file=treefile)
		
		zero_name = item.get_attribute("original_name").strip()+"_Zero"
		zero_def = fill(TEMPLATE_DIR+"zero_lm.template", name=zero_name).strip()
		
		LM_3 = fill(LM_template, sent_beg = SENTENCE_START, name=tri_name, tree=tree_name, tree_def=tree_def, backoff_def=zero_def, backoff_name=zero_name, M=3, disc=0)
		out = fill(TEMPLATE_DIR+"main.template", lmname=tri_name, lmdef=LM_3).strip()
		item.set_attribute(out_attr, out)


def make_trigram_document_lms(itemiterator, cnt_attr, out_attr, bg_trigram_file, bg_trigram_name, bg_weight = 0.5):
	tree_template = TEMPLATE_DIR+"tree.template"
	LM_template = TEMPLATE_DIR+"absdisc_lm.template"
	for item in itemiterator:
		tri_name = item.get_attribute("original_name").strip()+"_DocumentTrigram"

		treefile = item.get_attribute_path(cnt_attr)
		tree_name = item.get_attribute("original_name").strip()+"_DocumentTree"
		tree_def = fill(tree_template, tree_name=tree_name, tree_file=treefile).strip()
		
		bg_trigram = fill(TEMPLATE_DIR+"include_lm.template", lmname=bg_trigram_name, lmfile=bg_trigram_file).strip()
		
		LM_3 = fill(LM_template, sent_beg = SENTENCE_START, name=tri_name, tree=tree_name, tree_def=tree_def, backoff_name=tri_name+"_Zero", backoff_def=fill(TEMPLATE_DIR+"zero_lm.template", name=tri_name+"_Zero").strip(), M=3, disc=0).strip()

		linear_lm = fill(TEMPLATE_DIR+"linear_lm.2.template", name=tri_name+"_main", lm1_name=tri_name, lm1_weight=1-float(bg_weight), lm1_def=LM_3, lm2_name=bg_trigram_name, lm2_weight=bg_weight, lm2_def=bg_trigram).strip()

		out = fill(TEMPLATE_DIR+"main.template", lmname=tri_name+"_main", lmdef=linear_lm).strip()
		item.set_attribute(out_attr, out)
