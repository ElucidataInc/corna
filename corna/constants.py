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
LABEL_STATE_NOT_CORRECT = 'a required format "C13-Label-1"'
LABEL_STATE_NOT_FORMULA = 'no label in formula'
LABEL_STATE_NUMBER_MORE_FORMULA = 'element_in_label_more_than_formula'
ELEMENT_LIST = set(['C','N','H','S', 'O'])
UNLABELLED_LABEL = 'C12 PARENT'
FORMULA_STATE_INVALID = 'formula not correct'
COLUMN_STATE = 'state'
COLUMN_ROW = 'row_number'
COLUMN_NAME = 'column_name'
COMPONENT_NAME = 'Component Name'
NAME_COL = 'Name'
NA_LCMS = 'na_lcms'
NA_MSMS = 'na_msms'
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
MISSING_COMPONENTS = "missing_components"
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
PATTERN_MASSINFO_COL = '\d+.*\d+\s*\/\s*\d+.*\d+'
SAMPLE_NAME_COL_PATTERN = '^([a-zA-Z0-9_\s\-]*)$'
## Dict storing mass diff between isotopes
#formula used = {(O17-O16) - (C13-C12)}
MASS_DIFF_DICT = {
  'O17': {
    'C': 0.0008619999999999184,
    'N': 0.007181906799999971,
    'H': 0.0020598999999998924,
    'S34': 0.9915791999999999,
    'Si29': 0.0046167999999999765,
    'Si30': 0.9926267,
    'S33': 0.0048367999999999745,
  },
  'H2': {
    'O17': 0.0020598999999998924,
    'C': 0.0029218999999998108,
    'N': 0.009241806799999863,
    'S34': 0.9895193,
    'Si29': 0.006676699999999869,
    'Si30': 0.9905668000000001,
    'S33': 0.006896699999999867,
    'O18': 0.9987233
  },
  'N15': {
    'O17': 0.007181906799999971,
    'C': 0.0063199068000000524,
    'H': 0.009241806799999863,
    'S34': 0.9987611067999999,
    'Si29': 0.0025651067999999944,
    'Si30': 0.9998086067999999,
    'S33': 0.0023451067999999964,
    'O18': 1.0079651068
  },
  'C13': {
    'O17': 0.0008619999999999184,
    'N': 0.0063199068000000524,
    'H': 0.0029218999999998108,
    'S34': 0.9924411999999998,
    'Si29': 0.003754800000000058,
    'Si30': 0.9934886999999999,
    'S33': 0.003974800000000056,
    'O18': 1.0016451999999998
  },
  'S34': {
    'O17': 0.9915791999999999,
    'C': 0.9924411999999998,
    'N': 0.9987611067999999,
    'H': 0.9895193,
    'Si29': 0.9961959999999999,
    'Si30': 0.00104750000000009,
    'O18': 0.00920399999999999
  },
  'Si29': {
    'O17': 0.0046167999999999765,
    'C': 0.003754800000000058,
    'N': 0.0025651067999999944,
    'H': 0.006676699999999869,
    'S34': 0.9961959999999999,
    'S33': 0.00021999999999999797,
    'O18': 1.0053999999999998
  },
  'Si30': {
    'O17': 0.9926267,
    'C': 0.9934886999999999,
    'N': 0.9998086067999999,
    'H': 0.9905668000000001,
    'S34': 0.00104750000000009,
    'S33': 0.9974635,
    'O18': 0.0081564999999999
  },
  'S33': {
    'O17': 0.0048367999999999745,
    'C': 0.003974800000000056,
    'N': 0.0023451067999999964,
    'H': 0.006896699999999867,
    'Si29': 0.00021999999999999797,
    'Si30': 0.9974635,
    'O18': 1.00562
  },
  'O18': {
    'C': 1.0016451999999998,
    'N': 1.0079651068,
    'H': 0.9987233,
    'S34': 0.00920399999999999,
    'Si29': 1.0053999999999998,
    'Si30': 0.0081564999999999,
    'S33': 1.00562,
  }
}
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
RAW_LCMS = 'Input_Data'
META_LCMS = 'Meta_Data'

FILE_PATH = 'file_path'

SAMPLE_METADATA_REQUIRED_COLS = ['Original Filename', 'Sample Name', 'Background Sample',\
                                 'Phenotype', 'Sample_no', 'Time Course']

METADATA_MQ_REQUIRED_COLS = ['Component Name', 'Unlabeled Fragment', 'Isotopic Tracer', 'Name', 'Formula',
                             'Parent Formula']

RAW_MQ_DICT = {
    'file_path': None,
    'required_columns': ['Original Filename'],
    'warnings': {
        'missing': 'FILL_NA',
        'duplicate': 'DROP',
    },
    'functions': {
        'numerical': {'column_list': AREA_COLUMN_RAWFILE,
                      'negative state': 'negative',
                      'invalid state': 'invalid num'},
        'pattern_match': {'column_name': MASSINFO_COL,
                          'regex_pattern': PATTERN_MASSINFO_COL,
                          'state':'not in correct format'},
        'missing_data': {'state': 'missing'},
    }
}

METADATA_MQ_DICT = {
    'file_path': '',
    'required_columns': METADATA_MQ_REQUIRED_COLS,
    'warnings': {
        'missing': 'FILL_NA',
        'duplicate': 'DROP',
    },
    'functions': {
        'chemical_formula': {'column_list': FORMULA_COL_METADATAFILE,
                            'state': 'invalid formula'},
        'value_in_constant': {'column_name': ISOTRACER_COL,
                              'constant_list' : ISOTOPE_VALUES,
                              'state' : 'invalid'},
        'missing_data': {'state': 'missing'},
        }

}

SAMPLE_METADATA_DICT = {
    'file_path': '',
    'required_columns': SAMPLE_METADATA_REQUIRED_COLS,
    'warnings': {
        'missing': 'FILL_NA',
        'duplicate': 'DROP',
    },
    'functions': {
        'chemical_formula': {'column_list': ORIGINAL_FILENAME,
                            'state': 'invalid formula'},
        'missing_data': {'state': 'missing'},
        }
}
