import pandas as pd

from corna import constants as con
from corna.input_validation import get_df
from inputs.column_conventions import maven as maven_file

REQUIRED_COLUMN_LIST = [maven_file.NAME, maven_file.LABEL, maven_file.FORMULA]


class ValidationReport():
    """
    This is validation report class. This can be use to generate report of
    all the warning and error after performing validation check in different
    formats such as waning, error dict or can be row wise df. It also helps
    deciding what action is to be taken.
    """

    def __init__(self):
        """
        Intialising self global variables here.
        report_df: appends all the validation df return by
                   all validation function
        result: this variable groups report_df and store it in
                dictionary form
        invalid_row: list of all rows which contains errors and warnings
        warning_row: list of all rows which contains warnings
        error_row: list of all rows which contains errors and warnings
        action_messages: list of message generated for action to be sent as log
        action: dictionary mapping of action performed paired with row of df
        warning_error_dict: logs of all the warnings and errors
        """
        self.report_df = get_df()
        self.result = {}
        self.required_column_list = REQUIRED_COLUMN_LIST
        self.invalid_row = []
        self.warning_row = []
        self.error_row = []
        self.action_messages = []
        self.action = {}
        self.warning_error_dict = {con.VALIDATION_WARNING:
                                   {con.VALIDATION_MESSAGE: [],
                                    con.VALIDATION_ACTION: []},
                                   con.VALIDATION_ERROR: []}

    def append_df_to_global_df(self, df):
        """
        Append the data frame to the global report data frame.
        :param df: function wise report df
        """
        self.report_df = self.report_df.append(df)

    def generate_report(self):
        """
        This can be used to generate the validation report in
        the form of dict object which is previously in the form
        of df. Also this help getting the row number where error
        and warnings are present. First it will find unique row
        number then for each row it forms a df , then iterating
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
        {'1':{'warning': [['label','invalid_label],['formula','invalid_formula]
        ], 'errors':[]},'4':{'warning':[['label','invalid_label']],'errors':[]},
        '19':{'warning':[],'errors':['Sample1','negative]}}
        """
        row_having_error = self.get_unique_row_having_error(self)

        for each_row in row_having_error:
            self.append_warning_error_dict_for_row(each_row)

        self.invalid_row = self.get_key_list(self.result)
        self.error_row = self.get_key_list(self.result, con.VALIDATION_ERROR)
        self.warning_row = self.get_key_list(self.result, con.VALIDATION_WARNING)

        return self.result

    def generate_action(self):
        """
        This function generates the action to be taken for each validation
        result and save the action report as key value pair where key is
        the row number.

        for example:

        if result
            {'1':{'warning': [['label','invalid_label],['formula','
            invalid_formula']], 'errors':[]},'4':{'warning':[
            ['label','invalid_label']],'errors':[]},'19':{'warning':[],
            'errors':['Sample1','negative]}}

        final result:
            {'1':{'warning': [['label','invalid_label','DROP'],['formula',
            'invalid_formula','DROP']],'errors':[]},'4':{'warning':[[
            'label','invalid_label','DROP']],'errors':[]},'19':{'warning':
            [],'errors':['Sample1','negative','STOP']}}
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

        for ex: result:
            {'1':{'warning': [['label','invalid_label','DROP'],['formula',
            'invalid_formula','DROP']],'errors':[]},
            '4':{'warning':[['label','invalid_label','DROP']],'errors':[]},
            '19':{'warning':[],'errors':['Sample1','negative','STOP']}}

        action = {'action': 'STOP_TOOL}

        if  result:
            {'1':{'warning': [['label','invalid_label','DROP'],['formula',
            'invalid_formula','DROP']],'errors':[]},
            '4':{'warning':[['label','invalid_label','DROP']],'errors':[]} }
        action :
            {'action': 'ROW_WISE_ACTION',
            '1': [{'column': 'label', 'state': 'invalid_label, 'action': 'DROP'},
            {'column': 'Formula', 'state': 'invalid_formula, 'action': 'DROP'}],
            '4': [{'column': 'label', 'state': 'invalid_label, 'action': 'DROP'}]}

        :param data_frame: data frame on which action is to be taken
        :return: dict object: action list for row wise
        """
        if self.error_row:
            self.action[con.VALIDATION_ACTION] = con.VALIDATION_ACTION_STOP

        elif self.warning_row:
            self.action[con.VALIDATION_ACTION] = con.VALIDATION_ACTION_ROW_WISE

            for row in self.warning_row:
                self.append_action(row)
        else:
            self.action[con.VALIDATION_ACTION] = con.VALIDATION_ACTION_OK

        return self.action

    def take_action(self, data_frame):
        """
        With the help of action report this function perform actions on the
        row also it returns the filtered data frame after performing the action.

        TODO: now using if and else to take the action because only two actions
        are there , need to change this when there are number of actions.

        for ex: action = {'action': 'ROW_WISE_ACTION',
                          '1': [{'column': 'label', 'state': 'invalid_label, 'action': 'DROP'},
                                {'column': 'Formula', 'state': 'invalid_formula, 'action': 'DROP'}],
                          '4': [{'column': 'label', 'state': 'invalid_label, 'action': 'DROP'}]}
        actions performed are drop row 1, drop row 4.
        In line 203: We need break because if the row is dropped there is no need
        of other action
        :param data_frame:
        :return: data_frame
        """
        output_df = get_df()
        list_of_rows_to_drop = []

        if not self.check_action_is_stop_tool():
            resultant_df = data_frame
            rows_to_take_action_on = [rows for rows in self.action
                                      if rows not in [con.VALIDATION_ACTION]]

            for rows in rows_to_take_action_on:

                for each_action in self.action[rows]:

                    if each_action[con.VALIDATION_ACTION] == con.VALIDATION_ACTION_DROP:
                        list_of_rows_to_drop.append(rows)
                        action_msg = con.VALIDATION_MSG_ROW_DROPPED
                        break
                    else:
                        resultant_df.set_value(rows, each_action[con.VALIDATION_COLUMN_NAME], 0)
                        action_msg = con.VALIDATION_MSG_FILL_NA

                self.action_messages.append(action_msg)
            output_df = self.action_drop_rows(resultant_df, list_of_rows_to_drop)
        self.warning_error_dict[con.VALIDATION_WARNING][con.VALIDATION_ACTION] = self.action_messages

        return output_df

    def generate_warning_error_list_of_strings(self):
        """
        This function generates the report of validation check in the form of list of
        strings. This is needed because the response we are sending to front end is in
        the format of list of strings. Also HTML tags are added in the message to highlight
        important info in the front end.

        for ex : if result = {'1':{'warning': [['label','invalid_label','DROP'],['formula',
                                            'invalid_formula','DROP']],'errors':[]},
                              '4':{'warning':[['label','invalid_label','DROP']],'errors':[]}
        logs will be = { 'warning': { 'action': ['ROW is DROPPED','ROW is DROPPED],
                       'message': ['ROW number 1: column label has invalid label,
                        column formula has invalid]}'errors' : []}
        :return: dict where keys are error and warnings, and values are list of
        messages.
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
        """
        This is used to drop the rows in a df. Static keyword is used because
        it is behaving as plain function no need to pass self or cls argument.
        :param df: DF on which action is to be performed
        :param row_list: list of row to dropped
        return: DF after row is dropped
        """

        df.drop(df.index[row_list], inplace=True)

        return df

    @staticmethod
    def get_unique_row_having_error(self):
        """
        This is for getting unique value of row_number
        :return: list of unique value
        """
        return self.report_df.row_number.unique()

    @staticmethod
    def get_slice_df_with_row(df, row):
        """
        This method is used to slice the df, wrt to row_number
        """
        return df.loc[df[con.COLUMN_ROW] == row]

    @staticmethod
    def get_key_list(input_dict, condition=None):
        """
        This is used to get the key list of input_dict. Also a condition
        can be given according to which the key is to be choosen.

        :param dict: dictionary
        :param condition: on which key is to be choosen
        :return: list of key in a dictionary
        """
        if condition:
            return [key for key in input_dict.keys() if input_dict[key][condition]]
        else:
            return input_dict.keys()

    @staticmethod
    def get_action_name(result):
        """
        This will return action name which is calculated on basis of
        predefined conditions.

        :param result: dict having state and column name value
        :return: action name according to state and column
        """
        column_name = result[0]
        state = result[1]

        if state == con.MISSING_STATE:

            if column_name in REQUIRED_COLUMN_LIST:
                action = con.VALIDATION_ACTION_DROP
            else:
                action = con.VALIDATION_ACTION_FILL_NA

        elif state == con.DUPLICATE_STATE:
            action = con.VALIDATION_ACTION_DROP

        else:
            action = con.VALIDATION_ACTION_STOP

        return action

    @staticmethod
    def get_action_object(each_result):
        """
        This will give action object for each result for example.

        result = ['label','missing','drop']
        action_object = {'column': 'label',
                         'state': 'missing',
                         'action':'DROP'}
        """

        action_object = {con.VALIDATION_COLUMN_NAME: each_result[0],
                         con.COLUMN_STATE: each_result[1],
                         con.VALIDATION_ACTION: each_result[2]}

        return action_object

    def check_action_is_stop_tool(self):
        """
        This will check if action is not stop_tool
        """
        return self.action[con.VALIDATION_ACTION] == con.VALIDATION_ACTION_STOP

    def append_warning_action_to_result(self, row):
        """
        This is just to append warning action to result.
        """

        for each_result in self.result[row][con.VALIDATION_WARNING]:
            each_result.append(self.get_action_name(each_result))

    def append_error_action_to_result(self, row):
        """
        This is to append error action to result.
        """
        for each_result in self.result[row][con.VALIDATION_ERROR]:
            each_result.append(self.get_action_name(each_result))

    def append_action(self, row):
        """
        This is to append action object to action dict.
        """
        column_state_action_list = []
        for each_result in self.result[row][con.VALIDATION_WARNING]:
            column_state_action_list.append(self.get_action_object(each_result))
        self.action[row] = column_state_action_list

    def append_warning_error_dict_for_row(self, each_row):
        """
        This function append warning and error dict for each row.
        Warning or error dictionary is key value pair where for each row
        specific warning or error message is described.
        :param each_row: this is row number where warning or error is present
        :return: warning error dict for each row so that
        """
        row_df = self.get_slice_df_with_row(self.report_df, each_row)
        warning_error_dict_for_row = {con.VALIDATION_WARNING: [],
                                      con.VALIDATION_ERROR: []}

        for index, row in row_df.iterrows():

            warning_or_error_msg = [row[con.COLUMN_NAME], row[con.COLUMN_STATE]]

            if row[con.COLUMN_STATE] in con.WARNING_STATE:
                warning_error_dict_for_row[con.VALIDATION_WARNING].\
                    append(warning_or_error_msg)
            else:
                warning_error_dict_for_row[con.VALIDATION_ERROR].\
                    append(warning_or_error_msg)
        self.result[row[con.COLUMN_ROW]] = warning_error_dict_for_row