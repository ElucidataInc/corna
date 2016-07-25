"""
This module is a wrapper around algorithms.py. It calls different functions from algorithms.py
and performs na correction (na_correction function). The output is given in the form of fragments
dictionary model which can further be used in post processing function, converting to dataframr, etc
"""
import algorithms_agios as algo
import numpy as np
from itertools import product




def na_correction(fragments_dict, iso_tracers, eleme_corr, na_dict):
    """
    This function is wrapper around algorithms.py function. It performs na correction
    for single and multiple tracers and creates the output in the form of fragment
    dictionary model with corrected intensities.

    Args:
        merged_df : dataframe with input + metadata file in long form

        iso_tracer : List of isotopic tracer elements

        eleme_corr : Indistinguishable species to be considered for correction
                     along with isotopic tracers

        na_dict : Dictionary of natural abundance values

    Returns:
        nacorr_dict_model : fragments dictionary with corrected intensity values
    """

    samp_lab_dict = algo.samp_label_dcit(iso_tracers, fragments_dict)

    trac_atoms = algo.get_atoms_from_tracers(iso_tracers)

    formula_dict = algo.formuladict(fragments_dict)


    correc_inten_dict = {}


    for samp_name, label_dict in samp_lab_dict.iteritems():

        inten_index_dict = multi_trac_na_correc(iso_tracers, trac_atoms, eleme_corr, formula_dict, label_dict, na_dict)

        correc_inten_dict[samp_name] = inten_index_dict


    nacorr_dict_model = corr_int_dict_model(iso_tracers, correc_inten_dict, fragments_dict)

    return nacorr_dict_model


def corr_int_dict_model(iso_tracers, correc_inten_dict, fragments_dict):
    """
    This function returns the na correction dictionary model
    """
    label_list = algo.check_labels_corrdict(correc_inten_dict)
    lab_samp_dict = algo.label_sample_dict(label_list, correc_inten_dict)
    nacorr_dict_model = algo.fragmentdict_model(iso_tracers, fragments_dict, lab_samp_dict)

    return nacorr_dict_model


def multi_corr_inten_dict(eleme_corr, eleme_corr_list, no_atom_tracer, icorr, lab_dict):
    """
    This function creates a dictionary of labels and corrected intensities for multi tracer
    na correction
    """

    intens_idx_dict = {}

    positions = indis_tuple_position(eleme_corr, eleme_corr_list)
    tup_list = element_tuple_list(no_atom_tracer)
    correct_idx_dict = dict(zip(tup_list, icorr))

    for tuples, vals in correct_idx_dict.iteritems():
        tuple_l = list(tuples)
        filtered_tuple = [tuple_l[x] for x in positions]
        if sum(filtered_tuple) == 0:
            rqrd_pos = [tuple_l[x] for x in range(0,len(tuple_l)) if x not in positions]
            rqrd_tup = tuple(rqrd_pos)
            if rqrd_tup in lab_dict.keys():
                intens_idx_dict[rqrd_tup] = vals

    return intens_idx_dict


def multi_trac_intensities_list(no_atom_tracer, eleme_corr, eleme_corr_list, lab_dict):
    """
    This function returns the list of intensities in order of tuple list ( which contains
    all posible combinaltion for elements to be corrected). This intensity list vector
    is used for correction
    """
    num_label_tuples = element_tuple_list(no_atom_tracer)
    indist_el_position = indis_tuple_position(eleme_corr, eleme_corr_list)
    intensities_list = algo.input_intens_list(num_label_tuples, lab_dict, indist_el_position)

    return intensities_list


def indis_tuple_position(eleme_corr, eleme_corr_list):
    """
    This function returns the positions of indistinguishable elements from
    tuple list
    """
    indist_sp = sum(eleme_corr.values(), [])
    tup_pos = [i for i, e in enumerate(eleme_corr_list) if e in indist_sp]

    return tup_pos


def element_tuple_list(no_atom_tracer):
    """
    This function returns the tuple list of elements to be corrected. it generates
    all possible combinations of the elements in the form of a tuple
    """
    combinations = [np.arange(num_atoms+1) for num_atoms in no_atom_tracer]
    num_label_tuples = list(product(*combinations))

    return num_label_tuples


def multi_trac_na_correc(iso_tracers, trac_atoms, eleme_corr, formula_dict, lab_dict, na_dict):
    """
    This function returns the list of corrected intensities in order of tuple list for multi
    tracer na correction
    """
    if not eleme_corr:
        eleme_corr_list = trac_atoms
    else:
        eleme_corr_list = algo.eleme_corr_to_list(iso_tracers, eleme_corr)

    no_atom_tracer = []
    for i in eleme_corr_list:
        no_atom_tracer.append(formula_dict[i])

    intensities_list = multi_trac_intensities_list(no_atom_tracer,
                                                   eleme_corr, eleme_corr_list, lab_dict)
    icorr = algo.multi_label_correc(na_dict, formula_dict,
                                    eleme_corr_list, intensities_list)

    intens_idx_dict = multi_corr_inten_dict(eleme_corr, eleme_corr_list,
                                            no_atom_tracer, icorr, lab_dict)

    return intens_idx_dict
