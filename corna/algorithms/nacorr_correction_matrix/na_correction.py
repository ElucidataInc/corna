"""
This module is a wrapper around algorithms.py. It calls different functions from algorithms.py
and performs na correction (na_correction function). The output is given in the form of fragments
dictionary model which can further be used in post processing function, converting to dataframr, etc
"""
import numpy as np
from itertools import product
from ... helpers import get_isotope_element, first_sub_second
import pandas as pd
from corna.inputs.maven_parser import convert_labels_to_std
from . algorithms import label_sample_df, formuladict, fragmentdict_model, \
    fragmentsdict_model, make_all_corr_matrices
from ...constants import INTENSITY_COL

def na_correction(merged_df, iso_tracers, eleme_corr, na_dict, intensity_col=INTENSITY_COL):
    """
    This function  is a wrapper over nacorr_each_metab performs na correction for all
    metabolites given in input data file for single and multiple tracers and
    creates the output in the form of dictionary with corrected intensities.

    Args:
        merged_df : dataframe with input + metadata file in long form
        iso_tracer : List of isotopic tracer elements
        eleme_corr : Indistinguishable species to be considered for correction
                     along with isotopic tracers
        na_dict : Dictionary of natural abundance values

    Returns:
        na_corr_dict : dictionary with corrected intensity values for all
                       metabolites given in input data file
    """
    eleme_corr_invalid_entry(iso_tracers, eleme_corr)
    std_label_df = convert_labels_to_std(merged_df, iso_tracers)
    metabolite_dict = fragmentsdict_model(std_label_df, intensity_col)
    na_corr_dict = {}

    for metabolite, fragments_dict in metabolite_dict.iteritems():
        na_corr_dict[metabolite] = nacorr_each_metab(
            fragments_dict, iso_tracers, eleme_corr, na_dict)

    return na_corr_dict


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

    lab_samp_df = label_sample_df(iso_tracers, fragments_dict)
    formula_dict = formuladict(fragments_dict)
    corr_mats = make_all_corr_matrices(iso_tracers, formula_dict, na_dict, eleme_corr)
    df_corr_C_N = correct_label_sample_df(iso_tracers, lab_samp_df, corr_mats)
    nacorr_dict_model = fragmentdict_model(
        iso_tracers, fragments_dict, df_corr_C_N)
    return nacorr_dict_model


def correct_label_sample_df(isotracers, lab_samp_df, corr_mats):
    curr_df = lab_samp_df
    if len(isotracers) == 1:
        curr_df = multiplying_with_matrix(isotracers[0], corr_mats, curr_df)
    else:
        for isotracer in isotracers:
            index_cols = first_sub_second(isotracers, [isotracer])
            group_by_index_cols = curr_df.groupby(level = index_cols)
            L=[]
            keys=[]
            for group_no, group in group_by_index_cols:
                group.index = group.index.get_level_values(isotracer)
                corr_df = multiplying_with_matrix(isotracer, corr_mats, group)
                L.append(corr_df)
                keys.append(group_no)
            curr_df = pd.concat(L, keys=keys, names=index_cols)
            curr_df.index = curr_df.index.reorder_levels(lab_samp_df.index.names)

    return curr_df.to_dict(orient='index')

def multiplying_with_matrix(isotracer, corr_mats, curr_df):
    num_rows, num_cols = corr_mats[isotracer].shape
    curr_df = curr_df.reindex(np.arange(num_cols)).fillna(0)
    corr_data = np.matmul(corr_mats[isotracer], curr_df.values)
    corr_df = pd.DataFrame(index=pd.index.np.arange(num_rows),columns=curr_df.columns, data=corr_data)
    corr_df.index.name = isotracer
    return corr_df




