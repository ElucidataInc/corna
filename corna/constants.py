"""
Note: 
    NA values are referenced from:
    CRC Handbook of Chemistry and Physics (83rd ed.). Boca Raton, FL: CRC Press. ISBN 0-8493-0483-0.
    by Lide, D. R.
    ed. (2002) 
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
SAMPLE_NAME = 'Sample Name'
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
COMPONENT_NAME = 'Component Name'
NAME_COL = 'Name'
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
MASS_DIFF_DICT = {'O17': {'N': 0.0044, 'H': 0.0025, 'S34': 0.0894, 'S33': 0.0548, 'C': 0.0194, 'Si29': 0.1216, 'Si30': 0.1059},
                  'N15': {'O17': 0.0044, 'H': 0.0069, 'S34': 0.085, 'S33': 0.0504, 'O18': 0.0028, 'C': 0.015, 'Si29': 0.1172, 'Si30': 0.1015}, 
                  'H2': {'O17': 0.0025, 'N': 0.0069, 'S34': 0.0919, 'S33': 0.0573, 'O18': 0.0041, 'C': 0.0219, 'Si29': 0.1241, 'Si30': 0.1084}, 
                  'S34': {'O17': 0.0894, 'N': 0.085, 'H': 0.0919, 'O18': 0.0878, 'C': 0.07, 'Si29': 0.0322, 'Si30': 0.0165}, 
                  'S33': {'O17': 0.0548, 'N': 0.0504, 'H': 0.0573, 'O18': 0.0532, 'C': 0.0354, 'Si29': 0.0668, 'Si30': 0.0511}, 
                  'O18': {'N': 0.0028, 'H': 0.0041, 'S34': 0.0878, 'S33': 0.0532, 'C': 0.0178, 'Si29': 0.12, 'Si30': 0.1043}, 
                  'C13': {'O17': 0.0194, 'N': 0.015, 'H': 0.0219, 'S34': 0.07, 'S33': 0.0354, 'O18': 0.0178, 'Si29': 0.1022, 'Si30': 0.0865}, 
                  'Si29': {'O17': 0.1216, 'N': 0.1172, 'H': 0.1241, 'S34': 0.0322, 'S33': 0.0668, 'O18': 0.12, 'C': 0.1022}, 
                  'Si30': {'O17': 0.1059, 'N': 0.1015, 'H': 0.1084, 'S34': 0.0165, 'S33': 0.0511, 'O18': 0.1043, 'C': 0.0865}}
## Isotope dictionary
ISOTOPE_DICT = {'O': ['O17', 'O18'], 'S': ['S33', 'S34'], 'Si': ['Si29', 'Si30']}

##List for isotopic elements that are added in na_dict
ISOTOPE_LIST = ['O17', 'O18', 'S33', 'S34', 'Si29', 'Si30']

##Output column names
INDIS_ISOTOPE_COL = 'Indistinguishale_isotope'
POOL_TOTAL_COL = 'Pool_total'
METABOLITE_NAME = 'metab_name'

##summary tab
SUMMARY_LABEL = 'label'
SUMMARY_VAL = 'value'
SUMMARY_TITLE = 'title'
SUMMARY = 'summary'
RAW_FIELD_SUMMARY_LIST = ['Number of rows', 'Number of samples', 'Number of cohorts', 'Number of metabolites']
META_FIELD_SUMMARY_LIST = ['Number of fragments', 'Number of unlabeled fragments', 'isotopic tracer']
SAMPLE_FIELD_SUMMARY_LIST = ['Number of background samples', 'Fields in metadata']
LCMS_RAW_FIELD_SUMMARY = ['Number of metabolites', 'Number of samples', 'Number of blank intensity cells', 'Number of rows']
LCMS_META_FILED_SUMMARY = ['Fields in metadata', 'Number of rows in metadata']

## file type
RAW_MSMS = 'InputData'
META_MSMS = 'MetaData'
SMP_MSMS = 'SampleData'
RAW_LCMS = 'InputFile'
META_LCMS = 'MetadataFile'



