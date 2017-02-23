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
