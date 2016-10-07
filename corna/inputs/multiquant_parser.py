import os
import pandas as pd
from collections import namedtuple
import warnings

from ..data_model import standard_model
from . column_conventions import multiquant
from ..helpers import read_file, get_unique_values
from ..isotopomer import bulk_insert_data_to_fragment
from ..constants import INTENSITY_COL

Multiquantkey = namedtuple('MultiquantKey', 'name formula parent parent_formula')

def concat_txts_into_df(directory):
    """read text files with same column names and merge them to one
    dataframe
    Args:
        directory: path of the directory containing the text files
    Returns:
        merged dataframe
    """
    txt_files = []
    txt_files += [each for each in os.listdir(directory) if each.endswith('.txt')]
    df_list= []
    col_names = [multiquant.MQ_SAMPLE_NAME, multiquant.MQ_FRAGMENT, multiquant.MASSINFO, multiquant.AREA]
    for files in txt_files:
        df = read_file(directory + '/' + files)
        col_headers =  df.columns.tolist()
        check_mq_column_headers(col_headers, col_names)
        df_list.append(df)
    concat_df = pd.concat(df_list).reset_index(drop=True)

    return concat_df

def read_multiquant(dir_path):
    mq_df = concat_txts_into_df(dir_path)
    return mq_df

def read_multiquant_metadata(path):
    """read metadata file"""
    mq_metdata = read_file(path)
    col_headers = mq_metdata.columns.values
    col_names = [multiquant.PARENT, multiquant.MQ_FRAGMENT,
                 multiquant.FORMULA, multiquant.PARENT_FORMULA]
    check_mq_column_headers(col_headers, col_names)
    return mq_metdata

def read_sample_metadata(path):
    """read metadata file"""
    std_smpl_metadata = read_file(path)
    col_headers = std_smpl_metadata.columns.values
    col_names = [multiquant.MQ_SAMPLE_NAME]
    check_mq_column_headers(col_headers, col_names)


    return std_smpl_metadata

def check_mq_column_headers(col_headers, col_names):
    """
    This function verifies that all defasult columns are present in input
    text files for multiquant
    """
    err_msg = """Required column/s not found, Column: {!r}""".format(list(set(col_names) - set(col_headers)))
    assert set(col_names).issubset(set(col_headers)), err_msg


def mq_merge_meta(input_data, metadata):
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
        merged_df = input_data.merge(metadata, how='inner',
                              left_on=multiquant.MQ_FRAGMENT,
                              right_on=multiquant.MQ_FRAGMENT)

    except KeyError:
        raise KeyError('Missing columns: ' + multiquant.MQ_FRAGMENT)
    merged_df[multiquant.MASSINFO] = merged_df[multiquant.MASSINFO].str.replace(' / ', "_")
    return merged_df

def merge_samples(merged_df, sample_metadata):
    if sample_metadata is not None:
        col_headers_sample = sample_metadata.columns.values
        col_headers_merged = merged_df.columns.values
        bg_corr_col_names_sample = [multiquant.BACKGROUND, multiquant.MQ_COHORT_NAME]
        bg_corr_col_names_merged = [multiquant.MQ_COHORT_NAME]
        try:
            check_mq_column_headers(col_headers_sample, bg_corr_col_names_sample)
            check_mq_column_headers(col_headers_merged, bg_corr_col_names_merged)

            merged_df = merged_df.merge(sample_metadata, how='inner',
                                    on=[multiquant.MQ_SAMPLE_NAME, multiquant.MQ_COHORT_NAME])
        except AssertionError:
            warnings.warn("Background Correction can't be performed")
            merged_df = merged_df.merge(sample_metadata, how='inner',
                                    on=[multiquant.MQ_SAMPLE_NAME])

    # first change Sample Name to Cohort Name, then Original Filename to Sample
    # refer to multiquant raw output
    merged_df.rename(
            columns={multiquant.MQ_COHORT_NAME: multiquant.COHORT}, inplace=True)
    merged_df.rename(
            columns={multiquant.MQ_SAMPLE_NAME: multiquant.SAMPLE}, inplace=True)

    remove_stds = remove_mq_stds(merged_df)
    remove_stds.rename(columns={"Area": multiquant.INTENSITY}, inplace=True)
    return remove_stds

def mq_merge_dfs(input_data, metadata, sample_metadata):
    merged_data = mq_merge_meta(input_data, metadata)
    return merge_samples(merged_data, sample_metadata)

def remove_mq_stds(merged_df):
    """
    This function removes the standard samples from multiquant data
    """
    try:
        merged_df = merged_df[not merged_df[multiquant.COHORT].str.contains("std")]
    except:
        warnings.warn('Std samples not found in' + multiquant.COHORT + ' column')

    merged_df[multiquant.LABEL] = merged_df[multiquant.ISOTRACER] + "_" + merged_df[multiquant.MASSINFO]
    merged_df.rename(
        columns={multiquant.PARENT: multiquant.NAME}, inplace=True)
    merged_df.pop(multiquant.MASSINFO)
    merged_df.pop(multiquant.ISOTRACER)
    return merged_df


def get_replicates(sample_metadata, sample_name, cohort_name, background_sample):
    sample_index_df = sample_metadata.set_index(sample_name)
    sample_index_df['Background Cohort'] = sample_index_df[
        background_sample].map(sample_index_df[cohort_name])
    replicate_groups = []
    # std should not be present in sample_metadata
    cohort_list = get_unique_values(sample_index_df,'Background Cohort')
    for cohorts in cohort_list:
        newdf = sample_index_df[sample_index_df[
            'Background Cohort'] == cohorts]
        replicate_groups.append(get_unique_values(newdf, background_sample))
    return replicate_groups


def get_background_samples(sample_metadata, sample_name, background_sample):
    sample_background = sample_metadata.set_index(sample_name).to_dict()
    return sample_background[background_sample]


def frag_key(df):
    """
    This function creates a fragment key column in merged data based on parent information.
    """
    def _extract_keys(x):
        return Multiquantkey(x[multiquant.MQ_FRAGMENT],
                x[multiquant.FORMULA],
                x[multiquant.NAME],
                x[multiquant.PARENT_FORMULA])
    try:
        df[multiquant.FRAG] = df.apply(_extract_keys, axis=1)
    except KeyError:
        raise KeyError('Missing columns in data')
    return df

def merge_mq_metadata(mq_df, metdata, sample_metdata):
    merged_data = mq_merge_dfs(mq_df, metdata, sample_metdata)
    merged_data.fillna(0, inplace=True)
    list_of_replicates = []
    sample_background = []

    if sample_metdata is not None:
        col_headers = merged_data.columns.values
        bg_corr_col_names = [multiquant.BACKGROUND, multiquant.MQ_COHORT_NAME]
        try:
            check_mq_column_headers(col_headers, bg_corr_col_names)
        except AssertionError:
            return merged_data, list_of_replicates, sample_background

        list_of_replicates = get_replicates(
            sample_metdata, multiquant.MQ_SAMPLE_NAME, multiquant.MQ_COHORT_NAME, multiquant.BACKGROUND)
        sample_background = get_background_samples(
            sample_metdata, multiquant.MQ_SAMPLE_NAME, multiquant.BACKGROUND)
    return merged_data, list_of_replicates, sample_background

def mq_df_to_fragmentdict(merged_df, intensity_col=INTENSITY_COL):
    frag_key_df = frag_key(merged_df)
    std_model_mq = standard_model(frag_key_df, intensity_col)
    metabolite_frag_dict = {}
    for frag_name, label_dict in std_model_mq.iteritems():
        curr_frag_name = Multiquantkey(frag_name.name, frag_name.formula,
                                       frag_name.parent, frag_name.parent_formula)
        if metabolite_frag_dict.has_key(frag_name.parent):
            metabolite_frag_dict[frag_name.parent].update(bulk_insert_data_to_fragment(curr_frag_name,
                                                                              label_dict, mass=True))
        else:
            metabolite_frag_dict[frag_name.parent] = bulk_insert_data_to_fragment(curr_frag_name,
                                                                              label_dict, mass=True)
    return metabolite_frag_dict