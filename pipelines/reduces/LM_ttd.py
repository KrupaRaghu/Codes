from data_manager.templates import fill
from pipelines.exp_config import TEMPLATE_DIR, SENTENCE_START

def LMs_FMA(itemiterator, out_attr, cnt_tree1, cnt_tree2, cnt_tree3, KNM2_tree, KNM3_tree):
#	FMA_template = TEMPLATE_DIR+"FL_FMA_lm.template"
#	lm_uni_template = TEMPLATE_DIR+"lm_uni_lm.template"	
#	tree_template = TEMPLATE_DIR+"tree.template"

	for item in itemiterator:
		
		name1 = item.get_attribute("original_name").strip()
		tree_name = name1+"_caption_Uni_tree"
		tree_def = fill(TEMPLATE_DIR+"template1",name1=name1, tree_name=tree_name,cnt_tree3=name1+'_cnt_tree3', path_cnt3=item.get_attribute_path(cnt_tree3), cnt_tree2=name1+'_cnt_tree2', path_cnt2=item.get_attribute_path(cnt_tree2), cnt_tree1=name1+'_cnt_tree1', path_cnt1=item.get_attribute_path(cnt_tree1), KNM2_tree=name1+'_KNM2_tree', path_KNM2=item.get_attribute_path(KNM2_tree), KNM3_tree=name1+'_KNM3_tree', path_KNM3=item.get_attribute_path(KNM3_tree), Bi_KN=name1+'_Bi_KN',Uni_KN=name1+'_Uni_KN',zero_kn=name1+'_zero_kn').strip()
#		FMA_def = fill(FMA_template, name1=name1).strip()
		item.set_attribute(out_attr, tree_def)
