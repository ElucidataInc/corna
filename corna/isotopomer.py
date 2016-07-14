from model import Fragment
import helpers as hl
import numpy as np

def create_fragment_from_number(name, formula, label_dict):
    frag = Fragment(name, formula, label_dict=label_dict)
    return {name:frag}

def validate_data(data):
    if not hl.check_if_all_elems_same_type(data.keys(), str):
        raise TypeError('Sample names should be of type string')
    if not hl.check_if_all_elems_same_type(data.values(), np.ndarray):
        raise TypeError('Intensities should be of type numpy arrays')

def add_data_fragment(fragment_dict, data, label_info, name):
    frag_key, frag = fragment_dict.items()[0]
    assert isinstance(data, dict)
    validate_data(data)
    return {frag_key: [frag, data, label_info, name]}

def parse_label_number(label_number):
    return hl.create_dict_from_isotope_label_list(label_number.split('_'))

def insert_data_to_fragment(frag_info, label, sample_dict):
    label_number_dict = parse_label_number(label)
    name = frag_info[0]
    frag_name = frag_info[0] + '_' + label
    formula = frag_info[1]
    frag = create_fragment_from_number(frag_name, formula, label_number_dict)
    frag_key, frag_value = frag.items()[0]
    label_info = frag_value.check_if_unlabel()
    return add_data_fragment(frag, sample_dict, label_info, name)

def bulk_insert_data_to_fragment(frag_info, list_data_dict):
    fragment_list = {}
    for key, value in list_data_dict.iteritems():
        fragment_list.update(insert_data_to_fragment(frag_info, key, value))
    return fragment_list

def fragment_to_input_model(fragment):
    frag = fragment[0]
    frag_formula = frag.formula
    name = fragment[3]
    key_tuple = (name, frag_formula)
    label_dict_key = hl.label_dict_to_key(frag.label_dict)
    label_dict_value = fragment[1]
    return {key_tuple:{label_dict_key:label_dict_value}}

def fragment_dict_to_std_model(fragment_dict):
    output_fragment_dict = {}
    for key, value in fragment_dict.iteritems():
        label_dict = fragment_to_input_model(value)
        curr_key = hl.get_key_from_single_value_dict(label_dict)
        try:
            output_fragment_dict[curr_key].update(label_dict[curr_key])
        except KeyError:
            output_fragment_dict.update(label_dict)
    return output_fragment_dict
