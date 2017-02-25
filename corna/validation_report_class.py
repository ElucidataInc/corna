"""
TODO: this module has scope where it can be refactored to make it more robust.
separate class can be made for Action etc.
"""



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
        based on the values of report data frame. First it will find how
        unique row number then for each row it forms a df , then iterarting
        over that df it saves error and warning.

        :TODO : remove the hard coded values of column names and state.
                so that it is easy to make it more generalise.

        :return: dict object
        """
        result_object = {}
        row_having_error = self.report_dataframe.row_number.unique()
        for each_row in row_having_error:
            row_df = self.report_dataframe.loc[self.report_dataframe[con.COLUMN_ROW] == each_row]
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

    def generate_action(self):
        """
        This function geneartes the action to be taken for each validation
        result and save the action report as key value pair where key is
        the row number.

        :return: dict object
        """

        for row in self.warning_row:
            for entries in self.result[row][con.VALIDATION_WARNING]:

                if entries[1] == con.MISSING_STATE:
                    if entries[0] not in self.required_column_list:
                        action = con.VALIDATION_ACTION_FILL_NA
                    else:
                        action = con.VALIDATION_ACTION_DROP
                    entries.append(action)
                if entries[1] == con.DUPLICATE_STATE:
                    action = con.VALIDATION_ACTION_DROP
                    entries.append(action)

        for row in self.error_row:
            for entries in self.result[row][con.VALIDATION_ERROR]:
                action = con.VALIDATION_ACTION_STOP
                entries.append(action)

        return self.result

    def decide_action(self):
        """
            This function with the help of report object decide final action
            to be taken on row . If there is any error then simply it
            save STOP_TOOL and halts there.
        :param data_frame:
        :return: dict object
        """
        if self.error_row:
            self.action[con.VALIDATION_ACTION] = con.VALIDATION_ACTION_STOP

        elif self.warning_row:
            self.action[con.VALIDATION_ACTION] = con.VALIDATION_ACTION_ROW_WISE
            for row in self.warning_row:
                column_state_action_list = []
                for entries in self.result[row][con.VALIDATION_WARNING]:
                    column_state_action_list.append({'column': entries[0],
                                                     con.COLUMN_STATE: entries[1],
                                                     con.VALIDATION_ACTION: entries[2]})
                self.action[row] = column_state_action_list
        else:
            self.action[con.VALIDATION_ACTION] = con.VALIDATION_ACTION_OK

        return self.action

    def take_action(self, data_frame):
        """
        With the help of action report this function perform actions on the
        row also it returns the filtered data frame after performing the action.
        TODO: now using if and else to take the action because only two actions
        are there , need to change this when there are nuber of actions.
        :param data_frame:
        :return: data_frame
        """
        resultant_dataframe = pd.DataFrame()
        list_of_rows_to_drop = []
        if not self.action[con.VALIDATION_ACTION] == con.VALIDATION_ACTION_STOP:
            resultant_dataframe = data_frame
            for rows in [rows for rows in self.action if rows not in [con.VALIDATION_ACTION]]:
                for each_action in self.action[rows]:
                    if each_action[con.VALIDATION_ACTION] == con.VALIDATION_ACTION_DROP:
                        list_of_rows_to_drop.append(rows)
                        action_msg = "Row is Dropped"
                    else :
                        resultant_dataframe.set_value(rows, each_action['column'], 0)
                        action_msg = "Missing value of columns replaced with 0"
                self.action_messages.append(action_msg)
            output_df = self.action_drop_rows(resultant_dataframe,list_of_rows_to_drop)
        self.warning_error_dict[con.VALIDATION_WARNING][con.VALIDATION_ACTION] = self.action_messages

        return resultant_dataframe

    def generate_warning_error_list_of_strings(self):
        """
        This function generates the report of validation check in the form
        of list of strings.

        :return: dict object
        """

        for row in self.result.keys():
            if self.result[row][con.VALIDATION_WARNING]:
                msg = []
                for warning in self.result[row][con.VALIDATION_WARNING]:
                    msg.append("column <b>{c[0]}</b> has <b>{c[1]}</b> value".format(c=warning))
                final_msg = "Row Number <b>%i</b> : " % row + " , ".join(msg)
                self.warning_error_dict[con.VALIDATION_WARNING][con.VALIDATION_MESSAGE].append(final_msg)

            if self.result[row][con.VALIDATION_ERROR]:
                msg = []
                for error in self.result[row][con.VALIDATION_ERROR]:
                    msg.append("column <b>{c[0]}</b> has <b>{c[1]}</b> value".format(c=error))
                final_msg = "Row Number <b>%i</b> : " % row + " , ".join(msg)
                self.warning_error_dict[con.VALIDATION_ERROR].append(final_msg)

        return self.warning_error_dict

    @staticmethod
    def action_drop_rows(df, row_list):
        output_df = df.drop(df.index[row_list], inplace=True)
        return output_df
