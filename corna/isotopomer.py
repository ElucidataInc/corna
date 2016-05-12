from model import Fragment

def create_isotopomers_from_label(name, formula, label_dict_list):
    frag = Fragment(name, formula)
    for label_dict in label_dict_list:
        frag.check_if_valid_label(label_dict)

    return {frag : label_dict_list}
