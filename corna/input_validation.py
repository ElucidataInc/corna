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