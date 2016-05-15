from model import Fragment
import helpers as hl
import numpy as np

def create_fragment_from_mass(name, formula, parent, isotope, isotope_mass, molecular_mass=None, mode=None):
    if molecular_mass != None:
        frag = Fragment(name, formula, parent, isotracer=isotope, isotope_mass=isotope_mass, molecular_mass=molecular_mass)
    elif mode != None:
        frag = Fragment(name, formula, parent, isotracer=isotope, isotope_mass=isotope_mass, mode=mode)
    else:
        raise IOError('One of molecular mass/mode is required to create fragment from mass')
    return {name:frag}

def create_fragment_number(name, formula, parent, label_dict):
    frag = Fragment(name, formula, parent, label_dict)
    return {name:frag}

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

def parse_label_mass(label_mass):
    massdata = label_mass.split('_')
    try:
        isotracer = massdata[0]
        hl.get_isotope(isotracer)
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

def parse_label_number(label_number):
    return hl.create_dict_from_isotope_label_list(label_number.split('_'))