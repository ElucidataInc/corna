"""
Note: 
    NA values are referenced from paper Correcting Mass Isotopomer
    Distributions for Naturally Occurring Isotopes.
    By: Wouter A. van Winden,1* Christoph Wittmann,2 Elmar Heinzle,2
    Joseph J. Heijnen
"""

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
ELEMENT_SYMBOL = ('[A-Z][a-z]?')
LEVEL_0_COL = "level_0"
LEVEL_1_COL = "level_1"
INTENSITY_COL = 'Intensity'
SAMPLE_COL = 'Sample'
PARENT_COL = 'Unlabeled Fragment'
LABEL_COL = 'Label'
FRAG_COL = 'frag_keys'
MASSINFO_COL = 'Mass Info'
ISOTRACER_COL = 'Isotopic Tracer'
FORMULA_COL = 'Formula'
VALID_STATE = 'correct'
MISSING_STATE = 'missing'
DUPLICATE_STATE = 'duplicate'
LABEL_STATE_INVALID = 'invalid label data'
LABEL_STATE_NOT_CORRECT = 'label not correct'
LABEL_STATE_NOT_FORMULA = 'label_not_in_formula'
LABEL_STATE_NUMBER_MORE_FORMULA = 'element_in_label_more_than_formula'
ELEMENT_LIST = set(['C','N','H','S'])
UNLABELLED_LABEL = 'C12 PARENT'
FORMULA_STATE_INVALID = 'formula not correct'
COLUMN_STATE = 'state'
COLUMN_ROW = 'row_number'
COLUMN_NAME = 'column_name'
UNLABELLED_LABEL_DICT = {'C': 0,'N': 0}
INTENSITY_STATE_NEGATIVE = 'negative'
INTENSITY_STATE_INVALID = 'invalid_intensity_value'
VALIDATION_WARNING = 'warnings'
VALIDATION_ERROR = 'errors'
VALIDATION_MESSAGE = 'message'
VALIDATION_ACTION = 'action'
VALIDATION_ACTION_DROP = 'DROP'
VALIDATION_ACTION_FILL_NA = 'FILL_NA'
VALIDATION_ACTION_STOP = 'Stop_Tool'
VALIDATION_ACTION_OK = 'All_Ok'
VALIDATION_ACTION_ROW_WISE = 'Row_Wise_Action'
WARNING_STATE = [DUPLICATE_STATE,MISSING_STATE]
VALIDATION_COLUMN_NAME = 'column'
VALIDATION_MSG_ROW_DROPPED = "Row is Dropped"
VALIDATION_MSG_FILL_NA = "Missing value of columns replaced with 0"
MOL_MASS_VALIDATE = 'Molecular weight of a metabolite cannot be zero'
PPM_REQUIREMENT_VALIDATION = 'The ppm requirement is at the boderline for '
##Keys in ISOTOPE_NA_MASS dictionary
KEY_NA = "naValue"
KEY_AMU = "amu"
KEY_ELE = "element"
KEY_NAT_ISO = "naturalIsotope"
ORIGINAL_FILENAME = "Original Filename"
BACKGROUND_SAMPLE = "Background Sample"
FORMULA_COL_METADATAFILE = ['Formula', 'Parent Formula']
AREA_COLUMN_RAWFILE = ['Area']
COLUMN_ISOTOPE_TRACER = 'Isotopic Tracer'
ISOTOPE_VALUES = ['C13', 'N15', 'H2', 'S34']
BORDERLINE_LIMIT = 0.5
PATTERN_MASSINFO_COL = '\d+.0 \/ \d+.0'
## Dict storing mass diff between isotopes
MASS_DIFF_DICT = {"C13": {'N': 0.00631, 'O17': 0.00087, 'O18': 1.00089, 'H': 0.00292, 'S33': 0.0049, 'S34': 0.9924},
                  "N15": {'C': 0.00631, 'O17': 0.00718, 'O18': 1.00721, 'H': 0.00924, 'S33': 0.0028, 'S34': 0.998},
                  "H2": {'C': 0.00292, 'O17': 0.0021, 'O18': 0.9979, 'N': 0.00924, 'S33': 0.0064, 'S34': 0.989},
                  "S33": {'N': 0.0023, 'O17': 0.0044, 'O18': 1.0044, 'H': 0.00689, 'C': 0.004},
                  "S34": {'N': 0.0023, 'O17': 0.9916, 'O18': 0.0084, 'H': 0.00689, 'C': 0.004},
                  "O17": {'C': 0.00087, 'N': 0.00718, 'H': 0.00206, 'S33': 0.0044, 'S34': 0.9915},
                  "O18": {'C': 0.00087, 'N': 0.00718, 'H': 0.00206, 'S33': 1.0044, 'S34': 0.0084}}
## Isotope dictionary
ISOTOPE_DICT = {'O': ['O17', 'O18'], 'S': ['S33', 'S34']}

##List for isotopic elements that are added in na_dict
ISOTOPE_LIST = ['O17', 'O18', 'S33', 'S34']

##Output column names
INDIS_ISOTOPE_COL = 'Indistinguishale_isotope'
POOL_TOTAL_COL = 'Pool_total'




