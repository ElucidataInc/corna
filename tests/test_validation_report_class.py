from corna.validation_report_class import ValidationReport
import pytest
import pandas as pd
from corna.model import Ion

class TestValidationReport:

    @classmethod
    def setup_class(cls):
        cls.validation=ValidationReport()

    @classmethod
    def teardown_class(cls):
        del cls.validation

    def test_append(self):
        df = pd.DataFrame({'column_name': 'Name', 'row_number': 1, 'state': 'missing'}, index=[0])
        self.validation.append(df)
        assert self.validation.report_dataframe.equals(df)