import os
import pandas as pd

import constants as cs

ELE_ATOMIC_WEIGHTS = cs.const_element_mol_weight_dict()

def get_atomic_weight(element):
    try:
        return ELE_ATOMIC_WEIGHTS[element]
    except KeyError:
        raise KeyError('Element doesnt exist')


def read_file(path):

	excel = ['.xls', '.xlsx']

	if os.path.splitext(path)[1] in excel:
		input_file = pd.read_excel(path, header = 0)

	elif os.path.splitext(path)[1] == '.csv':
		input_file = pd.read_csv(path, header = 0)

	else:
		raise IOError('only csv/xls/xlsx extensions are allowed')

	return input_file

def filter_df(df, column_name, column_value):

	filtered_df = df[df[str(column_name)] == str(column_value)]

	return filtered_df

