from ..formats.KMeans import *
from ..formats.SIFT import *
from ..experiment_config import *
from sys import stdout

def get_SIFTs_from_items(itemiterator, siftattr):
    SIFTs = []
    for item in itemiterator:
        newSIFT = SIFT.from_SIFT_output(item.get_attribute(siftattr))
        SIFTs.extend(newSIFT.descriptors)
    return SIFTs

def print_SIFTs_from_items(itemiterator, siftattr=IMG_SIFT_RAW):
    data = get_SIFTs_from_items(itemiterator, siftattr)
    from json import dumps
    for d in list(data):
        print dumps(list(d))

def join_SIFTs(attrname, itemiterator):
    SIFTs = []
    for item in itemiterator:
        newSIFT = item.get_attr(attrname)
        SIFTS.extend(newSIFT.descriptors)
    return SIFTs

def train_kmeans_from_SIFT(itemiterator, k, silent=False):
    """Trains a MiniBatchKMeans labeler from the SIFT data of the given items."""
    data = get_SIFTs_from_items(itemiterator, IMG_SIFT_RAW)
    params = dict(MINIBATCH_KMEANS_DEFAULT_PARAMS)
    params["n_clusters"] = int(k)
    labeler = KMeansLabeler(**params)
    labeler.fit(data)
    if not silent:
        stdout.write(labeler.encode())
