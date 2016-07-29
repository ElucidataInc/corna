import numpy as np

# XXX: Change before showing to Victor
# Figure out a better way.
from .inputs.column_conventions import multiquant as c


def get_sample_names(df):
    """
    This function gets the unique sample names from data

    Args:
        df : dataframe with Sample column
    Returns:
        sample_list : list of unique sample names from data
    """
    try:
        sample_list = df[c.SAMPLE].unique().tolist()
    except:
        raise KeyError('Column' + c.SAMPLE + 'not found in dataframe')

    return sample_list


def standard_model(df):
    """
    This function convert the merged data into standard data model
    """

    unique_frags = df[c.FRAG].unique().tolist()
    std_model_dict = {}

    for frags in unique_frags:
        df_subset = df[df[c.FRAG] == frags]
        unq_labels = df_subset[c.LABEL].unique().tolist()
        lab_dict = {}
        for label in unq_labels:
            df_labels = df_subset[df_subset[c.LABEL] == label]
            label_frame = df_labels.groupby(c.SAMPLE)[c.INTENSITY].apply(_to_np_array)
            label_dict = label_frame.to_dict()
            lab_dict[label] = label_dict
        std_model_dict[frags] = lab_dict

    return std_model_dict


def _to_np_array(x):
    return np.array(x.tolist())
