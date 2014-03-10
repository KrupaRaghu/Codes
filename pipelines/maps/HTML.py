#NOHTML
import HTMLParser
import re
from pprint import pprint

def nohtml_item(item, in_attr = "html", out_attr = "nohtml"):
    text = item.get_attribute(in_attr)
    item.set_attribute(out_attr, nohtml(text))

def nohtml(text):
    """
    Transforms the string text by removing all HTML markup. Returns string.
    """
    parser = DataHTMLParser()
#    print "nohtml"
    #pprint(text)
    parser.feed(text)
    out = filter(lambda x: not re.match(HTML_PARSING_EXCLUDE_REGEXP, x), parser.txt)
    parser.close()
#    pprint(out)
    return " ".join(out)

#An HTML parser for our data
class DataHTMLParser(HTMLParser.HTMLParser):
    def __init__(self):
        self.txt = []
        HTMLParser.HTMLParser.__init__(self)

    def handle_data(self, data):
#       print "HTML PARSER", data
        if data:
            self.txt.append(data.strip())

HTML_PARSING_EXCLUDE_REGEXP = r'^\s*$'
