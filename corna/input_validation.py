from dataframe_validator import check_if_file_exist,check_data_frame_empty
from dataframe_validator import check_file_empty,read_input_file
from dataframe_validator import get_missing_required_column
from custom_exception import handleError,MissingRequiredColumnError
from inputs.column_conventions import maven as c
import os
import pandas as pd

#getting required columns for input file
required_columns_raw_data = (c.NAME, c.LABEL, c.FORMULA)


@handleError
def validate_input_file(path,required_columns_name):
    """
    This function will validate the file using the functions defined
    above.
    :param path:
    :return:
    """
    check_if_file_exist(path)
    check_file_empty(path)
    data_frame = read_input_file(path)
    check_data_frame_empty(data_frame)


    missing_columns = get_missing_required_column(data_frame, *required_columns_name)

    if missing_columns:
        raise MissingRequiredColumnError(missing_columns)