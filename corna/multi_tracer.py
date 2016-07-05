from numpy.linalg import pinv
import re
import pandas as pd
import numpy as np
from itertools import product
import algorithms as algo






def multi_label_matrix(na_dict, formula_dict, eleme_corr_list):

    correction_vector = [1.]
    correction_matrix = [1.]

    for trac in eleme_corr_list:
        no_atom_tracer = formula_dict[trac]
        eleme_corr = {}
        matrix_tracer = algo.corr_matrix(str(trac), formula_dict, eleme_corr, no_atom_tracer, na_dict, correction_vector)
        correction_matrix = np.kron(correction_matrix, matrix_tracer)

    return correction_matrix

def multi_label_correc(na_dict, formula_dict, eleme_corr_list, intensities_list):

    M = multi_label_matrix(na_dict, formula_dict, eleme_corr_list)

    Minv=pinv(M)

    icorr = np.matmul(Minv,intensities_list)

    return icorr



def eleme_corr_to_list(iso_tracers, eleme_corr):

    trac_atoms = algo.get_atoms_from_tracers(iso_tracers)

    eleme_corr_list = []
    for i in trac_atoms:
        eleme_corr_list.append([i])
        if i in eleme_corr.keys():
            eleme_corr_list.append(eleme_corr[i])

    return sum(eleme_corr_list, [])



def filter_tuples(tuple_list, value_dict, positions):
    result_tuples = []
    for tuples in tuple_list:
        tuple_l = list(tuples)
        filtered_tuple = [tuple_l[x] for x in positions]
        if sum(filtered_tuple) == 0:
            rqrd_pos = [tuple_l[x] for x in range(0,len(tuple_l)) if x not in positions]
            rqrd_tup = tuple(rqrd_pos)
            if rqrd_tup in value_dict.keys():
                result_tuples.append(value_dict[rqrd_tup][0])
            else:
                result_tuples.append(0)
        else:
            result_tuples.append(0)
    return result_tuples