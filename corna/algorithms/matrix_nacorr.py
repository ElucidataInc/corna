"""
This module is a wrapper around algorithms.py. It calls different functions from algorithms.py
and performs na correction (na_correction function). The output is given in the form of fragments
dictionary model which can further be used in post processing function, converting to dataframr, etc
"""

import numpy as np
import pandas as pd

import corna.algorithms.matrix_calc as algo
from corna.autodetect_isotopes import get_element_correction_dict
from corna.constants import INTENSITY_COL
from corna.helpers import get_isotope_element, first_sub_second
from corna.inputs.maven_parser import convert_labels_to_std


def eleme_corr_invalid_entry(iso_tracers, eleme_corr):
    """
    This function raises an error if the user inputs incorrect values in  eleme_corr dictionary.
    The indistinguishable element specified in the eleme_corr dictionary cannot be an isotracer
    element. This is logically incorrect input, hence raises an error.
    """
    for key, value in eleme_corr.iteritems():
        for isotracer in iso_tracers:
            el = get_isotope_element(isotracer)
            if el in value:
                raise KeyError('An iso tracer cannot'
                               ' be an Indistinguishable element (' + el +
                               ') , invalid input in eleme_corr dictionary')


def nacorr_each_metab(fragments_dict, iso_tracers, eleme_corr, na_dict):
    """
    This function is wrapper around matrix_calc.py function. It performs na correction
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

    lab_samp_df = algo.label_sample_df(iso_tracers, fragments_dict)
    formula_dict = algo.formuladict(fragments_dict)
    corr_mats = algo.make_all_corr_matrices(iso_tracers, formula_dict, na_dict, eleme_corr)
    df_corr_C_N = correct_label_sample_df(iso_tracers, lab_samp_df, corr_mats)
    nacorr_dict_model = algo.fragmentdict_model(
        iso_tracers, fragments_dict, df_corr_C_N, eleme_corr)
    return nacorr_dict_model


def correct_label_sample_df(isotracers, lab_samp_df, corr_mats):
    curr_df = lab_samp_df
    if len(isotracers) == 1:
        curr_df = multiplying_df_with_matrix(isotracers[0], corr_mats[isotracers[0]], curr_df)
    else:
        for isotracer in isotracers:
            index_cols = first_sub_second(isotracers, [isotracer])
            group_by_index_cols = curr_df.groupby(level = index_cols)
            L=[]
            keys=[]
            for group_no, group in group_by_index_cols:
                group.index = group.index.get_level_values(isotracer)
                corr_df = multiplying_df_with_matrix(isotracer, corr_mats[isotracer], group)
                L.append(corr_df)
                keys.append(group_no)
            curr_df = pd.concat(L, keys=keys, names=index_cols)
            curr_df.index = curr_df.index.reorder_levels(lab_samp_df.index.names)

    return curr_df.to_dict(orient='index')

def multiplying_df_with_matrix(isotracer, corr_mat_for_isotracer, curr_df):
    """This function takes the correction matrix for given isotracer and multiplies
    it with the sample values of the dataframe to give corrected sample values
    Example:
        C13 Sample1 Sample2
        0   0.21    0.98
        1   0.34    0.11
        multiplied with matrix [0.99 0]
                               [0.01 1]
        will give output

        C13 Sample1 Sample2
         0  0.2079  0.9702
	     1  0.3421  0.1198
    """
    num_rows, num_cols = corr_mat_for_isotracer.shape
    curr_df = curr_df.reindex(np.arange(num_cols)).fillna(0)
    corr_data = np.matmul(corr_mat_for_isotracer, curr_df.values)
    corr_df = pd.DataFrame(index=pd.index.np.arange(num_rows),columns=curr_df.columns, data=corr_data)
    corr_df.index.name = isotracer
    return corr_df


def na_correction(merged_df, iso_tracers, ppm_input_user, na_dict, eleme_corr,
                  intensity_col=INTENSITY_COL,autodetect=False):
    std_label_df = convert_labels_to_std(merged_df, iso_tracers)
    metabolite_dict = algo.fragmentsdict_model(std_label_df, intensity_col, eleme_corr)
    na_corr_dict = {}
    if autodetect:
        for metabolite, fragments_dict in metabolite_dict.iteritems():
            auto_eleme_corr = get_element_correction_dict(ppm_input_user, metabolite.formula,iso_tracers)
            na_corr_dict[metabolite] = nacorr_each_metab(fragments_dict, iso_tracers, auto_eleme_corr, na_dict)
    else:
        eleme_corr_invalid_entry(iso_tracers, eleme_corr)
        for metabolite, fragments_dict in metabolite_dict.iteritems():
            na_corr_dict[metabolite] = nacorr_each_metab(fragments_dict, iso_tracers, eleme_corr, na_dict)
    return na_corr_dict
