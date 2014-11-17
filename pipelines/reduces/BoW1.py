from pipelines.formats.BoW1 import BoW
from pipelines.formats.Sentences1 import *
from pprint import pprint

def compute_joint_BoW(itemiterator, attributes, content_format="text"):
    out = BoW({})
    for item in itemiterator:
        for attribute in attributes:
            if content_format == "text":
                bow = BoW(item.get_attribute(attribute).split())
                out.update(bow)
            elif content_format == "sentences":
                bow = BoW(item.get_attribute(attribute, Sentences).get_text().split())
                out.update(bow)
            elif content_format == "BoW":
                out.update(item.get_attribute(attribute, BoW))
    return out

def join_BoWs(bowiterator):
    """Returns one large bag of words constructed by joining together all input bags of words."""
    out = BoW({})
    for bow in bowiterator:
        out.update(bow)
    return out


