from math import exp, log, pi, sqrt

class LengthModel(object):
    def prob(length):
        raise NotImplementedError()

    def score(length):
        return -log(self.prob(length))

class GaussianLengthModel(LengthModel):
    def __init__(self, mean, std_dev):
        self.mean = mean
        self.standard_deviation = std_dev

    @staticmethod
    def decode(string):
        return GaussianLengthModel(float(string.split()[0]), float(string.split()[1]))

    def encode(self):
        return str(self.mean)+" "+str(self.standard_deviation)

    def prob(self, length):
        return 1.0/(self.standard_deviation*sqrt(2*pi))*exp(-(length - self.mean)**2/2.0/self.standard_deviation**2)