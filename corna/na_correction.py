"""
This module is a wrapper around algorithms.py. It calls different functions from algorithms.py
and performs na correction (na_correction function). The output is given in the form of fragments
dictionary model which can further be used in post processing function, converting to dataframr, etc
"""
import algorithms as algo
import helpers as hl
import numpy as np
from itertools import product




def na_correction(merged_df, iso_tracers, eleme_corr, na_dict):
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
    hl.convert_labels_to_std(merged_df, iso_tracers)

    samp_lab_dict = algo.samp_label_dcit(iso_tracers, merged_df)

    trac_atoms = algo.get_atoms_from_tracers(iso_tracers)

    formula_dict = algo.formuladict(merged_df)

    fragments_dict = algo.fragmentsdict_model(merged_df)

    correc_inten_dict = {}

    for samp_name, label_dict in samp_lab_dict.iteritems():

        inten_index_dict = label_corr_intens_dict(iso_tracers, trac_atoms, label_dict, formula_dict, eleme_corr, na_dict)

        correc_inten_dict[samp_name] = inten_index_dict

    nacorr_dict_model = corr_int_dict_model(iso_tracers, correc_inten_dict, fragments_dict)

    return nacorr_dict_model


def label_corr_intens_dict(iso_tracers, trac_atoms, label_dict, formula_dict, eleme_corr, na_dict):
    """
    This function creates a dictionary with keys as labels and values as corrected intensities for
    single and multiple tracer
    """

    if len(trac_atoms) == 1:
        icorr = single_corr_list(label_dict, trac_atoms, formula_dict, eleme_corr, na_dict)
        inten_index_dict = singe_corr_inten_dict(icorr)
    else:
        inten_index_dict = multi_trac_na_correc(iso_tracers, trac_atoms, eleme_corr, formula_dict, label_dict, na_dict)

    return inten_index_dict


def corr_int_dict_model(iso_tracers, correc_inten_dict, fragments_dict):
    """
    This function returns the na correction dictionary model
    """
    sample_list = algo.check_samples_ouputdict(correc_inten_dict)
    # { 0: { sample1 : val, sample2: val }, 1: {}, ...}
    lab_samp_dict = algo.label_sample_dict(sample_list, correc_inten_dict)

    nacorr_dict_model = algo.fragmentdict_model(iso_tracers, fragments_dict, lab_samp_dict)

    return nacorr_dict_model


def single_corr_list(label_dict, trac_atoms, formula_dict, eleme_corr, na_dict):
    """
    This function returns the list of corrected intensities for single tracer na correction
    """

    intensities = np.concatenate(np.array((label_dict).values()))

    iso_tracer = trac_atoms[0]

    no_atom_tracer = formula_dict[iso_tracer]

    icorr = algo.single_lab_corr(formula_dict, iso_tracer, eleme_corr, no_atom_tracer, na_dict, intensities)

    return icorr


def singe_corr_inten_dict(icorr):
    """
    This function creates a dictionary of labels and corrected intensities for single tracer
    na correction
    """

    inten_index_dict = {}
    for i in range(0, len(icorr)):
        inten_index_dict[i] = icorr[i]

    return inten_index_dict


def multi_corr_inten_dict():
    """
    This function creates a dictionary of labels and corrected intensities for multi tracer
    na correction
    """

    intens_idx_dict = {}

    return intens_idx_dict


def multi_trac_intensities_list(no_atom_tracer, eleme_corr, eleme_corr_list, lab_dict):
    """
    This function returns the list of intensities in order of tuple list ( which contains
    all posible combinaltion for elements to be corrected). This intensity list vector
    is used for correction
    """
    l = [np.arange(x+1) for x in no_atom_tracer]

    tup_list = list(product(*l))

    indist_sp = sum(eleme_corr.values(),[])

    tup_pos = [i for i, e in enumerate(eleme_corr_list) if e in indist_sp]

    intensities_list = algo.filter_tuples(tup_list, lab_dict, tup_pos)

    return intensities_list


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

    intens_idx_dict = {}

    intensities_list = multi_trac_intensities_list(no_atom_tracer, eleme_corr, eleme_corr_list, lab_dict)

    icorr = algo.multi_label_correc(na_dict, formula_dict, eleme_corr_list, intensities_list)
    print 'corrected inten'
    print icorr
    ############### line below is incorroect dictionary for now
    # to do here, this is input data dict only - to get the icorr values with keys here
    #intens_idx_dict = multi_corr_inten_dict()
    intens_idx_dict = lab_dict

    return intens_idx_dict



