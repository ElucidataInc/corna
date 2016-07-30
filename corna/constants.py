import os
import json

elementdata = os.path.join(os.path.dirname(__file__),'element_data.json')
with open(elementdata) as data_file:
    data = json.load(data_file)

ELE_ATOMIC_WEIGHTS = data["element_mol_weight_dict"]
ISOTOPE_NA_MASS = data["isotope_na_mass"]
UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER_CASE = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
VAR_COL = "variable"
VAL_COL = "value"
LEVEL_0_COL = "level_0"
LEVEL_1_COL = "level_1"
INTENSITY_COL = 'Intensity'
SAMPLE_COL = 'Sample Name'
PARENT_COL = 'Unlabeled Fragment'
LABEL_COL = 'Label'
FRAG_COL = 'frag_keys'
MASSINFO_COL = 'Mass Info'
ISOTRACER_COL = 'Isotopic Tracer'
