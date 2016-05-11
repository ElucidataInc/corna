import os
import pandas as pd

import constants as cs

ELE_ATOMIC_WEIGHTS = cs.const_element_mol_weight_dict()
ISOTOPE_NA_MASS = cs.const_isotope_na_mass()

def get_atomic_weight(element):
    try:
        return ELE_ATOMIC_WEIGHTS[element]
    except KeyError:
        raise KeyError('Element doesnt exist')

def get_isotope(iso):
    try:
        return ISOTOPE_NA_MASS[iso]
    except KeyError:
        raise KeyError('Check available isotope list')

def get_isotope_mass(iso):
    return get_isotope(iso)['mol_mass']

def get_isotope_na(iso):
    return get_isotope(iso)['NA']

def get_isotope_natural(iso):
    return get_isotope(iso)['nat_form']

def read_file(path):

	excel = ['.xls', '.xlsx']

	if os.path.splitext(path)[1] in excel:
		input_file = pd.read_excel(path)

	elif os.path.splitext(path)[1] == '.csv':
		input_file = pd.read_csv(path)

	else:
		raise IOError('only csv/xls/xlsx extensions are allowed')

	return input_file

