from numpy import mean,cov,double,cumsum,dot,linalg,array,rank
from pylab import plot,subplot,axis,stem,show,figure

def PCA(A):
 # computing eigenvalues and eigenvectors of covariance matrix
 M = (A-mean(A.T,axis=1)).T # subtract the mean (along columns)
 [latent,coeff] = linalg.eig(cov(M)) # attention:not always sorted
 score = dot(coeff.T,M) # projection of the data in the new space
 return coeff,score,latent

from pprint import pprint
from json import dumps

def plot_PCA(A, colors=None, additional_data = None):
   if colors is None:
       colors = ["g"]*len(A)
   coeff, score, latent = PCA(A)
   print dumps(list(latent))
   scoreT = score.T
   figure()
   subplot(121)
   m = mean(A,axis=1)
   plot([0, -coeff[0,0]*2]+m[0], [0, -coeff[0,1]*2]+m[1],'--k')
   plot([0, coeff[1,0]*2]+m[0], [0, coeff[1,1]*2]+m[1],'--k')
#   plot(A[0,:],A[1,:],'ob') # the data
   for x,c in zip(A, colors):
      if c == "g":
          c = "b"
      plot(x[0], x[1], 'o', color=c)
   axis('equal')
   subplot(122)
   reds = []
   if not additional_data is None:
      transformed = []
      for d in additional_data:
          res = dot(coeff.T, array(d))
          transformed.append(res)
      for t in transformed:
          plot(t[0], t[1], "xb")
   for x,c in zip(score.T, colors):
      if c == "r":
          reds.append(x)
      plot(x[0], x[1], '*', color=c)
   axis('equal')
   show()
