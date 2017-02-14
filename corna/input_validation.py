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

    return data_frame

@handleError
def validator_column_wise(input_data_frame, axis=0, column_list=[], function_list=[]):
    """
    This is basically a schema for performing column wise validation checks.
    Validaton functions are passed as an argumnet.
    The resultant data frame is returned which contains state for cell
    which function is applied.

    :param input_data_frame: the data frame on which validation is to be applied
    :param axis: for defining row wise or column wise operations
    :param column_list: column of data frame on which validation is to be applied
    :param function_list: list of validatin function
    :return: resultant dataframe
    """
    resultant_dataframe=pd.DataFrame()
    for function in function_list:
        column_dataframe=pd.DataFrame()
        for column in column_list:
            function_name=function.__name__
            column_dataframe['status']=input_data_frame[column].apply(function)
            column_dataframe['column_name'],column_dataframe['function_name']=column,function_name
            resultant_dataframe=resultant_dataframe.append(column_dataframe)
    return resultant_dataframe

@handleError
def check_missing(input_data_frame):
    """
    This function returns the data frame containing state of every cell which has
    missing value. We are using pandas.isnull method.
    
    :param input_data_frame:
    :return: resultant data frame
    """
    missing_dataframe = input_data_frame.isnull()
    missing_dataframe['function_name'] = 'missing'
    missing_dataframe['row_number'] = missing_dataframe.index
    resultant_dataframe= pd.melt(missing_dataframe, id_vars=['function_name', 'row_number'],
                                 var_name='column_name')
    return resultant_dataframe


