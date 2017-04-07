"""This module helps to do validation using validation package olmonk"""

from corna import constants
from olmonk import basic_validation, data_validation

def get_validation_df(path, required_columns=None):
    """takes path of the file, validates it and returns result

    Using path of the file, it instantiates the validation class
    and use its methods to validate file and returns result of
    that. If file not passes the validation checks, then it will
    raise an error, otherwise it will returns validated df.
    Args:
        path: file path for which validation is needed

    Returns: instance of validated df
    """
    try:
        basic_validator = get_class_inst(basic_validation.BasicValidator, path, required_columns)
        basic_validation_result(basic_validator)
        return basic_validator
    except Exception as e:
        raise Exception(e)


def get_class_inst(class_name, file_path, required_columns):
    """
    Instantiates class with its argument and returns it
    """

    return class_name(file_path, required_columns)


def basic_validation_result(basic_validator):
    """
    Takes instance of BASIC VALIDATION class, do basic validation
    such as if file path exists, is file empty. This function will
    raise an error if any check fails.
    """

    try:
        basic_validator.check_path_exist()
        basic_validator.check_file_empty()
        basic_validator.check_if_convert_to_df()
    except Exception as e:
        raise Exception(e)


def data_validation_raw_df(df):
    """do datavalidtaion for raw_file_df and returns report_df

    It takes df of raw_mq file, creates an instance of DataValidation
    using this df. It then does validation related to file and returns
    the report_df.

    Args:
        df: raw_mq_file df

    Returns:
        report_df contains report of error & warning in this df
    """
    # :TODO: update doc when this function will be updated
    try:
        raw_df_validator = data_validation.DataValidator(df)
        raw_df_validator.missing_data()
        raw_df_validator.numerical(constants.AREA_COLUMN_RAWFILE)
        raw_df_validator.pattern_match([constants.MASSINFO_COL],
                                       constants.PATTERN_MASSINFO_COL)
        raw_df_validator.perform_action_and_generate_logs()
        return raw_df_validator
    except Exception as e:
        raise Exception(e)


def data_validation_metadata_df(df):
    """do datavalidtaion for metadata_mq_df and returns instance of
    DATA VALIDATION class.

    It takes df of metadata_mq file, creates an instance of DataValidation
    using this df. It then does validation related to file and returns
    the report_df.

    Args:
        df: metadata_mq_file df

    Returns:
        report_df contains report of error & warning in this df
    """
    # :TODO: update doc when this function will be updated
    try:
        metadata_df_validator = data_validation.DataValidator(df)
        metadata_df_validator.missing_data()
        metadata_df_validator.chemical_formula(constants.FORMULA_COL_METADATAFILE)
        metadata_df_validator.value_in_constant(constants.ISOTRACER_COL,
                                                constants.ISOTOPE_VALUES)
        metadata_df_validator.perform_action_and_generate_logs()
        return metadata_df_validator
    except Exception as e:
        raise Exception(e)
