import os
import pandas as pd

def check_required_column(data_frame,*arg):
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
    missing_column=list()
    for column_name in required_column_names:
        if column_name not in data_frame_columns:
            missing_column.append(column_name)
    return missing_column

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
        raise IOError('only csv/xls/xlsx/txt extensions are allowed')

    return input_file



def check_file_empty(path):
    """
    This function checks for the file size. We are assuming an empty
    file is of zero size. It will return Boolean after checking the
    file size.
    :param path: Input file path
    :return: Boolean
    """
    file_info = os.stat(path)

    if file_info.st_size > 0:
        return True
    else:
        return False


