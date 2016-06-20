import os
import json
import numpy as np
import pandas as pd
import helpers as hl
import config as conf




def maven_merge_dfs(df1, df2):
    """
    This function combines the input file dataframe and the metadata
    file dataframe

    Args:
        input_data : input data in form of pandas dataframe

        metadata : metadata in the form of pandas dataframe

    Returns:
        combined_data : dataframe with input data and metadata combined
    """

    long_form = melt_df(df1)

    try:
        merged_df = hl.merge_dfs(long_form, df2, how = 'left', left_on = 'variable', right_on = 'sample')
    except KeyError:
        raise KeyError('sample column not found in metadata')

    merged_df[conf.PARENT_COL] = merged_df[conf.NAME_COL]

    merged_df.rename(columns={"variable": conf.SAMPLE_COL, "value":conf.INTENSITY_COL}, inplace=True)

    return merged_df


def mq_merge_dfs(df1, df2):

    try:
        merged_df = hl.merge_dfs(df1, df2, how= 'inner', left_on = 'Component Name', right_on = 'Fragment')
    except KeyError:
        raise KeyError('Missing columns: Componenet Name or Fragment')

    merged_df['Mass Info'] = merged_df['Mass Info'].str.replace(' / ', "_")

    remove_stds = remove_mq_stds(merged_df)

    remove_stds.rename(columns={"Component Name":conf.NAME_COL, "Area":conf.INTENSITY_COL}, inplace=True)
    return remove_stds


def get_sample_names(df):
    """
    This function gets the unique sample names from data
    """
    try:
        sample_list = df['Sample Name'].unique().tolist()
    except:
        raise KeyError('Column'+ conf.SAMPLE_COL + 'not found in dataframe')
    return sample_list


def standard_model(df, parent = False):
    """
    This function convert the merged data into standard data model
    """

    df = frag_key(df, parent = False)
    unique_frags = df[conf.FRAG_COL].unique().tolist()
    std_model_dict = {}

    for frags in unique_frags:
        df_subset = df[df[conf.FRAG_COL] == frags]
        unq_labels = df_subset[conf.LABEL_COL].unique().tolist()
        lab_dict = {}
        for label in unq_labels:
            df_subset_on_labels = df_subset[df_subset[conf.LABEL_COL] == label]

            label_frame = df_subset_on_labels.groupby(conf.SAMPLE_COL)[conf.INTENSITY_COL].apply(lambda x: np.array(x.tolist()))
            label_dict = label_frame.to_dict()
            lab_dict[label] = label_dict
        std_model_dict[frags] = lab_dict

    return std_model_dict


def melt_df(df1):
    """
    This function melts the dataframe in long form based on some fixed columns
    """
    fixed_cols = [conf.NAME_COL, conf.LABEL_COL, conf.FORMULA_COL]

    melt_cols = [x for x in df1.columns.tolist() if x not in fixed_cols]

    try:
        long_form = pd.melt(df1, id_vars=fixed_cols, value_vars=melt_cols)
    except KeyError():
        raise KeyError('columns' + conf.NAME_COL + conf.LABEL_COL + conf.FORMULA_COL + 'not found in data')

    return long_form

def remove_mq_stds(merged_df):
    """
    This function removes the standard samples from multiquant data
    """
    try:
        remove_stds = merged_df[merged_df['Sample Name'].str.contains("std") == False]
    except:
        raise KeyError('Std samples not found in' + conf.SAMPLE_COL +' column')
    remove_stds['Label'] = remove_stds['Isotopic Tracer'] + "_" + remove_stds['Mass Info']
    remove_stds.pop('Mass Info')
    remove_stds.pop('Isotopic Tracer')
    return remove_stds


def frag_key(df, parent = False):
    """
    This function creates a fragment key column in merged data based on parent information.
    """
    try:
        if parent == True:
            df[conf.FRAG_COL] = df.apply(lambda x : tuple([x[conf.NAME_COL], x[conf.FORMULA_COL], x[conf.PARENT_COL], x["Parent_Formula"]]), axis=1)
        elif parent == False:
            df[conf.FRAG_COL] = df.apply(lambda x : tuple([x[conf.NAME_COL], x[conf.FORMULA_COL]]), axis=1)
    except:
        raise KeyError('Missing columns in data')
    return df
















