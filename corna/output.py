from collections import namedtuple

import pandas as pd

import constants as const
from helpers import concatenate_dataframes_by_col
from helpers import label_dict_to_key, get_key_from_single_value_dict
from inputs.column_conventions import multiquant as c
from inputs.column_conventions.maven import NAME, SAMPLE
from postprocess import pool_total, pool_total_MSMS
from inputs.maven_parser import MavenKey
from inputs.multiquant_parser import Multiquantkey


OutKey = namedtuple('OutKey', 'name formula')

def convert_dict_df(nest_dict):
    """
    This function convert the fragment dictionary model in dataframe
    Args:
        nest_dict : dictionary of the form ('L-Methionine', 'C5H10NO2S'):
        {'C13_1': {'sample_1': 3.18407678e-07}, 'C13_0': {'sample_1': 0.48557866}..}

    Returns:
        final_df : final dataframe
    """
    for frag_name, label_dict in nest_dict.iteritems():
        df = lists_labeldict(frag_name, label_dict)
    df.rename(columns={
        const.LEVEL_0_COL: c.LABEL,
        0: c.SAMPLE,
        1: c.INTENSITY},
        inplace=True)
    df.pop(const.LEVEL_1_COL)

    return df


def lists_labeldict(frag_name, label_dict):
    """
    This function extracts lists of metabolite name, formula, parent from
    label dictionary model
    Args:
        df_list : list of dataframes to be combined

        frag_name : metabolite and its formula

        label_dict : dictionary with labels as keys adn intensity as intensalues

    Returns:
        (df, df_list) : final dataframe or list of dataframes to be appended
        :param parent:
    """
    lab = []
    frames = []
    for label, samp_dict in label_dict.iteritems():
        lab.append(label)

        #TODO: explain why there is a need of conversion of dict to
        #list of tuples when pd.DataFrame accept dict. Currently, it shows
        #error - ValueError: If using all scalar values, you must pass an index

        frames.append(pd.DataFrame(list(samp_dict.iteritems())))
        df = pd.concat(frames, keys=lab).reset_index()
        df[c.NAME] = frag_name.name
        df[c.FORMULA] = frag_name.formula

    return df


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
        model_to_df = convert_dict_df(std_model)
        df_list.append(model_to_df)
        model_to_df = concatenate_dataframes_by_col(df_list)

    model_to_df.rename(
        columns={c.INTENSITY: str(colname)}, inplace=True)

    return model_to_df


def convert_to_df_nacorr(dict_output, ele_corr_dict, parent, colname='col_name'):
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
        model_to_df = convert_dict_df(std_model)
        df_list.append(model_to_df)
        model_to_df = concatenate_dataframes_by_col(df_list)

    model_to_df.rename(
        columns={c.INTENSITY: str(colname)}, inplace=True)
    pool_total_df = pool_total(model_to_df, str(colname))
    model_to_df[const.INDIS_ISOTOPE_COL] = model_to_df[NAME].map(ele_corr_dict)
    model_to_df[const.POOL_TOTAL_COL] = model_to_df.apply(lambda x: pool_total_df[x[NAME]][x[SAMPLE]], axis=1)
    return model_to_df

def convert_to_df_nacorr_MSMS(dict_output, parent, colname='col_name'):
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
        model_to_df = convert_dict_df(std_model)
        df_list.append(model_to_df)
        model_to_df = concatenate_dataframes_by_col(df_list)

    model_to_df.rename(
        columns={c.INTENSITY: str(colname)}, inplace=True)
    pool_total_df = pool_total_MSMS(model_to_df, str(colname))
    model_to_df[const.POOL_TOTAL_COL] = model_to_df.apply(lambda x: pool_total_df[x[const.METABOLITE_NAME]][x[SAMPLE]], axis=1)
    return model_to_df



def save_to_csv(df, path):
    """
    This function saves the dataframe to specified path

    Args:
        df : dataframe to be saved in directory
        path : path to directory
    """
    df.to_csv(path)


def fragment_to_output_model_mass(infopacket):
    parent_frag, daughter_frag = infopacket.frag
    daughter_formula = daughter_frag.formula
    key_tuple = OutKey(infopacket.name, daughter_formula)
    label_dict_key = str(parent_frag.isotracer) + '_' + \
        str(parent_frag.isotope_mass) + '_' + \
        str(daughter_frag.isotope_mass)
    return {key_tuple: {label_dict_key: infopacket.data}}


def fragment_to_output_model_number(infopacket):
    key_tuple = OutKey(infopacket.name, infopacket.frag.formula)
    label_dict_key = label_dict_to_key(infopacket.frag.label_dict)
    return {key_tuple: {label_dict_key: infopacket.data}}


def fragment_dict_to_std_model(fragment_dict, parent):
    output_fragment_dict = {}
    if parent:
        for key, value in fragment_dict.iteritems():
            label_dict = fragment_to_output_model_mass(value)
            curr_key = get_key_from_single_value_dict(label_dict)
            try:
                output_fragment_dict[curr_key].update(label_dict[curr_key])
            except KeyError:
                output_fragment_dict.update(label_dict)
    else:
        for key, value in fragment_dict.iteritems():
            label_dict = fragment_to_output_model_number(value)
            curr_key = get_key_from_single_value_dict(label_dict)
            try:
                output_fragment_dict[curr_key].update(label_dict[curr_key])
            except KeyError:
                output_fragment_dict.update(label_dict)
    return output_fragment_dict

