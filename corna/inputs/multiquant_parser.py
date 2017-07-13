# TODO : many functions need to be documneted refer issue NCT-303

from collections import namedtuple
import os
import warnings


import pandas as pd

from .column_conventions import multiquant
from corna import constants
from ..constants import INTENSITY_COL
from corna.inputs import validation
from ..data_model import standard_model
from ..helpers import read_file, get_unique_values, check_column_headers
from ..isotopomer import bulk_insert_data_to_fragment

Multiquantkey = namedtuple('MultiquantKey', 'name formula parent parent_formula')


def get_validated_df_and_logs(input_files):
    """takes input files, validate it and sends back merge df

    This function takes input_file path in form of dictionary in which
    each key is name of the file and value as path of the file stored in
    local folder. It then validates these file and returns instance of
    all these files having validated df and its logs

    Args:
        input_files: {
            "mq_file_path": absolute path_of_mq_file,
            "mq_metadata_path": absolute path_of_metadata_file,
            "mq_sample_metadata_path": absolute path_of_sample_metadata_file
        }

    Returns:
        validated_raw_mq: instance of DATA VALIDATION class containing
            logs & validated_df for raw_mq file.
        validated_metadata_mq: instance of DATA VALIDATION class containing
            logs & validated_df for metadata_mq file.
        sample_metadata_mq: instance of BASIC VALIDATION class containing
            validated_df for sample_metadata_mq file.                        
    """
    try:
        raw_mq, metadata_mq, sample_metadata_mq = get_basic_validation_instance(input_files)
        if sample_metadata_mq:
            raw_mq_df = get_filtered_raw_mq_df(raw_mq, sample_metadata_mq)
        else:
            raw_mq_df = raw_mq.df
        validated_raw_mq = validation.data_validation_raw_df(raw_mq_df)
        validated_metadata_mq = validation.data_validation_metadata_df(metadata_mq.df)
        return validated_raw_mq, validated_metadata_mq, sample_metadata_mq
    except Exception as e:
        raise Exception(e)


def get_basic_validation_instance(input_files):
    """takes input file, does basic validation and returns instance of BASIC
    VALIDATION class of olmonk package

    This method takes dictionary of file_path, using BASIC VALIDATION class
    it validates the file and returns back the BASIC VALIDATION class instance
    of the file.

    Args:
        input_files: {
            "mq_file_path": path_of_mq_file,
            "mq_metadata_path": path_of_metadata_file,
            "mq_sample_metadata_path": path_of_sample_metadata_file
        }

    Returns:
        raw_mq: instance of basic_validation class for raw_mq_file
        metadata_mq: instance of basic_validation class for metadata_mq file
        sample_metadata_mq: instance of basic_validation class for sample_metadata_mq file
    """

    # :TODO: add exception handling in this file
    # :TODO: move constants to constants.py file
    mq_file_path = input_files.get("mq_file_path")
    raw_mq = validation.get_validation_df(mq_file_path)
    mq_metadata_path = input_files.get("mq_metadata_path")
    metadata_mq = validation.get_validation_df(mq_metadata_path)

    if input_files['mq_sample_metadata_path']:
        mq_sample_metadata_path = input_files.get('mq_sample_metadata_path')
        sample_metadata_mq = validation.get_validation_df(mq_sample_metadata_path)
    else:
        sample_metadata_mq = None
    return raw_mq, metadata_mq, sample_metadata_mq


def get_filtered_raw_mq_df(raw_mq, sample_metadata_mq):
    """
    This function apply validation on the the raw_mq df using columns of
    sample_metadata df as arguments and returns a filtered df
    according to the validation report.

    The function takes instance of basic_validation class of raw_mq &
    sample_metadata_mq do validation and returns updated raw_mq df
    using instance of raw_mq & sample_metadata_mq, it checks for subset and
    intersection of specific column, which updates the df of raw_mq. It then
    returns updated df of raw_mq

    Args:
        raw_mq: instance of basic_validation class for raw_mq file
        sample_metadata_mq: instance of basic_validation class for sample_metadata_file

    Returns:
        raw_mq.df: updates df of raw_mq file
    """
    # :TODO: update doc with exceptions info
    try:
        raw_filename_set = get_set_from_df_column(raw_mq.df, constants.ORIGINAL_FILENAME)
        sample_metadata_mq.check_if_subset(constants.BACKGROUND_SAMPLE, raw_filename_set)
        sample_filename_set = get_set_from_df_column(sample_metadata_mq.df, constants.ORIGINAL_FILENAME)
        raw_mq.check_if_intersect(constants.ORIGINAL_FILENAME, sample_filename_set)
        return raw_mq.df
    except Exception as e:
        raise Exception(e)


def get_set_from_df_column(df, col_name):
    """creates set of a particular column of a df"""

    return set(list(df[col_name]))


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
        if merged_df.empty:
            raise Exception('Empty Merge, no common entries to process, please check input files')
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
            check_column_headers(col_headers_sample, bg_corr_col_names_sample)
            check_column_headers(col_headers_merged, bg_corr_col_names_merged)
            assert set(sample_metadata[multiquant.BACKGROUND]).issubset(set(sample_metadata[multiquant.MQ_SAMPLE_NAME]))
            merged_df = merged_df.merge(sample_metadata, how='inner',
                                        on=[multiquant.MQ_SAMPLE_NAME, multiquant.MQ_COHORT_NAME])
            if merged_df.empty:
                raise Exception('Empty Merge, no common entries to process, please check input files')
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
    cohort_list = get_unique_values(sample_index_df, 'Background Cohort')
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
        bg_corr_col_names = [multiquant.BACKGROUND, multiquant.COHORT]
        try:
            check_column_headers(col_headers, bg_corr_col_names)
        except AssertionError:
            return merged_data, list_of_replicates, sample_background
        # consider only those sample names which are present in raw file
        sample_metdata = sample_metdata[sample_metdata[multiquant.MQ_SAMPLE_NAME].isin(merged_data[multiquant.SAMPLE])]
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