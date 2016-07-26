import numpy as np
import pandas as pd

import helpers as hl
from . import config as conf


def get_sample_names(df):
    """
    This function gets the unique sample names from data

    Args:
        df : dataframe with Sample column
    Returns:
        sample_list : list of unique sample names from data
    """
    try:
        sample_list = df[conf.SAMPLE_COL].unique().tolist()
    except:
        raise KeyError('Column' + conf.SAMPLE_COL + 'not found in dataframe')

    return sample_list


def standard_model(df):
    """
    This function convert the merged data into standard data model
    """

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














