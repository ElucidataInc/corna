import constants as con
import custom_exception
import dataframe_validator
import pandas as pd
import re

from corna.helpers import chemformula_schema,get_formula
from inputs.column_conventions import maven


#getting required columns for input file
REQUIRED_COLUMNS = [maven.NAME, maven.LABEL, maven.FORMULA]


@custom_exception.handleError
def validate_input_file(path):
    """
    This is the function for checking basic validation of file.
    If any exception raises during validation check , handleError
    decorator will catch it and processed accordingly.
    :param path:
    :return: True, if no exception is raised
    """

    if not dataframe_validator.check_if_file_exist(path):
        raise custom_exception.FileExistError

    if not dataframe_validator.check_file_empty(path):
        raise custom_exception.FileEmptyError

    return True


@custom_exception.handleError
def validate_df(df, required_columns_name=None):
    """
    This function validates the df. First it checks for df empty ,
    then for the required columns.If any exception raises during validation
    check ,handleError decorator will catch it and processed accordingly.
    :param path:
    :return:True, if no exception is raised
    """
    if not dataframe_validator.check_df_empty(df):
        raise custom_exception.DataFrameEmptyError
    missing_column_status,missing_columns = dataframe_validator.\
                                             check_required_column(df,*required_columns_name)
    if not missing_column_status:
        raise custom_exception.MissingRequiredColumnError(missing_columns)

    return True


@custom_exception.handleError
def validator_column_wise(input_data_frame, axis=0, column_list=[], function_list=[]):
    """
    This is basically a schema for performing column wise validation checks.
    Validaton functions are passed as an argumnet. First we are iterating over function
    then for columns. So every column is checked for every function. The nested for is
    required to give the output_df in defined format of ['row_number','column_name,'state']


    :param input_data_frame: the data frame on which validation is to be applied
    :param axis: for defining row wise or column wise operations
    :param column_list: column of data frame on which validation is to be applied
    :param function_list: list of validatin function
    :return: resultant dataframe
    """
    resultant_df = get_df()
    for function in function_list:
        column_df = get_df()
        for column in column_list:
            column_df[con.COLUMN_STATE] = input_data_frame[column].apply(function)
            column_df[con.COLUMN_NAME] = column
            column_df[con.COLUMN_ROW] = column_df.index
            resultant_df = resultant_df.append(column_df)
    output_df = resultant_df.loc[resultant_df[con.COLUMN_STATE] != con.VALID_STATE]
    return output_df

@custom_exception.handleError
def validator_for_two_column(input_data_frame, check_column='', required_column='', function=''):
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
    resultant_df = get_df()

    resultant_df[con.COLUMN_STATE] = input_data_frame.apply(
                                    lambda x: function(x[check_column], x[required_column]), axis=1)

    resultant_df[con.COLUMN_NAME] = check_column
    resultant_df[con.COLUMN_ROW] = resultant_df.index
    output_df = resultant_df.loc[resultant_df[con.COLUMN_STATE] != con.VALID_STATE]
    return output_df

@custom_exception.handleError
def check_missing(input_df):
    """
    This function returns the data frame containing state of every cell which has
    missing value. We are using pandas.isnull method.

    :param input_data_frame:
    :return: resultant data frame
    """
    missing_df = input_df.isnull()
    missing_df[con.COLUMN_ROW] = missing_df.index
    resultant_df = change_df_to_std_report_form(missing_df)
    output_df = resultant_df.loc[resultant_df[con.COLUMN_STATE] == True]
    output_df[con.COLUMN_STATE] = con.MISSING_STATE

    return output_df

@custom_exception.handleError
def check_duplicate(input_df, axis=0, column_list=[]):
    """
    This function checks for a duplicate value in a column. It
    saves the state duplicate if any duplicate value is found.
    :param input_df: data frame
    :param axis:
    :param column_list: colum for which we need to check duplicacy
    :return: resultant_df of validation check
    """
    resultant_df = get_df()
    for column in column_list:
            column_df = get_df()
            column_df[con.COLUMN_STATE] = input_df.duplicated(column)
            column_df[con.COLUMN_NAME] = '-'.join(column)
            column_df[con.COLUMN_ROW] = column_df.index
            resultant_df = resultant_df.append(column_df)
    output_df = resultant_df.loc[resultant_df[con.COLUMN_STATE] == True]
    output_df[con.COLUMN_STATE] = con.DUPLICATE_STATE
    return output_df


def check_intensity_value(cell_value):
    """
    This function checks for intensity value i.e. only numerical positive
    value is correct. Here we are converting the value to float so if there is
    any exception we can assert that this is becuase it is not numerical and after
    that we are checking if it positive.
    Example : 0.673 --> Correct
              0.as34 --> Invalid
              -0.123 --> Negative
    :param cell_value:
    :return: State
    """

    try:
        value = float(cell_value)
        if value < 0:
            return con.INTENSITY_STATE_NEGATIVE
        else:
            return con.VALID_STATE
    except ValueError:
        return con.INTENSITY_STATE_INVALID


def check_label_column_format(label):
    """
    This function is check if the label is in correct format or not. The
    correct format is C13-N15-label-1-2. So using get label we extract
    all the isotopes and then check if they exist. Also if the label column
    value is missing we are treating it as correct state here becuase that case
    is handled when checking for missing value. Also the case of label value = 'C12 PARENT'
    is also correct.

    :param label:
    :return: State (ex. Invalid, Correct etc.)
    """
    if label == con.UNLABELLED_LABEL or pd.isnull(label):
        return con.VALID_STATE
    else:
        parsed_label = get_label(label)
        if parsed_label and set(parsed_label).issubset(con.ELEMENT_LIST):
            return con.VALID_STATE
        else:
            return con.LABEL_STATE_INVALID


def check_formula_is_correct(formula):
    """
    This function is checking for formula values. We are using pre defined
    function get_formula which will raise exception if the formula is not correct.
    Also if the label column value is missing we are treating it as correct state
    because that case is handled when checking for missing value.
    Example: C2H6O -->correct
             XY12C2 -->invalid
    :param formula:
    :return:
    """
    try:
        if pd.isnull(formula):
            return con.VALID_STATE
        else:
            get_formula(formula)
            return con.VALID_STATE
    except Exception:
        return con.FORMULA_STATE_INVALID


def check_label_in_formula(label,formula):
    """
    This function checks if all label element are in formula.
    Also label element must be less than or equal to corresponding
    element in formula.

    :param label: label value of column
    :param formula: formula value of column
    :return: state
    """

    if not check_label_column_format(label) == con.VALID_STATE:
        return con.LABEL_STATE_NOT_CORRECT

    if not check_formula_is_correct(formula) == con.VALID_STATE :
        return con.FORMULA_STATE_INVALID

    if pd.isnull(label) or pd.isnull(formula):
        return con.VALID_STATE

    try:
        parsed_label = get_label(label)
        parsed_formula = get_formula(formula)

        if parsed_label == con.UNLABELLED_LABEL_DICT:
            return con.VALID_STATE

        label_element_set = set(parsed_label.keys())
        formula_element_set = set(parsed_formula.keys())

        if not label_element_set.issubset(formula_element_set) :
            return con.LABEL_STATE_NOT_FORMULA


        for element in label_element_set:
            if not parsed_label[element] <= parsed_formula[element]:
                return con.LABEL_STATE_NUMBER_MORE_FORMULA

        return con.VALID_STATE
    except Exception:
        return con.LABEL_STATE_INVALID


def get_label(label):
    """
    This function takes label value as an argument and parsed it to
    save as dictionary in the form of element,value pair.
    If there is any exception we are returning NONE , assuming LABEL is
    not in correct format.The none case is handled by the function from
    this fucntion will be called.
    for ex: label = C13-N15-label-1-2
            label_number_of_elements = [1,2]
            label_isotopes = ['C','N']
            parsed_label = {'C':1,'N':2}

    :param label: label value
    :return: dict
    """

    if label == con.UNLABELLED_LABEL:
        return con.UNLABELLED_LABEL_DICT

    else:
        try:
            label_isotopes,label_number_of_elements = get_isotopes_name_and_number(label)

            if len(label_isotopes) != len(label_number_of_elements):
                return None
            parsed_label = dict(zip(label_isotopes, label_number_of_elements))

            return parsed_label

        except ValueError:
            return None


def get_df():
    """
    This function will return a empty pandas df for now. In future there can be need where
     we need a predefined df so then this function can be modified.
    :return:
    """
    return pd.DataFrame()


def change_df_to_std_report_form(df):
    """
    This function will change the input dataframe to standard dataframe of validation report.
    This is required becuase some validation can be applied to multiple column but we need
    our report dataframe to be single row column wise. We are using pandas melt to convert it
    to long form from wide form. It is melting the df using 'row_number' and 'column_name'
    :return:
    """
    output_df = pd.melt(df, id_vars=[con.COLUMN_ROW],
                        var_name=con.COLUMN_NAME, value_name=con.COLUMN_STATE)
    return output_df

def get_isotopes_name_and_number(label):
    """
    This fucntion take label value and returns isotopes present and
    its corresponding number. It first splits the label from "-label-"
    then take out each isotope and its number.
    :param label:
    :return: isotopes in label and number of elements
    """
    label_all_element, label_all_number = label.split('-label-')
    label_isotopes_list = list(str(x) for x in label_all_element.split('-'))
    label_isotopes = get_isotope_name(label_isotopes_list)
    label_number_of_elements = list(int(x) for x in label_all_number.split('-'))

    return label_isotopes, label_number_of_elements

def get_isotope_name(list_of_istope_with_number):
    """
    This function will sepearte isotope from its atomic number and returns the list.
    Here using regex to spliting C13 in 'C' and '13'.
    :param istope_with_number: istope in the form C13,N15 etc.
    :return: seperated isotope C,N etc.
    """
    label_element_pattern = re.compile("([a-zA-Z]+)([0-9]+)")
    label_elements = [label_element_pattern.match(isotope).group(1)
                      for isotope in list_of_istope_with_number]

    return label_elements

def get_seperated_label_isotope_name_number(label):
    label_all_element, label_all_number = label.split('-label-')
    label_isotopes = get_isotope_name(label_all_element)


