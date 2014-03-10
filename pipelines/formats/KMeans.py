from json import dumps,loads
from sklearn.cluster import MiniBatchKMeans
from ..experiment_config import K
from numpy import array

VISITERM_STRING = "<VISITERM_%s_%s>"
KMEANS_VISITERM_METHOD="K_MEANS2_SCIKIT"

MINIBATCH_KMEANS_DEFAULT_PARAMS={"n_clusters":K, "init":'k-means++', "max_iter":50000, "batch_size":100, "verbose":0, "compute_labels":True, "random_state":None, "tol":0.0, "max_no_improvement":50, "init_size":None, "n_init":3, "reassignment_ratio":0.05}

def make_kmeans_visiterm(index):
    return make_visiterm(KMEANS_VISITERM_METHOD, index)

def make_visiterm(methodname, index):
    return VISITERM_STRING % (methodname, str(index+1))

from pprint import pprint

class KMeansLabeler(MiniBatchKMeans):
    def __init__(self, **kwargs):
        self.params = kwargs
        MiniBatchKMeans.__init__(self, **kwargs)
    def encode(self):
        cc = None
        if hasattr(self, "cluster_centers_"):
            cc = self.cluster_centers_.tolist()
        return dumps((self.params,cc))
    @staticmethod
    def decode(string):
        args = loads(string)
        labeler = KMeansLabeler(**args[0])
        if not args[1] is None:
            labeler.cluster_centers_ = array(args[1])
        return labeler
