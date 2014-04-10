from json import dumps,loads
from sklearn.cluster import MiniBatchKMeans
from ..experiment_config import *
from numpy import array

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
