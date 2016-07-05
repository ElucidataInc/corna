from scipy.special import binom
from numpy.linalg import pinv
import re
import pandas as pd
import numpy as np
from itertools import product
import algorithms as algo



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





def na_corr_double_trac(na_dict, formula_dict, eleme_corr_list):
    na_dict = {'C':[0.95,0.05],
           'H':[0.98,0.01,0.01], 'N':[0.8,0.2],
           'O':[0.95,0.03,0.02],
           'S': [0.8,0.05,0.15]}

    formula_dict = {'C': 5, 'H': 10, 'N':1, 'O':2, 'S':1}
    correction_vector = [1.]
    eleme_corr_list = ['C', 'H', 'N']
    # if eleme_corr = {} then eleme_corr_list = iso_tracers
    correction_matrix = [1.]
    for trac in eleme_corr_list:
        no_atom_tracer = formula_dict[trac]
        eleme_corr = {}
        matrix_tracer = algo.corr_matrix(str(trac), formula_dict, eleme_corr, no_atom_tracer, na_dict, correction_vector)
        correction_matrix = np.kron(correction_matrix, matrix_tracer)
    return correction_matrix

def double_na_correc(na_dict, formula_dict, eleme_corr_list, intensities_list):
    na_dict = {'C':[0.95,0.05],
       'H':[0.98,0.01,0.01], 'N':[0.8,0.2],
       'O':[0.95,0.03,0.02],
       'S': [0.8,0.05,0.15]}
    formula_dict = {'C': 5, 'H': 10, 'N':1, 'O':2, 'S':1}
    #correction_vector = [1.]
    eleme_corr_list = ['C', 'H', 'N']

    M = na_corr_double_trac(na_dict, formula_dict, eleme_corr_list)

    Minv=pinv(M)

    icorr = np.matmul(Minv,intensities_list)

    return icorr
















