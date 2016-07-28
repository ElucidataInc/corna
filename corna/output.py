import pandas as pd

from . import config as conf
from . helpers import concatenate_dataframes_by_col, LEVEL_0_COl, LEVEL_1_COL
from . isotopomer import fragment_dict_to_std_model


def convert_dict_df(nest_dict, parent):
    """
    This function convert the fragment dictionary model in dataframe
    Args:
        nest_dict : dictionary of the form ('L-Methionine', 'C5H10NO2S'):
        {'C13_1': {'sample_1': array([  3.18407678e-07])}, 'C13_0': {'sample_1': array([ 0.48557866])}..}

    Returns:
        final_df : final dataframe
    """
    df_list = []
    for frag_name, label_dict in nest_dict.iteritems():
        df, df_list = lists_labeldict(df_list, frag_name, label_dict, parent)
    if parent is True:
        final_df = pd.concat(df_list)
    else:
        final_df = df
    final_df.rename(columns={
        LEVEL_0_COl: conf.LABEL_COL,
        0: conf.SAMPLE_COL,
        1: conf.INTENSITY_COL},
        inplace=True)
    final_df.pop(LEVEL_1_COL)

    return final_df


def lists_labeldict(df_list, frag_name, label_dict, parent):
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
    name = []
    formula = []
    parent_list = []
    lab = []
    frames = []

    for label, samp_dict in label_dict.iteritems():
        tup = []
        for samp, intens in samp_dict.iteritems():
            for intensity in intens:
                tup.append((samp, intensity))
                name.append(frag_name[0])
                formula.append(frag_name[1])
                if parent:
                    parent_list.append(frag_name[2])
        lab.append(label)
        frames.append(pd.DataFrame(tup))
        df = pd.concat(frames, keys=lab).reset_index()
        df[conf.NAME_COL] = name
        df[conf.FORMULA_COL] = formula
        if parent:
            df[conf.PARENT_COL] = parent_list
            df_list.append(df)

    return (df, df_list)


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

    model_to_df.rename(
        columns={conf.INTENSITY_COL: str(colname)}, inplace=True)

    return model_to_df


def save_to_csv(df, path):
    """
    This function saves the dataframe to specified path

    Args:
        df : dataframe to be saved in directory
        path : path to directory
    """
    df.to_csv(path)
