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
		input_file = pd.read_excel(path)

	elif os.path.splitext(path)[1] == '.csv':
		input_file = pd.read_csv(path)

	else:
		raise IOError('only csv/xls/xlsx extensions are allowed')

	return input_file

