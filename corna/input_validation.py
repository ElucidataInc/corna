from dataframe_validator import check_if_file_exist,check_data_frame_empty
from dataframe_validator import check_file_empty,read_input_file
from dataframe_validator import get_missing_required_column
from custom_exception import handleError,MissingRequiredColumnError
from inputs.column_conventions import maven as c
import os
import pandas as pd
import numbers
import re
import constants as cs
from corna.helpers import chemformula_schema,get_formula

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
    resultant_dataframe = pd.DataFrame()
    for function in function_list:
        column_dataframe = pd.DataFrame()
        for column in column_list:
            column_dataframe['state'] = input_data_frame[column].apply(function)
            column_dataframe['column_name'] = column
            column_dataframe['row_number'] = column_dataframe.index
            resultant_dataframe = resultant_dataframe.append(column_dataframe)
    output_dataframe = resultant_dataframe.loc[resultant_dataframe['state'] != 'correct']
    return output_dataframe

@handleError
def check_missing(input_data_frame):
    """
    This function returns the data frame containing state of every cell which has
    missing value. We are using pandas.isnull method.

    :param input_data_frame:
    :return: resultant data frame
    """
    missing_dataframe = input_data_frame.isnull()
    missing_dataframe['row_number'] = missing_dataframe.index
    resultant_dataframe = pd.melt(missing_dataframe, id_vars=['row_number'],
                                  var_name='column_name', value_name='state')
    output_dataframe = resultant_dataframe.loc[resultant_dataframe['state'] == True]
    output_dataframe['state'] = "missing"

    return output_dataframe

@handleError
def check_duplicate(input_data_frame, axis=0, column_list=[]):
    """
    This function checks for a duplicate value in a column. It
    saves the state duplicate if any duplicate value is found.
    :param input_data_frame:
    :param axis:
    :param column_list:
    :return:
    """
    resultant_dataframe=pd.DataFrame()
    print column_list
    for column in column_list:
            column_dataframe = pd.DataFrame()
            column_dataframe['state']=input_data_frame.duplicated(column)
            column_dataframe['column_name']=column
            column_dataframe['row_number']=column_dataframe.index
            resultant_dataframe=resultant_dataframe.append(column_dataframe)
    output_dataframe=resultant_dataframe.loc[resultant_dataframe['state']==True]
    output_dataframe['state'] = "duplicate"
    return output_dataframe

def check_postive_numerical_value(cell_value):
    try :
        value=float(cell_value)
        if value<0:
            return 'negative'
        else:
            return 'correct'
    except ValueError:
        return 'invalid_intensity_value'

def check_label_column_format(label):
    if label == 'C12 PARENT':
        return 'correct'
    else:
        if not '-label-' in label:
            return 'invalid_label'
        formula, enums = label.split('-label-')
        if not re.match("^[A-Za-z0-9]*$", formula):
            return 'invalid_label'
        if not re.match("^[0-9-]*$", enums):
            return 'invalid_labe'
        isotopes = set(''.join(map(str, i)) for i in chemformula_schema.parseString(formula))
        elements = set(cs.data['isotope_na_mass']["element"])
        if not isotopes.issubset(elements):
            return 'invalid_label'
        number_of_isotopes = set(enums.split('-'))
        if not len(isotopes) == len(number_of_isotopes):
            return 'invalid_label'

def check_formula_is_correct(formula):
    try :
        get_formula(formula)
    except KeyError :
        return 'invalid_formula'

