from scipy.special import binom
from numpy.linalg import pinv
import re
import pandas as pd
import numpy as np
from itertools import product



#sample_label_dict = algo.samp_label_dcit(iso_tracers, merged_df)
#trac_atoms = algo.get_atoms_from_tracers(iso_tracers)
# this onwards tracer C, N goes
#iso_tracers = trac_atoms

#formula_dict = algo.formuladict(merged_df)

#fragments_dict = algo.fragmentsdict_model(merged_df)
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



def p_double_corr(g,pA,pB,elemA,elemB,labelA_col,labelB_col,formula_col,value_col,corr_col):
    print g
    if len(g)==0:
        y=[]
    else:
        formula=g[formula_col].iloc[0]
        m=re.findall('{}(\d+)'.format(elemA),formula)
        nA=int(m[0])
        m=re.findall('{}(\d+)'.format(elemB),formula)
        nB=int(m[0])
        x=np.zeros((nA+1)*(nB+1))
        idx=list(product(np.arange(nA+1),np.arange(nB+1)))
        for i,r in g.iterrows():
            j=idx.index((r[labelA_col],r[labelB_col]))
            x[j]=r[value_col]

        corr_x=double_label_NA_corr(x,nA,nB,pA,pB)
        g[corr_col]=0
        for i,r in g.iterrows():
            j=idx.index((r[labelA_col],r[labelB_col]))
            g.loc[i,corr_col]=corr_x[j]
        return g


