from ..formats.BoW import *

def text_to_bow(text):
    """Transforms a text to a bag of words representation."""
    return BoW.from_text(text)
