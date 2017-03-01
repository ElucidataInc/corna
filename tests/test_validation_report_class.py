import os
import pandas as pd

from corna.validation_report_class import ValidationReport


class TestValidationReport():

    @classmethod
    def setup_class(cls):
        cls.validation=ValidationReport()

    @classmethod
    def teardown_class(cls):
        del cls.validation

    def test_append(self):
        df = pd.DataFrame({'column_name': 'Name', 'row_number': 0, 'state': 'missing'}, index=[0])
        self.validation.append(df)
        assert self.validation.report_df.equals(df)

    def test_generate_report(self):
        df = pd.DataFrame({'column_name': 'Name', 'row_number': 0, 'state': 'missing'}, index=[0])
        self.validation.report_dataframe = df
        test_result = {0: {'warning': [['Name', 'missing']], 'errors': []}}
        assert self.validation.generate_report() == test_result

    def test_generate_action(self):
        df = pd.DataFrame({'column_name': 'Name', 'row_number': 0, 'state': 'missing'}, index=[0])
        self.validation.report_dataframe = df
        test_result = {0: {'warning': [['Name', 'missing', 'DROP']], 'errors': []}}
        assert self.validation.generate_action() == test_result

    def test_decide_action(self):
        df = pd.DataFrame({'column_name': 'Name', 'row_number': 0, 'state': 'missing'}, index=[0])
        self.validation.report_dataframe = df
        assert self.validation.decide_action()['action'] == 'Row_Wise_Action'
        print self.validation.action

    def test_take_action(self):

        df = pd.DataFrame({'column_name': 'Name', 'row_number': 0, 'state': 'missing'}, index=[0])
        self.action = {'action': 'Row_Wise_Action', 0: [{'column': 'Name', 'action': 'DROP', 'state': 'missing'}]}

        new_df = self.validation.take_action(df)
        assert new_df.empty

    def test_action_drop_rows(self):

        df = pd.DataFrame({'column_name': 'Name', 'row_number': 0, 'state': 'missing'}, index=[0])
        assert self.validation.action_drop_rows(df,[0]).empty

    def test_get_unique_row_having_error(self):
        df = pd.DataFrame({'column_name': 'Name', 'row_number': 0, 'state': 'missing'}, index=[0])
        self.validation.report_dataframe = df

        assert self.validation.get_unique_row_having_error(self.validation) == [0]

    def test_get_slice_df_with_row(self):
        df = pd.DataFrame({'column_name': 'Name', 'row_number': 0, 'state': 'missing'}, index=[0])

        assert self.validation.get_slice_df_with_row(df, 0).empty == False

    def test_get_key_list(self):
        dict = {'A':1,'B':2}

        assert self.validation.get_key_list(dict) == ['A','B']

    def test_get_action_name(self):
        result = ['Sample','Invalid']

        assert self.validation.get_action_name(result) == 'Stop_Tool'

    def test_get_action_object(self):
        result = ['Sample','Invalid','Stop_Tool']

        assert self.validation.get_action_object(result) == {'column': 'Sample',
                                                            'action': 'Stop_Tool',
                                                            'state': 'Invalid'}



