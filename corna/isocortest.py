import re
import numpy
from scipy import optimize

def parse_formula(f):
    """
    Parse the elemental formula pand return the number
    of each element in a dictionnary d={'El_1':x,'El_2':y,...}.
    """
    s = "(" + "|".join(data.keys()) + ")([0-9]{0,})"
    d = dict((el,0) for el in data.keys())
    for el,n in re.findall(s,f):
        if n:
            d[el] += int(n)
        else:
            d[el] += 1
    return d

def calc_mdv(el_dict_meta, el_dict_der):
    """
    Calculate a mass distribution vector (at natural abundancy),
    based on the elemental compositions of both metabolite's and
    derivative's moieties.
    The element corresponding to the isotopic tracer is not taken
    into account in the metabolite moiety.
    """
    result = [1.]
    for el,n in el_dict_meta.iteritems():
        if el not in [el_cor, el_excluded]:
            for i in range(n):
                result = numpy.convolve(result, data[el])
    for el,n in el_dict_der.iteritems():
        for i in range(n):
            result = numpy.convolve(result, data[el])

    return list(result)

def cost_function(mid, v_mes, mat_cor):
    """
    Cost function used for BFGS minimization.
        return : (sum(v_mes - mat_cor * mid)^2, gradient)
    """
    x = v_mes - numpy.dot(mat_cor,mid)
    # calculate sum of square differences and gradient
    return (numpy.dot(x,x), numpy.dot(mat_cor.transpose(),x)*-2)

# data_iso / isotop
data = {'C': [0.99, 0.011], 'H' : [0.99, 0.00015], 'O': [0.99757, 0.00038, 0.00205]}
#chemical formulaof metabolite
f = 'C4H5O5'
der = ''
# no of atoms in chemical formula
el_dict_meta = parse_formula(f)
el_dict_der = parse_formula(der)
# isotopic tracer
el_cor = 'C'
# elements not to be included for correction
el_excluded = ['H', 'O']
# number of atoms to be corrected - takes only 1 , allow to take as list
nAtom_cor = el_dict_meta[el_cor]
# mass distribution vector
correction_vector = calc_mdv(el_dict_meta, el_dict_der)
c_size = len(correction_vector)
#length of measured vector
m_size = 5
# purity of the tracer - NA abundance
el_pur = [0.01, 0.99]

# creating a correction matrix:
correction_matrix = numpy.zeros((m_size, nAtom_cor+1))
for i in range(nAtom_cor+1):
    column = correction_vector[:m_size]
    for na in range(i):
        column = numpy.convolve(column, el_pur)[:m_size]
    if el_excluded != el_cor:
        for nb in range(nAtom_cor-i):
            column = numpy.convolve(column, data[el_cor])[:m_size]
    correction_matrix[:,i] = column


mid, residuum = [], [float('inf')]
mid_ini = numpy.zeros(nAtom_cor+1)
v_measured = [0.572503, 0.219132, 0.122481, 0.054081, 0.031800]
v_mes = numpy.array(v_measured).transpose()
mid, r, d = optimize.fmin_l_bfgs_b(cost_function, mid_ini, fprime=None, approx_grad=0,\
                                   args=(v_mes, correction_matrix), factr=1000, pgtol=1e-10,\
                                   bounds=[(0.,float('inf'))]*len(mid_ini))
resi = v_mes - numpy.dot(correction_matrix, mid)

# normalize mid and residuum between 0-1
sum_p = sum(mid)
if sum_p != 0:
    mid = [p/sum_p for p in mid]
sum_m = sum(v_measured)
if sum_m != 0:
    residuum = [v/sum_m for v in resi]

# mean enrichment
enr_calc = sum(p*i for i,p in enumerate(mid))/nAtom_cor
print enr_calc

