import numpy as np

from helpers import get_unique_values
from constants import FRAG_COL, LABEL_COL, SAMPLE_COL


def standard_model(df, intensity_col):
    """
    This function convert the merged data into standard data model
    """

    unique_frags = get_unique_values(df, FRAG_COL)
    std_model_dict = {}

    for frags in unique_frags:
        df_subset = df[df[FRAG_COL] == frags]
        unq_labels = get_unique_values(df_subset, LABEL_COL)
        lab_dict = {}
        for label in unq_labels:
            df_labels = df_subset[df_subset[LABEL_COL] == label]
            label_frame = df_labels.groupby(SAMPLE_COL)[intensity_col].apply(_to_float)
            label_dict = label_frame.to_dict()
            lab_dict[label] = label_dict
        std_model_dict[frags] = lab_dict

    return std_model_dict


def _to_float(x):
    return x.tolist()[0]
