import numpy as np
import warnings

from isotopomer import Infopacket

def zero_if_negative(num):
    """
    This function replaces negative numbers by zero_if_negative

    Args:
        num : any int value

    Return:
        1. zero if num is negative
        2. number itself if num is non negative
    """
    return 0 if num < 0 else num


def replace_vals(sample_int_dict):
    """
    This function replace negatives by zero in sample intensity dictionary
    Args:
        sample_int_dict : dictionary with keys as samples and values as corrected intensities

    Returns:
        dict_replaced_vals : sample_int_dict with negative intensities replaced by zeroes
    """
    dict_replaced_vals = {}

    for sample, intensity in sample_int_dict.iteritems():
        dict_replaced_vals[sample] = zero_if_negative(intensity)

    return dict_replaced_vals


def replace_negative_to_zero(corrected_dict):
    """
    This function replaces negative intensity values by zero from list of intensity
    in the standardised model dictionary

    Args:
        corrected_dict : nested dictionary (std model) with NA corrected intensity values

    Returns:
        post_proc_dict : returns nested dictionary with negative values replaced

    """

    post_proc_dict = {}

    for frag_key, frag_info in corrected_dict.iteritems():
        sample_int_dict = frag_info.data
        dict_replaced_vals = replace_vals(sample_int_dict)
        post_proc_dict[frag_key] = Infopacket(
            frag_info.frag, dict_replaced_vals, frag_info.unlabeled, frag_info.name)

    return post_proc_dict


def replace_negatives(na_corr_dict):
    """
    This function is a wrapper around replace_negatives_to_zero, it performs this
    function for all metabolites in the input data file

    Args:
        corrected_dict : nested dictionary (std model) with NA corrected intensity values

    Returns:
        post_proc_dict : returns nested dictionary with negative values replaced for
                         all the metabolites in the input data file

    """
    post_processed_dict = {}
    for metabolite, fragment_dict in na_corr_dict.iteritems():
        post_processed_dict[
            metabolite] = replace_negative_to_zero(fragment_dict)

    return post_processed_dict


def sum_intensities(fragments_dict):
    """
    This function calculates the sum of corrected intensities for a given sample

    Args:
        fragments_dict : dictionary of the form, example : {'Aceticacid_C13_1': [C2H4O2,
                         {'sample_1': array([ 0.0164])}, False, 'Aceticacid']
    Returns:
        sum_dict :  dictionary of sum of all corrected intensities for each sample
    """
    all_frag_info = fragments_dict.values()

    sample_names = []
    for frag in all_frag_info:
        sample_names.extend(frag.data.keys())
    sample_names = list(set(sample_names))

    sum_dict = {}

    for sample_name in sample_names:
        sum_dict[sample_name] = sum(value.data[sample_name] for value in all_values)

    return sum_dict


def enrichment(fragments_dict, decimals):
    """
    This function calculates the fractional enrichment for each label
    Fractional enrichment[sample1] = Corrected Intensity/ Sum of corrected intensities of all labels

    Args:
        fragments_dict : dictionary of the form, example : {'Aceticacid_C13_1': [C2H4O2,
                         {'sample_1': array([ 0.0164])}, False, 'Aceticacid']

        decimals : number of significant digits to keep

    Returns:
        fragments_fractional : fragment dictionary model of fractional enrichment values
    """
    fragments_fractional = {}
    sum_dict = sum_intensities(fragments_dict)

    for key, value in fragments_dict.iteritems():
        fractional_data = {}
        for sample_name, intensity in value.data.iteritems():
            if not sum_dict[sample_name] == 0:
                fractional_data[sample_name] = np.around(
                    intensity / sum_dict[sample_name], decimals)
            else:
                fractional_data[sample_name] = 0
                warnings.warn("{} {} {} {}".format('sum of labels is zero for sample ', sample_name.encode('utf-8'),
                                                   ' of ', (value.name).encode('utf-8')))
        fragments_fractional[key] = Infopacket(
            value.frag, fractional_data, value.unlabeled, value.name)

    return fragments_fractional


def fractional_enrichment(post_processed_out, decimals=4):
    """
    This function is a wrapper over enrichment function which calculates fractional enrichment
    for all the metabolites in the input data file

    Args:
        post_processed_out : Dictionary of the form, {'Metabname_label':
        [Fragment object, {'sample_name': corrected_intensity}, label/unlabe bool, metabname]
        decimals : number of decimals to keep

    Returns:
        frac_enrichment_dict : fragment dictionary model of fractional enrichment values for all
                               metabolites
    """
    frac_enrichment_dict = {}

    for metabolite, fragment_dict in post_processed_out.iteritems():
        frac_enrichment_dict[metabolite] = enrichment(fragment_dict, decimals)

    return frac_enrichment_dict
