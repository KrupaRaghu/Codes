from ..experiment_config import *
from ..formats.KMeans import *
from ..formats.SIFT import *
from data_manager.OSM import object_from_file
from collections import Counter 

def stat_visiterms_items(itemiterator, n, in_attr=IMG_VISI_KMEANS):
    res = Counter([])
    for item in itemiterator:
        visiterms = item.get_attribute(in_attr, list)
        res.update(Counter(visiterms))
    print "Visiterm occurrences:"
    empty = []
    for x in xrange(int(n)):
        occ = res.get(make_kmeans_visiterm(x),0)
        if occ == 0:
            empty.append(make_kmeans_visiterm(x))
        print make_kmeans_visiterm(x),":",occ
    print "Visiterms NOT occurring: %d/%d\n\n" % (len(empty), n)
    pprint(empty)

from json import dumps

def stat_visiterms_items_raw(itemiterator, n, in_attr=IMG_VISI_KMEANS):
    res = Counter([])
    for item in itemiterator:
        visiterms = item.get_attribute(in_attr, list)
        res.update(Counter(visiterms))
    empty = []
    for x in xrange(int(n)):
        occ = res.get(make_kmeans_visiterm(x),0)
        if occ == 0:
            empty.append(x)
    print dumps(empty)

def label_SIFT_items(itemiterator, labelerfile, in_attr=IMG_SIFT_RAW, out_attr=IMG_VISI_KMEANS):
    """Finds the visiterms corresponding to the items' SIFT data."""
    labeler = object_from_file(KMeansLabeler, labelerfile)
    
    for item in itemiterator:
        sift = SIFT.from_SIFT_output(item.get_attribute(in_attr))
        labels = labeler.predict(sift.descriptors)
        visiterms = []
        for l in labels:
            visiterms.append(make_kmeans_visiterm(l))
        item.set_attribute(out_attr, visiterms)
