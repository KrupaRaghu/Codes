from ..formats.StanfordDependencies import *
import re

def raw_Stanford_to_Dependencies_item(item, in_attr="stanford_raw", out_attr="stanford"):
    string = item.get_attribute(in_attr)
    item.set_attribute(out_attr, raw_Stanford_to_Dependencies(string))

def raw_Stanford_to_Dependencies(string):
    """Parses output from Stanford parser with formats wordsAndTags and typedDependencies"""
    #Extract every other sentence as tagged sentence, the next one as its dependencies.
    if string.__class__ == str:
	string = string.decode("utf-8")
    tagged = []
    depnds = []
    empties = 0
    sent_next = True
    cur_deps = []
    in_deps = False
    for i,line in enumerate(string.split("\n")):
	if not in_deps:
	    if line:
		tagged.append(line)
		in_deps = True
		empties = 0
		cur_deps = []
	    else:
		empties = empties + 1
	else:
	     if line:
		cur_deps.append(line)
	     else:
		empties = empties + 1
	     if empties > 1:
		depnds.append(cur_deps)
		cur_deps = []
		in_deps = False
    dependencies = zip(tagged, depnds)
    #Extract word at each position, tag at each position, and dependencies of each word
    W = []
    T = []
    D = []
    for dependency in dependencies:
        sent = dependency[0].split()
        if not sent:
            continue
        sent_deps = dependency[1]
        if not sent_deps:
            continue
        words = []
        tags = []
        deps = {}
        deps_out = []
        for dep in sent_deps:
	    #print "DEP", dep
            stuff = re.findall(TYPED_DEPS_REGEXP, dep)
            if len(stuff) != 3:
                continue
            if stuff[1] not in deps:
                deps[stuff[1]] = []
            #print "STUFF", stuff
	    p1 = int(stuff[1].split("-")[-1])
            w1 = "-".join(stuff[1].split("-")[0:-1])
            p2 = int(stuff[2].split("-")[-1])
            w2 = "-".join(stuff[2].split("-")[0:-1])

            deps[stuff[1]].append((stuff[0], p1, p2))
                
        for i,w in enumerate(sent):
            x = w.split("/")
            w = "/".join(x[0:-1])
            words.append((i+1,w))
            tags.append(x[-1])
            deps_out.append(deps.get(w+"-"+str(i+1),[]))
        W.append(words)
        T.append(tags)
        D.append(deps_out)
    return StanfordDependencies(W, T, D)

