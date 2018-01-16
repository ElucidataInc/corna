import collections
from operator import itemgetter
import os
from operator import itemgetter

import numpy as np
import pandas as pd

import constants as const
from formula import Formula
from formulaschema import FormulaSchema
from inputs.column_conventions import multiquant as c

schema_obj = FormulaSchema()
chemformula_schema = schema_obj.create_chemicalformula_schema()
polyatomschema = schema_obj.create_polyatom_schema()

#defined here as needed for webtool
#ISOTOPE_NA_MASS = const.ISOTOPE_NA_MASS

LEVEL_0_COL = const.LEVEL_0_COL
LEVEL_1_COL = const.LEVEL_1_COL
VAR_COL = const.VAR_COL
VAL_COL = const.VAL_COL


# def set_global_isotope_dict(isotope_dict):
#     global ISOTOPE_NA_MASS
#     ISOTOPE_NA_MASS = isotope_dict
#
def get_global_isotope_dict():
     return const.ISOTOPE_NA_MASS

def get_atomic_weight(element):
    try:
        return const.ELE_ATOMIC_WEIGHTS[element]
    except KeyError:
        raise KeyError('Element doesnt exist')


def check_if_isotope_in_dict(iso):
    return const.ISOTOPE_NA_MASS['element'].has_key(iso)


def get_isotope_element(iso):
    try:
        return const.ISOTOPE_NA_MASS['element'][iso]
    except KeyError:
        raise KeyError('Check available isotope list', iso)


def get_isotope_mass(iso):
    try:
        return const.ISOTOPE_NA_MASS['amu'][iso]
    except KeyError:
        raise KeyError('Check available isotope list', iso)


def get_isotope_na(iso, isotope_dict=const.ISOTOPE_NA_MASS):
    try:
        return isotope_dict['naValue'][iso]
    except KeyError:
        raise KeyError('Check available isotope list', iso)


def get_isotope_natural(iso):
    try:
        return const.ISOTOPE_NA_MASS['naturalIsotope'][iso]
    except KeyError:
        raise KeyError('Check available isotope list', iso)


def label_dict_to_key(label_dict):
    key = ''

    for ele, num in label_dict.iteritems():
        key = key + '_' + ele + '_' + str(num)
    key = key.strip('_')

    return key


def read_file(path, head=0):
    """
    This function reads the input file in xls, xlsx, txt and csv
    format
    Args:
        path : path to input file
        head: header of df, default is None

    Returns:
         input_file : input file in the form of pandas dataframe
    """

    excel = ['.xls', '.xlsx']

    if os.path.splitext(path)[1] in excel:
        input_file = pd.read_excel(path, header=head)

    elif os.path.splitext(path)[1] == '.csv':
        input_file = pd.read_csv(path, header=head)

    elif os.path.splitext(path)[1] == '.txt':
        input_file = pd.read_table(path, header=head)

    else:
        raise IOError('only csv/xls/xlsx/txt extensions are allowed')

    return input_file


def json_to_df(json_input):
    """
    This function takes input data in the form of json format and converts
    it in pandas dataframe

    Args:
        json_input : input data in form of json format

    Returns:
        json_to_df : pandas dataframe

    """
    # this should be the format of json input
    #json_input = json.dumps(input_data.to_dict())
    json_df = pd.read_json(json_input)

    return json_df


def merge_two_dfs(df1, df2, how='left', left_on='col1', right_on='col2'):
    merged_df = pd.merge(df1, df2, how=how, left_on=left_on,
                         right_on=right_on)
    merged_df.drop(right_on, axis=1, inplace=True)
    merged_df.fillna(0, inplace=True)

    return merged_df


def filter_df(df, colname_val_dict):
    """
    This function filters the dataframe over single/multiple column name(s) and single/
    multiple column values
    """

    for col_name, col_val_list in colname_val_dict.iteritems():
        filtered_df = df[(df[str(col_name)].isin(col_val_list))]

        return filtered_df


def create_dict_from_isotope_label_list(isonumlist):
    label_dict = collections.OrderedDict()

    for i in xrange(0, len(isonumlist), 2):
        try:
            get_isotope_element(isonumlist[i])
            label_dict.update({isonumlist[i]: int(isonumlist[i + 1])})
        except KeyError:
            raise KeyError('The key must be an isotope')
        except ValueError:
            raise ValueError('The number of labels should be integer')
    return label_dict


def get_unique_values(df, column_name):
    """
    This function gives the unique values from a column in the form of a list
    """
    try:
        unique_val_list = np.unique(df[[str(column_name)]])
    except:
        raise KeyError('Column' + column_name + 'not found in dataframe')

    return unique_val_list


def get_key_from_single_value_dict(inputdict):
    if len(inputdict) == 1:
        key, value = inputdict.items()[0]
    else:
        raise OverflowError('Dictionary not single key, value pair')
    return key


def get_value_from_single_value_dict(inputdict):
    if len(inputdict) == 1:
        key, value = inputdict.items()[0]
    else:
        raise OverflowError('Dictionary not single key, value pair')
    return value


def check_if_all_elems_same_type(inputlist, classname):
    return all(isinstance(x, classname) for x in inputlist)


def concatenate_dataframes_by_col(df_list):
    return pd.concat(df_list)


def parse_polyatom(polyatom_string):
    polyatomdata = polyatomschema.parseString(polyatom_string)
    polyatom = polyatomdata[0]
    return (polyatom.element, polyatom.number_atoms)


def get_formula(formula):
    """Parsing formula to store as an element -> number of atoms dictionary"""
    parsed_formula = Formula(formula).parse_formula_to_elem_numatoms()
    return parsed_formula


def merge_multiple_dfs(df_list):
    """
    This function takes the list of dataframes as an input
    and concatenates the dataframes based on their column names
    Args:
        df_list : list of dataframes
    Returns:
        combined_dfs : concatenated list of dataframes into one dataframe
    """
    combined_dfs = reduce(_merge_dfs, df_list)
    return combined_dfs


def _merge_dfs(df1, df2):
    return pd.merge(df1, df2,
                    on=[c.LABEL, c.SAMPLE,
                        c.NAME, c.FORMULA])

def get_isotope_na_value_dict(isotope_dict = const.ISOTOPE_NA_MASS):
    """
    This function returns a dictionary of isotopes as keys with na values of the
    isotope and their natural isotopes.
    Args:
        isotope_dict: constant dictionary containing natural abundance information
        of different isotopes

    Returns:
        isotope_na_val_dict: dictionary of type {'017':[0.99757,0.00038].

    """
    isotope_na_value_dict = {}
    NA = isotope_dict[const.KEY_NA]
    NAT_ISO = isotope_dict[const.KEY_NAT_ISO]

    for isotope in const.ISOTOPE_LIST:
        natural_iso = NAT_ISO[isotope]
        isotope_na_value_dict[isotope] = [NA[natural_iso], NA[isotope]]

    return isotope_na_value_dict

def get_na_value_dict(isotope_dict = const.ISOTOPE_NA_MASS):
    """
    This function returns the dictionary of default NA values (adapted from wiki)
    for all the isotopes. NA Correction matrix algorithm requires these lists in
    the order of increasing amus ([M, M+1, M+2...]) for proper creation of matrix.
    The matrix has to maintain an order such that the intensities multiplied to it
    are increasing masses, therefore order of amu is crucial.
    Args:
         isotope_dict: constant dictionary containing natural abundance information
        of different isotopes
    Returns:
         na_val_dict: dictionary of type {'C':[0.99,0.11], 'H':[0.98,0.02]}. The order
        of NA values is in increasing order of mass for example 'C': [na(C12), na(C13)]
        'O': [na(O16), na(O17), na(O18)]
    Correction:
        In the commit 442662f:
        The NA dictionary being obtained contains isotope -> NA values as list. These
        lists are sorted in decreasing order of NA values. It was assumed that this
        order would be the same as increasing order of amu. For example:
        C12: 0.989 C13: 0.011, in this case decreasing order of NA values (0.989, 0.011)
        is equivalent to increasing amu (12, 13). It's also true for many isotopes like
        H1,H2; O16,O17 when considering only M,M+1 hence went unnoticed while doing the
        corrections. But for O16,O17,O18 the order of decreasing NA values is not same
        as increasing amus because O18 is more abundant than O17.
        In the commit 9422427:
            Keeping in mind the errorneous order due to incorrect way of sorting, now the
        sorting is done on amus and corresponding NA values are saved. therefore, for
        O the list becomes [0.99757, 0.00038, 0.00205]
        test for this bug: test_get_na_value_dict_O in test_helpers
    """
    NA = isotope_dict[const.KEY_NA]
    amu = isotope_dict[const.KEY_AMU]
    elements = const.ISOTOPE_NA_MASS[const.KEY_ELE]
    na_val_dict = {}
    atoms = set(elements.values())
    for atom in atoms:
         isotope_list = [isotope for isotope, iso_atom
                     in elements.iteritems() if iso_atom == atom or isotope == atom]
         isotope_list = list(set(isotope_list) - set(elements.values()))
         na_val_amu = [(NA[val], amu[val]) for val in isotope_list]
         na_val_amu.sort(key=itemgetter(1))
         na_vals = [val_amu[0] for val_amu in na_val_amu]
         na_val_dict[atom] = na_vals

    na_val_dict.update(get_isotope_na_value_dict())

    return na_val_dict


def check_column_headers(col_headers, col_names):
    """
    This function verifies that all defasult columns are present in input
    text files for multiquant
    """
    err_msg = """Required column/s not found, Column: {!r}""".format(list(set(col_names) - set(col_headers)))
    assert set(col_names).issubset(set(col_headers)), err_msg


def first_sub_second(a, b):
    return [item for item in a if item not in b]


def get_metabolite(fragment):
    metab_name = fragment.split(' ')
    return metab_name[0]


def check_duplicates_in_list(given_list):
    """
    This function checks for duplicates in the given list.
    It iterates over the list and whenever a new element is found,
    we add that to first_occurrence

    :param given_list:
    :return: duplicate_list : list of all the duplicates in given list
    """
    first_occurrence = set()
    duplicate_list = set()
    first_occurrence_add = first_occurrence.add
    duplicate_list_add = duplicate_list.add
    for item in given_list:
        if item in first_occurrence:
            duplicate_list_add(item)
        else:
            first_occurrence_add(item)
    return list(duplicate_list)