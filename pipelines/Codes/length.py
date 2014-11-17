from data_manager.OSM import *

def length_extract(itemiterator, captions, output_attr):
	for i in itemiterator:
		C = i.get_attribute(captions).strip()
		i.set_attribute(output_attr, len(C))
