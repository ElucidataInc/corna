""""This module calls all the functions in the package. All user functions defined here."""
import pandas as pd

from . isotopomer import fragment_dict_to_std_model
from . postprocess import replace_negative_to_zero, enrichment
from . output import convert_dict_df
from . import config as conf
from . helpers import concatenate_dataframes_by_col, ISOTOPE_NA_MASS


def merge_dfs(df_list):
    """
    This function takes the list of dataframes as an input
    and concatenates the dataframes based on their column names
    Args:
        df_list : list of dataframes
    Returns:
        combined_dfs : concatenated list of dataframes into one dataframe
    """
    combined_dfs = reduce(_merge_two_dfs, df_list)
    return combined_dfs


def _merge_two_dfs(df1, df2):
    return pd.merge(df1, df2,
                    on=[conf.LABEL_COL, conf.SAMPLE_COL,
                        conf.NAME_COL, conf.FORMULA_COL])


def get_na_value_dict():
    """
    This function returns the dictionary of default NA values (adapted from wiki)
    for all the isotopes
    """
    na_mass_dict = ISOTOPE_NA_MASS
    NA = na_mass_dict['NA']
    elements = na_mass_dict['Element']
    na_val_dict = {}
    atoms = set(elements.values())

    for atom in atoms:
        isotope_list = [isotope for isotope, iso_atom
                        in elements.iteritems() if iso_atom == atom]
        na_vals = [NA[val] for val in isotope_list]
        na_vals.sort(reverse=True)
        na_val_dict[atom] = na_vals

    return na_val_dict


def replace_negatives(na_corr_dict, replace_negative=True):
    """
    This function replaces negative intensity values by zero from list of intensity
    in the standardised model dictionary

    Args:
        corrected_dict : nested dictionary (std model) with NA corrected intensity values
        replace_negative :
                          1. if True, replaces negative values and updates the dictionary
                          2. if False, return the nested dictionary with corrected values
                             as it is
    Returns:
        post_proc_dict : returns nested dictionary with negative values replaced

    """
    post_processed_dict = {}

    for metabolite, fragment_dict in na_corr_dict.iteritems():
        post_processed_dict[metabolite] = replace_negative_to_zero(fragment_dict,
                                                                           replace_negative)

    return post_processed_dict


def fractional_enrichment(post_processed_out, decimals=4):
    """
    This function calculates the fractional enrichment for each label
    Fractional enrichment[sample1] = Corrected Intensity/ Sum of corrected intensities of all labels

    Args:
        fragments_dict : Dictionary of the form, {'Metabname_label':
        [Fragment object, {'sample_name': intensity}, label/unlabe bool, metabname]
        decimals : number of decimals to keep

    Returns:
        fragments_fractional : fragment dictionary model of fractional enrichment values
    """
    frac_enrichment_dict = {}

    for metabolite, fragment_dict in post_processed_out.iteritems():
        frac_enrichment_dict[metabolite] = enrichment(fragment_dict, decimals)

    return frac_enrichment_dict


def convert_to_df(dict_output, parent, colname='col_name'):
    """
    This function convert the dictionary output from na_correction function, postprocessing
    and frac_enrichment_dict to dataframe

    Args:
        dict_output : dictionary model to be converted into df
        colname : specify name of column from which computation, the dictionary is obtained

    Returns:
        model_to_df : a pandas dataframe
        :param parent:
    """
    df_list = []

    for metabolite, fragment_dict in dict_output.iteritems():
        std_model = fragment_dict_to_std_model(fragment_dict, parent)
        model_to_df = convert_dict_df(std_model, parent)
        df_list.append(model_to_df)
        model_to_df = concatenate_dataframes_by_col(df_list)

    model_to_df.rename(columns={conf.INTENSITY_COL: str(colname)}, inplace=True)

    return model_to_df



def save_to_csv(df, path):
    """
    This function saves the dataframe to specified path

    Args:
        df : dataframe to be saved in directory
        path : path to directory
    """
    df.to_csv(path)
