from model import Fragment
import helpers as hl
import numpy as np

def create_fragment(name, formula, parent):
    frag = Fragment(name, formula, parent)
    return {name: frag}

def create_isotopomer_label(frag_dict, label_dict):
    frag_key, frag = frag_dict.items()[0]
    frag.check_if_valid_label(label_dict)
    label_key = hl.label_dict_to_key(label_dict)
    label = {label_key: label_dict}
    return {frag_key: label}, frag_dict

def get_label_dict_mass(frag, isotope, isotope_mass, mode):
    return frag.create_label_dict_from_mass(isotope, isotope_mass, mode)

def add_data_isotopomers(frag_key, label_dict, intensity):
    label_key = hl.label_dict_to_key(label_dict)
    try:
        assert isinstance(intensity, np.ndarray)
    except AssertionError:
        raise AssertionError('intensity should be numpy array')
    label_intensity = {label_key: intensity}
    return {frag_key: label_intensity}

def parse_label_mass(label):
    pass

def parse_label_number(label_number):
    return hl.create_dict_from_isotope_label_list(label_number.split('_'))