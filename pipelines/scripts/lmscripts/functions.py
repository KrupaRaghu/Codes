"""
Contains functions for transforming texts.
"""

from __future__ import division
import os
from definitions import *
import re
import subprocess
from math import sqrt, log
from scipy.stats import norm, poisson
from lsvlmc.lm_wrapper import LMWrapper
from collections import OrderedDict
from pprint import pprint
import shutil

def histogram(data):
    bins = {}
    for d in data:
        if d in bins:
            bins[d] = bins[d]+1
        else:
            bins[d] = 1
    return bins

def read_caption_lengths(listfile):
    files = read_filelist(listfile)
    lengths={}
    for f in files:
        cfile = open(f, "r")
        w = cfile.read().split()
        lengths[f] = len(w)
    return lengths

def read_bigram_probability_file(filename):
    cont = sentences_from_file(filename)
    res = {}
    for (a,b,c) in cont:
        if a not in res:
            res[a] = {}
        res[a][b] = float(c)
    return res

def read_probability_file(filename, ignore_first=True, idxed=True):
    def f(x):
        if idxed:
            return int(x)
        else:
            return x
    if ignore_first:
        return OrderedDict(map(lambda (a,b): (f(a), float(b)), sentences_from_file(filename)[1:]))
    else:
        return OrderedDict(map(lambda (a,b): (f(a), float(b)), sentences_from_file(filename)))

def read_bigram_probability_file(filename):
    cont = sentences_from_file(filename)
    res = {}

    for (w1, w2, p) in cont:
        if w1 not in res:
            res[w1] = {}
        res[w1][w2] = float(p)
    
    return res

def read_file(filename):
    f = open(filename, "r")
    data = f.read().strip()
    f.close()
    return data

def read_filelist(filename):
    return read_file(filename).split("\n")

def text_from_file(filename):
    f = open(filename, "r")
    data = f.read()
    f.close()
    return data

def text_to_file(filename, text):
    f = open(filename, "wb")
    f.write(text)
    f.close()

def sentences_to_file(filename, sentences):
    return text_to_file(filename, sentences_to_text(sentences))

def sentences_from_file(filename):
    return text_to_sentences(text_from_file(filename))

def text_to_sentences(content):
    return map(lambda x:x.split(), content.split("\n"))

def sentences_to_text(sentences):
    return "\n".join(map(lambda x:" ".join(x), sentences))

def apply_treetagger(text):
    """
    Applies treetagger and returns list of tuples with output.
    """
    p = subprocess.Popen(TREETAGGER_ARGS, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = open("/dev/null", "w"))
    (tagged, errors) = p.communicate(text)
    return filter(lambda x: len(x) > 0, map(lambda x: x.split(),tagged.split("\n")))

sent_ignore_tags = ["''"]
def wtl_to_sentences(keep_punct, wtl):
    """
    Splits list of treetagger output into list of lists of treetagger output tuples.
    """
    sents = []
    found_sent_tag = False
    cur_sent = []
    for l in wtl:
        if len(l) < 3:
            continue
        if l[1] not in sent_ignore_tags and found_sent_tag == True:
            sents.append(cur_sent)
            cur_sent = []
            found_sent_tag = False
        if l[1] == SENTENCE_TAG:
            if keep_punct:
                cur_sent.append(l)
            found_sent_tag = True
        else:
            cur_sent.append(l)
    if len(cur_sent) > 0:
        sents.append(cur_sent)
    return sents

def apply_to_sentences(f, sents):
    """
    Applies function f to each sentence in list of given sentences. Returns list of outputs of f.
    """
    result = []
    for s in sents:
        result.append(f(s))
    return result

def remove_by_tags(tags, wtl):
    """
    Filters the word-tag list wtl to include only tuples tagged NOT with one of the tag set tags.
    """
    result = []
    for l in wtl:
        if not l:
            continue
        if l[1] in tags:
            continue
        result.append(l)
    return result

def keep_by_tags(tags, wtl):
    """
    Filters the word-tag list wtl to include only tuples tagged with one of the tag set tags.
    """
    result = []
    for l in wtl:
        if not l:
            continue
        if len(l) < 3:
            continue
        if l[1] not in tags:
            continue
        result.append(l)
    return result

#NOHTML routines.
def nohtml(text):
    """
    Transforms the string text by removing all HTML markup. Returns string.
    """
    return " ".join(nohtml_wordlist(text))

def nohtml_wordlist(text):
    """
    Transforms the string text by removing all HTML markup. Returns list of words.
    """
    parser = DataHTMLParser()
    parser.feed(text)
    out = filter(lambda x: not re.match(EXCLUDE_REGEXP, x), parser.txt)
    parser.close()
    return out

#NOSGML routines.
def nosgml(text):
    s = find_sgml_sentences(text)
    s = map(remove_sgml_nospace_pun_tags, s)
    s = map(remove_sgml_space_pun_tags, s)
    s = map(get_words_from_sgml,s)
    s = map(lambda x:" ".join(x.split()), s)
    return "\n".join(s)

def replace_SGML_codes(text):
    for (x,y) in conv.iteritems():
        text = replace(text, "&"+x+";", y) 
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

def lemmas(wtl):
    """
    Returns the lemmas from the list of tuples wtl. Returns list of words.
    """
    lemmas = []
    for l in wtl:
        if not l:
            continue
        lemmas.append((l[2] if l[2] != "<unknown>" else l[0]))
    return lemmas

def words(wtl):
    """
    Returns the words from the list of tuples wtl. Returns list of words.
    """
    words = []
    for l in wtl:
        if not l:
            continue
        words.append(l[0])
    return words

def nva(wtl):
    """
    Returns only the nouns, verbs, and adjectives from wtl. Returns list of words.
    """
    return words(keep_by_tags(NVA_TAGS, wtl))

def lemmas_nva(wtl):
    """
    Returns the lemmas of nouns, verbs, and adjectives in wtl. Returns as list of words.
    """
    return lemmas(keep_by_tags(NVA_TAGS, wtl))

def get_tags_from_dependency_file(filename):
    raw = read_file(filename).split("\n\n")
    dep_raw = filter(lambda (i,x): i % 2 == 0, enumerate(raw))
    RE = r"\(([^\(\)]*) ([^\)\(]*)\)"
    return map(lambda (i,raw):re.findall(RE,raw), dep_raw)

def read_dependency_file(filename):
    raw = read_file(filename).split("\n\n")
    dep_raw = filter(lambda (i,x): i % 2 == 1, enumerate(raw))
    dep_raw = map(lambda (i,x): x.split("\n"), dep_raw)
    rel_RE = r"([^\(]*)\("
    w_RE = r"\((.+), (.+)\)"
    match = []
    for P in dep_raw:
        new = []
        for d in P:
            rel = re.findall(rel_RE, d)
            words = re.findall(w_RE,d) 
            for w in words:
                a = w[0]
                b = w[1]
                new.append((rel[0], a, b))
        match.append(new)
    return match

def get_word_num_from_str(w):
    x = w.split("-")
    word = "-".join(x[0:len(x)-1])
    num = x[-1]
    return word, int(num.strip("'"))

def function_phrases_c_if_d(infile):
    """Yields a function that returns probabilities for phrases being part of a caption if they are also part of the document."""
    probabilities = read_probability_file(infile)

    def f(p):
        prob = 0.0
        for w in p:
            prob = prob * probabilities[w]
        return prob
    return f

def get_gaussian_from_file(infile):
    var = dict(map(lambda x:x.split(":"),read_file(infile).split()))
    m = float(var["M"])
    v = float(var["V"])
    
    d = sqrt(v)
    return norm(loc=[m], scale=d)

def gaussian_model_from_file(infile):
    f = get_gaussian_from_file(infile)

    def p(x):
        v = f.pdf(x)
        return v[0]
    return p

def get_poisson_from_file(infile):
    var = dict(map(lambda x:x.split(":"),read_file(infile).split()))
    return poisson(float(var["lambda"]))

def poisson_model_from_file(infile):
    f = get_poisson_from_file(infile)
    return f.pmf

def histogram_model_from_file(infile):
    var = dict(map(lambda x: (int(x.split(":")[0]), float(x.split(":")[1])),read_file(infile).split()))
    def p(x):
        if x in var:
            return var[x]
        else:
            return 0.0
    return p

def get_length_model(modelfile):
    root, ext = os.path.splitext(modelfile)
    
    if ext == ".gaussian":
        return gaussian_model_from_file(modelfile)
    elif ext == ".poisson":
        return poisson_model_from_file(modelfile)
    elif ext == ".histogram":
        return histogram_model_from_file(modelfile)
    def f(x):
        return 0.0
    return f

def get_immediate_subdirectories(directory):
        return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

def add_names_to_list(L, directory, names):
    x = [directory+"/"+name for name in names if not os.path.isdir(os.path.join(directory,name))]
    L.extend(x)

def get_all_files(directory):
    L = []
    os.path.walk(directory, add_names_to_list, L)
    return L


#Language models
def make_linear_lm(name, outfile, lms, lmfiles, weights):
    #print "name", name
    #print "outfile", outfile
    #print "lms", lms
    #print "lmfiles", lmfiles
    #print "weights", weights
    out = [["# Parameters 1"]]
    out.append(["MainLM %s" % (name)])
    out.append(["# LMDefinition %d" % (2+len(lms)*2)])
    out.append(["Name\t%s" % (name)])
    out.append(["Type\tLinear"])
    
    lmlines = []

    for (i,lm) in enumerate(lms):
        out.append(["LM[%d]\t%s" % (i, lm)])
        out.append(["Weight[%d]\t%s" % (i, weights[i])])
        lmlines.append(["# LMDefinition 3"])
        lmlines.append(["Name\t%s" % (lm)])
        lmlines.append(["Type\tInclude"])
        lmlines.append(["File\t%s" % (lmfiles[i])])

    out = out + lmlines
    sentences_to_file(outfile, out)


def make_loglinear_lm(name, outfile, lms, lmfiles, weights, noNorm = False):
    #print "name", name
    #print "outfile", outfile
    #print "lms", lms
    #print "lmfiles", lmfiles
    #print "weights", weights
    out = [["# Parameters 1"]]
    out.append(["MainLM %s" % (name)])
    out.append(["# LMDefinition %d" % (3+len(lms)*2)])
    out.append(["Name\t%s" % (name)])
    out.append(["Type\tLogLinearLM"])
    
    lmlines = []

    for (i,lm) in enumerate(lms):
        out.append(["LM[%d]\t%s" % (i, lm)])
        out.append(["Weight[%d]\t%s" % (i, weights[i])])
        lmlines.append(["# LMDefinition 3"])
        lmlines.append(["Name\t%s" % (lm)])
        lmlines.append(["Type\tInclude"])
        lmlines.append(["File\t%s" % (lmfiles[i])])

    if NoNorm:
        out.append(["NoNorm\t1"])
    out = out + lmlines
    sentences_to_file(outfile, out)

def make_class_lm(name, outfile, emissionlm, predictionlm, classmap):
    out = [["# Parameters 1"]]
    out.append(["MainLM %s" % (name)])
    out.append(["# LMDefinition 5"])
    out.append(["Name\t%s" % (name)])
    out.append(["Type\tClassLM"])
    out.append(["EmissionLM\t%sEmission" % (name)])
    out.append(["ClassPredictLM\t%sPrediction" % (name)])
    out.append(["Word2ClassMap\t%sClassMap" % (name)])
    out.append(["# ClassMapDefinition 2"])
    out.append(["Name\t%sClassMap" % (name)])
    out.append(["File\t%s" % (classmap)])
    out.append(["# LMDefinition 3"])
    out.append(["Name\t%sEmission" % (name)])
    out.append(["Type\tInclude"])
    out.append(["File\t%s" % (emissionlm)])
    out.append(["# LMDefinition 3"])
    out.append(["Name\t%sPrediction" % (name)])
    out.append(["Type\tInclude"])
    out.append(["File\t%s" % (predictionlm)])
    sentences_to_file(outfile, out)

def make_probdisc_lm(name, outfile, fglm, bglm, offset, a, b, c):
    out = [["# Parameters 1"]]
    out.append(["MainLM %s" % (name)])
    out.append(["# LMDefinition 8"])
    out.append(["Name\t%s" % (name)])
    out.append(["Type\tProbDiscLM"])
    out.append(["ForegroundLM\t%sFG" % (name)])
    out.append(["BackOffLM\t%sBG" % (name)])
    out.append(["OffSet\t%e" % (offset)])
    out.append(["Alpha\t%e" % (a)])
    out.append(["Beta\t%e" % (b)])
    out.append(["Gamma\t%e" % (c)])
    out.append(["# LMDefinition 3"])
    out.append(["Name\t%sFG" % (name)])
    out.append(["Type\tInclude"])
    out.append(["File\t%s" % (fglm)])
    out.append(["# LMDefinition 3"])
    out.append(["Name\t%sBG" % (name)])
    out.append(["Type\tInclude"])
    out.append(["File\t%s" % (bglm)])
    sentences_to_file(outfile, out)

def probabilities_to_file(outfile, probs):
    out = [["# Probabilities %d" % (len(probs))]] + map(lambda ((a,b)): (str(a), str(b)), sorted(probs.iteritems()))
    sentences_to_file(outfile, out)

def multiprobs_to_file(outfile, probs):
    out = []
    for w in probs:
        line = [w]
        for (k,v) in probs[w].iteritems():
            line.append(str(k)+":"+str(v))
        out.append(line) 
    sentences_to_file(outfile, out)

def multiprobs_from_file(infile):
    probs = {}
    cont = sentences_from_file(infile)

    for line in cont:
        if not line:
            continue
        l = map(lambda x: x.split(":"), line)
        mp = dict(map(lambda x: (int(x[0]),float(x[1])), l[1:]))
        probs[line[0]] = mp
    return probs

def renorm_dict(d):
    total = sum(d.itervalues())
    for (k,v) in d.iteritems():
        d[k] = v/total
    return d

def sentences_from_phrases(phraselist):
    sents = []
    cur_sent = []
    seen_content = False
    for phrase in phraselist:
        if phrase == [SENTENCE_END_TOKEN]:
            if seen_content == True:
                cur_sent = cur_sent + phrase
                sents.append(cur_sent)
                seen_content = False
            cur_sent = []
        else:
            if phrase != [SENTENCE_START_TOKEN]:
                seen_content = True
            cur_sent = cur_sent + phrase

    return sents

def phraselists_from_phrases(phraselist):
    sents = []
    cur_sent = []
    seen_content = False
    for phrase in phraselist:
        if phrase == [SENTENCE_END_TOKEN]:
            if seen_content == True:
                cur_sent.append(phrase)
                sents.append(cur_sent)
                seen_content = False
            cur_sent = []
        else:
            if phrase != [SENTENCE_START_TOKEN]:
                seen_content = True
            cur_sent.append(phrase)

    return sents
def apply_plda_inference(modelfile, corpusfile, outfile):
    args = ['--inference_data_file', corpusfile, '--model_file', modelfile, '--inference_result_file', outfile]
    p = subprocess.call(PLDA_INFERENCE_ARGS+args)

def build_plda_corpus_file(files, outfile):
    data = {}

    for f in files:
#        print f
        if f:
            path, ext = os.path.splitext(f)
            fname = path.split("/")[-1]
            fname = fname.split(".")[0]
            if fname not in data:
                data[fname] = []
            data[fname].append(text_to_bow(read_file(f).split()))
    
    joint = {}

    for f in data:
        if f not in joint:
            joint[f] = {}
        for bow in data[f]:
            for (k,v) in bow.iteritems():
                joint[f][k] = joint[f].get(k,0) + v
    
    out = []
    listout = []

    for f in joint:
        line = []
        listout.append([f])
        for (k,v) in joint[f].iteritems():
            line.append(k+" "+str(v))

        out.append(line)
    
    sentences_to_file(outfile+"_filelist", listout)
    sentences_to_file(outfile, out)

def generate_plda_corpus_from_neighbouring_sentences(phrased_document, outfile, num_neighbours = 1):
    doc_phrases = sentences_from_file(phrased_document)
    doc_sents = sentences_from_phrases(doc_phrases)
    
    out = []
    indexlist = []

    for i in xrange(len(doc_sents)):
        bow = {}
#        print "i =",i
        lrange = i - num_neighbours
        hrange = i + num_neighbours + 1
        if i < num_neighbours:
            lrange = 0
        if i + num_neighbours >= len(doc_sents):
            hrange = len(doc_sents)
        indexlist.append([str(i)+" +- "+str(num_neighbours)])
        for j in range(lrange, hrange):
            bow = join_bows(bow, text_to_bow(doc_sents[j]))
#            print "j =",j
#            print "adding sentence",doc_sents[j]
        line = []
        for (k,v) in bow.iteritems():
            line.append(k+" "+str(v))
        out.append(line)
   
    sentences_to_file(outfile, out)
    sentences_to_file(outfile+".sent_index_list", indexlist)

def read_plda_model_file(vocfile, modelfile):
    voc = read_vocabulary(vocfile)
    twords = []
    sum_scores = []

    model_c = sentences_from_file(modelfile)

    num_topics = 0

    for l in model_c:
        if len(l) == 0:
            continue
        sep = l[1:]
        word = l[0]
        if num_topics == 0:
            num_topics = len(sep)
            #Do setup for all topics
            for i in range(num_topics):
              twords.append({})
              sum_scores.append(0.0)
        for i in range(len(sep)):
            twords[i][word] = float(sep[i])
            sum_scores[i] = sum_scores[i] + float(sep[i])
    """
    for i in range(num_topics):
        for w in twords[i]:
            twords[i][w] = twords[i][w]/sum_scores[i]
    """
    return twords, sum_scores

def read_plda_inference_file(infile):
    docs = []
#    print "Reading inference file ",infile
    fc = sentences_from_file(infile)

    for l in fc:
        tmp = []
        total = 0.0
        probs = []
        for v in l:
            tmp.append(float(v))
            total = total + float(v)
        for x in tmp:
            probs.append(x/total)
        if probs:
            docs.append(probs)

    return docs

def kl_divergence(vocabulary, p,q):
    div = 0.0
    q_loc = dict(q)

    #smooth q if there are probabilities equal 0 which are non-zero in p
    smooth = False
    for w in vocabulary:
        if p[w] > 0.0 and q[w] == 0.0:
            smooth = True

    if smooth:
        new_probmass = 1.0 + len(vocabulary)*KL_DIVERGENCE_EPS  
        for w in vocabulary:
            q_loc[w] = (q_loc[w]+KL_DIVERGENCE_EPS)/new_probmass

    for w in vocabulary:
        #print "w:",w, "P:",p[w], "Q:",q[w]
        if p[w] == 0.0:
            continue
        div = div + p[w]*log(p[w]/q_loc[w])
    return div

def js_divergence(vocabulary, p, q):
    sym_dist = {}
    for w in vocabulary:
        sym_dist[w] = (p[w] + q[w])/2.0
    return (kl_divergence(vocabulary, p, sym_dist) + kl_divergence(vocabulary, q, sym_dist))/2.0

def choose_best_sentences(document, image, outfile, num_neighbours, num_sentences, model = "/home/andrea/studium/BA/NICE/DEV/experiments/original/components/LMs/LDA/dMix-1000/plda_mix_model.txt"):
    #Use dMix for simplicity - results do not seem to differ much from using all models.
    #models = [("/home/andrea/studium/BA/NICE/DEV/experiments/original/components/LMs/LDA/dDoc-1000/plda_doc_model.txt", 0.84), ("/home/andrea/studium/BA/NICE/DEV/experiments/original/components/LMs/LDA/dMix-1000/plda_mix_model.txt", 0.12), ("/home/andrea/studium/BA/NICE/DEV/experiments/original/components/LMs/LDA/dImg-1000/plda_img_model.txt", 0.04)]
    
    #Get sentence topic distributions (possibly including some neighbours)
    corpfile = outfile+".phrase_corpus"
    generate_plda_corpus_from_neighbouring_sentences(document, corpfile, num_neighbours)

    mname = model.split("/")[-1].split(".")[0]
    minfoutfile = outfile+"."+mname
    apply_plda_inference(model, corpfile, minfoutfile)
    sentence_weights = read_plda_inference_file(minfoutfile)

    doc_phrases = sentences_from_file(document)
    doc_sents = sentences_from_phrases(doc_phrases)
    
    #Get the topic distribution for the image
    #The visiterm image file
    imgcorpfile = image+".plda_corpus"
    build_plda_corpus_file([image], imgcorpfile)
    
    mname = model.split("/")[-1].split(".")[0]
    imginfoutfile = outfile+".image.plda_inference."+mname
    apply_plda_inference(model, imgcorpfile, imginfoutfile)
    image_weights = read_plda_inference_file(imginfoutfile)
    
    image_dist = dict(zip(xrange(len(image_weights[0])), image_weights[0]))
#    print "IMAGE_DIST:", len(image_dist)
#    pprint(image_dist)

    kl_scores = []
    js_scores = []

    for (i,s) in enumerate(sentence_weights):
#        print "SENTENCE_DIST:", len(s)
#        pprint(s)
        sentence_dist = dict(zip(xrange(len(s)), s))
        kl_scores.append((kl_divergence(xrange(len(s)), image_dist, sentence_dist),i))
        js_scores.append((js_divergence(xrange(len(s)), image_dist, sentence_dist),i))
    
#    print sorted(kl_scores)
    idxes_js = map(lambda (a,b): b, sorted(js_scores)[0:num_sentences])
    idxes_kl = map(lambda (a,b): b, sorted(kl_scores)[0:num_sentences])
    out_js = []
    out_kl = []
    for idx in idxes_js:
        out_js.append(doc_sents[idx])
    for idx in idxes_kl:
        out_kl.append(doc_sents[idx])
    return (out_js, idxes_js), (out_kl, idxes_kl)

def get_unique_phrases_from_phraselist(phraselist, remove_sent_tokens=True):
    res = []
    known = []
    for phrase in phraselist:
        if remove_sent_tokens:
            if phrase != [SENTENCE_START_TOKEN] and phrase != [SENTENCE_END_TOKEN]:
                if " ".join(phrase) not in known:
                    known.append(" ".join(phrase))
                    res.append(phrase)
        else:
            if " ".join(phrase) not in known:
                known.append(" ".join(phrase))
                res.append(phrase)
    return res


def compute_perplexity(vocfile, lmfile, corpusfile):
    """Uses the LSVLM perplexity tool to find the perplexity of the language model in lmfile on the corpus in corpusfile."""
    
    f = open(corpusfile, "r")
    p = subprocess.Popen(PERP_ARGS+ ["-M %d" % (M), "-sep "+SENTENCE_END_TOKEN, "-sentbeg "+SENTENCE_START_TOKEN, vocfile, lmfile], stdin = f, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    #p = subprocess.Popen(PERP_ARGS+ [vocfile, lmfile], stdin = f, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    (response, errors) = p.communicate()
    response = response.split(";")
    assert len(response) >= 2, lmfile+" "+corpusfile+" "+vocfile+"\n"+";".join(response)+"\n"+errors
    perp = float(response[0].split()[-1])
    score = float(response[1].split()[-1])
    return (perp, score)

def make_loo_corpora(files, outfolder):
    if not outfolder.endswith("/"):
        outfolder = outfolder+"/"
    
    for f in files:
        path, ext = os.path.splitext(f)
        fname = path.split("/")[-1]
        corpfile = outfolder+fname+"_left-out.corpus"

        contfiles = files[:]
        contfiles.remove(f)
        with open(corpfile,"w") as outfile:
            for cf in contfiles:
                with open(cf, "r") as infile:
                    shutil.copyfileobj(infile, outfile)
    return

def apply_seldoc(target_unigram_tree_file, bg_unigram_tree_file, bg_corpus_file):
    """
    Applies document selection tool and returns tuples containing the document id and the corresponding change in perplexity.
    """
    f = open(bg_corpus_file, "r")
    p = subprocess.Popen(SELDOC_ARGS+[target_unigram_tree_file, bg_unigram_tree_file], stdin = f, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    
    (output, errors) = p.communicate()
    res = map(str.split, output.split("\n"))
    result = []
    for x in res:
        if len(x) < 2:
            continue
        else:
            docstr = x[0]
            perp = x[1]
        M = re.match(SELDOC_ID_REGEXP, docstr)
        result.append([float(perp), M.group(1)])

    return sorted(result)

def read_perplexity_list(filename):
    cont = sentences_from_file(filename)
    res = []

    for x in cont:
        if len(x) < 2:
            continue
        else:
            res.append([float(x[0]), x[1]])

    return sorted(res)

def pick_documents_by_perplexity(doclist, threshold):
    return filter(lambda x: x[0] < threshold, doclist)

def read_sentences_lazy(infile):
    with open(infile, "r") as inf:
        for line in inf:
            yield line.split()
