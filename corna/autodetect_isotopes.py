import re
import warnings

import constants as cs
from helpers import get_formula, get_atomic_weight


def get_mol_weight(formula):
    """
    This function returns molecular weight of a metabolite.
    :param formula: formula of the metabolite
    :return: molecular weight (float)
    """
    parsed_formula = get_formula(formula)
    mol_wt = 0
    for sym, qty in parsed_formula.iteritems():
        mol_wt = mol_wt + get_atomic_weight(sym) * qty
        if mol_wt == 0.0:
            raise Exception(cs.MOL_MASS_VALIDATE)
        return mol_wt



def get_ppm_required(formula, delta_m):
    """
    This function calculates the ppm of the machine
    required to distinguish between the two elements
    in a metabolite.
    :param formula: formula of the metabolite
    :param delta_m: mass diff. between the two elements
    :return: required pp
    """
    metabolite_mass = get_mol_weight(formula)
    required_ppm = 1000000 * (delta_m / metabolite_mass)
    return required_ppm


def get_elements_from_formula(formula):
    """
    This functions creates a list of all the elements
    present in the formula
    :param formula:formula of the metabolite
    :return: ele_list: list of elements present in
    the formula
    """
    ele_list = re.findall(cs.ELEMENT_SYMBOL, str(formula))
    return ele_list


def raise_warning(ppm_user_input, required_ppm, formula, ele):
    """
    This function raises warning when the required ppm and
    user input ppm are nearly equal.
    :param ppm_user_input: ppm of the machine used by the user
    :param required_ppm:ppm required to distinguish between the two elements
    :param formula:formula for which the elements are distinguished
    :param ele:element for which ppm requirements are measured
    """
    if (required_ppm - 0.5) <= ppm_user_input <= (required_ppm + 0.5):
        warnings.warn(cs.PPM_REQUIREMENT_VALIDATION + formula + ':' + ele, UserWarning)
        return True


def get_indistinguishable_ele(isotracer, element, formula, ppm_user_input):
    """
    This function calculates the mass difference (delta m)
    between between the isotracer and element.
    :param isotracer:labeled element for
           which na correction is done
    :param element:element in the formula
    :return:mass difference
    """
    try:
        mass_diff = cs.MASS_DIFF_DICT[isotracer][element]
        required_ppm = get_ppm_required(formula, mass_diff)
        validate = ppm_validation(ppm_user_input, required_ppm, formula, element)
        if validate is True:
            return element
    except KeyError:
        return None


def ppm_validation(ppm_user_input, required_ppm, formula, ele):
    """
    This function validates the requirements for adding
    the element indistinguishable isotope list.
    :param ppm_user_input : ppm of machine
    :param required_ppm: ppm required
    :param formula: formula of the metabolite
    :param ele : element for which validation is carried out
    :return: boolean value if the requirement is met
    """
    if raise_warning(ppm_user_input, required_ppm, formula, ele) is True:
        return True
    if ppm_user_input > required_ppm:
        return True


def get_element_correction_dict(ppm_user_input, formula, isotracer):
    """
    This function returns a dictionary with all isotracer elements
    as key and indistinguishable isotopes as values.
    :param ppm_user_input:ppm of the machine used.
    :param formula:formula of the metabolite
    :param isotracer:labelled element which is to be corrected
    :return:element correction dictionary.
    """
    element_correction_dict = {}
    ele_list = get_elements_from_formula(formula)
    isotracer_ele = get_elements_from_formula(isotracer)
    for element in isotracer_ele:
        ele_list_without_isotracer = list(set(ele_list) - set(element))
        element_correction_dict[element] = []
        for ele in ele_list_without_isotracer:
            indis_element = get_indistinguishable_ele(element, ele,formula,ppm_user_input)
            if indis_element is not None:
                element_correction_dict.get(element).append(indis_element)
    return element_correction_dict