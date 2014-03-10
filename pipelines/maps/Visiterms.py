
def SIFT_to_visiterms_item(item, labeler, in_attr="sift", out_attr="visiterms"):
    sift = item.get_attribute(in_attr)
    item.set_attribute(out_attr, SIFT_to_visiterms(labeler, sift))

def SIFT_to_visiterm_indices_item(item, labeler, in_attr="sift", out_attr="visiterms"):
    sift = item.get_attribute(in_attr)
    item.set_attribute(out_attr, SIFT_to_visiterm_indices(labeler, sift))

def SIFT_to_visiterm_indices(visiterm_labeler, SIFT):
    return visiterm_labeler.make_indexed_text(SIFT)

def SIFT_to_visiterms(visiterm_labeler, SIFT):
    return visiterm_labeler.make_visual_text(SIFT)
