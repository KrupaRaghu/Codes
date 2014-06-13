import shutil
import os, os.path
from pipelines.formats.Sentences import *

def add_ID_file(item, ID_attr):
	item.set_attribute(ID_attr, item.ID)

def extract_text_from_sent_attr(item, sent_attr, one_per_line = False):
	sents = item.get_attribute(sent_attr, Sentences)
	print sents.get_text(one_per_line=one_per_line)
