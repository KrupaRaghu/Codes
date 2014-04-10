from scipy.stats import *
from pylab import *

L = 11.62

R = poisson.rvs(L, size=100)
hist(R)
f = poisson(L)
print dir(f)
print dir(poisson)
x = xrange(15)
y = poisson.pdf(x, L)
#plot(x,y)
