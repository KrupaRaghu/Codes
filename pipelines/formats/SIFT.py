#A class containing SIFT locations and descriptors. Allows to compute a match to a second set of SIFT descriptors.
from json import dumps, loads
from meta import *
from numpy import *
import pylab

class SIFT(object):
    __metaclass__ = FormatMeta
    def __init__(self, locs, decs):
        self.locations = locs[:]
        self.descriptors = decs[:]

    @staticmethod
    def decode(text):
        c = text.split("\n")
        return SIFT(array(loads(c[0])), array(loads(c[1])))

    def encode(self):
        return dumps(self.locations.tolist())+"\n"+dumps(self.descriptors.tolist())

    def __getitem__(self, item):
        return self.locations[item], self.descriptors[item]

    @staticmethod
    def from_SIFT_output(output):
        output = output.split("\n", 1)
        header = output[0].split()
        
        num = int(header[0]) #the number of features
        featlength = int(header[1]) #the length of the descriptor
        if featlength != 128: #should be 128 in this case
            raise RuntimeError, 'Keypoint descriptor length invalid (should be 128).' 
            
        locs = zeros((num, 4))
        descriptors = zeros((num, featlength));        

        e = output[1].split() #split the rest into individual elements
        pos = 0
        for point in range(num):
            #row, col, scale, orientation of each feature
            for i in range(4):
                locs[point,i] = float(e[pos+i])
            pos += 4
            
            #the descriptor values of each feature
            for i in range(featlength):
                descriptors[point,i] = int(e[pos+i])
            #print descriptors[point]
            pos += 128
            
            #normalize each input vector to unit length
            descriptors[point] = descriptors[point] / linalg.norm(descriptors[point])
            #print descriptors[point]
            
        return SIFT(locs,descriptors)

    @conversion(str)
    def from_str(output):
        return SIFT.from_SIFT_output(output)
