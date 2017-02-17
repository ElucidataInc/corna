import pandas as pd
from inputs.column_conventions import maven as c

class ValidationReport(object):
    """
    This is validation report class. This class helps in generating report of
    all the warning and error in different formats. It also helps deciding
    what action is to be taken after performing all the test.

    """

    def __init__(self):
        """
        Intialising variables here.

        """

        self.report_dataframe = pd.DataFrame()
        self.result={}
        self.required_column_list=[c.NAME, c.LABEL, c.FORMULA]
        self.invalid_row=[]
        self.warning_row=[]
        self.error_row=[]
        self.action={}
        self.warning_error_dict={'warning':[],'error':[]}
