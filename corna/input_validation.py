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
def validator_for_two_column(input_data_frame,check_column = '',required_column = '', function = ''):
    """
    This is basically a schema for performing two column validation checks.
    The check column is validated with the help of required column value.
    The resultant data frame is returned which contains state for cell
    which function is applied.

    :param input_data_frame: the data frame on which validation is to be applied
    :param check_column: the column on which check is to be performed
    :param required_column: the column which helps in performing check
    :param function: validatin function
    :return: resultant dataframe
    """
    resultant_dataframe = pd.DataFrame()

    resultant_dataframe['state'] = input_data_frame.apply(
                                    lambda x: function(x[check_column], x[required_column]), axis=1)

    resultant_dataframe['column_name'] = check_column
    resultant_dataframe['row_number'] = resultant_dataframe.index
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
                                  var_name = 'column_name', value_name='state')
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
            column_dataframe['state'] = input_data_frame.duplicated(column)
            column_dataframe['column_name'] = '-'.join(column)
            column_dataframe['row_number'] = column_dataframe.index
            resultant_dataframe = resultant_dataframe.append(column_dataframe)
    output_dataframe = resultant_dataframe.loc[resultant_dataframe['state'] == True]
    output_dataframe['state'] = "duplicate"
    return output_dataframe

def check_postive_numerical_value(cell_value):
    try :
        value = float(cell_value)
        if value < 0:
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
        return 'correct'

def check_formula_is_correct(formula):
    try :
        get_formula(formula)
        return 'correct'
    except :
        return 'invalid_formula'

def check_label_in_formula(label,formula):
    """
    This function checks if all label element are in formula.
    Also label element must be less than or equal to corresponding
    element in formula.

    :param label: label value of column
    :param formula: formula value of column
    :return: state
    """

    if not check_label_column_format(label) == 'correct':
        return 'label_not_correct'
    if not check_formula_is_correct(formula) == 'correct':
        return 'formula_not_correct'

    parsed_label = get_label(label)
    parsed_formula = get_formula(formula)

    label_element_set = set(parsed_label.keys())
    formula_element_set = set(parsed_formula.keys())

    if not label_element_set.issubset(formula_element_set) :
        return "label_not_in_formula"


    for element in label_element_set:
        if not parsed_label[element] <= parsed_formula[element]:
            return "element_in_label_more_than_formula"

    return 'correct'

def get_label(label):
    """
    This function takes label value as an argument and parsed it to
    save dictionary  as element,value pair. For ex:
    label= C13N15-label-4-5
    dict={'C': 4, 'N': 5}

    :param label: label value
    :return: dict
    """

    if label=='C12 PARENT':
        return {'C':1}
    else:
        label_formula, enums = label.split('-label-')
        label_isotopes = list(''.join(map(str, i)) for i in chemformula_schema.parseString(label_formula))
        label_number_of_elements = list(int(x) for x in enums.split('-'))
        label_element_pattern = re.compile("([a-zA-Z]+)([0-9]+)")
        label_elements = [label_element_pattern.match(isotope).group(1) for isotope in label_isotopes]
        parsed_label = dict(zip(label_elements, label_number_of_elements))

        return parsed_label
