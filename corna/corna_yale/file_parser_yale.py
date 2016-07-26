from corna.helpers import merge_dfs
import config_yale

def mq_merge_dfs(df1, df2, df3):
    """
    This function combines the MQ input file dataframe and the metadata
    file dataframe

    Args:
        input_data : MQ input data in form of pandas dataframe

        metadata : metadata in the form of pandas dataframe

    Returns:
        combined_data : dataframe with input data and metadata combined
        :param df3:
    """

    try:
        merged_df = df1.merge(df2, how='inner', left_on=config_yale.MQ_FRAGMENT_COL,
                                 right_on=config_yale.MQ_FRAGMENT_COL)
        merged_df = merged_df.merge(df3, how='inner', left_on=config_yale.MQ_SAMPLE_NAME,
                              right_on=config_yale.MQ_SAMPLE_NAME)
    except KeyError:
        raise KeyError('Missing columns:' + config_yale.MQ_FRAGMENT_COL + 'or' + config_yale.MQ_SAMPLE_NAME)

    merged_df[config_yale.MASSINFO_COL] = merged_df[config_yale.MASSINFO_COL].str.replace(' / ', "_")
    merged_df.rename(columns={config_yale.MQ_FRAGMENT_COL: config_yale.NAME_COL,
                              config_yale.MQ_COHORT_NAME: config_yale.COHORT_COL}, inplace=True)
    #first change Sample Name to Cohort Name, then Original Filename to Sample Name
    #refer to multiquant raw output
    merged_df.rename(columns={config_yale.MQ_SAMPLE_NAME: config_yale.SAMPLE_COL}, inplace=True)
    remove_stds = remove_mq_stds(merged_df)

    remove_stds.rename(columns={"Component Name":config_yale.NAME_COL, "Area":config_yale.INTENSITY_COL}, inplace=True)
    return remove_stds


def remove_mq_stds(merged_df):
    """
    This function removes the standard samples from multiquant data
    """
    try:
        remove_stds = merged_df[merged_df[config_yale.COHORT_COL].str.contains("std") == False]
    except:
        raise KeyError('Std samples not found in' + config_yale.COHORT_COL +' column')
    remove_stds[config_yale.LABEL_COL] = remove_stds[config_yale.ISOTRACER_COL] + "_" + remove_stds[config_yale.MASSINFO_COL]
    remove_stds.pop(config_yale.MASSINFO_COL)
    remove_stds.pop(config_yale.ISOTRACER_COL)
    return remove_stds


def frag_key(df):
    """
    This function creates a fragment key column in merged data based on parent information.
    """
    try:
        df[config_yale.FRAG_COL] = df.apply(lambda x : tuple([x[config_yale.NAME_COL],
                                                              x[config_yale.FORMULA_COL],
                                                              x[config_yale.PARENT_COL],
                                                              x[config_yale.PARENT_FORMULA_COL]]), axis=1)
    except KeyError:
        raise KeyError('Missing columns in data')
    return df