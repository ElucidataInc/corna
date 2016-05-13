from model import Fragment
from helpers import label_dict_to_key
import numpy as np

def create_fragment(name, formula):
    frag = Fragment(name, formula)
    frag_key = name + '_' + formula
    return {frag_key: frag}

def create_isotopomer_label(frag_dict, label_dict):
    frag_key, frag = frag_dict.items()[0]
    frag.check_if_valid_label(label_dict)
    label_key = label_dict_to_key(label_dict)
    label = {label_key: label_dict}
    return {frag_key: label}, frag_dict

def get_label_dict_mass(frag, isotope, isotope_mass, mode):
    return frag.create_label_dict_from_mass(isotope, isotope_mass, mode)

def add_data_isotopomers(frag_key, label_dict, intensity):
    label_key = label_dict_to_key(label_dict)
    try:
        assert isinstance(intensity, np.ndarray)
    except AssertionError:
        raise AssertionError('intensity should be numpy array')
    label_intensity = {label_key: intensity}
    return {frag_key: label_intensity}

