import numpy as np

from . model import Fragment
from . import helpers as hl


def create_fragment_from_mass(name, formula, isotope, isotope_mass, molecular_mass=None, mode=None):
    if molecular_mass != None:
        frag = Fragment(name, formula, isotracer=isotope, isotope_mass=isotope_mass, molecular_mass=molecular_mass)
    elif mode != None:
        frag = Fragment(name, formula, isotracer=isotope, isotope_mass=isotope_mass, mode=mode)
    else:
        frag = Fragment(name, formula, isotracer=isotope, isotope_mass=isotope_mass)
    return {name:frag}

def create_fragment_from_number(name, formula, label_dict):
    frag = Fragment(name, formula, label_dict=label_dict)
    return {name:frag}

def create_combined_fragment(parent_fragment_dict, daughter_fragment_dict):
    parent_key, parent_fragment = parent_fragment_dict.items()[0]
    daughter_key, daughter_fragment = daughter_fragment_dict.items()[0]
    return {(parent_key, daughter_key): [parent_fragment, daughter_fragment]}

def parse_label_mass(label_mass):
    massdata = label_mass.split('_')
    try:
        isotracer = massdata[0]
        hl.get_isotope_element(isotracer)
        parent_mass = float(massdata[1])
        daughter_mass = float(massdata[2])
    except IndexError:
        raise IndexError('The key should have three components, isotope, parent mass '
                         'and daughter mass separated by _ in the same order')
    except KeyError:
        raise KeyError('First part of the key must be an isotope')
    except ValueError:
        raise ValueError('Masses should be convertible to floats')
    return {'tracer': isotracer, 'parent_mass': parent_mass, 'daughter_mass': daughter_mass}


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

def insert_data_to_fragment_mass(frag_info, label, sample_dict, mode=None):
    label_mass_dict = parse_label_mass(label)
    name = frag_info[0]
    daughter_formula = frag_info[1]
    parent_formula = frag_info[2]
    isotope = str(label_mass_dict['tracer'])
    parent_mass = label_mass_dict['parent_mass']
    parent_name = name + '_' + str(parent_mass)
    daughter_mass = label_mass_dict['daughter_mass']
    daughter_name = name + '_' + str(daughter_mass)
    parent_frag = create_fragment_from_mass(parent_name, parent_formula, isotope, parent_mass, mode=mode)
    daughter_frag = create_fragment_from_mass(daughter_name, daughter_formula, isotope, daughter_mass, mode=mode)
    frag = create_combined_fragment(parent_frag, daughter_frag)
    parent_frag_key, parent_frag_value = parent_frag.items()[0]
    label_info = parent_frag_value.check_if_unlabel()
    return add_data_fragment(frag, sample_dict, label_info, name)

def insert_data_to_fragment_number(frag_info, label, sample_dict):
    label_number_dict = parse_label_number(label)
    name = frag_info[0]
    frag_name = frag_info[0] + '_' + label
    formula = frag_info[1]
    frag = create_fragment_from_number(frag_name, formula, label_number_dict)
    frag_key, frag_value = frag.items()[0]
    label_info = frag_value.check_if_unlabel()
    return add_data_fragment(frag, sample_dict, label_info, name)

def bulk_insert_data_to_fragment(frag_info, list_data_dict, mass=False, number=False):
    fragment_list = {}
    for key, value in list_data_dict.iteritems():
        if number:
            fragment_list.update(insert_data_to_fragment_number(frag_info, key, value))
        elif mass:
            fragment_list.update(insert_data_to_fragment_mass(frag_info, key, value))
    return fragment_list

def fragment_to_input_model_mass(fragment):
    parent_frag, daughter_frag = fragment[0]
    parent_formula = parent_frag.formula
    daughter_formula = daughter_frag.formula
    name = fragment[3]
    key_tuple = (name, daughter_formula, parent_formula)
    label_dict_key = str(parent_frag.isotracer) + '_' + \
                 str(parent_frag.isotope_mass) + '_' + \
                 str(daughter_frag.isotope_mass)
    label_dict_value = fragment[1]
    return {key_tuple:{label_dict_key:label_dict_value}}


def fragment_to_input_model_number(fragment):
    frag = fragment[0]
    frag_formula = frag.formula
    name = fragment[3]
    key_tuple = (name, frag_formula)
    label_dict_key = hl.label_dict_to_key(frag.label_dict)
    label_dict_value = fragment[1]
    return {key_tuple:{label_dict_key:label_dict_value}}

def fragment_dict_to_std_model(fragment_dict, parent):
    output_fragment_dict = {}
    if parent:
        for key, value in fragment_dict.iteritems():
            output_fragment_dict.update(fragment_to_input_model_mass(value))
    else:
        for key, value in fragment_dict.iteritems():
            label_dict = fragment_to_input_model_number(value)
            curr_key = hl.get_key_from_single_value_dict(label_dict)
            try:
                output_fragment_dict[curr_key].update(label_dict[curr_key])
            except KeyError:
                output_fragment_dict.update(label_dict)
    return output_fragment_dict
