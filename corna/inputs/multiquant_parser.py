from .. import config as config_yale
from ..helpers import concat_txts_into_df, read_file


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
        merged_df.drop(config_yale.MQ_COHORT_NAME, axis=1, inplace=True)
        merged_df = merged_df.merge(df3, how='inner', left_on=config_yale.MQ_SAMPLE_NAME,
                                    right_on=config_yale.MQ_SAMPLE_NAME)
    except KeyError:
        raise KeyError('Missing columns:' + config_yale.MQ_FRAGMENT_COL +
                       'or' + config_yale.MQ_SAMPLE_NAME)

    merged_df[config_yale.MASSINFO_COL] = merged_df[
        config_yale.MASSINFO_COL].str.replace(' / ', "_")
    merged_df.rename(
        columns={config_yale.MQ_FRAGMENT_COL: config_yale.NAME_COL}, inplace=True)
    # first change Sample Name to Cohort Name, then Original Filename to Sample Name
    # refer to multiquant raw output
    merged_df.rename(
        columns={config_yale.MQ_SAMPLE_NAME: config_yale.SAMPLE_COL}, inplace=True)
    remove_stds = remove_mq_stds(merged_df)
    remove_stds.rename(columns={"Component Name": config_yale.NAME_COL,
                                "Area": config_yale.INTENSITY_COL}, inplace=True)
    return remove_stds


def remove_mq_stds(merged_df):
    """
    This function removes the standard samples from multiquant data
    """
    try:
        remove_stds = merged_df[
            merged_df[config_yale.COHORT_COL].str.contains("std") == False]
    except:
        raise KeyError('Std samples not found in' +
                       config_yale.COHORT_COL + ' column')
    remove_stds[config_yale.LABEL_COL] = remove_stds[
        config_yale.ISOTRACER_COL] + "_" + remove_stds[config_yale.MASSINFO_COL]
    remove_stds.pop(config_yale.MASSINFO_COL)
    remove_stds.pop(config_yale.ISOTRACER_COL)
    return remove_stds


def get_replicates(sample_metadata, sample_name, cohort_name, background_sample):
    sample_index_df = sample_metadata.set_index(sample_name)
    sample_index_df['Background Cohort'] = sample_index_df[
        background_sample].map(sample_index_df[cohort_name])
    replicate_groups = []
    # std should not be present in sample_metadata
    cohort_list = sample_index_df['Background Cohort'].unique()
    for cohorts in cohort_list:
        newdf = sample_index_df[sample_index_df[
            'Background Cohort'] == cohorts]
        replicate_groups.append(newdf[background_sample].unique())
    return replicate_groups


def get_background_samples(sample_metadata, sample_name, background_sample):
    sample_background = sample_metadata.set_index(sample_name).to_dict()
    return sample_background[background_sample]


def frag_key(df):
    """
    This function creates a fragment key column in merged data based on parent information.
    """
    def _extract_keys(x):
        return (x[config_yale.NAME_COL],
                x[config_yale.FORMULA_COL],
                x[config_yale.PARENT_COL],
                x[config_yale.PARENT_FORMULA_COL])
    try:
        df[config_yale.FRAG_COL] = df.apply(_extract_keys, axis=1)
    except KeyError:
        raise KeyError('Missing columns in data')
    return df


def read_multiquant(dir_path):
    mq_df = concat_txts_into_df(dir_path)
    return mq_df


def read_multiquant_metadata(path):
    mq_metdata = read_file(path)
    return mq_metdata


def merge_mq_metadata(mq_df, metdata, sample_metdata):
    merged_data = mq_merge_dfs(mq_df, metdata, sample_metdata)
    merged_data.fillna(0, inplace=True)
    list_of_replicates = get_replicates(
        sample_metdata, config_yale.MQ_SAMPLE_NAME, config_yale.COHORT_COL, config_yale.BACKGROUND_COL)
    sample_background = get_background_samples(
        sample_metdata, config_yale.MQ_SAMPLE_NAME, config_yale.BACKGROUND_COL)
    return merged_data, list_of_replicates, sample_background
