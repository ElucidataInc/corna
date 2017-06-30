from collections import namedtuple
import numbers

from model import Fragment
import helpers as hl


Infopacket = namedtuple('Infopacket', 'frag data unlabeled name')


def create_fragment_from_mass(name, formula, isotope, isotope_mass, molecular_mass=None, mode=None):
    if molecular_mass != None:
        frag = Fragment(name, formula, isotracer=isotope,
                        isotope_mass=isotope_mass, molecular_mass=molecular_mass)
    elif mode != None:
        frag = Fragment(name, formula, isotracer=isotope,
                        isotope_mass=isotope_mass, mode=mode)
    else:
        frag = Fragment(name, formula, isotracer=isotope,
                        isotope_mass=isotope_mass)
    return {name: frag}


def create_fragment_from_number(name, formula, label_dict):
    frag = Fragment(name, formula, label_dict=label_dict)
    return {name: frag}


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
        raise KeyError('Isotope should be part of the constants')
    except ValueError:
        raise ValueError('Masses should be convertible to floats')
    return {'tracer': isotracer, 'parent_mass': parent_mass, 'daughter_mass': daughter_mass}


def validate_data(data):
    if not hl.check_if_all_elems_same_type(data.keys(), basestring):
        raise TypeError('Sample Names should be of type unicode or string')
    if not hl.check_if_all_elems_same_type(data.values(), numbers.Number):
        raise TypeError('Intensities should be numerical values')


def add_data_fragment(fragment_dict, data, label_info, name):
    frag_key, frag = fragment_dict.items()[0]
    assert isinstance(data, dict)
    validate_data(data)
    return {frag_key: Infopacket(frag, data, label_info, name)}



def parse_label_number(label_number):
    return hl.create_dict_from_isotope_label_list(label_number.split('_'))


def insert_data_to_fragment_mass(frag_info, label, sample_dict, mode=None):
    label_mass_dict = parse_label_mass(label)
    daughter_formula = frag_info.formula
    parent_formula = frag_info.parent_formula
    isotope = str(label_mass_dict['tracer'])
    parent_mass = label_mass_dict['parent_mass']
    parent_name = frag_info.name + '_' + str(parent_mass)
    daughter_mass = label_mass_dict['daughter_mass']
    daughter_name = frag_info.name + '_' + str(daughter_mass)
    parent_frag = create_fragment_from_mass(
        parent_name, parent_formula, isotope, parent_mass, mode=mode)
    daughter_frag = create_fragment_from_mass(
        daughter_name, daughter_formula, isotope, daughter_mass, mode=mode)
    frag = create_combined_fragment(parent_frag, daughter_frag)
    parent_frag_key, parent_frag_value = parent_frag.items()[0]
    label_info = parent_frag_value.check_if_unlabel()
    return add_data_fragment(frag, sample_dict, label_info, frag_info.parent)


def insert_data_to_fragment_number(frag_info, label, sample_dict):
    label_number_dict = parse_label_number(label)
    frag_name = frag_info.name + '_' + label
    frag = create_fragment_from_number(frag_name, frag_info.formula, label_number_dict)
    frag_key, frag_value = frag.items()[0]
    label_info = frag_value.check_if_unlabel()
    return add_data_fragment(frag, sample_dict, label_info, frag_info.name)


def bulk_insert_data_to_fragment(frag_info, list_data_dict, mass=False, number=False):
    fragment_list = {}
    for key, value in list_data_dict.iteritems():
        if number:
            fragment_list.update(
                insert_data_to_fragment_number(frag_info, key, value))
        elif mass:
            fragment_list.update(
                insert_data_to_fragment_mass(frag_info, key, value))
    return fragment_list


