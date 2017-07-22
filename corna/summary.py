import pandas as pd

import constants as cs


def create_list_of_dict(list_of_fields, fields_dict):
    """
    It returns a list of dictionaries defining fields (rows,
    columns, metabolites) in the dataframe
    :param list_of_fields:list of fields to be displayed
           example : ['number of rows']
    :param fields_dict: dictionary with field as key and
    corresponding function as value
    :return: list of dictionary
    """
    summary_list = []
    for i in range(0, len(list_of_fields)):
        summary_dict = {}
        summary_dict[cs.SUMMARY_LABEL] = list_of_fields[i]
        summary_dict[cs.SUMMARY_VAL] = fields_dict[list_of_fields[i]]
        summary_list.append(summary_dict)
    return summary_list


def summary_raw_intensity_msms(raw_intensity_df):
    """
    This function returns summary list for lcms/ms raw
     intensity file
    :param raw_intensity_df: raw intensity input file
    :return: summary list
    """
    field_dict = {cs.RAW_FIELD_SUMMARY_LIST[0]: raw_intensity_df[cs.ORIGINAL_FILENAME].count(),
                  cs.RAW_FIELD_SUMMARY_LIST[1]: len(raw_intensity_df[cs.ORIGINAL_FILENAME].unique()),
                  cs.RAW_FIELD_SUMMARY_LIST[2]: len(raw_intensity_df[cs.SAMPLE_NAME].unique()),
                  cs.RAW_FIELD_SUMMARY_LIST[3]: len(raw_intensity_df[cs.COMPONENT_NAME].unique())}
    dict_label_list = field_dict.keys()
    return create_list_of_dict(dict_label_list, field_dict)


def summary_metadata_mq(metadata_mq_df):
    """
    This function returns summary list for lcms/ms
        metadata mq file
    :param metadata_mq_df: metadata mq input file
    :return: summary list
    """
    field_dict = {cs.META_FIELD_SUMMARY_LIST[0]: metadata_mq_df[cs.COMPONENT_NAME].count(),
                  cs.META_FIELD_SUMMARY_LIST[1]: len(metadata_mq_df[cs.PARENT_COL].unique()),
                  cs.META_FIELD_SUMMARY_LIST[2]: list((metadata_mq_df[cs.ISOTRACER_COL].unique()))
            }
    dict_label_list = field_dict.keys()
    return create_list_of_dict(dict_label_list, field_dict)


def summary_sample_metadata(metadata_std_df):
    """
    This function returns summary list for lcms/ms sample
        metadata file
    :param metadata_std_df: raw intensity input file
    :return: summary list
    """
    field_dict = {cs.SAMPLE_FIELD_SUMMARY_LIST[0]: len(metadata_std_df[cs.BACKGROUND_SAMPLE].unique()),
                  cs.SAMPLE_FIELD_SUMMARY_LIST[1]: ", ".join(list(metadata_std_df)),
                 }
    dict_label_list = field_dict.keys()
    return create_list_of_dict(dict_label_list, field_dict)


def summary_raw_intensity_lcms(raw_intensity_df):
    """
    This function returns summary list for lcms raw
        intensity file
    :param raw_intensity_df: raw intensity input file
    :return: summary list
    """
    field_dict = {cs.LCMS_RAW_FIELD_SUMMARY[0]: len(raw_intensity_df[cs.NAME_COL].unique()),
                  cs.LCMS_RAW_FIELD_SUMMARY[1]: (len(list(raw_intensity_df)) - 3),
                  cs.LCMS_RAW_FIELD_SUMMARY[2]: raw_intensity_df.isnull().values.ravel().sum(),
                  cs.LCMS_RAW_FIELD_SUMMARY[3]: raw_intensity_df[cs.LABEL_COL].count()}
    dict_label_list = field_dict.keys()
    return create_list_of_dict(dict_label_list, field_dict)


def lcms_metadata(meta_df):
    """
    This function returns summary list for lcms
          metadata file
    :param meta_df: lcms metadata input file
    :return: summary list
    """
    field_dict = {cs.LCMS_META_FILED_SUMMARY[0]: ", ".join(list(meta_df)),
                  cs.LCMS_META_FILED_SUMMARY[1]: list(meta_df[[0]].count())[0],}
    dict_label_list = field_dict.keys()
    return create_list_of_dict(dict_label_list, field_dict)