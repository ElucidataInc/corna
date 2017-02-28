import pandas as pd

from corna import constants as con
from inputs.column_conventions import maven as c

REQUIRED_COLUMN_LIST = [c.NAME, c.LABEL, c.FORMULA]


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
        based on the values of report data frame. First it will find
        unique row number then for each row it forms a df , then iterating
        over that df it saves error and warning.
        For ex:
        if report_df :
            row_number    column_name       state
                  1           label      invalid_label
                  1           formula    invalid formula
                  4           label      invalid_label
                  19          Sample1    negative

        row_having_error = [1,4,19]

        in between loop, warning_or_error_msg = ['label','invalid_label']

        and final result:
        {'1':{'warning': [['label','invalid_label],['formula','invalid_formula]], 'errors':[]},
             '4':{'warning':[['label','invalid_label']],'errors':[]},
             '19':{'warning':[],'errors':['Sample1','negative]}}



        :return: dict object
        """

        row_having_error = self.get_unique_row_having_error(self)

        for each_row in row_having_error:

            row_df = self.get_slice_df_with_row(self.report_dataframe,each_row)
            row_object = {con.VALIDATION_WARNING: [], con.VALIDATION_ERROR: []}

            for index, row in row_df.iterrows():

                warning_or_error_msg = [row[con.COLUMN_NAME], row[con.COLUMN_STATE]]

                if row[con.COLUMN_STATE] in con.WARNING_STATE:
                    row_object[con.VALIDATION_WARNING].append(warning_or_error_msg)
                else:
                    row_object[con.VALIDATION_ERROR].append(warning_or_error_msg)

            self.result[row[con.COLUMN_ROW]] = row_object

        self.invalid_row = self.get_key_list(self.result)
        self.error_row = self.get_key_list(self.result, con.VALIDATION_ERROR)
        self.warning_row = self.get_key_list(self.result, con.VALIDATION_WARNING)

        return self.result

    def generate_action(self):
        """
        This function generates the action to be taken for each validation
        result and save the action report as key value pair where key is
        the row number.

        :return: dict object
        """
        for row in self.warning_row:
            self.append_warning_action_to_result(row)

        for row in self.error_row:
            self.append_error_action_to_result(row)

        return self.result

    def decide_action(self):
        """
            This function with the help of report object decide final action
            to be taken on row i.e it decides if the row is being dropped,
            or individual column action is to be taken. If there is any error then simply it
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

        return output_df

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

    @staticmethod
    def get_unique_row_having_error(self):

        return self.report_dataframe.row_number.unique()

    @staticmethod
    def get_slice_df_with_row(df,row):

        return df.loc[df[con.COLUMN_ROW] == row]

    @staticmethod
    def get_key_list(dict,condition=None):
        if condition:
            return [key for key in dict.keys() if dict[key][condition]]
        else:
            return dict.keys()

    @staticmethod
    def get_action_name(result):

        column_name = result[0]
        state = result[1]

        if state is con.MISSING_STATE:

            if column_name in REQUIRED_COLUMN_LIST:
                action = con.VALIDATION_ACTION_DROP
            else:
                action = con.VALIDATION_ACTION_FILL_NA

        elif state is con.DUPLICATE_STATE:
            action = con.VALIDATION_ACTION_DROP

        else:
            action = con.VALIDATION_ACTION_STOP

        return action

    def append_warning_action_to_result(self, row):

        for each_result in self.result[row][con.VALIDATION_WARNING]:
            each_result.append(self.get_action_name(each_result))

    def append_error_action_to_result(self, row):

        for each_result in self.result[row][con.VALIDATION_ERROR]:
            each_result.append(self.get_action_name(each_result))