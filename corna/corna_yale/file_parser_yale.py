from .. helpers import merge_dfs
from .. import config as conf

def mq_merge_dfs(df1, df2):
    """
    This function combines the MQ input file dataframe and the metadata
    file dataframe

    Args:
        input_data : MQ input data in form of pandas dataframe

        metadata : metadata in the form of pandas dataframe

    Returns:
        combined_data : dataframe with input data and metadata combined
    """

    try:
        merged_df = merge_dfs(df1, df2, how= 'inner', left_on = 'Component Name', right_on = 'Fragment')
    except KeyError:
        raise KeyError('Missing columns: Component Name or Fragment')

    merged_df[conf.MASSINFO_COL] = merged_df[conf.MASSINFO_COL].str.replace(' / ', "_")

    remove_stds = remove_mq_stds(merged_df)

    remove_stds.rename(columns={"Component Name":conf.NAME_COL, "Area":conf.INTENSITY_COL}, inplace=True)
    return remove_stds


def remove_mq_stds(merged_df):
    """
    This function removes the standard samples from multiquant data
    """
    try:
        remove_stds = merged_df[merged_df[conf.SAMPLE_COL].str.contains("std") == False]
    except:
        raise KeyError('Std samples not found in' + conf.SAMPLE_COL +' column')
    remove_stds[conf.LABEL_COL] = remove_stds[conf.ISOTRACER_COL] + "_" + remove_stds[conf.MASSINFO_COL]
    remove_stds.pop(conf.MASSINFO_COL)
    remove_stds.pop(conf.ISOTRACER_COL)
    return remove_stds


def frag_key(df):
    """
    This function creates a fragment key column in merged data based on parent information.
    """
    try:

        df[conf.FRAG_COL] = df.apply(lambda x : tuple([x[conf.NAME_COL], x[conf.FORMULA_COL], x[conf.PARENT_COL], x["Parent Formula"]]), axis=1)
    except KeyError:
        raise KeyError('Missing columns in data')
    return df