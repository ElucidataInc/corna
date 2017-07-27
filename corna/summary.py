import pandas as pd

import constants as cs


def create_list_of_dict(list_of_fields, fields_dict):
    """
    It returns a list of dictionaries defining fields (rows,
    columns, metabolites) in the data frame
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


def summary_raw_msms(raw_df):
    """
    This function creates a dictionary of functions
    to be performed on input df
    :param raw_df: input data frame
    :return: dictionary of data frame operations

    """
    summary_dict = {cs.RAW_FIELD_SUMMARY_LIST[0]: raw_df[cs.ORIGINAL_FILENAME].count(),
                    cs.RAW_FIELD_SUMMARY_LIST[1]: len(raw_df[cs.ORIGINAL_FILENAME].unique()),
                    cs.RAW_FIELD_SUMMARY_LIST[2]: len(raw_df[cs.SAMPLE_NAME].unique()),
                    cs.RAW_FIELD_SUMMARY_LIST[3]: len(raw_df[cs.COMPONENT_NAME].unique())}
    return summary_dict


def summary_meta_msms(raw_df):
    """
    This function creates a dictionary of functions
    to be performed on metadata mq df
    :param raw_df: input data frame
    :return: dictionary of data frame operations

    """
    summary_dict = {cs.META_FIELD_SUMMARY_LIST[0]: raw_df[cs.COMPONENT_NAME].count(),
                    cs.META_FIELD_SUMMARY_LIST[1]: len(raw_df[cs.PARENT_COL].unique())}
    if cs.COLUMN_ISOTOPE_TRACER in list(raw_df):
        summary_dict[cs.META_FIELD_SUMMARY_LIST[2]] = (raw_df[cs.COLUMN_ISOTOPE_TRACER].unique()).item()
    return summary_dict


def summary_smp_msms(raw_df):
    """
    This function creates a dictionary of functions
    to be performed on sample metadata df
    :param raw_df: input data frame
    :return: dictionary of data frame operations

    """
    summary_dict = {cs.SAMPLE_FIELD_SUMMARY_LIST[0]: len(raw_df[cs.BACKGROUND_SAMPLE].unique()),
                    cs.SAMPLE_FIELD_SUMMARY_LIST[1]: ", ".join(list(raw_df))}
    return summary_dict


def summary_raw_lcms(raw_df):
    """
    This function creates a dictionary of functions
    to be performed on raw intensity df
    :param raw_df: input data frame
    :return: dictionary of data frame operations

    """
    summary_dict = {cs.LCMS_RAW_FIELD_SUMMARY[0]: len(raw_df[cs.NAME_COL].unique()),
                    cs.LCMS_RAW_FIELD_SUMMARY[1]: (len(list(raw_df)) - 3),
                    cs.LCMS_RAW_FIELD_SUMMARY[2]: raw_df.isnull().values.ravel().sum(),
                    cs.LCMS_RAW_FIELD_SUMMARY[3]: raw_df[cs.LABEL_COL].count()}
    return summary_dict


def summary_meta_lcms(raw_df):
    """

    This function creates a dictionary of functions
    to be performed on metadata df
    :param raw_df: input data frame
    :return: dictionary of data frame operations

    """
    summary_dict = {cs.LCMS_META_FILED_SUMMARY[0]: ", ".join(list(raw_df)),
                    cs.LCMS_META_FILED_SUMMARY[1]: list(raw_df[[0]].count())[0]}
    return summary_dict


def create_summary(raw_df, df_type):
    """

    This function returns details of input df to be
    displayed on summary tab.
    :param raw_df: input data frame
    :param df_type: file type of data frame
    :return: array of fields (eg. number of rows) in the input data frame

    """
    summary_filetype_dict = {cs.RAW_MSMS: summary_raw_msms,
                             cs.META_MSMS: summary_meta_msms,
                             cs.SMP_MSMS: summary_smp_msms,
                             cs.RAW_LCMS: summary_raw_lcms,
                             cs.META_LCMS: summary_meta_lcms}

    try:
        summary_field_dict = summary_filetype_dict[df_type].__call__(raw_df)
    except KeyError:
        return None

    dict_label_list = summary_field_dict.keys()

    return create_list_of_dict(dict_label_list, summary_field_dict)


def return_summary_dict(df_type, df):
    """
    This function returns summary of type
    {title: INPUT DATA, summary: ['number of rows': 3]}
    :param df_type: type of df like input df, metadata df
    :param df: data frame
    :return: summary dictionary
    """
    summary_dict = {cs.SUMMARY_TITLE: df_type,
                    cs.SUMMARY: create_summary(df, df_type)}

    return summary_dict
