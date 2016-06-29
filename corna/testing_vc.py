
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


def p_single_corr(g,p,value_col='value',label_col='label',formula_col='Chemical Formula',corr_col='NA corrected',elem='C'):
    if len(g)==0:
        y=[]
    else:
        formula=g[formula_col].iloc[0]
        m=re.findall('{}(\d+)'.format(elem),formula)
        if len(m)!=1:
            raise ValueError("Couldn't get number of {} from formula {}".format(elem,formula))
        nC=int(m[0])
        x=np.zeros(nC+1)
        x[g[label_col].values]=g[value_col].values
        corr_x=single_label_NA_corr(x,p)
        y=[]

        for l in g[label_col]:
            y.append(corr_x[l])
        g[corr_col]=y
    return g

def p_double_corr(g,pA,pB,elemA,elemB,labelA_col,labelB_col,formula_col,value_col,corr_col):
    print 'g'
    print g
    print 'pA', pA
    print 'pB', pB
    print 'elemA', elemA
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
            print 'labels', (r[labelA_col],r[labelB_col])
            print 'j', j
            x[j]=r[value_col]
        print 'int x', x
        corr_x=double_label_NA_corr(x,nA,nB,pA,pB)
        g[corr_col]=0
        for i,r in g.iterrows():
            j=idx.index((r[labelA_col],r[labelB_col]))
            g.loc[i,corr_col]=corr_x[j]
        return g


def forward_sim(formula_atom_bag,expt_labels,expt_freqs,label_matches,label_names,natural_abundance_dict,N=10000):
    M={}

    for i in range(N):
        keys=np.zeros(len(label_names),dtype=int)
        expt_isotopes=np.random.choice(expt_labels,p=expt_freqs)
        for i,elems in enumerate(label_matches):
            mass_shift=0
            for elem in elems:
                elem_count=formula_atom_bag.get(elem,0)
                real_isotope=expt_isotopes.get(elem,0)
                n_natural=elem_count-real_isotope
                na_freq=natural_abundance_dict[elem]
                na_isotopes=np.random.choice(len(na_freq),p=na_freq,size=n_natural)
                #print 'naiso', na_isotopes
                mass_shift+=na_isotopes.sum()+real_isotope
                #print 'mass_shift', mass_shift
            keys[i]=mass_shift
        M.setdefault(tuple(keys),0)
        M[tuple(keys)]+=1.0/N
        #print M
    D=pd.DataFrame([list(x)+[y] for x,y in M.items()],columns=label_names+['freq'])
    return D


label_matches=[['C'],['N']]
label_names=['13C','15N']
#natural_abundance_dict={'C':[0.99,0.01],
#           'N':[1-0.0036,0.0036],}
natural_abundance_dict={'C':[0.95,0.05],
           'N':[0.8,0.2],} #exaggerated for effect
#C5H10NO2S
formula_atom_bag={'C':5,
                 'N':1,
                 'O':2,
                 'H':10,
                 'S':1}
expt_labels=[{'C':0,'N':0},
             {'C':5,'N':1}]
#expt_freqs=[1,0]
expt_freqs=[0.4,0.6]

M2=forward_sim(formula_atom_bag=formula_atom_bag,
                expt_labels=expt_labels,
               expt_freqs=expt_freqs,
              label_matches=label_matches,
               label_names=label_names,
              natural_abundance_dict=natural_abundance_dict,
              N=20000)
#M1 = pd.DataFrame({'13C': {0: 0, 1: 1, 2: 2}, 'freq': {0: 0.5, 1: 1, 2: 0.5}})
M2.sort_values(label_names,inplace=True)
M2['formula']="".join(["{}{}".format(x,y) for x,y in formula_atom_bag.items()])
M2
print 'data'
print M2
M2=p_double_corr(M2,0.05,0.2,'C','N','13C','15N','formula','freq','double_corr')
print 'double corr'
print 'corr'
print M2








