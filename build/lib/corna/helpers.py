import os
import pandas as pd
import numpy as np

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
        raise KeyError('Check available isotope list', iso)

def get_isotope_mass(iso):
    return get_isotope(iso)['mol_mass']

def get_isotope_na(iso):
    return get_isotope(iso)['NA']

def get_isotope_natural(iso):
    return get_isotope(iso)['nat_form']

def label_dict_to_key(label_dict):
    key = ''
    for ele, num in label_dict.iteritems():
        key = ele + '_' + str(num) + '_' + key
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


def json_to_df(json_input, input_data):
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


def create_dict_from_isotope_label_list(isonumlist):
    label_dict = {}
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
