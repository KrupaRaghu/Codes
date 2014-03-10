

def latin_1_to_unicode(item, in_attr, out_attr):
    item.set_attribute(out_attr, item.get_attribute(in_attr).decode("latin-1"))
