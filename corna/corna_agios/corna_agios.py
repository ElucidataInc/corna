""""This module calls all the functions in the package. All user functions defined here."""
from .. helpers import convert_labels_to_std
from . file_parser_agios import melt_df, column_manipulation
from . algorithms_agios import fragmentsdict_model, get_atoms_from_tracers
from . na_correction import nacorrection


def convert_inputdata_to_stdfrom(input_df):
    """
    This function convert the input data file(maven format) into standard data model. It gives
    the same format as in merged data (maven + metadata). This function can be used if the user
    does not wish to input metadata file and proceed as it is with the input data file

    Args:
        input_df : MAVEN input data in the form of pandas dataframe
    Returns:
        std_form_df : dataframe with input data in standard data model format that can be
                    used in further processing
    """

    long_form = melt_df(input_df)
    std_form_df = column_manipulation(long_form)

    return std_form_df


def na_correction(merged_df, iso_tracers, eleme_corr, na_dict):
    """
    This function performs na correction for single and multiple tracers and
    creates the output in the form of dictionary with corrected intensities.

    Args:
        merged_df : dataframe with input + metadata file in long form
        iso_tracer : List of isotopic tracer elements
        eleme_corr : Indistinguishable species to be considered for correction
                     along with isotopic tracers
        na_dict : Dictionary of natural abundance values

    Returns:
        na_corr_dict : dictionary with corrected intensity values
    """
    eleme_corr_invalid_entry(iso_tracers, eleme_corr)
    std_label_df = convert_labels_to_std(merged_df, iso_tracers)
    metabolite_dict = fragmentsdict_model(std_label_df)
    na_corr_dict = {}

    for metabolite, fragments_dict in metabolite_dict.iteritems():
        na_corr_dict[metabolite] = nacorrection(fragments_dict, iso_tracers, eleme_corr, na_dict)

    return na_corr_dict


def eleme_corr_invalid_entry(iso_tracers, eleme_corr):
    """
    This function raises an error if the user inputs incorrect values in  eleme_corr dictionary.
    The indistinguishable element specified in the eleme_corr dictionary cannot be an isotracer
    element. This is logically incorrect input, hence raises an error.
    """
    for key, value in eleme_corr.iteritems():
        for el in get_atoms_from_tracers(iso_tracers):
            if el in value:
                raise KeyError('An iso tracer cannot'
                               ' be an Indistinguishable element (' + el +
                               ') , invalid input in eleme_corr dictionary')



