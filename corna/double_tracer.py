from scipy.special import binom
from numpy.linalg import pinv
import re
import pandas as pd
import numpy as np
from itertools import product



def expNA(delta,nC,p):
    return binom(nC,delta)*(1-p)**(nC-delta)*(p)**delta


def double_label_NA_matrix(nA,nB,pA,pB):
    n=(nA+1)*(nB+1)
    M=np.zeros(((nA+1)*(nB+1),(nA+1)*(nB+1)))
    idx=list(product(np.arange(nA+1),np.arange(nB+1)))
    for iA in range(nA+1):
        for jA in range(iA+1):
            for iB in range(nB+1):
                for jB in range(iB+1):
                    i=idx.index((iA,iB))
                    j=idx.index((jA,jB))
                    x=expNA(iA-jA,nA-jA,pA)*expNA(iB-jB,nB-jB,pB)
                    M[i,j]=x
    return M

def double_label_NA_corr(x,nA,nB,pA,pB):
    M=double_label_NA_matrix(nA,nB,pA,pB)
    Minv=pinv(M)
    return np.matmul(Minv,x)






