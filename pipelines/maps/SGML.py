#NOSGML
import re, htmlentitydefs

def nosgml(text):
    """
    Transforms the string text by removing all SGML markup. Returns string.
    """
    s = find_sgml_sentences(text)
    s = map(remove_sgml_nospace_pun_tags, s)
    s = map(remove_sgml_space_pun_tags, s)
    s = map(get_words_from_sgml,s)
    s = map(lambda x:" ".join(x.split()), s)
    return "\n".join(s)

def nosgml_item(item, in_attr = "sgml", out_attr = "nosgml"):
    text = item.get_attribute(in_attr)
    item.set_attribute(out_attr, nosgml(text))

def nosgml_ap_item(item, in_attr = "sgml", out_attr = "nosgml"):
    text = item.get_attribute(in_attr)
    raw_text = "\n".join(text.split("<TEXT>")[1].split("\n")[0:-2])
    item.set_attribute(out_attr, nosgml(raw_text))

# SGML regexps
SGML_SENTENCE_REGEXP = r"""<s .*\n"""
SGML_PUN_NOSPACE_REGEXP = r"<c PUN>|<c PUR>"
SGML_PUN_SPACE_REGEXP = r"<c[^>]*>"
SGML_WORD_REGEXP = r"<w.*?>[^<]*"

def replace_SGML_codes(text):
    text = unescape(text)
    for (x,y) in conv.iteritems():
        text = text.replace("&"+x+";", y) 
    return text

def get_words_from_sgml(text):
    content = ""
    wtemp = re.findall(SGML_WORD_REGEXP, text)
    for w in wtemp:
        content = content+replace_SGML_codes(w.split(">")[1])
    return content

def remove_sgml_space_pun_tags(text):
    return re.sub(SGML_PUN_SPACE_REGEXP, " ", text)

def remove_sgml_nospace_pun_tags(text):
    return re.sub(SGML_PUN_NOSPACE_REGEXP, "", text)

def find_sgml_sentences(text):
    X = re.findall(SGML_SENTENCE_REGEXP, text)
    out=[]
    for x in X:
        out.append(x)
    return out

#Adopted from http://effbot.org/zone/re-sub.htm#unescape-html
#Credits and thanks to Fredrik Lundh
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

# SGML to text or HTML conversions
conv = {}
conv['ast']= "*"
conv['equals']= "="
conv['percnt']= "%"
conv['plus']= "+"
conv['sol']= "/"
conv['half']= "&#189"
conv['horbar']= "[horbar]"
conv['lowbar']= "_"
conv['dash']= "-"
conv['Aacute']= "&#193"
conv['aacute']= "&#225"
conv['abreve']= "[abreve]"
conv['Acirc']= "&#194"
conv['acirc']= "&#226"
conv['acute']= "&#180"
conv['AElig']= "&#198"
conv['aelig']= "&#230"
conv['agr']= "[agr ]"
conv['Agrave']= "&#192"
conv['agrave']= "&#224"
conv['Amacr']= "[Amacr ]"
conv['amacr']= "[amacr ]"
conv['amp']= "&"
conv['ape']= "[ape ]"
conv['aogon']= "[aogon ]"
conv['Aring']= "&#197"
conv['aring']= "&#229"
conv['atilde']= "&#227"
conv['Auml']= "&#196"
conv['auml']= "&#228"
conv['Bgr']= "[Bgr ]"
conv['bgr']= "[bgr ]"
conv['bquo']= ' " '
conv['bsol']= "&#92"
conv['bull']= "[bull ]"
conv['cacute']= "[cacute]"
conv['Ccaron']= "[Ccaron]"
conv['ccaron']= "[ccaron]"
conv['Ccedil']= "&#199"
conv['ccedil']= "&#231"
conv['ccirc']= "[ccirc ]"
conv['cent']= "&#162"
conv['check']= "[check ]"
conv['cir']= "[cir ]"
conv['circ']= "&#94"
conv['commat']= "@"
conv['copy']= "&#169"
conv['darr']= "[darr ]"
conv['dcaron']= "[dcaron]"
conv['deg']= "&#176"
conv['Dgr']= "[Dgr ]"
conv['dgr']= "[dgr ]"
conv['die']= "&#168"
conv['divide']= "&#247"
conv['dollar']= "&#36"
conv['dstrok']= "[dstrok]"
conv['dtrif']= "[dtrif ]"
conv['Eacute']= "&#201"
conv['eacute']= "&#233"
conv['Ecaron']= "[Ecaron]"
conv['ecaron']= "[ecaron]"
conv['Ecirc']= "&#202"
conv['ecirc']= "&#234"
conv['eegr']= "[eegr ]"
conv['Egr']= "[Egr ]"
conv['egr']= "[egr ]"
conv['Egrave']= "&#200"
conv['egrave']= "&#232"
conv['Emacr']= "[Emacr ]"
conv['emacr']= "[emacr ]"
conv['eogon']= "[eogon ]"
conv['equo']= ' " '
conv['eth']= "&#240"
conv['Euml']= "&#203"
conv['euml']= "&#235"
conv['flat']= "[flat ]"
conv['formula']= "[formula]"
conv['frac12']= "&#189"
conv['frac13']= "[frac13]"
conv['frac14']= "&#188"
conv['frac15']= "[frac15]"
conv['frac16']= "[frac16]"
conv['frac17']= "[frac17]"
conv['frac18']= "[frac18]"
conv['frac19']= "[frac19]"
conv['frac23']= "[frac23]"
conv['frac25']= "[frac25]"
conv['frac34']= "&#190"
conv['frac35']= "[frac35]"
conv['frac38']= "[frac38]"
conv['frac45']= "[frac45]"
conv['frac47']= "[frac47]"
conv['frac56']= "[frac56]"
conv['frac58']= "[frac58]"
conv['frac78']= "[frac78]"
conv['ft']= "'"
conv['ge']= "[ge ]"
conv['Ggr']= "[Ggr ]"
conv['ggr']= "[ggr ]"
conv['grave']= "&#96"
conv['gt']= ">"
conv['Gt']= "[Gt ]"
conv['hearts']= "[hearts]"
conv['hellip']= "..."
conv['hstrok']= "[hstrok]"
conv['Iacute']= "&#205"
conv['iacute']= "&#237"
conv['Icirc']= "&#206"
conv['icirc']= "&#238"
conv['iexcl']= "&#161"
conv['igr']= "[igr ]"
conv['igrave']= "&#236"
conv['imacr']= "[imacr ]"
conv['infin']= "[infin ]"
conv['ins']= '"'
conv['iquest']= "&#191"
conv['Iuml']= "&#207"
conv['iuml']= "&#239"
conv['kgr']= "[kgr ]"
conv['khgr']= "[khgr ]"
conv['Lacute']= "[Lacute]"
conv['lacute']= "[lacute]"
conv['larr']= "[larr ]"
conv['lcub']= "{"
conv['le']= "[le ]"
conv['lgr']= "[lgr ]"
conv['lsqb']= "["
conv['Lstrok']= "[Lstrok]"
conv['lstrok']= "[lstrok]"
conv['lt']= "<"
conv['Lt']= "[Lt ]"
conv['mdash']= "-"
conv['Mgr']= "[Mgr ]"
conv['mgr']= "[mgr ]"
conv['micro']= "&#181"
conv['middot']= "&#183"
conv['nacute']= "[nacute]"
conv['natur']= "[natur ]"
conv['ncaron']= "[ncaron]"
conv['ncedil']= "[ncedil]"
conv['ndash']= "-"
conv['ngr']= "[ngr ]"
conv['Ntilde']= "&#209"
conv['ntilde']= "&#241"
conv['num']= "#"
conv['Oacute']= "&#211"
conv['oacute']= "&#243"
conv['Ocirc']= "&#212"
conv['ocirc']= "&#244"
conv['OElig']= "[OElig ]"
conv['oelig']= "[oelig ]"
conv['Ogr']= "[Ogr ]"
conv['ogr']= "[ogr ]"
conv['ograve']= "&#242"
conv['OHgr']= "[OHgr ]"
conv['ohgr']= "[ohgr ]"
conv['ohm']= "[ohm ]"
conv['omacr']= "[omacr ]"
conv['Oslash']= "&#216"
conv['oslash']= "&#248"
conv['Otilde']= "&#213"
conv['otilde']= "&#245"
conv['Ouml']= "&#214"
conv['ouml']= "&#246"
conv['Pgr']= "[Pgr ]"
conv['pgr']= "[pgr ]"
conv['PHgr']= "[PHgr ]"
conv['phgr']= "[phgr ]"
conv['plusmn']= "&#177"
conv['pound']= "&#163"
conv['Prime']= "[Prime ]"
conv['prime']= "[prime ]"
conv['PSgr']= "[PSgr ]"
conv['psgr']= "[psgr ]"
conv['quot']= ' " '
conv['racute']= "[racute]"
conv['radic']= "[radic ]"
conv['rarr']= "[rarr ]"
conv['Rcaron']= "[Rcaron]"
conv['rcaron']= "[rcaron]"
conv['rcub']= "}"
conv['reg']= "&#174"
conv['rehy']= "-"
conv['rgr']= "[rgr ]"
conv['rsqb']= "]"
conv['Sacute']= "[Sacute]"
conv['sacute']= "[sacute]"
conv['Scaron']= "[Scaron]"
conv['scaron']= "[scaron]"
conv['Scedil']= "[Scedil]"
conv['scedil']= "[scedil]"
conv['scirc']= "[scirc ]"
conv['sect']= "&#167"
conv['Sgr']= "[Sgr ]"
conv['sgr']= "[sgr ]"
conv['sharp']= "[sharp ]"
conv['sim']= "[sim ]"
conv['shilling']= "/-"
conv['sup1']= "&#185"
conv['sup2']= "&#178"
conv['sup3']= "&#179"
conv['szlig']= "&#223"
conv['tcaron']= "[tcaron]"
conv['tcedil']= "[tcedil]"
conv['tgr']= "[tgr ]"
conv['THgr']= "[THgr ]"
conv['thgr']= "[thgr ]"
conv['THORN']= "&#222"
conv['thorn']= "&#254"
conv['tilde']= "&#126"
conv['times']= "&#215"
conv['trade']= "[trade ]"
conv['Uacute']= "&#218"
conv['uacute']= "&#250"
conv['Ucirc']= "&#219"
conv['ucirc']= "&#251"
conv['Ugr']= "[Ugr ]"
conv['ugr']= "[ugr ]"
conv['ugrave']= "&#249"
conv['umacr']= "[umacr ]"
conv['uml']= "&#168"
conv['uring']= "[uring ]"
conv['Uuml']= "&#220"
conv['uuml']= "&#252"
conv['verbar']= "|"
conv['wcirc']= "[wcirc ]"
conv['xgr']= "[xgr ]"
conv['yacute']= "&#253"
conv['Ycirc']= "[Ycirc ]"
conv['ycirc']= "[ycirc ]"
conv['yen']= "&#165"
conv['Yuml']= "[Yuml ]"
conv['yuml']= "&#255"
conv['zacute']= "[zacute]"
conv['Zcaron']= "[Zcaron]"
conv['zcaron']= "[zcaron]"
conv['zdot']= "[zdot ]"
conv['Zgr']= "[Zgr ]"
conv['zgr']= "[zgr ]"
