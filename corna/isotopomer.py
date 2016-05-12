from model import Fragment
from helpers import label_dict_to_key

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

def create_isotopomers_from_label(name, formula, label_dict_list):
    frag = Fragment(name, formula)
    frag_key = name + '_' + formula
    label_key_list = []
    label_labdict = {}
    for label_dict in label_dict_list:
        frag.check_if_valid_label(label_dict)
        label_key = label_dict_to_key(label_dict)
        label_key_list.append(label_key)
        label_labdict[label_key] = label_dict
    return {frag_key : label_key_list}, label_labdict, {frag_key:frag}

# def add_data_isotopomers(isotopomer, label_intensity, label_key_list):
#     for label in label_key_list:

