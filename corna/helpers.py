import constants as cs

ELE_ATOMIC_WEIGHTS = cs.const_element_mol_weight_dict()

def get_atomic_weight(element):
    try:
        return ELE_ATOMIC_WEIGHTS[element]
    except KeyError:
        raise KeyError('Element doesnt exist')
