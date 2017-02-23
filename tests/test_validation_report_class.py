from corna.validation_report_class import ValidationReport
import pandas as pd


class TestValidationReport:

    @classmethod
    def setup_class(cls):
        cls.validation=ValidationReport()

    @classmethod
    def teardown_class(cls):
        del cls.validation

    def test_append(self):
        df = pd.DataFrame({'column_name': 'Name', 'row_number': 0, 'state': 'missing'}, index=[0])
        self.validation.append(df)
        assert self.validation.report_dataframe.equals(df)

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

    def test_take_action(self):
        df = pd.DataFrame({'column_name': 'Name', 'row_number': 0, 'state': 'missing'}, index=[0])
        self.validation.report_dataframe = df
        new_df = self.validation.take_action(df)
        assert new_df.empty


