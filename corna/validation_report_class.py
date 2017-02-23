from corna import constants as con
from inputs.column_conventions import maven as c
import pandas as pd

class ValidationReport():
    """
    This is validation report class. This class helps in generating report of
    all the warning and error in different formats. It also helps deciding
    what action is to be taken after performing all the test.

    """

    def __init__(self):
        """
        Intialising self global variables here.
        report_dataframe: appends all the validation dataframe return by
                         all validation function
        result: this variable groups report_dataframe and store it in
                dictionary form
        invalid_row: list of all rows which contains errors and warnings
        warning_row: list of all rows which contains warnings
        error_row: list of all rows which contains errors and warnings
        action_messages: list of message generated for action to be sent as log
        action: dictionary mapping of action performed paired with row of df
        warning_error_dict: logs of all the warnings and errors

        """

        self.report_dataframe = pd.DataFrame()
        self.result = {}
        self.required_column_list = [c.NAME, c.LABEL, c.FORMULA]
        self.invalid_row = []
        self.warning_row = []
        self.error_row = []
        self.action_messages = []
        self.action = {}
        self.warning_error_dict = {con.VALIDATION_WARNING: {con.VALIDATION_MESSAGE: [],
                                                            con.VALIDATION_ACTION: []},
                                   con.VALIDATION_ERROR: []}

    def append(self, dataframe):
        # append the data frame to the global report data frame
        self.report_dataframe = self.report_dataframe.append(dataframe)

    def generate_report(self):
        """
        This function generates the report in the form of dict object
        based on the values of report data frame.

        :TODO : remove the hard coded values of column names and state.
                so that it is easy to make it more generalise.

        :return: dict object
        """
        result_object = {}
        row_key = list(self.report_dataframe.groupby([con.COLUMN_ROW]).groups.keys())
        for key in row_key:
            row_df = self.report_dataframe.loc[self.report_dataframe[con.COLUMN_ROW] == key]
            warning = []
            error = []
            row_object = {}
            for index, row in row_df.iterrows():
                if row[con.COLUMN_STATE] == con.MISSING_STATE:
                    warning.append([row[con.COLUMN_NAME], row[con.COLUMN_STATE]])
                elif row[con.COLUMN_STATE] == con.DUPLICATE_STATE:
                    warning.append([row[con.COLUMN_NAME], row[con.COLUMN_STATE]])
                else:
                    error.append([row[con.COLUMN_NAME], row[con.COLUMN_STATE]])

            row_object[con.VALIDATION_WARNING] = warning
            row_object[con.VALIDATION_ERROR] = error
            result_object[row[con.COLUMN_ROW]] = row_object

        self.result = result_object
        self.invalid_row = result_object.keys()
        self.error_row = [key for key in result_object.keys()
                          if result_object[key][con.VALIDATION_ERROR]]
        self.warning_row = [key for key in result_object.keys()
                            if result_object[key][con.VALIDATION_WARNING]]

        return self.result