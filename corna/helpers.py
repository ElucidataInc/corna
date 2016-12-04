import collections
import os

import numpy as np
import pandas as pd

from . import constants as cs
from . formula import Formula
from . formulaschema import FormulaSchema
from . inputs.column_conventions import multiquant as c

schema_obj = FormulaSchema()
chemformula_schema = schema_obj.create_chemicalformula_schema()
polyatomschema = schema_obj.create_polyatom_schema()

#defined here as needed for webtool
#ISOTOPE_NA_MASS = cs.ISOTOPE_NA_MASS

LEVEL_0_COL = cs.LEVEL_0_COL
LEVEL_1_COL = cs.LEVEL_1_COL
VAR_COL = cs.VAR_COL
VAL_COL = cs.VAL_COL


# def set_global_isotope_dict(isotope_dict):
#     global ISOTOPE_NA_MASS
#     ISOTOPE_NA_MASS = isotope_dict
#
def get_global_isotope_dict():
     return cs.ISOTOPE_NA_MASS

def get_atomic_weight(element):
    try:
        return cs.ELE_ATOMIC_WEIGHTS[element]
    except KeyError:
        raise KeyError('Element doesnt exist')


def check_if_isotope_in_dict(iso):
    return cs.ISOTOPE_NA_MASS['element'].has_key(iso)


def get_isotope_element(iso):
    try:
        return cs.ISOTOPE_NA_MASS['element'][iso]
    except KeyError:
        raise KeyError('Check available isotope list', iso)


def get_isotope_mass(iso):
    try:
        return cs.ISOTOPE_NA_MASS['amu'][iso]
    except KeyError:
        raise KeyError('Check available isotope list', iso)


def get_isotope_na(iso, isotope_dict=cs.ISOTOPE_NA_MASS):
    try:
        return isotope_dict['naValue'][iso]
    except KeyError:
        raise KeyError('Check available isotope list', iso)


def get_isotope_natural(iso):
    try:
        return cs.ISOTOPE_NA_MASS['naturalIsotope'][iso]
    except KeyError:
        raise KeyError('Check available isotope list', iso)


def label_dict_to_key(label_dict):
    key = ''

    for ele, num in label_dict.iteritems():
        key = key + '_' + ele + '_' + str(num)
    key = key.strip('_')

    return key


def read_file(path):
    """
    This function reads the input file in xls, xlsx, txt and csv
    format
    Args:
        path : path to input file

    Returns:
         input_file : input file in the form of pandas dataframe
    """

    excel = ['.xls', '.xlsx']

    if os.path.splitext(path)[1] in excel:
        input_file = pd.read_excel(path, header=0)

    elif os.path.splitext(path)[1] == '.csv':
        input_file = pd.read_csv(path, header=0)

    elif os.path.splitext(path)[1] == '.txt':
        input_file = pd.read_table(path, header=0)

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


# def concat_txts_into_df(directory):
#     #data_frames = [read_file(os.path.join(directory, f))
#     #               for f in os.listdir(directory)
#     #               if f.endswith('.txt')]

#     txt_files = []

#     txt_files += [each for each in os.listdir(directory) if each.endswith('.txt')]

#     df_list= []
#     for files in txt_files:
#         df = read_file(directory + '/' + files)
#         col_head =  df.columns.tolist()
#         assert(set(col_head), set(default_cols))
#         df_list.append(df)
#         df_list.append(read_file(directory + '/' + files))

#     concat_df = pd.concat(df_list)

#     return concat_df

    #return pd.concat(data_frames)


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
    combined_dfs = combined_dfs.T.drop_duplicates().T
    return combined_dfs


def _merge_dfs(df1, df2):
    return pd.merge(df1, df2,
                    on=[c.LABEL, c.SAMPLE,
                        c.NAME])


def get_na_value_dict(isotope_dict = cs.ISOTOPE_NA_MASS):
    """
    This function returns the dictionary of default NA values (adapted from wiki)
    for all the isotopes
    """
    NA = isotope_dict['naValue']
    elements = cs.ISOTOPE_NA_MASS['element']
    na_val_dict = {}
    atoms = set(elements.values())

    for atom in atoms:
        isotope_list = [isotope for isotope, iso_atom
                        in elements.iteritems() if iso_atom == atom]
        na_vals = [NA[val] for val in isotope_list]
        na_vals.sort(reverse=True)
        na_val_dict[atom] = na_vals

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
