from ..formats.SIFT import *

SIFT_COMMAND = "sift"

def convert_to_SIFT_item(item, in_attr = "sift_raw", out_attr="sift"):
    data = item.get_attribute(in_attr)
    item.set_attribute(out_attr, raw_SIFT_output_to_SIFT(data))

def raw_SIFT_output_to_SIFT(output):
    """Builds a SIFT item from the output"""
    return SIFT.from_SIFT_output(output)
