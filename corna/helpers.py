import os
import pandas as pd
import numpy as np
import collections

import constants as cs
from formula import Formula
from formulaschema import FormulaSchema

schema_obj = FormulaSchema()
chemformula_schema = schema_obj.create_chemicalformula_schema()
polyatomschema = schema_obj.create_polyatom_schema()

ELE_ATOMIC_WEIGHTS = cs.const_element_mol_weight_dict()
ISOTOPE_NA_MASS = cs.const_isotope_na_mass()
NA_DICT = cs.const_na_dict()

def get_atomic_weight(element):
    try:
        return ELE_ATOMIC_WEIGHTS[element]
    except KeyError:
        raise KeyError('Element doesnt exist')

def check_if_isotope_in_dict(iso):
    return ISOTOPE_NA_MASS['Element'].has_key(iso)

def get_isotope(iso):
    try:
        return ISOTOPE_NA_MASS['Element'][iso]
    except KeyError:
        raise KeyError('Check available isotope list', iso)

def get_isotope_mass(iso):
    try:
        return ISOTOPE_NA_MASS['amu'][iso]
    except KeyError:
        raise KeyError('Check available isotope list', iso)

def get_isotope_na(iso):
    try:
        return ISOTOPE_NA_MASS['NA'][iso]
    except KeyError:
        raise KeyError('Check available isotope list', iso)

def get_isotope_natural(iso):
    try:
        return ISOTOPE_NA_MASS['Natural Isotope'][iso]
    except KeyError:
        raise KeyError('Check available isotope list', iso)

def get_sub_na_dict(elements):
    sub_na_dict = {}
    for element in elements:
        sub_na_dict[element] = NA_DICT[element]
    return sub_na_dict

def label_dict_to_key(label_dict):
    key = ''

    for ele, num in label_dict.iteritems():
        key = key + '_' + ele + '_' + str(num)

    key = key.strip('_')
    return key

def read_file(path):

    excel = ['.xls', '.xlsx']

    if os.path.splitext(path)[1] in excel:
        input_file = pd.read_excel(path, header = 0)

    elif os.path.splitext(path)[1] == '.csv':
        input_file = pd.read_csv(path, header = 0)

    elif os.path.splitext(path)[1] == '.txt':
        input_file = pd.read_table(path, header = 0)

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
    #this should be the format of json input
    #json_input = json.dumps(input_data.to_dict())

    json_df = pd.read_json(json_input)

    return json_df


def concat_txts_into_df(direc):

    txt_files = []

    txt_files += [each for each in os.listdir(direc) if each.endswith('.txt')]

    df_list= []

    for files in txt_files:
        df_list.append(read_file(direc + files))

    concat_df = pd.concat(df_list)

    return concat_df

def merge_dfs(df1, df2, how = 'left', left_on = 'col1', right_on = 'col2'):

    merged_df = pd.merge(df1, df2, how= how, left_on=left_on,
                             right_on=right_on)

    #merged_df.drop(right_on, axis=0, inplace=True)
    merged_df.drop(right_on, axis=1, inplace=True)


    merged_df.fillna(0, inplace = True)

    return merged_df


def filter_df(df, column_name, column_value):

    #write test if col name not string
    filtered_df = df[df[str(column_name)] == column_value]

    if filtered_df.empty == 'TRUE':
        raise ValueError('column value does not exist in dataframe', column_value)

    return filtered_df


def filtering_df(df, num_col=3, col1='col1', list_col1_vals=[], col2='col2', list_col2_vals=[], col3='col3', list_col3_vals=[]):
    if num_col==1:
        filtered_df = df[(df[str(col1)].isin(list_col1_vals))]

    elif num_col==2:
        filtered_df = df[(df[str(col1)].isin(list_col1_vals)) & (df[str(col2)].isin(list_col2_vals))]

    elif num_col==3:
        filtered_df = df[(df[str(col1)].isin(list_col1_vals)) & (df[str(col2)].isin(list_col2_vals)) & (df[str(col3)].isin(list_col3_vals))]

    return filtered_df

def create_dict_from_isotope_label_list(isonumlist):
    label_dict = collections.OrderedDict()

    for i in xrange(0,len(isonumlist),2):
        try:
            get_isotope(isonumlist[i])
            label_dict.update({isonumlist[i]: int(isonumlist[i+1])})
        except KeyError:
            raise KeyError('The key must be an isotope')
        except ValueError:
            raise ValueError('The number of labels should be integer')
    return label_dict


def get_unique_values(df, column_name):

    unique_val_list = np.unique(df[[str(column_name)]])

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

def concatentate_dataframes_by_col(df_list):
    return pd.concat(df_list)

def parse_polyatom(polyatom_string):
    polyatomdata = polyatomschema.parseString(polyatom_string)
    polyatom = polyatomdata[0]
    return (polyatom.element, polyatom.number_atoms)

def get_formula(formula):
    """Parsing formula to store as an element -> number of atoms dictionary"""
    parsed_formula = Formula(formula).parse_formula_to_elem_numatoms()
    return parsed_formula


def convert_labels_to_std(df, iso_tracers):
    new_labels = []
    for labels in df['Label']:
        if labels == 'C12 PARENT':
            labe = ''
            for tracs in iso_tracers:
                labe = labe + tracs+'_0_'
            new_labels.append(labe.strip('_'))
        else:
            splitted = labels.split('-label-')
            split2 = splitted[1].split('-')
            isotopelist = chemformula_schema.parseString(splitted[0])
            el1 = (''.join(str(x) for x in isotopelist[0]))
            el1_num = el1 + '_'+ split2[0]
            if len(iso_tracers) == 1:
                new_labels.append(el1_num)

            else:
                try:
                    el2 = '_'+(''.join(str(x) for x in isotopelist[1])) + '_' + split2[1]

                    el = el1_num+el2
                    new_labels.append(el)
                except:
                    for tracer in iso_tracers:
                        if tracer != el1:
                            el = el1_num + '_' + tracer + '_0'
                            new_labels.append(el)

    df['Label'] = new_labels

    return df