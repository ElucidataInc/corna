import custom_exception
import os
import pandas as pd

def check_if_file_exist(path):
    """
    This function will raise error if file does not exist in given path.
    :param path:
    :return:
    """
    if not os.path.isfile(path) : raise custom_exception.FileExistError

def get_missing_required_column(data_frame,*arg):
    """
    This function takes data frame and column_name as an argumnet.
    It checks whether the required columns is present in a data_
    farme or not. It will populates the list of all the column name
    which are not present in data frame.

    :param data_frame: The data frame which we need to assert
    :param arg: all the column name as argument
    :return: missing column list
    """
    required_column_names=[column_name.upper() for column_name in arg]
    data_frame_columns=[column_name.upper() for column_name in data_frame.columns.tolist()]

    return [column_name for column_name in required_column_names
                    if column_name not in data_frame_columns ]

def read_input_file(path):
    """
    This function reads the input file and returns a Pandas Data Frame.
    First it is checking for the extension and then it calls for required
    pandas function to convert the file. It also raises IOerror if the file
    is other than .xlsx,.xls,.csv,.txt
    Args:
        path : path to input file

    Returns:
         input_file : input file in the form of pandas dataframe
    """

    excel_file_extension = ['.xls', '.xlsx']

    if os.path.splitext(path)[1] in excel_file_extension:
        input_file = pd.read_excel(path, header=0)

    elif os.path.splitext(path)[1] == '.csv':
        input_file = pd.read_csv(path, header=0)

    elif os.path.splitext(path)[1] == '.txt':
        input_file = pd.read_table(path, header=0)

    else:
        raise custom_exception.FileExtensionError

    return input_file



def check_file_empty(path):
    """
    This function checks for the file size. We are assuming an empty
    file is of zero size. It will raise error if file is of 0 mb size.
    :param path: Input file path
    :return: Boolean
    """
    if os.stat(path) == 0 : raise custom_exception.FileEmptyError


def check_data_frame_empty(data_frame):
    """
    This function check if the data frame is empty.
    It returns boolean response based on the check.

    :param data_frame:
    :return: Boolean
    """
    return data_frame.empty


@custom_exception.handleError
def validate_input_file(path):
    """
    This function will validate the file using the functions defined
    above.
    :param path:
    :return:
    """
    if check_file_empty(path):
        data_frame=read_input_file(path)
    else:
        return "The file is empty, cannot proceed further"

    if check_data_frame_empty(data_frame):
        return "The data frame is empty, cannot proceed further"