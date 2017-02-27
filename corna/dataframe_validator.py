import custom_exception
import os
import pandas as pd

from inputs.column_conventions import maven as c

REQUIRED_COLUMNS_RAW_DATA = (c.NAME, c.LABEL, c.FORMULA)
KNOWN_EXTENSION = {'.xls': pd.read_excel,
                   '.xlsx': pd.read_excel,
                   '.csv': pd.read_csv,
                   '.txt': pd.read_table}


def check_if_file_exist(path):
    """
    This function will return False if file does not exist in given path.
    :param path:
    :return:
    """
    return os.path.isfile(path)
    

def check_required_column(data_frame,*arg):
    """
    This function takes data frame and column_name as an argumnet.
    Then it converts all the column header in UPPER CASE, after this
    it checks whether the required columns is present in provided data_
    farme or not. It will return True if all the required columns are
    present otherwise it will return false with list of missing columns.

    :param data_frame: The data frame which we need to assert
    :param arg: all the column name as argument
    :return: missing column list
    """
    required_column_names = [column_name.upper() for column_name in arg]
    data_frame_columns = [column_name.upper() for column_name in data_frame.columns.tolist()]

    missing_columns = [column_name for column_name in required_column_names
                       if column_name not in data_frame_columns]

    if missing_columns:
        return False, missing_columns
    else:
        return True, missing_columns


def read_input_file(path):
    """
    This function reads the input file and returns a Pandas Data Frame.
    First it is checking for the extension and then it calls for required
    pandas function to convert the file. It also raises FileExtensionError if the file
    is other than known extensions.
    Args:
        path : path to input file

    Returns:
         input_file : input file in the form of pandas dataframe
    """
    extension_of_file = get_extension(path)
    if extension_of_file not in KNOWN_EXTENSION.keys():
        raise custom_exception.FileExtensionError
    else:
        return KNOWN_EXTENSION[extension_of_file](path, header=0)


def check_file_empty(path):
    """
    This function checks for the file size. We are assuming an empty
    file is of 0 size. It will return false if file is of 0 mb size.
    :param path: Input file path
    :return: Boolean
    """
    if os.stat(path).st_size == 0:
        return False
    else:
        return True


def check_df_empty(df):
    """
    This function takes data_frame as an argument and with the help of
    Pandas inbuilt function it checks if the data_frame empty or not.
    The function return false if the df is empty.

    :param: data_frame
    :return: boolean
    """
    if df.empty:
        return False
    else:
        return True


def get_extension(path):
    """
    This function takes file path and returns the extension of the file.
    :param path:
    :return:
    """
    extension = os.path.splitext(path)[1]
    return extension




